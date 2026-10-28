from dataclasses import dataclass
from typing import Optional

import requests 


@dataclass
class CountryLookupResult:
    """Represent a lookup outcome; name, capital, and error are absent when inapplicable."""

    found: bool
    name: Optional[str]
    capital: Optional[str]
    error: Optional[str]


def lookup_country(country_code: str) -> CountryLookupResult:
    """Return country details, no-match status, or a request/response error."""
    try:
        json_response = make_api_request(create_url(), country_code)
        if not isinstance(json_response, dict):
            raise ValueError('Expected a JSON object from the API')
        data = json_response.get('data')
        if not isinstance(data, dict):
            raise ValueError('Missing data object in API response')
        country = data.get('country')
        if not country:
            return CountryLookupResult(False, None, None, None)
        if not isinstance(country, dict):
            raise ValueError('Expected country data to be a JSON object')
        name, capital = get_country_details_from_response(country)
        return CountryLookupResult(True, name, capital, None)
    except requests.RequestException as error:
        return CountryLookupResult(False, None, None, f'Error connecting to API: {error}')
    except (KeyError, TypeError, ValueError) as error:
        return CountryLookupResult(False, None, None, f'Error reading API response: {error}')


def create_url():
    # The former REST Countries v3.1 endpoint is deprecated; use the keyless GraphQL endpoint.
    url = 'https://countries.trevorblades.com/'
    return url


def make_api_request(url, country_code):
    # Ask only for the name and capital, normalizing the code and passing it as a variable.
    query = '''
        query CountryByCode($code: ID!) {
            country(code: $code) {
                name
                capital
            }
        }
    '''
    response = requests.post(
        url,
        json={'query': query, 'variables': {'code': country_code.upper()}},
        timeout=10,
    )
    # Raise HTTP/GraphQL errors here so lookup_country can return them in its result.
    response.raise_for_status()
    json_response = response.json()
    if not isinstance(json_response, dict):
        raise ValueError('Expected a JSON object from the API')
    if json_response.get('errors'):
        message = json_response['errors'][0].get('message', 'Unknown API error')
        raise ValueError(message)
    return json_response


def get_country_details_from_response(country):
    # The GraphQL API returns the capital as a string that may be null.
    name = country['name']
    capital = country.get('capital')
    return name, capital
