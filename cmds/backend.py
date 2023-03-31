import discord
from discord import app_commands
from discord.ext.commands import has_permissions
from tools.extension import CogExtension
from tools.log import log_message


class Backend(CogExtension):
    @app_commands.command(name="log", description="read the daily log file exclude today")
    @has_permissions(administrator=True)
    async def log(self, interaction: discord.Interaction, date: str):
        log_msg = f'{interaction.user} is using commands【/log】'
        await log_message(self.backend, log_msg, guild=interaction.guild, channel=interaction.channel, command=True)
        try:
            await interaction.response.send_message(f'Log file of {date}', file=discord.File(f'.\\logs\\logfile_{date}.log'))
        except FileNotFoundError:
            await interaction.response.send_message(f'Log file not found!!!\n'
                                                    f'> date format: YYYY-MM-DD\n'
                                                    f'> example: 2023-02-13')

    # @commands.command()
    # async def audit(self, ctx):
    #     if ctx.message.author.guild_permissions.administrator:
    #         async for entry in ctx.guild.audit_logs(limit=1):
    #             await ctx.send(f'**{entry.user.name}#{entry.user.discriminator}** do【{str(entry.action).split("AuditLogAction.")[1]}】')


async def setup(bot):
    await bot.add_cog(Backend(bot))
