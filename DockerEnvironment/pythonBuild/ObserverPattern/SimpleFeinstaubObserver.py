#!/usr/bin/env python
from Observer import Publisher, Subscriber

tBot = Publisher()

users = []
users.append('Bob')
users.append('Chris')
users.append('Peter')

for user in users:
    tBot.register(Subscriber(user))

def deleteuser(name):
    for subscriber in tBot.subscribers:
        if(subscriber.name is name):
            tBot.unregister(tBot.subscribers[tBot.subscribers.index(subscriber)])
            print('Deleted: {}'.format(name))
            return
    print('User: {} not found'.format(name))

tBot.dispatch("Feinstaubalarm am 10.05.2017")

deleteuser('Peter')
deleteuser('John')
deleteuser('Chris')


tBot.dispatch("Feinstaubalarm am 15.05.2017")

tBot.register(Subscriber('Holly'))
deleteuser('Bob')

tBot.dispatch("Feinstaubalarm am 06.06.2017")

deleteuser('Holly')