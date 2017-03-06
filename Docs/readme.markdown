---
layout: "post"
title: "Setup"
date: "2017-03-03 15:45"
---
# Mongo-Python Stack
## Step by Step
1. change your current directory to DockerEnvironment (folder)
2. run docker-compose up -d and your good to go
3. If you have updated your scripts somehow use docker-compose build to update the python environment (volumes do not work - at least under my Windows setup)
4. Restart the environment docker-compose down and then docker-compose up -d

## Adding python libs from pip
In order to add libs to the python environment use pyhton pip
Add the libs you want in the dockerfile there is already one:
python -m pip install pymongo.
Modify it: python -m pip install pymongo yourlib

## The start script
There is a python script that is run once the container starts,
if it exits the container also exits.
There is a sample with some simple calls to MongoDB.

## Usage on localhost
You should be able to connect to MongoDB on localhost as well,
but your local python interpreter won't have pymongo installed.
You have to do it by yourself. I recommend a
[virtualenv][7d5bdd2c].

The pymongo connection is then client = MongoClient('localhost', 27017).

Have Fun

---
  [7d5bdd2c]: http://docs.python-guide.org/en/latest/dev/virtualenvs/ "Python Virtual Environements"
