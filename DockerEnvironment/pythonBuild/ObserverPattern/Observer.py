#!/usr/bin/env python
class Subscriber:
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))
        
class Publisher:
    def __init__(self):
        self.subscribers = list()
    def register(self, who):
        self.subscribers.append(who)
    def unregister(self, who):
        self.subscribers.remove(who)
    def dispatch(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)