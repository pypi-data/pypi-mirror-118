from typing import Union
from discord import Client, AutoShardedClient
from discord.ext.commands import Bot, AutoShardedBot
from .http import Route
from .error import SBLError

class SBLApiClient:
  """SBLApiClient is the client of https://SmartBots.tk api

  Parameters
  ------------
  bot: Union[:class:`~discord.ext.commands.Bot`, :class:`~discord.ext.commands.AutoShardedBot`]
    Your dpy Bot
  auth_token: :class:`~str`
    Bot's auth token of SBL Api
  """
  def __init__(
    self,
    bot: Union[
      Bot,
      AutoShardedBot
    ],
    auth_token: str
  ) -> None:
    """Constructor"""
    self.bot = bot
    self.token = auth_token
    self.bot.SBLClient = self

  @property
  def id(
    self
  ) -> int:
    return int(
      self.bot.user.id
    )

  def postBotStats(
    self
  ):
    """Posts Bot's server count"""
    headers = {
      "authorization": str(
        self.token
      ),
      "Content-Type": "application/json"
    }
    payload = {
      "server_count": len(
        self.bot.guilds
      )
    }
    route = Route(
      "POST",
      "/stats/{id}",
      headers = headers,
      json = payload,
      id = self.id
    )
    try:
      resp = route.go().json()
    except:
      print(
        "Ignoring exception in postBotStats, SmartBots server is offline"
      )
      return

    if str(
      resp.get(
        "success"
      )
    ).lower() == "false":
        raise SBLError(
          resp.get(
            "error"
          )
        )

    return resp

  def getBotLikes(
    self
  ):
    """Get likers of bot who liked within 12hrs"""
    headers = {
      "authorization": str(self.token)
    }
    route = Route(
      "GET",
      "/liked/{id}",
      headers = headers,
      id = self.id
    )
    try:
      resp = route.go().json()
    except:
      print(
        "Ignoring exception in getBotLikes, SmartBots server is offline"
      )
      return

    if str(
      resp.get(
        "success"
      )
    ).lower() == "false":
        raise SBLError(
          resp.get(
            "error"
          )
        )

    return resp
