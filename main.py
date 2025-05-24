import discord
from discord.ext import commands
import asyncio
import os
import random
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('anti_nuke_test_bot')

# Load environment variables
load_dotenv()

# Configuration
PREFIX = "!test "
DEFAULT_DELAY = 0.5  # Default delay between batch operations in seconds

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    logger.info(f'Use "{PREFIX} help" to see available commands')
    logger.info('WARNING: This bot is designed to test anti-nuke protection. Use only in test servers!')
    
    # Set bot status
    await bot.change_presence(activity=discord.Game(name=f"{PREFIX} help | Anti-Nuke Tester"))

@bot.command(name="help")
async def show_help(ctx):
    """Show help information about the bot"""
    embed = discord.Embed(
        title="Anti-Nuke Test Bot Commands",
        description="Use these commands to test your anti-nuke bot's effectiveness.",
        color=discord.Color.red()
    )
    
    embed.add_field(
        name=f"{PREFIX} channelspam [count] [delay]",
        value="Create multiple channels quickly (default: 5 channels, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} rolespam [count] [delay]",
        value="Create multiple roles quickly (default: 5 roles, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} delchannels [count] [delay]",
        value="Delete multiple channels quickly (default: 5 channels, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} delroles [count] [delay]",
        value="Delete multiple roles quickly (default: 5 roles, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} webhookspam [count] [delay]",
        value="Create multiple webhooks quickly (default: 5 webhooks, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} messagespam [count] [delay]",
        value="Send multiple messages quickly (default: 10 messages, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} mentionspam [count] [delay]",
        value="Send messages with multiple mentions (default: 5 messages, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} namechange [count] [delay]",
        value="Change server name multiple times (default: 3 times, 0.5s delay)",
        inline=False
    )
    embed.add_field(
        name=f"{PREFIX} banspam [count] [delay]",
        value="Simulate banning multiple users (default: 5 users, 0.5s delay)",
        inline=False
    )
    
    embed.set_footer(text="WARNING: Use only in test servers! This bot can cause damage to your server.")
    
    await ctx.reply(embed=embed)

