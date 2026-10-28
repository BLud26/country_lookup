""" A program for looking up a country's name from a country code. """

import country_api 

def main():
    while True:
        code = input('Enter country code or press enter to quit ')
        # Treat empty or whitespace-only input as the request to exit.
        if not code.strip():
            break

        result = country_api.lookup_country(code)
        
        if result.found:
            # Some countries may not have a capital listed by the API.
            if result.capital:
                print(f'{code} is the country code for {result.name}. Its capital is {result.capital}.')
            else:
                print(f'{code} is the country code for {result.name}. Its capital is unavailable.')
        elif not result.error:
            print('No country found for that code')
        else:
            # Include the detail from the lookup result instead of hiding the cause.
            print(f'Error fetching data: {result.error}')
        

# Allow importing main in tests or other modules without starting the prompt loop.
if __name__ == '__main__':
    main()
