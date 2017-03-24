# feinstrubbot
[![Build Status](https://travis-ci.org/JonnyMcMuff/feinstrubbot.svg?branch=master)](https://travis-ci.org/JonnyMcMuff/feinstrubbot)</br>
--------
Telegram bot which notifies the user if there is high fine dust pollution in Stuttgart.

## usage
In order to recieve notifications start a chat witch `@feinstrubbot` or add the bot to an existing group. Register for the service by executing the `/register [LOCATION]` command. Thereby the parameter location can be any location string the GoogleMaps API can handle.

## list of available commands

command | parameter | result
------------ | ------------- | -------------
/register | `[LOCATION]` | register for the feinstrubservice
/unregister | | unregister from the feinstrubservice
Please call me | `[NAME]` | Set a custom nickname
Remove from my locations: | `[LOCATION]` | Removes location from your list of locations
Add to my locations: | `[LOCATION]` | Add location
My current location is | `[LOCATION]` | Set default your location
How is the air quality in | `[LOCATION]` | Returns air-quality from location
How is the air quality? |  | Returns air-quality from default location
What are my locations stats? |  | Returns your locations


# setting up your own feinstrubbot

## prerequisite
First Install docker on your machine. For further instructions check out the Docker [documentation](https://docs.docker.com/engine/installation/).</br>

Get a GoogleAPI token. See this [Google API Key Tutorial](https://developers.google.com/maps/documentation/javascript/get-api-key) for further information. </br>

Get a Telegram Bot token. See the [Telegram Bot Documentation](https://core.telegram.org/bots) for further information. </br>

## setup

After installing Docker clone the repository by using</br>
`git clone https://github.com/JonnyMcMuff/feinstrubbot.git`</br>
Change your directory</br>
`cd feinstrubbot`</br>
Insert your GoogleAPI token in a file named `google.token` and your Telegram token into a file named `bot.token` and place them both into the `DockerEnvironment/pythonBuild/scripts` directory.</br>
Bring up the Docker-Stack by changing your current directory to `DockerEnvironment`. Then execute:</br>
`docker-compose up`</br>

Afterwards you can use your bot the same way you would use the original feinstrubbot. You only need to specify the name of your bot when your start a new chat. You can refer to your bot by using `@[YOUR_BOT_NAME]`
