from slackclient import SlackClient

class Spublisher:
        def __init__(self):
                print("initializing Slack API...")

                slackTokenFile = open("slack/token", "r")
                slackToken = slackTokenFile.read()
                self.client = SlackClient(slackToken)

                print("done")

        def post(self, url, location="mailbot", message="mail!", name="photo"):
                self.client.api_call(
                        "chat.postMessage",
                        channel=location,
                        text=message,
                        attachments=[{"title":name, "image_url":url}])
