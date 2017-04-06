from behave import *
from DockerEnvironment.pythonBuild.start import Feinstrubbot
from mock import *

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other

def prepare():
    # prepare all the stuff
    client = Mock()
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
    return Feinstrubbot(users=users, bot=bot, gmaps=gmaps, scheduler=scheduler, client=client)

@given('that there is a working setup of an external database')
def step_impl(context):
    context.feinstaub = prepare()


@when('the bot tries to connect to the database')
def step_impl(context):
    context.feinstaub.connectToDB = MagicMock()
    context.feinstaub.connectToDB()


@then('it should get a working connection and be able to retrieve user data')
def step_impl(context):
    return context.feinstaub.connectToDB.assert_called()