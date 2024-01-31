import json
import logging
import os

from google.cloud import pubsub_v1

from slack_bolt import App
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler

logging.basicConfig(level=logging.INFO)

# process_before_response must be True when running on FaaS
app = App(process_before_response=True, signing_secret=os.getenv("SIGNING_SECRET"), token=os.getenv("BOT_TOKEN"))

# Put some basic information on the bot home tab.
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    client.views_publish(
      user_id = event["user"],
      view={
        "type": "home",
        "callback_id": "home_view",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to PuzBot!* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "PuzBot is our attempt to streamline the mechanics of starting and stopping activity on a puzzle. More information about this is coming soon."
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "To contribute to Puzbot, please visit <https://github.com/adamshire123/puz-bot|*the Github repo*>"
            }
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# for testing
@app.command("/hello")
def hello_command(body, say, ack):
    logging.info(body)
    ack()
    say("Hi from Google Cloud Functions!")

# for testing
@app.event("app_mention")
def event_test(body, say, ack):
    logging.info(body)
    ack()
    say("Hi from Google Cloud Functions!")

# kick off new puzzle creation
@app.command("/init")
def initialize_puzzle(body, say, ack):
    ack('initializing puzzle...')
    if body['text']:
        send_pub_sub(body)
    else:
        say("please provide a puzzle name: e.g. puz-salad-daze")

# Listener for the demonstration modal
@app.shortcut("demonstrate_modal")
def demonstrate_modal(ack, shortcut, client, logger):
  ack()
  client.views_open(
    trigger_id=shortcut["trigger_id"],
    view={
      "type": "modal",
      "title": {"type": "plain_text", "text": "Demonstration modal box"},
      "close": {"type": "plain_text", "text": "Close"},
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "This is a demonstration of a modal box invoked by a shortcut. If this were a working form, there would be input boxes and a submit button.\n\nThis is only a demonstration."
          }
        }
      ]
    }
  )

handler = SlackRequestHandler(app)

# Cloud Function Entry Point
def cloud_function_handler(req):
   
    return handler.handle(req)

def send_pub_sub(data):

    project_id = os.getenv("PROJECT_ID")
    topic_id = os.getenv("PUBSUB_TOPIC")

    publisher = pubsub_v1.PublisherClient()
   
    topic_path = publisher.topic_path(project_id, topic_id)

    future = publisher.publish(topic_path, data=json.dumps(data).encode("utf8"))
    
    logging.info(future.result())
    logging.info(f"Published message to {topic_path}.")