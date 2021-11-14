# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from botbuilder.core import (BotTelemetryClient, MessageFactory,
                             NullTelemetryClient)
from botbuilder.dialogs import (DialogTurnResult, WaterfallDialog,
                                WaterfallStepContext)
from botbuilder.dialogs.prompts import (ConfirmPrompt, NumberPrompt,
                                        PromptOptions, PromptValidatorContext,
                                        TextPrompt)
from datatypes_date_time.timex import Timex
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


# import requests
def is_budget_numeric(budget):
        import locale
        import re
        budget = re.sub(r'[$,.€]', '', budget)
        if re.search('[a-zA-Z]', budget) is not None:
            # print("VALUE", value)
            return False # contains non only number
        return True
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
        self.add_dialog(TextPrompt('budget', BookingDialog.budget_prompt_validator))
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__
        self.history = set()
        self.logger = None
        self.stats = stats_module.stats
        self.view_manager = self.stats.view_manager
        self.stats_recorder = self.stats.stats_recorder
        # self.bot_measure = measure_module.MeasureInt("botdefects",
        #                                              "number of bot defects",
        #                                              "botdefects")

        # self.bot_view = view_module.View("defect view",
        #                                  "number of bot defects",
        #                                  [],
        #                                  self.bot_measure,
        #                                  aggregation_module.CountAggregation())
        # self.view_manager.register_view(self.bot_view)
        # self.mmap = self.stats_recorder.new_measurement_map()
        # self.tmap = tag_map_module.TagMap()
        # self.mmap.measure_int_put(self.bot_measure, 90)
        # self.mmap.record(self.tmap)
        print("Done setting metrics")
        # self.metrics_exporter = 
    # def set_logger(self, logger):
    #     self.logger = logger

    # def set_metrics_exporter(self, metrics_exporter):
        # self.metrics_exporter = metrics_exporter.new_metrics_exporter(connection_string='InstrumentationKey=e3493735-8516-4a46-a754-1ad2348cf0f5')

        # self.view_manager.register_exporter(metrics_exporter)

    async def budget_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
    # This condition is our validation rule. You can also change the value at this point.
        return is_budget_numeric(prompt_context.recognized.value)
    
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
            print("sending return date", )
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
        print(booking_details.get_details(), "result", step_context.result)
        # Capture the response to the previous step's prompt
        if type(step_context.result) is str:
            booking_details.return_date = step_context.result
        else:
            booking_details.return_date = step_context.result[0].timex.split("T")[0]

        print(booking_details.get_details())
        if booking_details.budget is None:
            return await step_context.prompt(
                "budget",
                PromptOptions(
                    prompt=MessageFactory.text(" What's your budget ?"),
                    retry_prompt=MessageFactory.text(
                    "Budget must not contain letters."
                ),
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options
        self.history.add(step_context._turn_context.activity.text)
        print(booking_details.get_details(), "result", step_context.result)

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
