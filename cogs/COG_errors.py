import discord
from discord.ext import commands
import log

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.log = log.log

    #Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Te falta un argumento requerido\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.MissingRole):
            await ctx.send(f"Necesitas otro rol!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f"Necesitas tener rol!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"No tienes el permiso necesario!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send(f"Te sobran comillas!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Parámetro inválido!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"Esto no funciona en DM!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f"Error en el check del comando! Contacta a @Appu#2187 si quieres saber más!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"El comando no existe o lo has escrito mal:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f"Comando desactivado!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"Error interno del comando! Repórtalo cuanto antes a @Appu#2187!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(f"El error lo dice todo.:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"Para eso hace falta ser el propietario del bot!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.ExtensionError):
            await ctx.send(f"Error en una extensión!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send(f"Extensión ya cragada!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(f"Extensión no cargada:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.NoEntryPointError):
            await ctx.send(f"Falta el setup de la extensión!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send(f"Error en el setup de la extensión!:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(f"Esa extensión ni siquiera existe:confused:\n*(Error: {error})*")
            await log.log(ctx, f"Error: {error}")

        # elif isinstance(error, ):
        #     await ctx.send(f":confused:\n*(Error: {error})*")
        #     await log.log(ctx, f"Error: {error}")

def setup(client):
    client.add_cog(Errors(client))
