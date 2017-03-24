# feinstrubbot
[![Build Status](https://travis-ci.org/JonnyMcMuff/feinstrubbot.svg?branch=master)](https://travis-ci.org/JonnyMcMuff/feinstrubbot)</br>
--------
Telegram bot which notifies the user if there is high fine dust pollution in Stuttgart.

## prerequisite
First Install docker on your machine. For further instructions check out the Docker [documentation](https://docs.docker.com/engine/installation/).</br>

Get a GoogleAPI token.
Get a Telegram Bot token.

## setup

After installing Docker clone the repository by using</br>
`git clone https://github.com/JonnyMcMuff/feinstrubbot.git`</br>
Change your directory</br>
`cd feinstrubbot`</br>
Bring up the Docker-Stack by executing:</br>
`cd DockerEnvironment`</br>
`docker-compose up`</br>

## usage
In order to recieve notifications start a chat witch `@nils_test_bot`.

### list of available commands

command | parameter | result
------------ | ------------- | -------------
Please call me | `[NAME]` | Set a custom nickname
Remove from my locations: | `[LOCATIONNAME]` | Removes location from your list of locations
Add to my locations: | `[LOCATIONNAME]` | Add location
My current location is | `[LOCATIONNAME]` | Set default your location
How is the air quality in | `[LOCATIONNAME]` | Returns air-quality from location
How is the air quality? |  | Returns air-quality from default location
What are my locations stats? |  | Returns your locations
