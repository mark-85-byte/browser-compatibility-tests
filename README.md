# Windows, macOS and Linux browser baseline

This small standalone package runs the same local browser diagnostic on three real execution operating systems using GitHub-hosted virtual machines. It does not need a Mac or Linux machine on your desk.

## What it measures

Actual host OS/build/architecture, browser version, reported graphics renderer, canvas sample repeatability, font sample widths, browser preferences and screen/window dimensions. Each result explicitly records headless mode and the execution OS.

Cloud hosts can expose software/virtual graphics. These baselines establish execution on the three listed OS environments, not coverage of every physical GPU, font set, wallet extension or trading flow. No simulated GPU/OS values or random canvas noise are injected.

## Files and account access

Upload only this standalone folder's files to a dedicated repository, preserving `.github/workflows/device-audit.yml`. It contains no wallet spreadsheet, private key, CAPTCHA API key, browser cookies, Telegram token or trading code. Keep the existing trading project separate.

In the repository, open Actions, choose **Windows macOS Linux browser audit**, then **Run workflow**. It runs only when manually triggered. Download the three `device-audit-*` artifacts after completion; retention is one day.

The approved private repository is `mark-85-byte/browser-compatibility-tests`. Read the status and artifacts of a completed workflow run before claiming OS coverage; committing this package alone does not verify any cloud environment.

## Cost and scope

GitHub's standard hosted runners are free on public repositories. Private repositories use the account's included allowance; GitHub Free lists 2,000 minutes/month and 500 MB artifact storage, shared with other account usage. Confirm remaining allowance and keep paid overage blocked before dispatching a private-repository test. The package cannot inspect or enforce your account billing budget by itself.

The workflow uses standard runner labels only, a twelve-minute limit per job, no schedule and one-day retention for a tiny JSON artifact. It is for brief compatibility diagnostics, not persistent hosting or a month-long trading bot.

Official sources:

- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://playwright.dev/python/docs/emulation

## Local use

With the requirements and Chromium installed:

```
python device_audit.py --headless --channels chromium --output outputs/device-audit.json
```

Omit `--headless` for a visible local browser; the measured mode remains explicit. Results from visible and headless browsers are separate configurations.
