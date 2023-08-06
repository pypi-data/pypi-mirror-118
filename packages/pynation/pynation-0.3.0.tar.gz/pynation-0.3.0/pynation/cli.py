
import click
from pynation.data import country_data, currency_data, country_calling_code


def return_country(data_source, column):
    _country = data_source.get(column.title(), None)
    if _country is None:
        return
    return _country


@click.group()
def cli1():
    """Gives information about a country"""
    pass


@cli1.command()
@click.argument('country_name')
def info(country_name):
    """Brief information about a country."""

    country = return_country(country_data, country_name)
    currency = return_country(currency_data, country_name)
    calling_code = return_country(country_calling_code, country_name)

    if currency is None and country is None and calling_code is None:
        return click.secho('Country does not exist. Perhaps, write the full name?', fg='red')

    curr_name, curr_symbol, continent = '-' if country is None else currency[1], currency[3], currency[0]
    alpha2 = country[0] if country is not None else '-'
    call_code = calling_code[0] if country is not None else '-'

    click.echo(click.style(
        "\nInformation about {}:\n"
        "  - Continent: {}\n"
        "  - Calling-Code: +({})\n"
        "  - Two digit abbreviation: {}\n"
        "  - Currency Name and Symbol: {}({})\n".format(country_name,
                                                        continent,
                                                        call_code,
                                                        alpha2,
                                                        curr_name,
                                                        curr_symbol)
        , fg='green'))


@cli1.command('short')
@click.option('--abbreviate', '-ab', default='2', show_default=True,
              type=click.Choice(['2', '3']),
              help="")
@click.argument('country_name')
def short_code(country_name, abbreviate):
    """Returns the short abbreviation code of a country.
    It can be two digit or three digit country code.
    The default is two digit."""

    value = 0 if abbreviate == '2' else 1
    country = return_country(country_data, country_name)
    if country:
        click.secho('The {0} digit country code for {1} is "{2}"'.format(abbreviate, country_name, country[value]),
                    fg="green")


@cli1.command('currency')
@click.option('--code/--no-code', default=False, help="Find the currency code for a country")
@click.argument('country_name')
def country_currency(code, country_name):
    """Gives information about the currency of a country"""

    _data = return_country(currency_data, country_name)

    if _data:
        _, currency_name, the_code, symbol = _data
    else:
        return click.secho('Country does not exist. Perhaps, write the full name?', fg='red')

    click.secho("The currency is: {}({})".format(currency_name, symbol), fg='green')

    if code:
        click.secho("The currency short code is: {}".format(the_code), fg='green')


@cli1.command('call')
def country_call_code():
    """Get information about the calling code of a country"""
    pass

