import asyncio
import datetime
import typing
import argparse
import enum

from discord.ext import commands
from discord.ext.commands.core import wrap_callback

from .custom_context import PrintContext
from .custom_cog import Cog
from .interactions.application_commands import ApplicationCommandType


class DiscordArgparser(argparse.ArgumentParser):

    @classmethod
    async def convert(cls, ctx, value):

        # Set up our parser
        parser = cls(add_help=False)  # exit_on_error only exists in later versions. Unfortunate.
        original_converters = {}
        for packed in ctx.command.argparse:
            try:
                *args, kwargs = packed
            except ValueError:
                *args, kwargs = packed, dict()
            converter = kwargs.pop("type", str)
            added = parser.add_argument(*args, **kwargs)
            original_converters[added.dest] = converter

        # Convert the given args
        try:
            args = parser.parse_args(value.split())
        except (argparse.ArgumentError, SystemExit) as e:
            ctx.bot.logger.error(e, exc_info=True)
            raise commands.BadArgument(str(e))
        for dest, kwarg_value in args._get_kwargs():
            converter = original_converters[dest]
            if isinstance(kwarg_value, (list, tuple)):
                converted = list()
                for i in kwarg_value:
                    converted.append(await ctx.command.do_conversion(ctx, converter, i, None))
            else:
                converted = await ctx.command.do_conversion(ctx, converter, kwarg_value, None)
            setattr(args, dest, converted)

        # Parse the arguments
        return args


