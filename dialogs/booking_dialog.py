# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from botbuilder.core import (BotTelemetryClient, MessageFactory,
                             NullTelemetryClient)
from botbuilder.dialogs import (DialogTurnResult, WaterfallDialog,
                                WaterfallStepContext)
from botbuilder.dialogs.prompts import ConfirmPrompt, PromptOptions, TextPrompt
from datatypes_date_time.timex import Timex

from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.departure_step,
                self.return_step,
                self.budget_step,
                self.confirm_step,
                self.final_step
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__
        self.history = set()
        self.logger = None
        self.stats = stats_module.stats
        self.view_manager = self.stats.view_manager
        self.stats_recorder = self.stats.stats_recorder
        self.bot_measure = measure_module.MeasureInt("botdefects",
                                                     "number of bot defects",
                                                     "botdefects")

        self.bot_view = view_module.View("defect view",
                                         "number of bot defects",
                                         [],
                                         self.bot_measure,
                                         aggregation_module.CountAggregation())
        self.view_manager.register_view(self.bot_view)
        self.mmap = self.stats_recorder.new_measurement_map()
        self.tmap = tag_map_module.TagMap()
        self.metrics_exporter = None

    def set_logger(self, logger):
        self.logger = logger

    def set_metrics_exporter(self, metrics_exporter):
        self.metrics_exporter = metrics_exporter
        self.view_manager.register_exporter(metrics_exporter)

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)

        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        print(booking_details.get_details())
        if booking_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def departure_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for departure date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)
        print(booking_details.get_details())
        # booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
        if not booking_details.departure_date or self.is_ambiguous(
            booking_details.departure_date
        ):
            # return await step_context.begin_dialog(
            #     DateResolverDialog.__name__, booking_details.departure_date
            # )  # pylint: disable=line-too-long
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, {"field": booking_details.departure_date, "booking_details": booking_details}
            )
        return await step_context.next(booking_details.departure_date)

    async def return_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for return date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)
        print(booking_details.get_details())
        # booking_details = step_context.options
        # Capture the results of the previous step
        booking_details.departure_date = step_context.result
        if not booking_details.return_date or self.is_ambiguous(
            booking_details.return_date
        ):
            # return await step_context.begin_dialog(
            #     DateResolverDialog.__name__, booking_details.return_date
            # )  # pylint: disable=line-too-long
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, {"field": booking_details.return_date, "booking_details": booking_details}
            )
        return await step_context.next(booking_details.return_date)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)

        # Capture the response to the previous step's prompt
        booking_details.return_date = step_context.result
        print(booking_details.get_details())
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(" What's your budget ?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)
        print(booking_details.get_details())

        # Capture the results of the previous step
        # booking_details.travel_date = step_context.result
        booking_details.budget = step_context.result
        msg = (
            f"Please confirm: you want to travel to { booking_details.destination }"
            f" from { booking_details.origin }, between { booking_details.departure_date}"
            f" and { booking_details.return_date}, with a budget of { booking_details.budget}"
            f"\n Is that correct ?"
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        if step_context.result:
            booking_details = step_context.options
            self.history.add(step_context._turn_context.activity.text)
            print(booking_details.get_details())
            # booking_details.return_date = step_context.result

            return await step_context.end_dialog(booking_details)

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
