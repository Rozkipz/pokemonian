import logging
import os
import time

import requests
from poke_model import pokemon as pokemon_model
from database_interface import upsert_pokemon

try:
    REQUEST_BACKOFF_IN_SECONDS = float(os.environ.get('BACKOFF', 0.3))
except (ValueError, TypeError):
    REQUEST_BACKOFF_IN_SECONDS = 0.3

try:
    TOTAL_POKEMON_TO_STORE = int(os.environ.get('TOTAL_POKEMON'))
except (ValueError, TypeError):
    TOTAL_POKEMON_TO_STORE = None


class UpdatePokemon(object):
    def __init__(self):
        self.api_uri = "https://pokeapi.co/api/v2/pokemon/"

    def get(self):
        res = requests.get(self.api_uri).json()
        pokemon_to_add = []

        while res.get('next'):
            logging.info(f"Just got {len(res.get('results'))} pokemon.")

            for base_poke_info in res.get('results'):
                # Create basic pokemon obj - Could do after the api calls in one go instead.
                url = base_poke_info.get('url')
                poke_id = url.split('/')[-2]

                pokemon = pokemon_model(
                    id=poke_id,
                    name=base_poke_info.get('name'),
                    url=url
                )

                if TOTAL_POKEMON_TO_STORE and pokemon.id > TOTAL_POKEMON_TO_STORE:
                    break

                # Get details about the pokemon.
                pokemon_details = requests.get(url).json()
                time.sleep(REQUEST_BACKOFF_IN_SECONDS)

                # Set the pokemon obj's stats.
                pokemon.weight = pokemon_details.get('weight')
                pokemon.height = pokemon_details.get('height')

                for x in pokemon_details.get('stats'):
                    if x.get('stat').get('name') == 'speed':
                        pokemon.speed = x.get('base_stat')

                # Add the new pokemon obj to a list to be upserted to the db later
                pokemon_to_add.append(pokemon)
                logging.debug(f"Got pokemon: {pokemon}")

            if res.get('next'):
                # If there is another page of pokemon, get the next page and run the loop again.
                res = requests.get(res.get('next')).json()
                time.sleep(REQUEST_BACKOFF_IN_SECONDS)  # Wait some seconds between api calls so we don't get rate limited.
            else:
                logging.info(f"Finished retrieving pokemon. Retrieved {len(pokemon_to_add)} total pokemon.")

        # Add the pokemon objs to the DB.
        for each_poke in pokemon_to_add:
            # TODO Add them as a batch
            upsert_pokemon(each_poke)

        logging.info("Successfully updated pokemon.", extra={"pokemon": pokemon_to_add})


if __name__ == "__main__":
    if os.environ.get('DEBUG'):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug(f"REQUEST_BACKOFF_IN_SECONDS: {REQUEST_BACKOFF_IN_SECONDS}")
    logging.debug(f"TOTAL_POKEMON_TO_STORE: {TOTAL_POKEMON_TO_STORE}")

    logging.info('Running.')

    update = UpdatePokemon()

    while True:
        update.get()
        time.sleep(600)  # Do API calls once every 10 minutes.
