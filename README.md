# 💣 Anti-Nuke Tester Bot for Discord

> **⚠️ WARNING**  
> This bot is for **educational and testing purposes only**.  
> Misusing this bot on live servers **violates Discord's Terms of Service** and can result in permanent bans.  
> Use **only** in private test environments!

---

## 📌 Overview

The **Anti-Nuke Tester Bot** simulates destructive behaviors like spam, channel deletions, and permission escalations.  
It's specifically designed to **test the strength and response** of Discord anti-nuke bots such as:

🔗 [Anti-Nuke Bot on Discord App Discovery](https://discord.com/discovery/applications/1317483934879055992)

---

## ✨ Features

| ✅ Feature                     | ⚙️ Description |
|------------------------------|----------------|
| 🔁 Channel/Role Spam         | Rapid creation of text channels or roles |
| 🗑️ Channel/Role Deletion     | Mass deletion to test response systems |
| 📣 Message/Mention Spam      | Simulates spam floods in a channel |
| 🎭 Webhook Spam              | Generates webhooks and sends spam messages |
| 🔒 Permission Attack         | Modifies channel permissions (escalation test) |
| 🌀 Server Name Change        | Loops through name changes |
| 🎯 Multi-Attack Mode         | Executes several attack vectors at once |
| 🔨 Simulated Ban Spam        | Tests how your bot handles fake ban attacks |

---

## ⚙️ Setup

### 🔧 Requirements
- Python 3.8+
- `discord.py` or a fork (like `py-cord`)
- `python-dotenv` for token management

---

### 📥 Installation

```bash
git clone https://github.com/AceCombatx/anti-nuke-tester.git
cd anti-nuke-tester
pip install -r requirements.txt
```

---

### 🔐 Token Configuration

Create a `.env` file in the project root:

```env
DISCORD_ATOKEN=your_bot_token_here
```

Then run the bot:

```bash
python main.py
```

---

## 💻 Commands

> All commands use the prefix `!test`

| Command | Action |
|--------|--------|
| `!test help` | Show available commands |
| `!test channelspam [count] [delay]` | Create spam channels |
| `!test rolespam [count] [delay]` | Create spam roles |
| `!test delchannels [count] [delay]` | Delete multiple channels |
| `!test delroles [count] [delay]` | Delete multiple roles |
| `!test webhookspam [count] [delay]` | Create webhooks |
| `!test messagespam [count] [delay]` | Send spam messages |
| `!test mentionspam [count] [delay]` | Send mention spam |
| `!test namechange [count] [delay]` | Change server name repeatedly |
| `!test banspam [count] [delay]` | Simulate user bans |
| `!test permissionattack [count] [delay]` | Modify channel permissions |
| `!test webhookmessagespam [count] [delay]` | Spam via webhook |
| `!test multiattack [count] [delay]` | Run all major tests together |

---

## ⚠️ Disclaimer

> This project is for educational testing only.  
> It must **not be used for malicious activity**.  
> The developer is **not responsible** for damage, bans, or consequences from misuse.  
> You are solely responsible for how this tool is used.

---

## 👨‍💻 Author

- GitHub: [AceCombatx](https://github.com/AceCombatx)
- Discord: `carzy.raptor`

---

⭐️ Star this project if you find it useful for testing your anti-nuke defense systems.

---

## 🔐 License

This project is under a **Custom No-Distribution, No-Commercial-Use License**.  
See [LICENSE](./LICENSE) for details. You may not distribute, modify, or sell this code.
