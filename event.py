import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from layer.common.utils import init_event


init_event()
# Install the Slack app and get xoxb- token in advance
app = App(
  token=os.environ.get('SLACK_BOT_TOKEN', None),
  signing_secret=os.environ.get('SLACK_SIGNING_SECRET', None)
)

@app.message("hello")
def message_hello(message, say):
  say(f"Hey there <@{message['user']}>!")

# Listens to incoming messages that contain "hello"
@app.message("show button")
def message_hello(message, say):
  # say() sends a message to the channel where the event was triggered
  say(
    # blocks 사용법 
    # https://api.slack.com/reference/block-kit/blocks
    blocks=[
      	{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*This* is :smile: markdown"
				},
				{
					"type": "image",
					"image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
					"alt_text": "cute cat"
				},
				{
					"type": "plain_text",
					"text": "Author: K A Applegate",
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click Me",
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		}
    ],
    text=f"Hey there <@{message['user']}>!"
  )

@app.action("button_click")
def action_button_click(body, ack, say):
  # Acknowledge the action
  ack()
  say(f"<@{body['user']['id']}> clicked the button")


if __name__ == "__main__":
  SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN', None)).start()
