import json
import pytest
import currency_conversion


def get_currency_rates_for_tests():
    # Read rates from a saved json
    with open("rates_for_tests.json", "r") as f:
        json_cont = json.load(f)
    return json_cont['rates']


def test_currency_values():
    test_rates = get_currency_rates_for_tests()
    current_rates = currency_conversion.get_currency_rates()

    # For every rate we have in the test rates
    for rate in test_rates:
        # Make sure the rate exists in the current rates
        assert rate in current_rates
        # Make sure the value is valid (has changed a maximum of 50%)
        assert float(current_rates[rate]) == pytest.approx(test_rates[rate], rel=0.5)


def test_currency_ratios_same_currency():
    assert currency_conversion.get_currency_ratio("USD", "USD") == 1
    assert currency_conversion.get_currency_ratio("ILS", "ILS") == 1


def test_currency_ratios_different_currencies():
    src_currency, dst_currency = "USD", "ILS"

    # Get ratio from test values
    test_rates = get_currency_rates_for_tests()
    test_ratio = test_rates[dst_currency] / test_rates[src_currency]

    # Get actual ratio
    current_ratio = currency_conversion.get_currency_ratio(src_currency, dst_currency)

    # Assert ratios are similar
    assert current_ratio == pytest.approx(test_ratio, rel=0.5)
