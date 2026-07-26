---
name: browser-session-rules
description: >-
  Enforces correct browser usage for all agents. NEVER launch a new browser or use Microsoft Edge. ALWAYS connect to an existing Brave or Chrome session via Chrome DevTools Protocol (CDP) on port 9222. Apply these rules to any Playwright, Puppeteer, Selenium, or browser_subagent call. Auto-triggers whenever a task involves web scraping, browser automation, or UI interaction.
---

# Browser Session Rules

## The Rule (Non-Negotiable)

> **NEVER launch a new browser. ALWAYS connect to an existing Brave or Chrome via CDP on port 9222.**

This applies to ALL browser automation: Playwright, Puppeteer, Selenium, browser_subagent, fetch intercepts, anything.

## ❌ Forbidden Patterns

```python
# WRONG — launches new browser
browser = await p.chromium.launch()
browser = await p.firefox.launch()
browser = await p.webkit.launch()

# WRONG — launches Edge
browser = await p.chromium.launch(channel="msedge")

# WRONG — launches new Chrome
browser = await p.chromium.launch(channel="chrome")
```

```javascript
// WRONG
const browser = await puppeteer.launch()
```

## ✅ Correct Pattern — Always CDP Connect

```python
# CORRECT — Playwright
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]       # reuse existing context (logged-in session)
    page = ctx.pages[0]             # reuse existing tab
```

```javascript
// CORRECT — Puppeteer
const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' })
```

## Step 0: Detect Which Browser Is Running

Before any action, identify the browser at CDP:

```powershell
# Check CDP is available and detect browser
$info = Invoke-RestMethod http://localhost:9222/json/version
if ($info.Browser -match 'Chrome') {
    Write-Host "Browser: $($info.Browser)"
}
```

This returns a `Browser` field like `Chrome/149.0.7827.201`. **Use this to determine relaunch instructions.**

## Prerequisite Check (Always Verify Before Running)

Before any browser task, verify the CDP endpoint is available:

```powershell
Invoke-RestMethod http://localhost:9222/json/version
```

If this fails → detect which browsers are installed, then prompt the user:

```powershell
# Detect installed browsers automatically
$bravePath = "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
$chromePath = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
$chromeAltPath = "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"

if (Test-Path $bravePath) {
    Write-Host "Brave found at: $bravePath"
}
if (Test-Path $chromePath) {
    Write-Host "Chrome found at: $chromePath"
}
if (Test-Path $chromeAltPath) {
    Write-Host "Chrome (user) found at: $chromeAltPath"
}
```

Prompt the user with the correct command based on what's installed:

```
⚠️ No browser found at localhost:9222.
Close all browser windows, then relaunch with:

For Brave:
  "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222

For Chrome:
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

Or if Chrome is installed per-user:
  "C:\Users\<USER>\AppData\Local\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Do NOT proceed with a browser launch as fallback.** Wait for user.

## Why Existing Session Matters

- Facebook, Google, and most sites require login — a new browser has no cookies
- Launching a new browser destroys the authenticated session
- Edge is not configured with the user's extensions, passwords, or settings
- User keeps their browser open with existing tabs for a reason

## Port Reference

| Port | Purpose |
|---|---|
| 9222 | Brave or Chrome with `--remote-debugging-port=9222` |

If port 9222 is taken by something else:
```powershell
netstat -ano | findstr :9222
```

## Auto-Detection Snippet

Paste this into any Playwright script to detect the active browser at runtime:

```python
import requests
info = requests.get("http://localhost:9222/json/version").json()
browser_name = info.get("Browser", "unknown")
print(f"Active browser: {browser_name}")
# browser_name will be e.g. "Chrome/149.0.7827.201" or "Brave/1.75.XX"
```

## Playwright: Reuse Existing Tab vs Open New

```python
ctx = browser.contexts[0]

# Option A: reuse first open tab
page = ctx.pages[0]

# Option B: open a new tab in the existing session (keeps login)
page = await ctx.new_page()
```

Always prefer Option A unless the task explicitly needs a clean tab.

## Common Mistakes

- **Falling back to `launch()`** when CDP connect fails — forbidden. Fix the CDP connection instead.
- **Using `browser.new_context()`** — this creates a fresh unauthenticated context. Use `browser.contexts[0]`.
- **Specifying `channel="msedge"`** — Edge is never the right browser for this user.
- **Forgetting to check CDP before writing scraper code** — always ping `localhost:9222` first as Step 1.
- **Assuming Brave from CDP Browser field** — always parse `Browser` field from `/json/version` to confirm. Chrome reports as `Chrome/X.Y.Z`, Brave reports as `Chrome/X.Y.Z` too (Chromium-based), so check for `Brave` in the `User-Agent` field if you need to distinguish.
- **Hardcoding a single browser path** in the "if CDP fails" prompt — always detect which browsers are installed and show the correct paths.
