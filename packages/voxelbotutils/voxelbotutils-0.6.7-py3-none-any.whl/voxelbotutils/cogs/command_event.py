from . import utils as vbu


class CommandEvent(vbu.Cog):

    CONTENT_LIMIT = 50

    @vbu.Cog.listener("on_command")
    async def on_command_log(self, ctx: vbu.Context):
        """
        Pinged when a command is invoked.
        """

        if ctx.command is None:
            return
        logger = getattr(getattr(ctx, 'cog', self), 'logger', self.logger)
        content = ctx.message.content.replace('\n', '\\n')[:self.CONTENT_LIMIT]
        if len(ctx.message.content) > self.CONTENT_LIMIT:
            content += '...'
        invoke_text = "Command invoked"
        if ctx.is_interaction:
            if getattr(ctx, "given_values", None) is not None:
                invoke_text = "Context invoked"
            else:
                invoke_text = "Interaction invoked"
        logger_prefix = f"{invoke_text} ({ctx.command.qualified_name.strip()})"
        if ctx.guild is None:
            return logger.info(f"{logger_prefix} ~ (G0/C{ctx.channel.id}/U{ctx.author.id}) :: {content}")
        logger.info(f"{logger_prefix} ~ (G{ctx.guild.id}/C{ctx.channel.id}/U{ctx.author.id}) :: {content}")

    @vbu.Cog.listener("on_command")
    async def on_command_statsd(self, ctx: vbu.Context):
        """
        Ping statsd.
        """

        command_stats_name = ctx.command.qualified_name.replace(' ', '_')
        command_stats_tags = {"command_name": command_stats_name, "slash_command": ctx.is_interaction}
        async with self.bot.stats() as stats:
            stats.increment("discord.bot.commands", tags=command_stats_tags)


def setup(bot: vbu.Bot):
    x = CommandEvent(bot)
    bot.add_cog(x)
