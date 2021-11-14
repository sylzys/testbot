# import sys
# import pathlib

# current = pathlib.Path(__file__).parent.parent
# libpath = current.joinpath("D:\\13.core-bot")
# sys.path.append(str(libpath))

# import app, json
# from bots.dialog_bot import DialogBot
# # from bots.dialog_bot import DialogBot
# import pytest
# import aiounittest
# from botbuilder.schema import Activity, ActivityTypes, Attachment
# from botbuilder.dialogs import DialogSet, DialogTurnStatus

# from botbuilder.core.adapters import TestAdapter
# from botbuilder.core import (
#     TurnContext, 
#     ConversationState, 
#     MemoryStorage, 
#     MessageFactory, 
# )

# from dialogs.cancel_and_help_dialog import CancelAndHelpDialog
# from dialogs.date_resolver_dialog import DateResolverDialog
# from dialogs import BookingDialog, MainDialog
# from dialogs import BookingDialog, MainDialog
# print(app.INSTRUMENTATION_KEY)
# from aiohttp import web
# from aiohttp.web import Request, Response, json_response
# from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
# from botbuilder.core import (BotFrameworkAdapterSettings, ConversationState,
#                              MemoryStorage, UserState)
# from botbuilder.core.integration import aiohttp_error_middleware
# from botbuilder.integration.applicationinsights.aiohttp import (
#     AiohttpTelemetryProcessor, bot_telemetry_middleware)
# from botbuilder.schema import Activity
# from botbuilder.dialogs.prompts import DateTimePrompt, PromptOptions
# from botbuilder.core import MessageFactory
# from botbuilder.core import ConversationState, MemoryStorage, TurnContext
# from botbuilder.dialogs import DialogSet, DialogTurnStatus
# from botbuilder.core.adapters import TestAdapter, TestFlow
# from config import DefaultConfig
# from adapter_with_error_handler import AdapterWithErrorHandler
# from bots import DialogAndWelcomeBot
# from config import DefaultConfig
# from dialogs import BookingDialog, MainDialog
# from flight_booking_recognizer import FlightBookingRecognizer
# import dialogs
# CONFIG = DefaultConfig()
# print("CONFIG", CONFIG)
# from botbuilder.dialogs import (DialogTurnResult, WaterfallDialog,
#                                 WaterfallStepContext)
# # Create adapter.
# # See https://aka.ms/about-bot-adapter to learn more about how bots work.
# SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)

# # Create MemoryStorage, UserState and ConversationState
# MEMORY = MemoryStorage()
# USER_STATE = UserState(MEMORY)
# CONVERSATION_STATE = ConversationState(MEMORY)

# # Create adapter.
# # See https://aka.ms/about-bot-adapter to learn more about how bots work.
# ADAPTER = AdapterWithErrorHandler(SETTINGS, CONVERSATION_STATE)

# # Create telemetry client.
# # Note the small 'client_queue_size'.  This is for demonstration purposes.  Larger queue sizes
# # result in fewer calls to ApplicationInsights, improving bot performance at the expense of
# # less frequent updates.
# INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY
# TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
#     INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=10
# )

# # Create dialogs and Bot
# RECOGNIZER = FlightBookingRecognizer(CONFIG)
# BOOKING_DIALOG = BookingDialog()
# DIALOG = MainDialog(RECOGNIZER, BOOKING_DIALOG, telemetry_client=TELEMETRY_CLIENT)
# BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG, TELEMETRY_CLIENT)


# import asyncio


# import aiounittest

# class DialogTest_(aiounittest.AsyncTestCase):
#     async def test_welcome(self):
#         async def exec_test(turn_context:TurnContext):
#             print("RESULqzdqsdss")
#             # dialog_context = await dialogs.create_context(turn_context)
#             # results = await dialog_context.continue_dialog()
#             print("RESULT", results)
#             # if (results.status == DialogTurnStatus.Empty):
                
