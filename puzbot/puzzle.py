# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os, logging

class Puzzle():
  """
  This is a wrapper for a puzzle. The intent is to use this to handle both the
  management of the Slack channel, as well as the Google Sheet, for a puzzle.
  This includes creation and solution events.
  """

  def __init__(self):
    self.data = {}
    self.data["channel-name"] = ""
    self.data["name"] = ""

  def create(self, client, logger, say, puzzle_name):
    self.data["name"] = puzzle_name
    self.data["channel-name"] = self.set_channel_name(logger, puzzle_name)

    try:
      # Call the conversations.create method using the WebClient
      # conversations_create requires the channels:manage bot scope
      result = client.conversations_create(
        name=self.data["channel-name"]
      )
      # Log the result which includes information like the ID of the conversation
      logger.info(result)
      say(f"The channel #{self.data["channel-name"]} has been created!")

    except Exception as e:
      # There is a more specific error which could be caught, but this works.
      logger.error("Error creating channel: {}".format(e))
      say(f"I tried to create the channel #{self.data["channel-name"]}. Unfortunately, I failed.")

  def set_channel_name(self, logger, puzzle_name):
    return "puzzle-" + puzzle_name.lower()
