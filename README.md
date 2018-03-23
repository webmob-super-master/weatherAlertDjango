# weatherAlertDjango
A Django web app using Wunderground to provide Slack alerts for poor weather conditions
---

weatherAlertDjango provides an easy-to-use Django app that can be used to programmatically send weather alerts for different geographical regions

## How it works

1. The user can deploy the app using Heroku or other hosting service.
2. Using Django's admin page, the user can add cities to alert.  Each city is associated with a region for multiple city batching.
3. Also in the admin page, the user can add responsible parties' Slack handles for each region.
4. Finally, Slack webhooks for the desired channel for the alerts may be added in the admin page.
5. Using the `/alert/<region>` endpoint all weather data for each city in the region is queried.
6. Inclement weather is flagged and sent to the designated channel from the set region webhook.  Responsible parties are also mentioned at the end of the message.

![Slack Notification](https://raw.githubusercontent.com/robertjkeck2/weatherAlertDjango/master/screenshots/Weather%20Bot.png)
