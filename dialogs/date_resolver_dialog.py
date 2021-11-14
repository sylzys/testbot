# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Handle date/time resolution for booking dialog."""

from botbuilder.core import (BotTelemetryClient, MessageFactory,
                             NullTelemetryClient)
from botbuilder.dialogs import (DialogTurnResult, WaterfallDialog,
                                WaterfallStepContext)
from botbuilder.dialogs.prompts import (DateTimePrompt, DateTimeResolution,
                                        PromptOptions, PromptValidatorContext)
from datatypes_date_time.timex import Timex

from .cancel_and_help_dialog import CancelAndHelpDialog


def are_dates_wrong(departure_date, return_date):
    if return_date is None or departure_date is None or return_date >= departure_date:
        return False
    else:
        if return_date < departure_date:
            return True


class DateResolverDialog(CancelAndHelpDialog):
    """Resolve the date"""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(DateResolverDialog, self).__init__(
            dialog_id or DateResolverDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client

        date_time_prompt = DateTimePrompt(
            DateTimePrompt.__name__, DateResolverDialog.datetime_prompt_validator
        )
        date_time_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__ + "2", [self.initial_step, self.final_step]
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(date_time_prompt)
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__ + "2"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the date."""
        timex = step_context.options['field']
        booking_details = step_context.options['booking_details']
        print(booking_details.get_details())
        if booking_details.departure_date is None:
            prompt_msg = "When would you like to leave ?"
        else:
            prompt_msg = "When will you come back ?"
        # prompt_msg = "On what date would you like to travel?"
        reprompt_msg = (
            "I'm sorry, for best results, please enter your travel "
            "date including the month, day and year."
        )

        if timex is None:
            print("TIMEX NONE")
            # We were not given any date at all so prompt the user.
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(  # pylint: disable=bad-continuation
                    prompt=MessageFactory.text(prompt_msg),
                    retry_prompt=MessageFactory.text(reprompt_msg),
                ),
            )
        # We have a Date we just need to check it is unambiguous.
        if "definite" in Timex(timex).types:
            print("TIMEW DEFINITE")
            # This is essentially a "reprompt" of the data we were given up front.
            return await step_context.prompt(
                DateTimePrompt.__name__, PromptOptions(prompt=reprompt_msg)
            )
        print("we got all", timex)
        return await step_context.next(DateTimeResolution(timex=timex))

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Cleanup - set final return value and end dialog."""
        timex = step_context.result[0].timex
        booking_details = step_context.options['booking_details']
        print("final step", timex)
        prompt_msg = ("I'm sorry, return date can't be before departure date. Please re-enter your return date.")
        # reprompt_date_msg = (
        #     "I'm sorry, return date can't be before departure date. Please re-enter your return date."
        # )
        if are_dates_wrong(booking_details.departure_date, timex):
            print("TIMEX WRONG")
            # return date is before departure date
            booking_details.return_date = None
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(  # pylint: disable=bad-continuation
                    prompt=MessageFactory.text(prompt_msg),
                    # retry_prompt=MessageFactory.text(reprompt_date_msg),
                ),
            )
        # else:
        #     return await step_context.next(DateTimeResolution(timex=timex))
        return await step_context.end_dialog(timex)

    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """Validate the date provided is in proper form."""
        print("PROMPT VALIDATOR")
        if prompt_context.recognized.succeeded:
            timex = prompt_context.recognized.value[0].timex.split("T")[0]
            return "definite" in Timex(timex).types
        return False
