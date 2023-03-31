import discord
from discord import app_commands
from discord.ext import commands
from tools.extension import CogExtension
from tools.log import log_message
from tools.data import get_json

data = get_json()


class Response(CogExtension):
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        if msg.content in data['key_word_1']:
            await msg.channel.send(file=discord.File(data['pic_1']), reference=msg, mention_author=False)
        if msg.content in data['key_word_2']:
            await msg.channel.send(file=discord.File(data['pic_2']), reference=msg, mention_author=False)
        if msg.content in data['key_word_3']:
            await msg.channel.send(file=discord.File(data['pic_3']), reference=msg, mention_author=False)

    @app_commands.command(name="hello", description="say hello")
    async def hello(self, interaction: discord.Interaction):
        log_msg = f'{interaction.user} is using commands【/hello】'
        await log_message(self.backend, log_msg, guild=interaction.guild, channel=interaction.channel, command=True)
        await interaction.response.send_message('Hello!')


async def setup(bot):
    await bot.add_cog(Response(bot))
