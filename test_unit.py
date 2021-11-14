import pandas as pd
import pytest

from dialogs.booking_dialog import is_budget_numeric
from dialogs.date_resolver_dialog import are_dates_wrong

# import are_dates_wrong

@pytest.mark.parametrize("from_date, to_date, expected", [("2021-11-11", "2021-11-01", True), ("2021-11-11", "2021-11-21", False)]
)  
def test_are_dates_wrong(from_date, to_date, expected):
    assert expected == are_dates_wrong(from_date, to_date)
    
    
@pytest.mark.parametrize("budget, expected", [("$876", True), ("$87budget", False)]
)  
def test_are_dates_wrong(budget, expected):
    assert expected == is_budget_numeric(budget)
    