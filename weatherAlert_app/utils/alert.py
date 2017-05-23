import requests

from .conditions import CONDITIONS


class Alert(object):
	"""Alert class for Weather Alert app

	Sends the queried weather alert to the midwest-weather slack channel at DoorDash

	Attributes:
		weather (:obj:'list'): List of weather conditions by hour
		location (str): Location where the weather alert is sent for

	"""

	def __init__(self, weather, location, webhook, region, ops_owner):
		"""Initialize method

		Args:
			weather (:obj:'list'): List of weather conditions by hour
			location (str): Location where the weather alert is sent for
			webhook (str): URL of incoming webhook for regional Slack channel
			region (str): Name of region associated with alert
			ops_owner(str): Slack handle for owner of region operations
		"""

		self.weather = weather
		self.location = location
		self.webhook = webhook
		self.region = region
		self.ops_owner = ops_owner
		self.name = "{} Weather Bot".format(self.region)

	def check_weather(self):
		"""Check the weather

		Iterates over time intervals to find inclement weather to alert about

		Args:
			N/A

		Returns:
			Calls alert_message method if inclement weather is found

		"""
		count = 0
		messages = []
		for hour in self.weather:
			for condition in CONDITIONS:
				if hour[1] == condition:
					count += 1
					messages.append(self.alert_message(hour))

		return count, messages

	def alert_message(self, hour):
		"""Write alert message

		Prepares the alert message to send in alert

		Args:
			hour (:obj:'list'): List of hour intervals for weather condition

		Returns:
			Calls the send_alert method after formatting the alert message

		"""

		msg = "{0} from {1} in {2}".format(hour[1], hour[0], self.location[0])
		self.send_alert(msg)
		return msg

	def notify_ops(self):
		"""Send notification to ops

		Sends the notification message to slack

		Args:
			N/A
		Returns:
			N/A

		"""

		payload = {
			"username": self.name,
			"icon_emoji": ":umbrella:",
			"text": self.ops_owner,
			"link_names": 1
		}

		response = requests.post(self.webhook, json=payload)
		return response

	def send_alert(self, msg):
		"""Send alert message

		Sends the alert message to slack

		Args:
			msg (str): Formatted alert message string

		Returns:
			N/A

		"""

		payload = {
			"username": self.name,
			'icon_emoji': ":umbrella:",
			"text": msg
		}

		response = requests.post(self.webhook, json=payload)
		return response