class Command(commands.Command):
    """
    A custom command class subclassing :class:`discord.ext.commands.Command` so that we can add
    some more attirbutes to it. Unlike normal Discord.py, the :attr:`cooldown_after_parsing` attribute
    is set to `True` by default. Can be used in a normal :code:`@commands.command`'s `cls` attribute, but easier
    is to just use this library's :code:`@command`;

    ::

        @voxelbotutils.command()
        async def example(self, ctx):
            ...

    Attributes:
        locally_handled_errors (typing.List[discord.ext.commands.CommandError]): A list of errors
            that are handled by the command's :func:`on_error` method before being passed onto
            the main bot's error handler.
        add_slash_command (bool): Whether or not this command should be added as a slash command.
        argument_descriptions (typing.List[str]): A list of descriptions for the command arguments to
            be used in slash commands.
        argparse (typing.Tuple[str, ..., typing.Dict[str, typing.Any]]): A list of args and kwargs
            to be expanded into argparse.

            For instance, if you had a ban command and wanted to specify a ban time with a :code:`-days` flag,
            you could set that up like so:

            ::

                @voxelbotutils.command(argparse=(
                    ("-days", "-d", {"type": int, "default": 0, "nargs": "?"}),
                ))
                async def ban(self, ctx, user: discord.Member, *, namespace: argparse.Namespace):
                    ban_time: int = namespace.days  # Conversion is handled automatically
                    ...

        context_command_type (voxelbotutils.ApplicationCommandType): The type of context command that your
            given command should be added as.
        context_command_name (str): The name of the context command that should be added.
    """

    def __init__(self, *args, **kwargs):
        """:meta private:"""

        super().__init__(*args, cooldown_after_parsing=kwargs.pop('cooldown_after_parsing', True), **kwargs)
        self.ignore_checks_in_help: bool = kwargs.get('ignore_checks_in_help', False)
        self.locally_handled_errors: list = kwargs.get('locally_handled_errors', None)
        self.add_slash_command: bool = kwargs.get('add_slash_command', True)
        self.argument_descriptions: typing.List[str] = kwargs.get('argument_descriptions', list())
        self.argparse: list = kwargs.get('argparse', list())
        self.context_command_type: ApplicationCommandType = kwargs.get("context_command_type", None)
        self.context_command_name: str = kwargs.get("context_command_name", None)

        # Fix cooldown to be our custom type
        cooldown = self._buckets._cooldown
        if cooldown is None:
            mapping = commands.CooldownMapping  # No mapping
        elif getattr(cooldown, 'mapping', None) is not None:
            mapping = cooldown.mapping  # There's a mapping in the instance
        elif getattr(cooldown, 'default_mapping_class') is not None:
            mapping = cooldown.default_mapping_class()  # Get the default mapping from the object
        else:
            raise ValueError("No mapping found for cooldown")
        self._buckets = mapping(cooldown)  # Wrap the cooldown in the mapping

    def get_remaining_cooldown(self, ctx: commands.Context, current: float = None) -> typing.Optional[float]:
        """
        Gets the remaining cooldown for a given command.

        Args:
            ctx (discord.ext.commands.Context): The context object for the command/author.
            current (float, optional): The current time.

        Returns:
            typing.Optional[float]: The remaining time on the user's cooldown or `None`.
        """

        bucket = self._buckets.get_bucket(ctx.message)
        return bucket.get_remaining_cooldown()

    async def _prepare_cooldowns(self, ctx: commands.Context):
        """
        Prepares all the cooldowns for the command to be called.

        :meta private:
        """

        if self._buckets.valid:
            current = ctx.message.created_at.replace(tzinfo=datetime.timezone.utc).timestamp()
            bucket = self._buckets.get_bucket(ctx.message, current)
            try:
                coro = bucket.predicate(ctx)
                if asyncio.iscoroutine(coro) or asyncio.iscoroutinefunction(coro):
                    await coro
            except AttributeError:
                ctx.bot.logger.critical(f"Invalid cooldown set on command {ctx.invoked_with}")
                raise commands.CheckFailure("Invalid cooldown set for this command")
            retry_after = bucket.update_rate_limit(current)
            if retry_after:
                try:
                    error = bucket.error
                    if error is None:
                        raise AttributeError
                except AttributeError:
                    error = getattr(bucket, 'default_cooldown_error', commands.CommandOnCooldown)
                raise error(bucket, retry_after)

    async def prepare(self, ctx: commands.Context):
        """
        This is entirely stolen from the original method so I could make `prepare_cooldowns` an async
        method.

        https://github.com/Rapptz/discord.py/blob/a4d29e8cfdb91b5e120285b605e65be2c01f2c87/discord/ext/commands/core.py#L774-L795

        :meta private:
        """

        ctx.command = self

        if not isinstance(ctx, PrintContext):
            if not await self.can_run(ctx):
                raise commands.CheckFailure('The check functions for command {0.qualified_name} failed.'.format(self))

        if self._max_concurrency is not None:
            await self._max_concurrency.acquire(ctx)

        try:
            if self.cooldown_after_parsing:
                await self._parse_arguments(ctx)
                await self._prepare_cooldowns(ctx)
            else:
                await self._prepare_cooldowns(ctx)
                await self._parse_arguments(ctx)
            await self.call_before_hooks(ctx)
        except Exception:
            if self._max_concurrency is not None:
                await self._max_concurrency.release(ctx)
            raise

    def _check_converter_is_argparser(self, annotation):
        return any((
            annotation in [argparse.ArgumentParser, argparse.Namespace],
            isinstance(annotation, (argparse.ArgumentParser, argparse.Namespace)),
        ))

    async def _actual_conversion(self, ctx, converter, argument, param):
        if self._check_converter_is_argparser(converter):
            converter = DiscordArgparser
        elif isinstance(converter, (enum.Enum, enum.IntEnum, enum.EnumMeta)):
            try:
                return converter[argument]
            except Exception:
                pass
        return await super()._actual_conversion(ctx, converter, argument, param)

    async def transform(self, ctx, param):
        try:
            return await super().transform(ctx, param)
        except commands.MissingRequiredArgument:
            if param.kind == param.KEYWORD_ONLY and self._check_converter_is_argparser(param.annotation):
                return await DiscordArgparser.convert(ctx, "")
            raise

    async def dispatch_error(self, ctx, error):
        """
        Like how we'd normally dispatch an error, but we deal with local lads.

        :meta private:
        """

        # They didn't set anything? Default behaviour then
        if self.locally_handled_errors is None:
            return await super().dispatch_error(ctx, error)

        ctx.command_failed = True

        # See if we want to ping the local error handler
        if isinstance(error, self.locally_handled_errors):

            # If there's no `on_error` attr then this'll fail, but if there IS no `on_error`, there shouldn't
            # be anything in `self.locally_handled_errors` and we want to raise an error anyway /shrug
            injected = wrap_callback(self.on_error)
            if self.cog:
                ret = await injected(self.cog, ctx, error)
            else:
                ret = await injected(ctx, error)

            # If we ping the local error handler and it returned FALSE then we ping the other error handlers;
            # if not then we return here
            if ret is False:
                pass
            else:
                return ret

        # Ping the cog error handler
        try:
            if self.cog is not None:
                local = Cog._get_overridden_method(self.cog.cog_command_error)
                if local is not None:
                    wrapped = wrap_callback(local)
                    await wrapped(ctx, error)

        # Ping the global error handler
        except Exception:
            ctx.bot.dispatch('command_error', ctx, error)


