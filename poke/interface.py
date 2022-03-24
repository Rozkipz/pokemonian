import random

import poke.database_interface as database_interfaces
from poke.poke_model import pokemon as pokemon_model


def get_pokemon(poke_id: int) -> pokemon_model:
    """ Get a pokemon's data from its ID.

    Args:
        poke_id: ID of the pokemon you want the data for.

    Returns:
        pokemon_model object containing the data for the pokemon found in the DB.

    Raises:
        NoResultFound: If there isn't a pokemon in the DB with the passed in ID.
    """
    pokemon = database_interfaces.get_pokemon(poke_id)
    return pokemon


def get_random_pokemon() -> pokemon_model:
    """ Generate a random number from 1->total number of pokemon and use it to return a pokemon with that ID.

    Returns:
        pokemon_model object containing a random pokemon's data.
    """
    total_pokemon = database_interfaces.get_total_pokemon()
    random_poke_id = random.randint(1, total_pokemon)
    pokemon = database_interfaces.get_pokemon(random_poke_id)
    return pokemon


def upsert_pokemon(poke: pokemon_model):
    """ Takes a pokemon_model to be upserted into the DB.

    Args:
        poke: pokemon_model objects that are to be created/updated in place in the DB

    """
    database_interfaces.upsert_pokemon(poke)
