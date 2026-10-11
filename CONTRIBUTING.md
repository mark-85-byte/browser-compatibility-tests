# Contributing

This is an early-stage browser diagnostics project. Contributions that improve
reproducibility, report validation, setup instructions or error handling are welcome.

1. Open an issue describing the problem, OS, browser channel and execution mode.
2. Use a fresh branch for the change.
3. Run `python -m unittest discover -v` and include a regression test for changed behavior.
4. For measurement changes, explain which browser configurations you actually ran.
5. Open a pull request with the change, its purpose and the validation results.

Tests for report comparison use fictional values and require no browser installation.
The browser audit requires Playwright and Chromium as described in the README.

Before attaching a diagnostic report, inspect its OS/build, renderer, languages,
timezone and display measurements. Share only what you intend to publish.
Do not attach browser profiles, cookies, credentials or unrelated files.

Code changes are contributed under the repository's MIT license.
