import pytest
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

from config import DefaultConfig

CONFIG = DefaultConfig()


@pytest.fixture(scope='module')
def client():
    return LUISRuntimeClient(
        CONFIG.LUIS_ENDPOINT,
        CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))


@pytest.fixture(scope='module')
def user_request():
    return 'I want to travel to New York from Paris between December 20th 2021 to December 31st 2021, my budget is 2000'


def test_intent(client, user_request):
    response = client.prediction.resolve(CONFIG.LUIS_APP_ID, query=user_request)
    expected = 'BookFlight'
    is_top_intent = response.top_scoring_intent.intent
    assert expected == is_top_intent


def test_origin(client, user_request):
    response = client.prediction.resolve(CONFIG.LUIS_APP_ID, query=user_request)
    expected = 'paris'
    all_entities = response.entities
    origin = ''

    for i in range(0, len(all_entities)):
        print('ent', all_entities[i])
        if all_entities[i].type == 'From':
            origin = all_entities[i].entity

    assert expected == origin


def test_destination(client, user_request):
    response = client.prediction.resolve(CONFIG.LUIS_APP_ID, query=user_request)

    expected = 'new york'
    destination = ''
    all_entities = response.entities

    for i in range(0, len(all_entities)):
        if all_entities[i].type == 'To':
            destination = all_entities[i].entity
    assert expected == destination
