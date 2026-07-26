# Emergency Flatten Skill

Trigger phrase: "flatten" / "emergency" / "kill engine" / "stop bleeding"

## IMMEDIATE ACTIONS (in order)

### 1. STOP SERVICES FIRST
```bash
ssh -i "C:\Users\smmgo\Documents\Agents\Openrouter models add\binance-bot-tokyo.pem" ubuntu@54.168.247.83 "sudo systemctl stop composite_multi_arb guardian pure_mm watchdog_secondary"
```

### 2. USE THE HARDENED SCRIPT
```bash
ssh -i "C:\Users\smmgo\Documents\Agents\Openrouter models add\binance-bot-tokyo.pem" ubuntu@54.168.247.83 "python3 /opt/sysd/emergency_flatten_v2.py"
```

### 3. IF SCRIPT FAILS (fallback)
```bash
ssh -i "C:\Users\smmgo\Documents\Agents\Openrouter models add\binance-bot-tokyo.pem" ubuntu@54.168.247.83 << 'PYEOF'
# Raw API flatten via Python inline
python3 -c "
import os, time, hashlib, hmac, urllib, requests
exec(open('/opt/sysd/.env').read().replace(\"'\"', ''))
B='https://fapi.binance.com'
# ... emergency inline code
"
PYEOF
```

## CRITICAL RULES (never violated again)
1. **Stop services FIRST** — no exceptions, before any order
2. **Cancel ALL orders** before closing positions
3. **Raw API** for flatten (no CCXT create_order — causes doubling bug)
4. **NO retry loops** — one clean pass. If it fails, abort.
5. **ONE-WAY mode** — `side` opposite of position, exact `quantity`, NO `reduceOnly`, NO `positionSide`
6. **$10 time limit** — if not flat in 60 seconds, abort and report
7. **Verify flat** — query positions, confirm 0

## Known Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Position doubles on sell | CCXT adds extra params to MARKET order | Use raw API, no CCXT |
| -2022 reduceOnly rejected | Binance rejects reduceOnly for some modes | Don't use reduceOnly in ONE-WAY |
| -4136 closePosition rejected | closePosition not supported for linear MARKET | Use plain MARKET with quantity |
| -5022 GTX rejected | Price would cross spread | Don't use GTX for flatten, use MARKET |

## Preset Commands
- `/flatten` → runs emergency_flatten_v2.py
- `/kill` → stop services + flatten
- `/status` → check positions, BNFCR, USDC
