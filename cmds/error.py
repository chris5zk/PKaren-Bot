from discord.ext import commands
from tools.extension import CogExtension
from cmds.backend import Backend
from cmds.owner import Owner
from cmds.send import Send


class Error(CogExtension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_command = f"{ctx.command}_error"
        if hasattr(ErrorHandler, error_command):
            exception = getattr(ErrorHandler, error_command)
            await exception(self, ctx, error)
            return
        else:
            await ErrorHandler.default_error(self, ctx, error)


async def setup(bot):
    await bot.add_cog(Error(bot))


class ErrorHandler:
    async def default_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command Not Found...")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Sorry {ctx.message.author.mention}, you do not have permissions to do that!")
        else:
            await ctx.send(error)
            print(error)

    @Send.embed.error
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing the argument.\n"
                           "> format: <title> <description>\n"
                           f"> example: {ctx.message.content} Welcome please")
        else:
            await ctx.send(error)
            print(error)

    @Backend.log.error
    async def log_error(self, ctx, error):
        await ctx.send(error)
        print(error)

    @Owner.load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, you don't have permission to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"【{ctx.command}】 is invoked! Please check the parameters again!")
        else:
            await ctx.send(error)
            print(error)

    @Owner.reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, you don't have permission to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"【{ctx.command}】 is invoked! Please check the parameters again!")
        else:
            await ctx.send(error)
            print(error)

    @Owner.unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, you don't have permission to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"【{ctx.command}】 is invoked! Please check the parameters again!")
        else:
            await ctx.send(error)
            print(error)

    @Owner.sync.error
    async def sync_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, you don't have permission for using 【{ctx.command}】")
        elif isinstance(error, commands.CommandLimitReached):
            await ctx.send(error)
        elif isinstance(error, commands.HTTPException):
            await ctx.send("Syncing the commands failed.")
        elif isinstance(error, commands.CommandSyncFailure):
            await ctx.send("Syncing the commands failed due to a user related error, typically because the command has invalid data. This is equivalent to an HTTP status code of 400.")
        elif isinstance(error, commands.MissingApplicationID):
            await ctx.send("The client does not have an application ID.")
        else:
            await ctx.send(error)
            print(error)
