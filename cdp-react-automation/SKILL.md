# Skill: CDP React Automation

Automate React SPAs (Payhip, agentskill.sh, Supabase, Vercel, etc.) via Chrome DevTools Protocol without needing Playwright/Puppeteer.

## The Problem
React SPAs check `event.isTrusted` — JS `.click()` produces `isTrusted: false`, so React ignores it. Playwright/Puppeteer `connect_over_cdp` often times out. Reconnecting to existing browser tabs via CDP websocket fails.

## The Fix — Four Rules

### Rule 1: ALWAYS create new tabs, never reconnect to existing
Connecting to an existing tab via websocket URL times out after ~5s. Instead:
```python
import json, urllib.request, websocket

BROWSER_WS = json.loads(
    urllib.request.urlopen("http://localhost:9222/json/version").read()
)["webSocketDebuggerUrl"]

ws = websocket.create_connection(BROWSER_WS, timeout=10)
ws.send(json.dumps({"id": 1, "method": "Target.createTarget",
    "params": {"url": "https://example.com"}}))
# Response contains targetId — use to find its websocket URL
```

After creating the tab, find its websocket URL:
```python
import time
time.sleep(3)  # Wait for tab to initialize
targets = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
for t in targets:
    if t["id"] == targetId:
        tab_ws_url = t["webSocketDebuggerUrl"]
```

### Rule 2: Use `Input.dispatchMouseEvent` for clicks
This produces `isTrusted: true` — React processes the event:
```python
# First get element position
result = page.call("Runtime.evaluate", {
    "expression": "(() => { const e = document.querySelector('button.submit'); const r = e.getBoundingClientRect(); return {x: r.x + r.width/2, y: r.y + r.height/2}; })()",
    "returnByValue": True
})
pos = result["result"]["value"]

# Then dispatch real mouse events
page.call("Input.dispatchMouseEvent", {
    "type": "mousePressed", "x": pos["x"], "y": pos["y"],
    "button": "left", "clickCount": 1
})
page.call("Input.dispatchMouseEvent", {
    "type": "mouseReleased", "x": pos["x"], "y": pos["y"],
    "button": "left", "clickCount": 1
})
```

If the element isn't visible, scroll first:
```python
page.call("Runtime.evaluate", {
    "expression": "document.querySelector('button.submit').scrollIntoView({block: 'center'})"
})
time.sleep(0.5)  # Wait for scroll
```

### Rule 3: Set form values via JS + dispatchEvent
`.value` alone doesn't trigger React. Follow it with `dispatchEvent`:
```python
page.call("Runtime.evaluate", {
    "expression": """
        const inp = document.querySelector('input[name=email]');
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        nativeInputValueSetter.call(inp, 'user@example.com');
        inp.dispatchEvent(new Event('input', {bubbles: true}));
        inp.dispatchEvent(new Event('change', {bubbles: true}));
    """
})
```

Or simpler for most fields:
```python
page.call("Runtime.evaluate", {
    "expression": """
        const inp = document.querySelector('input[type=text]');
        inp.value = 'some value';
        inp.dispatchEvent(new Event('input', {bubbles: true}));
    """
})
```

For textareas or contenteditable divs, use `Input.insertText`:
```python
page.call("Input.dispatchMouseEvent", {
    "type": "mousePressed", "x": x, "y": y,
    "button": "left", "clickCount": 1
})  # Focus the element first
page.call("Input.insertText", {"text": "Hello world"})
```

### Rule 4: File upload via DOM.setFileInputFiles
```python
page.call("DOM.setFileInputFiles", {
    "files": ["C:/path/to/file.zip"],
    "nodeId": node_id  # Get via DOM.querySelector
})
```

## CDP Helper Class
```python
class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=30)
        self.mid = 0

    def call(self, method, params=None):
        self.mid += 1
        msg = {"id": self.mid, "method": method}
        if params: msg["params"] = params
        self.ws.send(json.dumps(msg))
        while True:
            resp = json.loads(self.ws.recv())
            if resp.get("id") == self.mid:
                if "error" in resp:
                    raise RuntimeError(f"{method}: {resp['error']}")
                return resp.get("result", {})

    def eval(self, expr, await_promise=True):
        r = self.call("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": await_promise
        })
        return r.get("result", {}).get("value")

    def click(self, selector):
        pos = self.eval(f"""
            (() => {{
                const e = document.querySelector({repr(selector)});
                if (!e) return null;
                e.scrollIntoView({{block: 'center'}});
                const r = e.getBoundingClientRect();
                return {{x: r.x + r.width/2, y: r.y + r.height/2}};
            }})()
        """)
        if not pos: raise RuntimeError(f"Element not found: {selector}")
        self.call("Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": pos["x"], "y": pos["y"],
             "button": "left", "clickCount": 1})
        self.call("Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": pos["x"], "y": pos["y"],
             "button": "left", "clickCount": 1})

    def fill(self, selector, value):
        self.call("Runtime.evaluate", {"expression": f"""
            const inp = document.querySelector({repr(selector)});
            if (!inp) return;
            inp.value = {repr(value)};
            inp.dispatchEvent(new Event('input', {{bubbles: true}}));
        """})
```

## Common Cases

### React Portal (dropdown menu, modal)
Use `Input.dispatchMouseEvent` with absolute coordinates — works even when the element is in a portal outside the React root.

### Cloudflare-protected forms
Cloudflare challenges are auto-solved in the browser. CDP works on the already-authenticated session. Just create a new tab and go.

### Native submit `<input type=submit>`
Plain `.click()` via JS works here — native form submission doesn't check `isTrusted`. The React issue only applies to synthetic event handlers on `<div>`, `<button>`, etc.

## Creating a New Tab
```python
import json, urllib.request, websocket

BROWSER_WS = json.loads(
    urllib.request.urlopen("http://localhost:9222/json/version").read()
)["webSocketDebuggerUrl"]

ws = websocket.create_connection(BROWSER_WS, timeout=10)
ws.send(json.dumps({"id": 1, "method": "Target.createTarget",
    "params": {"url": "https://example.com"}}))
resp = json.loads(ws.recv())
tid = resp["result"]["targetId"]
ws.close()

# Wait for tab
import time
time.sleep(3)

# Get tab websocket URL
targets = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
tab_ws = None
for t in targets:
    if t["id"] == tid:
        tab_ws = t["webSocketDebuggerUrl"]
        break

if not tab_ws:
    raise RuntimeError("Tab not found")

page = CDP(tab_ws)
```
