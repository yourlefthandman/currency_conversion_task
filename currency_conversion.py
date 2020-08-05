import os
import sys
import json
import requests

API_CURRENY_RATES_URL = "https://openexchangerates.org/api/latest.json?app_id=b2cbe8b400fc436aa16a0e0ce37ab618"


def get_currency_rates():
    """
    This function returns the rates of conversion from USD to other currencies
    """
    get_response = requests.get(API_CURRENY_RATES_URL)
    assert get_response.ok, "Failed get request from currency API"
    json_cont = json.loads(get_response.text)
    return json_cont['rates']


def get_currency_ratio(src_currency, dst_currency):
    currency_rates = get_currency_rates()

    assert src_currency in currency_rates
    assert dst_currency in currency_rates

    return currency_rates[dst_currency] / currency_rates[src_currency]


def handle_file_currency_conversion(file_name):
    assert os.path.isfile(file_name), "File {} does not exists".format(file_name)

    with open(file_name, "r") as f:
        input_file_content = f.read()

    # Separate the currency names and the values to convert
    input_file_lines = input_file_content.replace("\r\n", "\n").split("\n")
    assert len(input_file_lines) >= 2, "Two currencies must be given, input data is not valid"
    src_currency, dst_currency = input_file_lines[:2]
    values_to_convert = input_file_lines[2:]

    # Get the currency ratio between the given currencies
    value_ratio = get_currency_ratio(src_currency, dst_currency)

    # For every value - print the value after the ratio conversion
    for value in values_to_convert:
        print(float(value) * value_ratio)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage {} <Name of file>".format(sys.argv[0]))
        exit()

    input_file_name = sys.argv[1]

    # Handle conversion of values in file
    handle_file_currency_conversion(input_file_name)
