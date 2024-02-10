`config.json`:

```json
{
    "QUART_ENV": "production",
    "MAINTENANCE": false
}
```

`config.py`:

```python
# Security
SECRET_KEY = "secret_key"

# FumeGuard
FUMEGUARD_STANDARD_PORT = 10001
FUMEGUARD_MULTICAST_PORT = 20001
FUMEGUARD_INVITE_URL = "fumeguard_invite_url"
FUMEGUARD_VOTE_URL = "fumeguard_vote_url"
FUMEGUARD_REVIEW_URL = "fumeguard_review_url"

# FumeTune
FUMETUNE_STANDARD_PORT = 10002
FUMETUNE_MULTICAST_PORT = 20002
FUMETUNE_INVITE_URL = "fumetune_invite_url"
FUMETUNE_VOTE_URL = "fumetune_vote_url"
FUMETUNE_REVIEW_URL = "fumetune_review_url"

# FumeTool
FUMETOOL_STANDARD_PORT = 10003
FUMETOOL_MULTICAST_PORT = 20003
FUMETOOL_INVITE_URL = "fumetool_invite_url"
FUMETOOL_VOTE_URL = "fumetool_vote_url"
FUMETOOL_REVIEW_URL = "fumetool_review_url"

# Community
COMMUNITY_GUILD_ID = 1234567890
COMMUNITY_INVITE_URL = "community_invite_url"

# Discord
DISCORD_CLIENT_ID = 1234567890
DISCORD_CLIENT_SECRET = "client_secret"
DISCORD_REDIRECT_URI = "callback_url"
DISCORD_BOT_TOKEN = "bot_token"

# Development
TEMPLATES_AUTO_RELOAD = False
```
