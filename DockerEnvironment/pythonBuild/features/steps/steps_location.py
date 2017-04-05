from behave import *
from DockerEnvironment.pythonBuild.start import Feinstrubbot
from mock import *

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other

def prepare():
    # prepare all the stuff
    bot = Mock
    bot.sendMessage = MagicMock()
    scheduler = Mock()
    users = Mock
    users.update = MagicMock(return_value=True)
    users.find_one = MagicMock(return_value={
            "userID": 1234,
            "userName": 'TestUser',
            "locations": [
                {
                    "name": 'Rotebühlplatz 41, Stuttgart',
                    "longitude": 9.17069,
                    "latitude": 48.77363949999999
                }
            ],
            "quietHours": [
                {
                    "start": "22:00",
                    "end": "06:00"
                }
            ],
            "alarmInterval": 5,  # Timeinterval in minutes
            "lastAction": '2017-04-03 15:23:49.011481',
            "chat_id": 2233
        })
    gmaps = Mock()
    gmaps.geocode = MagicMock(return_value= [{'geometry': {'location': {'lat': 48.77363949999999, 'lng': 9.17069},
 'viewport': {'southwest': {'lat': 48.7722905197085, 'lng': 9.169341019708497},
 'northeast': {'lat': 48.7749884802915, 'lng': 9.172038980291502}},
 'location_type': 'ROOFTOP'}, 'partial_match': True, 'types': ['street_address'],
 'place_id': 'ChIJg0Yy5kjbmUcR4QkTPqlizqA', 'address_components': [{'long_name': '41/1', 'types': ['street_number'],
 'short_name': '41/1'}, {'long_name': 'Rotebühlplatz', 'types': ['route'], 'short_name': 'Rotebühlpl.'},
 {'long_name': 'Stuttgart-Mitte', 'types': ['political', 'sublocality', 'sublocality_level_1'], 'short_name': 'Stuttgart-Mitte'},
 {'long_name': 'Stuttgart', 'types': ['locality', 'political'], 'short_name': 'Stuttgart'},
 {'long_name': 'Stuttgart', 'types': ['administrative_area_level_2', 'political'], 'short_name': 'Süd'},
 {'long_name': 'Baden-Württemberg', 'types': ['administrative_area_level_1', 'political'], 'short_name': 'BW'},
 {'long_name': 'Germany', 'types': ['country', 'political'], 'short_name': 'DE'},
 {'long_name': '70178', 'types': ['postal_code'], 'short_name': '70178'}],
 'formatted_address': 'Rotebühlpl. 41/1, 70178 Stuttgart, Germany'}])
    # Create the Feinstrubbot
    return Feinstrubbot(users=users, bot=bot, gmaps=gmaps, scheduler=scheduler)

def side_effect_find_next_sensor_values():
    return {'location': {'id': 563, 'latitude': '48.772', 'longitude': '9.169'}, 'sensor': {'id': 1148, 'sensor_type': {'name': 'SDS011', 'manufacturer': 'Nova Fitness', 'id': 14}}, 'timestamp': '2017-04-04 22:29:27', 'id': 66409523, 'sensordatavalues': [{'value_type': 'P1', 'id': 184095361, 'value': '11.16'}, {'value_type': 'P2', 'id': 184095362, 'value': '9.55'}]}

@given('that the user is registered to the service')
def step_impl(context):
    context.feinstaub = prepare()


@when('the user sends My current location is xxxx')
def step_impl(context):
    bot = context.feinstaub.bot
    update = Mock()
    update.message.from_user.id = 1234
    update.message.text = "My current location is Rotebuehlplatz 41, Stuttgart"
    context.feinstaub.text(bot, update)

@then('data is updated in the backend')
def step_impl(context):
    return context.feinstaub.users.update.assert_called_once()

@when('the user has send a proper location update string')
#@patch('DockerEnvironment.pythonBuild.start.findNextSensorValues', side_effect=side_effect_find_next_sensor_values)
def step_impl(context):
    bot = context.feinstaub.bot
    update = Mock()
    update.message.from_user.id = 1234
    update.message.text = "My current location is Rotebuehlplatz 41, Stuttgart"
    update.message.chat_id = 155
    context.feinstaub.findNextSensorValues = MagicMock(return_value={'location': {'id': 563, 'latitude': '48.772', 'longitude': '9.169'}, 'sensor': {'id': 1148, 'sensor_type': {'name': 'SDS011', 'manufacturer': 'Nova Fitness', 'id': 14}}, 'timestamp': '2017-04-04 22:29:27', 'id': 66409523, 'sensordatavalues': [{'value_type': 'P1', 'id': 184095361, 'value': '11.16'}, {'value_type': 'P2', 'id': 184095362, 'value': '9.55'}]})
    context.feinstaub.text(bot, update)

@then('the user gets a confirmation about the location change')
def step_impl(context):
    return context.feinstaub.bot.sendMessage.assert_called_with(chat_id=155, text=AnyStringWith("Rotebuehlplatz"))


@when('the user has send a bad location update string')
def step_impl(context):
    bot = context.feinstaub.bot
    context.feinstaub.gmaps.geocode = MagicMock(return_value=False)
    update = Mock()
    update.message.text = "My current location is invalid"
    update.message.chat_id = 125
    update.message.from_user.id = 1123

    context.feinstaub.text(bot, update)

@then('the user gets a error message')
def step_impl(context):
    return context.feinstaub.bot.sendMessage.assert_called_with(chat_id=125,text="Can't find location")
