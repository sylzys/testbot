# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging

import requests
from botbuilder.core import (BotTelemetryClient, CardFactory, MessageFactory,
                             NullTelemetryClient, TurnContext)
from botbuilder.dialogs import (ComponentDialog, DialogTurnResult,
                                WaterfallDialog, WaterfallStepContext)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt
from botbuilder.schema import Attachment, InputHints
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

from booking_details import BookingDetails
from config import DefaultConfig
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import Intent, LuisHelper

from .adaptive_card_example import FlightCard
from .booking_dialog import BookingDialog

CONFIG = DefaultConfig()


class MainDialog(ComponentDialog):
    def __init__(
        self,
        luis_recognizer: FlightBookingRecognizer,
        booking_dialog: BookingDialog,
        logger,
        telemetry_client: BotTelemetryClient = None,
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()
        # self.logger = logger
        # self.tracer = tracer
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = self.telemetry_client

        booking_dialog.telemetry_client = self.telemetry_client

        wf_dialog = WaterfallDialog(
            "WFDialog", [self.intro_step, self.act_step, self.final_step]
        )
        wf_dialog.telemetry_client = self.telemetry_client

        self._luis_recognizer = luis_recognizer
        self._logger = logger
        self._booking_dialog_id = booking_dialog.id

        self.add_dialog(text_prompt)
        self.add_dialog(booking_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = "WFDialog"

        self.logger = logging.getLogger(__name__)
        config = DefaultConfig()
        self.logger.addHandler(AzureLogHandler(connection_string=config.APPINSIGHTS_INSTRUMENTATION_STRING))

        stats = stats_module.stats
        view_manager = stats.view_manager
        stats_recorder = stats.stats_recorder

        exporter = metrics_exporter.new_metrics_exporter(connection_string=config.APPINSIGHTS_INSTRUMENTATION_STRING)
        view_manager.register_exporter(exporter)

        self.bot_measure = measure_module.MeasureInt(
            "Botdefects",
            "Number of bot errors",
            "BotErrors"
        )

        bot_view = view_module.View(
            "Bot Error View",
            "Number of bot errors",
            [],
            self.bot_measure,
            aggregation_module.CountAggregation()
        )
        view_manager.register_view(bot_view)

        self.accepted_booking_measure = measure_module.MeasureInt(
            "Accepted Bookings",
            "Amount of accepted bookings",
            "Accepted"
        )
        accepted_booking_view = view_module.View(
            "Accepted Booking view",
            "Amount of accepted bookings",
            [],
            self.accepted_booking_measure,
            aggregation_module.CountAggregation()
        )
        view_manager.register_view(accepted_booking_view)

        self.canceled_booking_measure = measure_module.MeasureInt(
            "Canceled Bookings",
            "Amount of canceled bookings",
            "Canceled"
        )

        canceled_booking_view = view_module.View(
            "Canceled Booking view",
            "number of Canceled booking",
            [],
            self.canceled_booking_measure,
            aggregation_module.CountAggregation()
        )
        view_manager.register_view(canceled_booking_view)

        self.bot_mmap = stats_recorder.new_measurement_map()
        self.bot_tmap = tag_map_module.TagMap()

        self.accepted_mmap = stats_recorder.new_measurement_map()
        self.accepted_tmap = tag_map_module.TagMap()

        self.canceled_mmap = stats_recorder.new_measurement_map()
        self.canceled_tmap = tag_map_module.TagMap()

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )
            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        if intent == Intent.GET_WEATHER.value:
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            self.logger.error("Bot dod not understand {}".format(luis_result), self.bot_mmap)
            self.bot_mmap.measure_int_put(self.bot_measure, 1)
            self.bot_mmap.record(self.bot_tmap)
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        reply = MessageFactory.list([])
        if step_context.result is not None:
            result = step_context.result
            print(result)
            msg_txt = f"I have you booked to {result.destination} from {result.origin}.\
                You'll be leaving on {result.departure_date}, and come back on {result.return_date}.\
                Your budget is {result.budget}."
            self.logger.warning(f"User has accepted the booking: {msg_txt}")
            self.accepted_mmap.measure_int_put(self.accepted_booking_measure, 1)
            self.accepted_mmap.record(self.accepted_tmap)
            print(CONFIG.PLACES[result.origin.lower()], CONFIG.PLACES[result.destination.lower()])
            await step_context.context.send_activity("Fetching SkyScanner quotes...")
            print("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/{}/{}/{}/{}?apikey=prtl6749387986743898559646983194".format(CONFIG.PLACES[result.origin.lower().strip()], CONFIG.PLACES[result.destination.lower().strip()], result.departure_date, result.return_date))
            r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/{}/{}/{}/{}?apikey=prtl6749387986743898559646983194"
                             .format(CONFIG.PLACES[result.origin.lower().strip()], CONFIG.PLACES[result.destination.lower().strip()], result.departure_date, result.return_date))
            quotes = r.json()
            if 'code' in quotes and quotes['code'] == 429:
                await step_context.context.send_activity("Skyscanner is unreachable at the moment...")
                result.outbound_carrier = ''
                result.inbound_carrier = ''
                result.airports = []
                result.quotes = result.budget

            else:
                result.outbound_carrier = quotes['Carriers'][0]['Name']
                result.inbound_carrier = quotes['Carriers'][1]['Name']
                result.airports = []
                result.quotes = str(quotes['Quotes'][0]['MinPrice'])
                for place in quotes['Places']:
                    if 'IataCode' in place:
                        result.airports.append(place['IataCode'])

            reply.attachments.append(self.create_adaptive_card(result))
            await step_context.context.send_activity(reply)
        else:
            self.logger.error("User has canceled the booking", self.canceled_mmap)
            self.canceled_mmap.measure_int_put(self.canceled_booking_measure, 1)
            self.canceled_mmap.record(self.canceled_tmap)
        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

    def create_adaptive_card(self, result) -> Attachment:
        return CardFactory.adaptive_card(FlightCard.generate_card(result))

    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: BookingDetails
    ) -> None:
        """
        Shows a warning if the requested From or To cities are recognized as entities but they are not in the Airport entity list.
        In some cases LUIS will recognize the From and To composite entities as a valid cities but the From and To Airport values
        will be empty if those entity values can't be mapped to a canonical item in the Airport.
        """
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f"{', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
