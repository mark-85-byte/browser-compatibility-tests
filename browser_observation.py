"""Observe the execution environment for cross-platform research; never spoof it."""
import asyncio
from datetime import datetime, timezone
import hashlib
import json
import platform


PROBE = r"""async () => {
    const fontNames=['Arial','Segoe UI','Calibri','Helvetica','Menlo','DejaVu Sans','Liberation Sans','Noto Sans'];
    const sampleText='mmmmmmmmlli00Aa';
    // Resolve native fonts before measurement; the first page may otherwise use a transient fallback.
    await Promise.all(fontNames.map(font=>document.fonts.load(`24px "${font}", monospace`,sampleText)));
    await document.fonts.load('18px sans-serif','Browser compatibility: Aa09');
    await document.fonts.ready;
    const canvas = document.createElement('canvas');
    canvas.width=300; canvas.height=90;
    const ctx=canvas.getContext('2d');
    ctx.fillStyle='#e6edf3';ctx.fillRect(0,0,300,90);
    ctx.font='18px sans-serif';ctx.fillStyle='#123456';
    ctx.fillText('Browser compatibility: Aa09',8,30);
    ctx.strokeStyle='#728394';ctx.beginPath();ctx.arc(140,60,16,0,Math.PI*2);ctx.stroke();
    const fonts={};
    for(const font of fontNames){
        ctx.font=`24px "${font}", monospace`;
        fonts[font]=ctx.measureText(sampleText).width;
    }
    const gl=document.createElement('canvas').getContext('webgl');
    let graphics=null;
    if(gl){
        const ext=gl.getExtension('WEBGL_debug_renderer_info');
        graphics={vendor:gl.getParameter(gl.VENDOR),renderer:gl.getParameter(gl.RENDERER),
            unmaskedVendor:ext?gl.getParameter(ext.UNMASKED_VENDOR_WEBGL):null,
            unmaskedRenderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null};
    }
    return {userAgent:navigator.userAgent,platform:navigator.platform,languages:navigator.languages,
        logicalCores:navigator.hardwareConcurrency,deviceMemoryGiB:navigator.deviceMemory??null,
        timezone:Intl.DateTimeFormat().resolvedOptions().timeZone,
        screen:{width:screen.width,height:screen.height,dpr:devicePixelRatio},
        viewport:{width:innerWidth,height:innerHeight},graphics,fontSampleWidths:fonts,
        canvasData:canvas.toDataURL()};
}"""


async def observe(context, *, channel, headless, preference_emulation=False, user_agent_override=False):
    page=None
    try:
        page=await context.new_page()
        values=await page.evaluate(PROBE)
        canvas=values.pop('canvasData')
        values['canvas_sample_sha256']=hashlib.sha256(canvas.encode()).hexdigest()
        host={'system':platform.system(),'release':platform.release(),
              'version':platform.version(),'architecture':platform.machine()}
        configuration={'actual_host':host,'browser_version':context.browser.version,
                       'channel':channel,'headless':headless,'preference_emulation':preference_emulation,
                       'user_agent_override':user_agent_override,'observed_browser':values}
        configuration['environment_id']=hashlib.sha256(json.dumps(configuration,sort_keys=True).encode()).hexdigest()[:20]
        configuration.update(measured_utc=datetime.now(timezone.utc).isoformat(),
            coverage='executed_on_'+host['system'],
            graphics_note='Observed renderer may be hardware or software; this is not proof of a physical GPU.',
            fonts_note='Sample text widths include fallback fonts; this is not a complete font inventory.',
            identity_note='Environment ID describes measured configuration, not a unique device identity.')
        return configuration
    finally:
        if page and not page.is_closed():await page.close()


async def observe_bounded(context, **kwargs):
    return await asyncio.wait_for(observe(context,**kwargs),timeout=5)