class Group(commands.Group):

    def __init__(self, *args, **kwargs):
        """:meta private:"""

        super().__init__(*args, cooldown_after_parsing=kwargs.pop('cooldown_after_parsing', True), **kwargs)
        self.ignore_checks_in_help: bool = kwargs.get('ignore_checks_in_help', False)
        self.locally_handled_errors: list = kwargs.get('locally_handled_errors', None)
        self.add_slash_command: bool = kwargs.get('add_slash_command', True)

        # Fix cooldown to be our custom type
        cooldown = self._buckets._cooldown
        if cooldown is None:
            mapping = commands.CooldownMapping  # No mapping
        elif getattr(cooldown, 'mapping', None) is not None:
            mapping = cooldown.mapping  # There's a mapping in the instance
        elif getattr(cooldown, 'default_mapping_class') is not None:
            mapping = cooldown.default_mapping_class()  # Get the default mapping from the object
        else:
            raise ValueError("No mapping found for cooldown")
        self._buckets = mapping(cooldown)  # Wrap the cooldown in the mapping

    async def can_run(self, ctx: commands.Context) -> bool:
        """
        The normal :func:`discord.ext.Command.can_run` but it ignores cooldowns.

        Args:
            ctx (discord.ext.commands.Context): The command we want to chek if can be run.

        Returns:
            bool: Whether or not the command can be run.
        """

        if self.ignore_checks_in_help:
            return True
        try:
            return await super().can_run(ctx)
        except commands.CommandOnCooldown:
            return True

    def command(self, *args, **kwargs):
        """
        Add the usual :class:`voxelbotutils.Command` to the mix.
        """

        if 'cls' not in kwargs:
            kwargs['cls'] = Command
        return super().command(*args, **kwargs)

    def group(self, *args, **kwargs):
        """
        Add the usual :class:`voxelbotutils.Group` to the mix.
        """

        if 'cls' not in kwargs:
            kwargs['cls'] = Group
        if 'case_insensitive' not in kwargs:
            kwargs['case_insensitive'] = True
        return super().group(*args, **kwargs)

    def subcommand_group(self, *args, **kwargs):
        """
        Add the usual :class:`voxelbotutils.Group` to the mix.
        """

        if 'cls' not in kwargs:
            kwargs['cls'] = SubcommandGroup
        if 'case_insensitive' not in kwargs:
            kwargs['case_insensitive'] = True
        return super().group(*args, **kwargs)

    async def dispatch_error(self, ctx, error):
        """
        Like how we'd normally dispatch an error, but we deal with local lads.

        :meta private:
        """

        # They didn't set anything? Default behaviour then
        if self.locally_handled_errors is None:
            return await super().dispatch_error(ctx, error)

        ctx.command_failed = True

        # See if we want to ping the local error handler
        if isinstance(error, self.locally_handled_errors):

            # If there's no `on_error` attr then this'll fail, but if there IS no `on_error`, there shouldn't
            # be anything in `self.locally_handled_errors` and we want to raise an error anyway /shrug
            injected = wrap_callback(self.on_error)
            if self.cog:
                ret = await injected(self.cog, ctx, error)
            else:
                ret = await injected(ctx, error)

            # If we ping the local error handler and it returned FALSE then we ping the other error handlers;
            # if not then we return here
            if ret is False:
                pass
            else:
                return ret

        # Ping the cog error handler
        try:
            if self.cog is not None:
                local = Cog._get_overridden_method(self.cog.cog_command_error)
                if local is not None:
                    wrapped = wrap_callback(local)
                    await wrapped(ctx, error)

        # Ping the global error handler
        except Exception:
            ctx.bot.dispatch('command_error', ctx, error)


class SubcommandGroup(Group):
    """
    A subcommand group specifically made so that slash commands can be just a little sexier.
    """

    pass
