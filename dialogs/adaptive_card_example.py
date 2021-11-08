# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Example content for an AdaptiveCard."""


class FlightCard():
    """Flight card """

    def __init__(
        self
    ):
        super(FlightCard, self).__init__(FlightCard.__name__)

    def generate_card(result):
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "type": "AdaptiveCard",
            "speak": "Here is your ticket",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Passengers",
                    "weight": "bolder",
                    "isSubtle": False,
                },
                {"type": "TextBlock", "text": "FlyMe Customer", "separator": True},
                {
                    "type": "TextBlock",
                    "text": "Direct",
                    "weight": "bolder",
                    "spacing": "medium",
                },
                {
                    "type": "TextBlock",
                    "text": result.departure_date,
                    "weight": "bolder",
                    "spacing": "none",
                },
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": [
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": result.origin.capitalize(),
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": "",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {"type": "TextBlock", "text": " "},
                                {
                                    "type": "Image",
                                    "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                                    "size": "small",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": result.destination.capitalize(),
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": "",
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "TextBlock",
                    "text": "Direct",
                    "weight": "bolder",
                    "spacing": "medium",
                },
                {
                    "type": "TextBlock",
                    "text": result.return_date,
                    "weight": "bolder",
                    "spacing": "none",
                },
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": [
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {"type": "TextBlock", "text": result.destination.capitalize(), "isSubtle": True},
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": "",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {"type": "TextBlock", "text": " "},
                                {
                                    "type": "Image",
                                    "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                                    "size": "small",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": result.origin.capitalize(),
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": "",
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "ColumnSet",
                    "spacing": "medium",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "1",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Total",
                                    "size": "medium",
                                    "isSubtle": True,
                                }
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": "$"+result.budget,
                                    "size": "medium",
                                    "weight": "bolder",
                                }
                            ],
                        },
                    ],
                },
            ],
        }
