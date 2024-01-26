# puz-bot

A slack-bolt app that acknowledges recipt of 
events, commands, etc from slack.

Publishes a message containing the data payload from Slack to a Google Cloud pub/sub topic to trigger additional functionality

# required ENV
BOT_TOKEN = Bot token from Slack
SIGNING_SECRET = Signing Secret from Slack
PROJECT_ID = Google Cloud project ID
PUBSUB_TOPIC = Google Cloud pub/sub topic