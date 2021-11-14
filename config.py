#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")#B8ls6I3mBMEXKcluov")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")#ac741b4a-08c6-45e4-b2fa-40dd46e85ed9")
    LUIS_APP_ID = os.environ.get("LUIS_APP_ID", "79b52831-0ac7-4089-825a-dbd70496bd3a")
    LUIS_API_KEY = os.environ.get("LUIS_API_KEY", "85a4549a0029455c882c6a04a2e6197d")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "e3493735-8516-4a46-a754-1ad2348cf0f5"
    )
