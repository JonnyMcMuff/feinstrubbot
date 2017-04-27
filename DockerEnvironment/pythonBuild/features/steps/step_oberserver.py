from behave import *
from SimpleFeinstaubObserver import *
from Observer import *

@given('that the user is subscribed to the alarm')
def step_impl(context):
	context.tBot = Publisher()
    context.tBot.register('Test') 
    
@when('the Feinstaubalarm is detected and the user has not been notified yet')
def step_impl(context):
    context.feinstaub.getAlarm()
    context.feinstaub.check4FeinstaubAlarm()
	context.tBot.dispatch("Test")

@then('the user is notified about the Feinstaub Alarm')
def step_impl(context):
    return context.tBot.subscribers.update.assert_called()