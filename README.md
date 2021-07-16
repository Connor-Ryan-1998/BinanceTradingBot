# Binance Trading Bot

## Trading Logic

Simple MA calculation, executes when outside average. Volitility makes me cry

## Binance Configuration

- Create a [Binance account](https://www.binance.com/en-AU/register?ref=C4IXSKA1) (Use please).
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
