# Matcherino Brawl Stars Discord Bot

This is a custom Discord bot designed for the Matcherino Brawl Stars server. The bot is capable of assigning region and role-based emojis, managing server rules, enforcing message content policies, and handling specific commands related to tournaments and pins.

## Features

- **Emoji-based Role Assignment**: Users can select their region and role by reacting to specific messages with predefined emojis.
- **Message Moderation**: The bot detects and removes banned words and unauthorized links.
- **Automatic Pin Announcement**: Based on message activity and certain keywords, the bot will post information about exclusive in-game pins for Brawl Stars.
- **Custom Commands**:
  - `/postrules`: Posts server rules.
  - `/selfrole`: Allows users to select their region and role.
- **Logging**: Deleted messages and moderation actions are logged to a specified channel.

## Prerequisites

- Python 3.8+
- A Discord bot token
- A `.env` file for managing private keys

### Environment Variables

Create a `.env` file in the root directory of your project with the following content:

```bash
TOKEN=discord_bot_token
LOG_CHANNEL_ID=log_channel_id
BYPASS_ROLE_ID=bypass_role_id
ORGANIZER_ROLE=organizer_role_id
BANNED_WORDS=banned_words_list
REGION_MESSAGE_ID=region_message_id
ROLE_MESSAGE_ID=role_message_id
