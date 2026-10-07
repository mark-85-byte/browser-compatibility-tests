"""Portable, local-only browser audit. Uses fresh profiles and never opens a wallet/site."""
import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from browser_observation import observe_bounded


async def main(args):
    results=[]
    async with async_playwright() as playwright:
        for channel in args.channels.split(','):
            channel=channel.strip()
            browser=None
            try:
                browser=await playwright.chromium.launch(channel=channel,headless=args.headless)
                context=await browser.new_context(no_viewport=True)
                result=await observe_bounded(context,channel=channel,headless=args.headless)
                # A second fresh local page must produce the same sample, without random noise.
                repeat=await observe_bounded(context,channel=channel,headless=args.headless)
                result['repeat_sample_stable']=result['environment_id']==repeat['environment_id']
                result['repeat_observation']=repeat
                results.append(result)
                print(f'{channel}: actual host={result["actual_host"]["system"]}; repeat stable={result["repeat_sample_stable"]}',flush=True)
                print('DIAGNOSTIC_JSON='+json.dumps(result,sort_keys=True),flush=True)
            except Exception as exc:
                results.append({'channel':channel,'status':'unavailable','error_type':type(exc).__name__})
                print(f'{channel}: unavailable ({type(exc).__name__})',flush=True)
            finally:
                if browser:await browser.close()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({'local_only':True,'wallets_opened':0,'paid_tasks':0,'trades':0,
        'results':results,'cross_os_coverage':'Only the execution hosts recorded above were tested.'},indent=2),encoding='utf-8')
    print('Report:',args.output,flush=True)
    if not any(r.get('repeat_sample_stable') for r in results):raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--channels',default='chromium')
    parser.add_argument('--headless',action='store_true',help='Cloud-friendly mode; recorded explicitly in results')
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'outputs'/'device-audit.json')
    asyncio.run(main(parser.parse_args()))
