import requests


#Wunderground API Key
API_KEY = ''

#Interval to search for inclement weather
FORECAST_HOURS = 8

class HourlyWeather(object):
	"""Hourly weather class for Weather Alert app

	Determines the hourly weather using Wunderground API

	Attributes:
		locations (:obj:'list'): List containing city and state of queried location
		base_url (str): Base Wudnerground API url

	"""

	def __init__(self, locations):
		"""Initialize method

		Args:
			locations (:obj:'list'): List containing city and state of queried location

		"""

		self.locations = locations
		self.base_url = 'http://api.wunderground.com/api/'

	def request_api(self, api_endpoint):
		"""Wunderground API request

		Returns JSON response of queried location from requested Wunderground API endpoint

		Args:
			api_endpoint (str): Requested endpoint from Wunderground API

		Returns:
			response (:obj:'json'): JSON response from API request

		"""

		url = '{0}{1}{2}{3}/{4}.json'.format(self.base_url,
			API_KEY,
			api_endpoint,
			self.locations[1],
			self.locations[0])
		respone = requests.get(url).json()
		return respone

	def hourly(self):
		"""Hourly condition report

		Returns formatted forecast for requested interval

		Args:
			N/A

		Returns:
			formatted_forecast (:obj:'list'): List of time intervals and corresponding condition

		"""
		api_endpoint = '/hourly/q/'
		response = self.request_api(api_endpoint)
		weather = []
		hours = []
		if int(response["hourly_forecast"][0]["FCTTIME"]["hour"]) < 12:
		    forecast_hours = 14
		else:
		    forecast_hours = FORECAST_HOURS
		for i in range(0,forecast_hours):
			time = response["hourly_forecast"][i]["FCTTIME"]["civil"]
			condition = response["hourly_forecast"][i]["condition"]
			if i == 0:
				weather.append(condition)
				hours.append(time)
			else:
				prev_condition = response["hourly_forecast"][i-1]["condition"]
				prev_time = response["hourly_forecast"][i-1]["FCTTIME"]["civil"]
				if (condition != prev_condition):
					if i == 1:
						hours.append(time)
					else:
						hours.append(prev_time)
					weather.append(condition)
				elif (i == (forecast_hours - 1)):
					hours.append(time)

		forecast = []
		for j in range(0,len(hours) - 1):
			forecast.append('{} to {}'.format(hours[j], hours[j+1]))

		formatted_forecast = []
		for k in range(0,len(forecast)):
			formatted_forecast.append((forecast[k], weather[k]))

		return formatted_forecast
