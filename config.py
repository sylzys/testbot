#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    LUIS_APP_ID = os.environ.get("LUIS_APP_ID", "")
    LUI_APP_VERSION = 0.1
    LUIS_API_KEY = os.environ.get("LUIS_API_KEY", "")
    LUIS_ENDPOINT = os.environ.get("LUIS_ENDPOINT", "https://flymep10.cognitiveservices.azure.com/")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")

    AUTHORING_KEY = os.environ.get("AUTHORING_KEY", "")
    AUTHORING_ENDPOINT = os.environ.get("AUTHORING_ENDPOINT", "")

    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("AppInsightsInstrumentationKey", "")
    APPINSIGHTS_INSTRUMENTATION_STRING = os.environ.get("AppInsightsInstrumentationString", "")

    PLACES = {
        "paris": "par",
        "london": "lond",
        "londres": "lond",
        "new york": "nyc",
        "roma": "rom",
        "rome": "rom",
        "miami": "mia",
        "madrid": "mad"
    }
