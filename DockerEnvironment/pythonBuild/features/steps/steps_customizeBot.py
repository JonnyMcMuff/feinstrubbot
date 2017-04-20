from behave import *
from mock import *
from start import Feinstrubbot
#from feinstrubbot.feinstrubdbpy import  FeinstrubDbManager

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other

def prepare():
    # prepare all the stuff
    bot = Mock
    bot.sendMessage = MagicMock()
    scheduler = Mock()
    returnValue = MagicMock()
    returnValue.inserted_id = 1420
    users = Mock
    users.insert_one = MagicMock(return_value=returnValue)
    gmaps = Mock()
    gmaps.geocode = MagicMock(return_value=[{'geometry': {'location': {'lat': 48.77363949999999, 'lng': 9.17069},
                                                          'viewport': {'southwest': {'lat': 48.7722905197085,
                                                                                     'lng': 9.169341019708497},
                                                                       'northeast': {'lat': 48.7749884802915,
                                                                                     'lng': 9.172038980291502}},
                                                          'location_type': 'ROOFTOP'}, 'partial_match': True,
                                             'types': ['street_address'],
                                             'place_id': 'ChIJg0Yy5kjbmUcR4QkTPqlizqA',
                                             'address_components': [{'long_name': '41/1', 'types': ['street_number'],
                                                                     'short_name': '41/1'},
                                                                    {'long_name': 'Rotebühlplatz', 'types': ['route'],
                                                                     'short_name': 'Rotebühlpl.'},
                                                                    {'long_name': 'Stuttgart-Mitte',
                                                                     'types': ['political', 'sublocality',
                                                                               'sublocality_level_1'],
                                                                     'short_name': 'Stuttgart-Mitte'},
                                                                    {'long_name': 'Stuttgart',
                                                                     'types': ['locality', 'political'],
                                                                     'short_name': 'Stuttgart'},
                                                                    {'long_name': 'Stuttgart',
                                                                     'types': ['administrative_area_level_2',
                                                                               'political'], 'short_name': 'Süd'},
                                                                    {'long_name': 'Baden-Württemberg',
                                                                     'types': ['administrative_area_level_1',
                                                                               'political'], 'short_name': 'BW'},
                                                                    {'long_name': 'Germany',
                                                                     'types': ['country', 'political'],
                                                                     'short_name': 'DE'},
                                                                    {'long_name': '70178', 'types': ['postal_code'],
                                                                     'short_name': '70178'}],
                                             'formatted_address': 'Rotebühlpl. 41/1, 70178 Stuttgart, Germany'}])
    return Feinstrubbot(users=users, bot=bot, gmaps=gmaps, scheduler=scheduler)

@given('that the user is registered to the service (customize)')
def step_impl(context):
    context.feinstaub = prepare()
    context.feinstaub.userExists = MagicMock(return_value=True)


@when('the the user text to the bot "Set quiet hours from $start$ to $end$"')
def step_impl(context):
    bot = context.feinstaub.bot
    username = Mock()
    username.message.from_user.id = 1420
    username.message.chat_id = 420
    username.message.from_user.first_name = "TestUser"
    username.message.text = "Please notify my every 5 min"
    context.feinstaub.text(bot, username)

@then('the user is notified about the his saved customisation.')
def step_impl(context):
    return context.feinstaub.bot.sendMessage.assert_called_with(chat_id=420,
                                                                text=AnyStringWith("Now I'm gonna keep you every"))



#-------------------------------------------------------------------------------------------------


@given('that the user is registered to the service (customize1)')
def step_impl(context):
    context.feinstaub = prepare()
    context.feinstaub.userExists = MagicMock(return_value=True)

@when('the user text to the bot "Set quiet hours from $start$ to $end$"')
def step_impl(context):
    bot = context.feinstaub.bot
    username = Mock()
    username.message.from_user.id = 1420
    username.message.chat_id = 420
    username.message.from_user.first_name = "TestUser"
    username.message.text = "Set quiet hours from 20:00 to 22:00"
    context.feinstaub.text(bot, username)

@then('the user is notified about the his new quiet hours.')
def step_impl(context):
    return context.feinstaub.bot.sendMessage.assert_called_with(chat_id=420,
                                                                text=AnyStringWith("TestUser please provide a valid time interval. Like '5 min' or '2 hours'. Please keep in mind, that we also the number 1 (1 hour ~ every hour)"))

#-------------------------------------------------------------------------------------------------
@given('that the user is registered to the service (customize2)')
def step_impl(context):
    context.feinstaub = prepare()
    context.feinstaub.userExists = MagicMock(return_value=True)

@when('the the user text to the bot "Please call me NewUsername"')
def step_impl(context):
    bot = context.feinstaub.bot
    username = Mock()
    username.message.from_user.id = 1420
    username.message.chat_id = 420
    username.message.from_user.first_name = "TestUser"
    username.message.text = "Please call me NewUsername"
    context.feinstaub.text(bot, username)

@then('the user is notified about the his new name.')
def step_impl(context):
    return context.feinstaub.bot.sendMessage.assert_called_with(chat_id=420,
                                                                text=AnyStringWith("Ok, now I'm gonna call you NewUsername"))
