from slackclient import SlackClient

class publisher:
	def __init__(self):
		slackTokenFile = open("token", "r")
		slackToken = slackTokenFile.read()
		self.client = SlackClient(slackToken)

	def post(self, url, location="mailbot", message="mail!", name="photo"):
		self.client.api_call(
			"chat.postMessage",
			channel=location,
			text=message,
			attachments=[{"title":name, "image_url":url}])