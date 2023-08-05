from discord.ext.commands import Cog, Bot, AutoShardedBot
from .client import SBLApiClient
from typing import Union

class SBLCog(
  Cog
):
  """Cog handler class for :class:`~sblpy.client.SBLApiClient`

  Parameters
  -----------
  bot: Union[:class:`~discord.ext.commands.Bot`, :class:`~discord.ext.commands.AutoShardedBot`]
    Your dpy Bot
  auth: :class:`~str`
    Your auth token of SBL Api
  """
  def __init__(
    self,
    bot: Union[
      Bot,
      AutoShardedBot
    ],
    auth: str
  ):
    """Constructor"""
    self.bot = bot
    if not hasattr(
      self.bot,
      "SBLClient"
    ):
      SBLApiClient(
        self.bot,
        auth
      )
    self.bot.add_cog(
      self
    )

  @Cog.listener()
  async def on_guild_join(
    self,
    guild
  ):
    """Posts server count when bot joins a guild"""
    self.bot.SBLClient.postBotStats()
    print("Posted stats on guild join")

  @Cog.listener()
  async def on_guild_remove(
    self,
    guild
  ):
    """Posts server count when bot leaves a guild"""
    self.bot.SBLClient.postBotStats()
    print("Posted stats on guild leave")

  @Cog.listener()
  async def on_ready(
    self
  ):
    """Posts server count when bot is ready to serve"""
    self.bot.SBLClient.postBotStats()
    print("Posted stats on ready")


  @classmethod
  def setup(
    cls,
    bot: Union[
      Bot,
      AutoShardedBot
    ],
    auth: str = ""
  ):
    """Main method

    Parameters
    -----------
    bot: Union[:class:`~discord.ext.commands.Bot`, :class:`~discord.ext.commands.AutoShardedBot`]
      Your dpy Bot
    auth: :class:`~str`
      Your auth token of SBL Api

    Examples
    ----------
    
    .. code-block:: python3

        from sblpy import SBLCog

        SBLCog.setup(bot, "SBL_AUTH_TOKEN")

    """
    cls(
      bot,
      auth
    )
