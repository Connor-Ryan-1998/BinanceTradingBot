# Binance Trading Bot

## Trading Logic

Explanation Here

## Binance Configuration

- Create a [Binance account](https://www.binance.com/en-AU/register?ref=C4IXSKA1) (Includes my referral link, I'll be super grateful if you use it).
- Enable Two-factor Authentication.
- Create a new API key.
- Get a cryptocurrency. If its symbol is not in the default list, add it.

## Local Config

- Build a variables.py file
- Add below

```
import os

os.environ["APIKey"] = 'ApiKeyHere'
os.environ["secretKey"] = 'secretKeyHere'
os.environ["coinToken"] = 'BTCAUD'
```