@bot.command(name="channelspam")
@commands.has_permissions(administrator=True)
async def create_channels(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Create multiple channels quickly"""
    await ctx.reply(f"Creating {count} channels with {delay}s delay...")
    
    created = 0
    for i in range(count):
        try:
            await ctx.guild.create_text_channel(
                name=f"test-channel-{i}",
                reason="Anti-nuke bot testing"
            )
            created += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to create channel {i}: {e}")
            await ctx.send(f"Failed to create channel {i}: {e}")
            break
    
    await ctx.send(f"Finished creating {created} channels.")

@bot.command(name="rolespam")
@commands.has_permissions(administrator=True)
async def create_roles(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Create multiple roles quickly"""
    await ctx.reply(f"Creating {count} roles with {delay}s delay...")
    
    created = 0
    for i in range(count):
        try:
            # Generate a random color
            color = discord.Color.from_rgb(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            
            await ctx.guild.create_role(
                name=f"Test Role {i}",
                color=color,
                reason="Anti-nuke bot testing"
            )
            created += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to create role {i}: {e}")
            await ctx.send(f"Failed to create role {i}: {e}")
            break
    
    await ctx.send(f"Finished creating {created} roles.")

@bot.command(name="delchannels")
@commands.has_permissions(administrator=True)
async def delete_channels(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Delete multiple channels quickly"""
    await ctx.reply(f"Deleting up to {count} channels with {delay}s delay...")
    
    # Get non-essential channels (exclude the current one)
    channels = [channel for channel in ctx.guild.channels 
                if channel.id != ctx.channel.id and 
                isinstance(channel, discord.TextChannel) and
                channel.permissions_for(ctx.guild.me).manage_channels]
    
    # Limit to the requested count
    channels = channels[:count]
    
    if not channels:
        return await ctx.send("No deletable channels found.")
    
    deleted = 0
    for channel in channels:
        try:
            await channel.delete(reason="Anti-nuke bot testing")
            deleted += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to delete channel {channel.name}: {e}")
            await ctx.send(f"Failed to delete channel {channel.name}: {e}")
            break
    
    await ctx.send(f"Finished deleting {deleted} channels.")

@bot.command(name="delroles")
@commands.has_permissions(administrator=True)
async def delete_roles(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Delete multiple roles quickly"""
    await ctx.reply(f"Deleting up to {count} roles with {delay}s delay...")
    
    # Get non-essential roles (exclude @everyone and managed roles)
    roles = [role for role in ctx.guild.roles 
             if not role.managed and 
             role.id != ctx.guild.id and
             role.position < ctx.guild.me.top_role.position]
    
    # Limit to the requested count
    roles = roles[:count]
    
    if not roles:
        return await ctx.send("No deletable roles found.")
    
    deleted = 0
    for role in roles:
        try:
            await role.delete(reason="Anti-nuke bot testing")
            deleted += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to delete role {role.name}: {e}")
            await ctx.send(f"Failed to delete role {role.name}: {e}")
            break
    
    await ctx.send(f"Finished deleting {deleted} roles.")

@bot.command(name="webhookspam")
@commands.has_permissions(administrator=True)
async def create_webhooks(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Create multiple webhooks quickly"""
    await ctx.reply(f"Creating {count} webhooks with {delay}s delay...")
    
    created = 0
    for i in range(count):
        try:
            await ctx.channel.create_webhook(
                name=f"Test Webhook {i}",
                reason="Anti-nuke bot testing"
            )
            created += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to create webhook {i}: {e}")
            await ctx.send(f"Failed to create webhook {i}: {e}")
            break
    
    await ctx.send(f"Finished creating {created} webhooks.")

@bot.command(name="messagespam")
@commands.has_permissions(administrator=True)
async def spam_messages(ctx, count: int = 10, delay: float = DEFAULT_DELAY):
    """Send multiple messages quickly"""
    await ctx.reply(f"Sending {count} spam messages with {delay}s delay...")
    
    sent = 0
    for i in range(count):
        try:
            await ctx.send(f"Test spam message #{i} - This is a test of the anti-spam system.")
            sent += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to send message {i}: {e}")
            await ctx.send(f"Failed to send message {i}: {e}")
            break
    
    await ctx.send(f"Finished sending {sent} spam messages.")

@bot.command(name="mentionspam")
@commands.has_permissions(administrator=True)
async def spam_mentions(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Send messages with multiple mentions"""
    await ctx.reply(f"Sending {count} mention spam messages with {delay}s delay...")
    
    # Get mentionable roles
    mentionable_roles = [role for role in ctx.guild.roles 
                         if role.mentionable and 
                         not role.managed and 
                         role.id != ctx.guild.id][:3]
    
    sent = 0
    for i in range(count):
        try:
            mention_text = f"Test mention spam #{i} - {ctx.author.mention} "
            
            # Add role mentions if available
            if mentionable_roles:
                mention_text += " ".join(role.mention for role in mentionable_roles)
            
            await ctx.send(mention_text)
            sent += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to send mention spam {i}: {e}")
            await ctx.send(f"Failed to send mention spam {i}: {e}")
            break
    
    await ctx.send(f"Finished sending {sent} mention spam messages.")

@bot.command(name="namechange")
@commands.has_permissions(administrator=True)
async def change_guild_name(ctx, count: int = 3, delay: float = DEFAULT_DELAY):
    """Change server name multiple times"""
    original_name = ctx.guild.name
    await ctx.reply(f"Changing server name {count} times with {delay}s delay...")
    
    changed = 0
    for i in range(count):
        try:
            await ctx.guild.edit(name=f"Test Server Name {i}", reason="Anti-nuke bot testing")
            changed += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to change server name {i}: {e}")
            await ctx.send(f"Failed to change server name {i}: {e}")
            break
    
    # Restore original name
    try:
        await ctx.guild.edit(name=original_name, reason="Restoring original name")
        await ctx.send(f"Finished changing server name {changed} times. Restored original name.")
    except discord.HTTPException as e:
        logger.error(f"Failed to restore original server name: {e}")
        await ctx.send(f"Failed to restore original server name: {e}")

@bot.command(name="banspam")
@commands.has_permissions(administrator=True)
async def ban_users(ctx, count: int = 5, delay: float = DEFAULT_DELAY):
    """Simulate banning multiple users"""
    # This is a simulated ban test - we'll just report what would happen
    await ctx.reply(f"SIMULATION: Would ban {count} users with {delay}s delay...")
    await ctx.send("This is a simulation only - no actual bans will be performed.")
    
    # Get a role to simulate banning from
    target_role = next((role for role in ctx.guild.roles 
                        if not role.managed and role.id != ctx.guild.id), None)
    
    if not target_role:
        return await ctx.send("No suitable role found for simulation.")
    
    await ctx.send(f"Simulating banning members from role: {target_role.name}")
    
    # Simulate the bans
    for i in range(count):
        try:
            await ctx.send(f"SIMULATION: Would ban user #{i} from role {target_role.name}")
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Error in ban simulation {i}: {e}")
            await ctx.send(f"Error in ban simulation {i}: {e}")
            break
    
    await ctx.send(f"Finished ban simulation for {count} users.")

@bot.command(name="permissionattack")
@commands.has_permissions(administrator=True)
async def permission_attack(ctx, count: int = 3, delay: float = DEFAULT_DELAY):
    """Modify permissions on multiple channels"""
    await ctx.reply(f"Modifying permissions on {count} channels with {delay}s delay...")
    
    # Get channels where we can modify permissions
    channels = [channel for channel in ctx.guild.channels 
                if channel.id != ctx.channel.id and
                isinstance(channel, discord.TextChannel) and
                channel.permissions_for(ctx.guild.me).manage_channels][:count]
    
    if not channels:
        return await ctx.send("No modifiable channels found.")
    
    modified = 0
    for channel in channels:
        try:
            # Give everyone permission to manage the channel
            await channel.set_permissions(
                ctx.guild.default_role,
                manage_channels=True,
                manage_webhooks=True,
                reason="Anti-nuke bot testing"
            )
            modified += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to modify permissions for {channel.name}: {e}")
            await ctx.send(f"Failed to modify permissions for {channel.name}: {e}")
            break
    
    await ctx.send(f"Finished modifying permissions on {modified} channels.")

@bot.command(name="webhookmessagespam")
@commands.has_permissions(administrator=True)
async def webhook_message_spam(ctx, count: int = 10, delay: float = DEFAULT_DELAY):
    """Send multiple messages through webhooks"""
    await ctx.reply(f"Sending {count} webhook spam messages with {delay}s delay...")
    
    # Create a webhook if none exists
    webhooks = await ctx.channel.webhooks()
    webhook = next((w for w in webhooks), None)
    
    if not webhook:
        try:
            webhook = await ctx.channel.create_webhook(name="Test Webhook", reason="Anti-nuke bot testing")
        except discord.HTTPException as e:
            logger.error(f"Failed to create webhook: {e}")
            return await ctx.send(f"Failed to create webhook: {e}")
    
    sent = 0
    for i in range(count):
        try:
            await webhook.send(
                content=f"Webhook spam message #{i} - Testing anti-spam protection",
                username=f"Test User {i}"
            )
            sent += 1
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Failed to send webhook message {i}: {e}")
            await ctx.send(f"Failed to send webhook message {i}: {e}")
            break
    
    await ctx.send(f"Finished sending {sent} webhook spam messages.")

@bot.command(name="multiattack")
@commands.has_permissions(administrator=True)
async def multi_attack(ctx, count: int = 3, delay: float = DEFAULT_DELAY):
    """Perform multiple attack vectors simultaneously"""
    await ctx.reply(f"Performing multi-vector attack with {count} iterations and {delay}s delay...")
    
    # Create a channel
    try:
        channel = await ctx.guild.create_text_channel(name="attack-test-channel", reason="Anti-nuke bot testing")
        await ctx.send(f"Created channel {channel.mention} for attack testing")
    except discord.HTTPException as e:
        logger.error(f"Failed to create test channel: {e}")
        channel = ctx.channel
    
    # Perform multiple actions
    for i in range(count):
        try:
            # Create a role
            role = await ctx.guild.create_role(name=f"Attack Test Role {i}", reason="Anti-nuke bot testing")
            await ctx.send(f"Created role {role.name}")
            
            # Create a webhook
            webhook = await channel.create_webhook(name=f"Attack Test Webhook {i}", reason="Anti-nuke bot testing")
            await ctx.send(f"Created webhook {webhook.name}")
            
            # Send a message with mentions
            await ctx.send(f"Multi-attack test message #{i} with mention: {ctx.author.mention}")
            
            # Send a webhook message
            await webhook.send(content=f"Webhook message from multi-attack test #{i}")
            
            await asyncio.sleep(delay)
        except discord.HTTPException as e:
            logger.error(f"Error in multi-attack iteration {i}: {e}")
            await ctx.send(f"Error in multi-attack iteration {i}: {e}")
    
    await ctx.send(f"Finished multi-vector attack test with {count} iterations.")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You need Administrator permissions to use this bot.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Unknown command. Use `{PREFIX} help` to see available commands.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.reply(f"An error occurred: {error}")

# Run the bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_ATOKEN")
    if not token:
        logger.error("No Discord token found. Please set the DISCORD_ATOKEN environment variable.")
        exit(1)
    
    bot.run(token)
