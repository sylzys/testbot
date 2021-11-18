import os


class AppConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "#B8ls6I3mBMEXKcluov")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "ac741b4a-08c6-45e4-b2fa-40dd46e85ed9")

    LUIS_APP_ID = os.environ.get("LUIS_APP_ID", "79b52831-0ac7-4089-825a-dbd70496bd3a")
    LUI_APP_VERSION = 0.1
    LUIS_API_KEY = os.environ.get("LUIS_API_KEY", "85a4549a0029455c882c6a04a2e6197d")
    LUIS_ENDPOINT = os.environ.get("LUIS_ENDPOINT", "https://flymep10.cognitiveservices.azure.com/")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")

    AUTHORING_KEY = os.environ.get("authoringKey", "66807a9398664e19b8e0c19e912ffc9e")
    AUTHORING_ENDPOINT = os.environ.get("authoringEndpoint", "https://luisocrp10-authoring.cognitiveservices.azure.com/")

    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("AppInsightsInstrumentationKey")
    APPINSIGHTS_INSTRUMENTATION_STRING = os.environ.get("AppInsightsInstrumentationString")

    INTENTS = ["BookFlight", "Cancel"]
    ENTITIES = ["From", "To", "Departure", "Return", "Budget"]
    PREBUILT_ENTITIES = ["datetimeV2"]

    TEST_SIZE = 0.2
    CANCEL_EXAMPLES = ["Quit", "Cancel", "Cancel booking", "Exit", "Bye"]
    NONE_EXAMPLES = [
        "What's the nearest hotel ?",
        "I want to book a quiet camping",
        "Do you think you can find an amazing trip ?",
        "Winter is coming",
        "My friends and I wanna have a great time",
        "I'd like to rent a car",
        "Find an airport near me",
        "Book an hotel in New York",
        "Find an asian restaurant",
        "Weather in India",
        "I'd like to book an hotel in Seattle",
        "What's the weather in New York tomorrow",
        "Where to eat a pizza in new york",
        "I want to eat a pizza",
        "I can t find a pizza at Roma",
        "I can t find a hotel in new york",
        "I  looking for a hotel",
        "I can t find a hotel at Paris",
        "I can t find a hotel at Seattle",
        "Where can I buy groceries ?",
        "I can t find a restaurant in new york",
        "I'm in Paris where can I eat ?",
        "I'm looking for a store in new york",
        "I can t find a store in Paris",
        "My family needs vacations in new york",
        "We want vacations",
        "i m looking for a pizza in new york",
        "i m looking for a pizza in Paris",
        "i m looking for a hamburger in Seattle",
        "i want some salad, I'm in brooklyn",
        "i m looking for some good time in new york",
        "i m looking for some good time in Paris",
        "Where can we have good family time ?",
        "i m looking for a hotel",
        "i m looking for a hotel at new york",
        "Book me an hotel room",
        "Where are the sneakers stores ?",
        "Is there kitchen stores in Miami ?",
        "i m looking for a store in Seattle",
        "I really need a break",
        "Where to go on vacations ?"
        "book a hotel in new york",
        "book a hotel in Paris",
        "book a restaurant table for 6",
        "book a restaurant table with menu under 30 in Paris",
        "book vacations tomorrow",
        "We want to go on vacations in Paris",
        "find me tacos in Roma",
        "find a hotel in new york",
        "I'm looking for a restaurant in new york",
        "we need a pizza in new york",
        "we need a pizza in Paris",
        "we want a sauna",
        "we need a place with Wifi and a spa",
        "My friends and I are in Ibiza we want some goot times",
        "we really want a pizza in new york"
    ]