#             # await dialog_context.members_added_activity("mockbot", "")
#                 # await dialog_context.prompt("emailprompt", "")
#             # else:
#             #     print("NOT EMPTY", results)
#         adapter = TestAdapter(exec_test)
#         dialogs_state = conv_state.create_property("dialog-state")
#         dialogs = DialogSet(dialogs_state)
#         dialogs.add(DialogBot(), "mockbot")
#         test_flow = TestFlow(None, adapter)
#         print("TRESTFLO", test_flow)
#         tf2 = await test_flow.send("hello")
#         print('TF4::::::::::', tf2)
#         await tf2.assert_reply("To what city would you like to travel?")
# #         # tf3 = await tf2.assert_reply("What date would you like?")
# #         # tf4 = await tf3.send("I want to travel to paris")
# #         # print('TF4::::::::::', tf2.reply)
# #         # await tf4.assert_reply("Timex: '2018-12-05T09' Value: '2018-12-05 09:00:00'")
        
#         # async def processActivity(activity, bot): 
#         #     context = TurnContext(adapter, activity)
#         #     await bot.run(context)



# def test_luis_intent():
#     """Check LUIS non-regression on *Top intent*
#     """
#     # Instantiate prediction client
#     clientRuntime = LUISRuntimeClient(
#         CONFIG.LUIS_API_HOST_NAME,
#         CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
#     # Create request
#     request ='book a flight from Tunis to Toronto between 22 October 2021 to 5 November 2021, for a budget of $3500'

#     # Get response
#     response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)

#     check_top_intent = 'BookFlight'
#     is_top_intent = response.top_scoring_intent.intent
#     assert check_top_intent == is_top_intent


# def test_luis_origin():
#     """Check LUIS non-regression on *Origin*
#     """
#     # Instantiate prediction client
#     clientRuntime = LUISRuntimeClient(
#         CONFIG.LUIS_API_HOST_NAME,
#         CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
#     # Create request
#     request ='book a flight from Tunis to Toronto between 22 October 2021 to 5 November 2021, for a budget of $3500'

#     # Get response
#     response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)
    
#     check_origin = 'tunis'
#     all_entities = response.entities
    
#     for i in range(0, len(all_entities)):
#         if all_entities[i].type == 'or_city':
#             is_origin = all_entities[i].entity
    
#     assert check_origin == is_origin


# def test_luis_destination():
#     """Check LUIS non-regression on *Destination*
#     """
#     # Instantiate prediction client
#     clientRuntime = LUISRuntimeClient(
#         CONFIG.LUIS_API_HOST_NAME,
#         CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))
    
#     # Create request
#     request ='book a flight from Tunis to Toronto between 22 October 2021 to 5 November 2021, for a budget of $3500'

#     # Get response
#     response = clientRuntime.prediction.resolve(CONFIG.LUIS_APP_ID, query=request)
    
#     check_destination = 'toronto'
#     all_entities = response.entities
    
#     for i in range(0, len(all_entities)):
#         if all_entities[i].type == 'dst_city':
#             is_destination = all_entities[i].entity
    
#     assert check_destination == is_destination
import pytest
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

from config import DefaultConfig

CONFIG = DefaultConfig()
print(CONFIG.LUIS_API_KEY)

@pytest.fixture(scope='module')
def client():
    return LUISRuntimeClient(
        CONFIG.LUIS_API_HOST_NAME,
        CognitiveServicesCredentials(CONFIG.LUIS_API_KEY))

@pytest.fixture(scope='module')
def user_request():
    return 'I want to travel to New York from Paris between December 20th 2021 to December 31st 2021, my budget is 2000'

@pytest.fixture(scope='module')
def response(client, user_request):
    response = client.prediction.resolve(CONFIG.LUIS_APP_ID, query=user_request)
    return response

@pytest.fixture(scope="module")
def entities(response):
    return response.entities
    
def test_intent(client, user_request, response):

    expected = 'BookFlight'
    is_top_intent = response.top_scoring_intent.intent
    assert expected == is_top_intent
    
def test_origin(client, user_request, entities):

    expected = 'paris'
    # all_entities = response.entities
    origin = ''
    
    for i in range(0, len(entities)):
        if entities[i].type == 'From':
            origin = entities[i].entity
    
    assert expected == origin


def test_destination(client, user_request, entities):
    expected = 'new york'
    destination = ''
    
    for i in range(0, len(entities)):
        if entities[i].type == 'To':
            destination = entities[i].entity
    
    assert expected == destination
<<<<<<< Updated upstream

    
=======
    
def test_airport(client, user_request, entities):
    expected = 'paris'
    airport = ''
    
    for i in range(0, len(entities)):
        if entities[i].type == 'Airport':
            airport = entities[i].entity
    
    assert expected == airport
>>>>>>> Stashed changes
