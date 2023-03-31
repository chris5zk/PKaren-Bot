import discord
from discord import app_commands
from discord.ext.commands import has_permissions
from tools.extension import CogExtension
from tools.log import log_message


class Manage(CogExtension):
    @app_commands.command(name="delete", description="delete a stack of message")
    @has_permissions(administrator=True)
    async def delete(self, interaction: discord.Interaction, num: int):
        log_msg = f'{interaction.user} is using commands【/delete】'
        await log_message(self.backend, log_msg, guild=interaction.guild, command=True)
        await interaction.response.send_message(f'Deleting...')
        await interaction.channel.purge(limit=num+1)
        await interaction.followup.send(f'{num} message are deleted!')


async def setup(bot):
    await bot.add_cog(Manage(bot))
