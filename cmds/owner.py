import discord
from discord.ext import commands
from typing import Literal, Optional
from tools.extension import CogExtension
from tools.log import log_message


class Owner(CogExtension):
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        log_msg = f"【{extension}】 is loaded by {ctx.author}"
        await self.bot.load_extension(f'cmds.{extension}')
        await log_message(self.backend, log_msg, guild=ctx.guild, command=True)
        await ctx.send(log_msg)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        log_msg = f"【{extension}】 is unloaded by {ctx.author}"
        await self.bot.unload_extension(f'cmds.{extension}')
        await log_message(self.backend, log_msg, guild=ctx.guild, command=True)
        await ctx.send(log_msg)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        log_msg = f"【{extension}】 is reloaded by {ctx.author}"
        await self.bot.reload_extension(f'cmds.{extension}')
        await log_message(self.backend, log_msg, guild=ctx.guild, command=True)
        await ctx.send(log_msg)

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx, spec: Optional[Literal["~", "*", "^"]] = None):
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return


async def setup(bot):
    await bot.add_cog(Owner(bot))
