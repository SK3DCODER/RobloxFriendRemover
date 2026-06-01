# Roblox Friend Remover

A Python script to remove all friends from your Roblox account automatically.

## Description

This script allows you to mass-remove all friends from your Roblox account. It automatically handles friend list pagination, manages CSRF tokens, and deals with rate limits.

## Features

- Automatic CSRF token retrieval
- Paginated loading of complete friend list
- Bulk friend removal with confirmation prompt
- Rate limit handling (automatic retry on HTTP 429)
- Automatic CSRF token refresh on HTTP 403 errors
- Progress display during removal
- Success/failure count summary

## Requirements

- Python 3.6 or higher
- `requests` library


1. Install the required dependency:

```bash
pip install requests
```

## How to Get Your .ROBLOSECURITY Cookie

1. Install a browser extension like **Cookie Editor** or **EditThisCookie** (Chrome/Firefox)

2. Log into your Roblox account at https://www.roblox.com

3. Open the extension and find the cookie named **.ROBLOSECURITY**

4. Copy its **value** (a long string of characters)

> don't share your .ROBLOSECURITY Cookie!

## Usage

Run the script:

```bash
python 1.py
```

Follow the prompts:

1. Paste your `.ROBLOSECURITY` cookie value when prompted
2. Review the number of friends found
3. Type `yes` to confirm removal (or `no` to cancel)
4. Wait while the script removes all friends

### Example Output

```
ENTER .ROBLOSECURITY COOKIE: [paste your cookie]
FRIENDS: 245
REMOVE 245 FRIENDS? (yes/no): yes
[1/245] REMOVING: PlayerName1... OK
[2/245] REMOVING: PlayerName2... OK
[3/245] REMOVING: PlayerName3... WAIT 5s - RATE LIMIT...
[3/245] REMOVING: PlayerName3... OK
...
REMOVED: 244
FAILED: 1
PRESS ENTER TO EXIT...
```

## How It Works

1. **Authentication** - Uses your `.ROBLOSECURITY` cookie to authenticate with Roblox API
2. **CSRF Token** - Obtains a CSRF token required for POST requests
3. **Fetch Friends** - Retrieves your entire friend list using paginated API requests
4. **Bulk Removal** - Sends unfriend requests for each friend with proper delays
5. **Error Handling** - Automatically retries on rate limits and refreshes expired CSRF tokens

## Configuration

You can adjust the delay between unfriend requests by modifying the `self.request_delay` variable in the script (default: 3.0 seconds). Lower values may trigger rate limits.

## Error Handling

| Error | Handling |
|-------|----------|
| HTTP 429 (Rate Limit) | Automatically retries up to 3 times with increasing delays |
| HTTP 403 (Invalid CSRF) | Automatically fetches new CSRF token and retries |
| Network errors | Skips the affected friend and continues |

## Limitations

- Roblox API has rate limits - the script includes delays to respect them
- Very large friend lists (1000+) may take significant time due to required delays
- Some failures may occur if Roblox API is experiencing issues

## Disclaimer

This script is for educational purposes. Use at your own risk. Excessive API requests may lead to temporary rate limiting or account restrictions.
