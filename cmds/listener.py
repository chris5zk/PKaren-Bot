import discord
from datetime import datetime
from discord.ext import commands
from tools.extension import CogExtension
from tools.log import log_message
from tools.data import get_json


class Listener(CogExtension):
    # Messages Listener
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel != self.backend and msg.channel != self.welcome and msg.channel != self.leave and msg.channel != self.announce:
            if not msg.content.startswith(self.bot.command_prefix):
                urls = [x.url for x in msg.attachments]
                stickers = [x.url for x in msg.stickers]
                if msg.reference:
                    reply = f" -> reply {msg.reference.jump_url} by {msg.reference.resolved.author if msg.reference.resolved else 'Unknown'}"
                log_msg = f"{msg.author}: {msg.content} {urls if urls else ''} {f'(Stickers: {stickers})' if stickers else ''} ({msg.id})" \
                          f"{reply if msg.reference else ''}"
                await log_message(self.backend, log_msg, guild=msg.guild, channel=msg.channel)

    @commands.Cog.listener()
    async def on_message_edit(self, msg_bf, msg_af):
        if msg_bf.channel != self.backend:
            log_msg = f"{msg_bf.author} edit content: {msg_bf.content} -> {msg_af.content}"
            await log_message(self.backend, log_msg, guild=msg_bf.guild, channel=msg_bf.channel)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id != self.backend and not payload.cached_message:
            guild = await self.bot.fetch_guild(payload.guild_id)
            channel = await self.bot.fetch_channel(payload.channel_id)
            log_msg = f"{payload.data['author']['username']} edit the raw content sent at {payload.data['timestamp'][:10]} -> {payload.data['content']}"
            await log_message(self.backend, log_msg, guild=guild.name, channel=channel.name)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.channel != self.backend:
            log_msg = f'Message of {msg.author} is deleted: {msg.content} ({msg.id})'
            await log_message(self.backend, log_msg, guild=msg.guild, channel=msg.channel, command=0)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.channel_id != self.backend and not payload.cached_message:
            guild = await self.bot.fetch_guild(payload.guild_id)
            channel = await self.bot.fetch_channel(payload.channel_id)
            log_msg = f'Raw message({payload.message_id}) is deleted.'
            await log_message(self.backend, log_msg, guild=guild.name, channel=channel.name, command=0)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, message):
        pass

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        pass

    # Members Listeners
    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_msg = f'{member} join the server.'
        embed = discord.Embed(title=f"Welcome to {member.guild}", description=f"Hello {member.mention}, relax and enjoy!", color=0x45cacd,
                              timestamp=datetime.now())
        embed.set_author(name="PKaren Bot", icon_url=self.bot.user.avatar.url, url="")
        embed.set_thumbnail(url=member.guild.icon if member.guild.icon else None)
        fields = [("Server Owner", f"{member.guild.owner.mention}", True),
                  ("Assistant", f"{self.bot.user.mention}", True),
                  ("Server Created At", f"{member.guild.created_at.strftime('%Y-%m-%d')}", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_image(url="https://media.discordapp.net/attachments/1077626848709709934/1077627200620204102/images.png")
        embed.set_footer(text="Timestamp")
        await self.welcome.send(embed=embed)
        await log_message(self.backend, log_msg, guild=member.guild, command=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_msg = f"{member} leave the server."
        await self.leave.send(log_msg)
        await log_message(self.backend, log_msg, guild=member.guild, command=0)

    # Guilds Listeners
    @commands.Cog.listener()
    async def on_guild_update(self, guild_old, guild_new):
        if guild_old.name != guild_new.name:
            log_msg = f"【{guild_old}】guild name change to 【{guild_new}】"
            await log_message(self.backend, log_msg, guild=guild_old)

    # @commands.Cog.listener()
    # async def on_guild_join(self):
    #     pass
    #
    # @commands.Cog.listener()
    # async def on_guild_remove(self):
    #     pass

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        log_msg = f"The Invite Code created by {invite.inviter}: {invite.code}"
        await log_message(self.backend, log_msg, guild=invite.guild, command=True)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        log_msg = f"The Invite Code deleted: {invite.code}"
        await log_message(self.backend, log_msg, guild=invite.guild, command=0)

    # Channels Listeners
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_msg = f'Channel "{channel.name}" is created.'
        await log_message(self.backend, log_msg, guild=channel.guild, command=True)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_msg = f'Channel "{channel.name}" is deleted.'
        await log_message(self.backend, log_msg, guild=channel.guild, command=0)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_bf, channel_af):
        if channel_bf.name != channel_af.name:
            log_msg = f'Channel name update: "{channel_bf.name}" -> "{channel_af.name}"'
            await log_message(self.backend, log_msg, guild=channel_bf.guild)


async def setup(bot):
    await bot.add_cog(Listener(bot))
