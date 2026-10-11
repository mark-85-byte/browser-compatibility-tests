# Browser Compatibility Diagnostics

A small Python toolkit for measuring browser environments and comparing diagnostic
reports across Windows, macOS and Linux. It helps answer: **what changed between
these two browser runs?**

Status: early-stage developer tooling. The code and documentation were developed
with AI assistance. There are no verified external adoption or download metrics.

## Features

- Record the actual execution OS, architecture and browser version.
- Measure reported graphics renderer, canvas repeatability, font sample widths,
  browser preferences and screen/window dimensions.
- Keep cold-start and warmed observations separate.
- Compare reports offline with explicit missing values and optional numeric tolerance.
- Run a manual GitHub Actions audit on Windows, macOS and Ubuntu hosts.
- Run offline regression tests without downloading a browser.

## Quick start

Use Python 3.11 or newer. Create and activate a virtual environment first:

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# Ubuntu / macOS
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and run the audit:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
python device_audit.py --headless --channels chromium --output outputs/baseline.json
```

On Ubuntu, `python -m playwright install --with-deps chromium` can also install the
required system libraries. It may require administrator privileges.
Omit `--headless` for a visible local browser. `--channels chromium,chrome,msedge`
also checks Chrome and Edge when those browsers are installed locally.

## Compare two reports

```bash
python compare_reports.py outputs/baseline.json outputs/current.json --output outputs/comparison.json
python compare_reports.py outputs/baseline.json outputs/current.json --tolerance 0.02
```

The comparison pairs results by browser channel. OS, browser version, execution
mode, repeatability and nested measurements remain visible as changed paths.
Timestamps, derived environment IDs and duplicate cold/warm observation objects
are excluded from comparison. Numeric tolerance is absolute and does not apply
to booleans. Duplicate channels and malformed reports are rejected.

Exit codes: **0** for equal measurements, **1** for differences, **2** for invalid
input or file errors. A difference is a diagnostic finding, not proof of a bug.
The comparison feature uses only Python's standard library.

## Tests

```bash
python -m unittest discover -v
```

Tests use fictional inputs to check nested differences, ordering, missing/null
values, numeric tolerance, unavailable channels, invalid input and CLI behavior.
They do not establish browser or physical device coverage.

## GitHub Actions

Open **Actions → Windows macOS Linux browser audit → Run workflow**.
The workflow runs only on request, uses standard hosted runners, limits each job
to twelve minutes and retains JSON artifacts for one day. Inspect completed run
results before claiming coverage. Report comparison tests can also run locally.

## Privacy and limitations

The audit launches fresh browser contexts and probes a blank page. It does not
visit external sites, load your existing browser profile or collect credentials.
Reports contain OS/build, renderer, languages, timezone and display measurements;
review these before sharing. Generated `outputs/` files are excluded from Git.
Dependency installation and GitHub Actions require network access; the probe and
offline comparison do not send reports to an external service.

Hosted VMs may expose software graphics. Canvas hashes describe a rendered sample,
not a unique device identity. Font widths can include fallback fonts. Results from
headless and visible browsers are different configurations. This toolkit does not
establish coverage of every GPU, font set, extension or website.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributions and [LICENSE](LICENSE) for
the MIT license.
