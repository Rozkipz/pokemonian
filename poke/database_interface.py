import os

from sqlmodel import create_engine, Session, select, update
from functools import lru_cache
from typing import Union
from sqlalchemy.exc import NoResultFound

engine = create_engine(os.environ.get('DB_CONN'))

# Grim hack to get the imports working with crawler and main.
# TODO: Split poke models and other common functions out into a separate package the api+crawler can share.
# TODO: After split crawler code out into a separate part of the repo and create an individual Docker image for it.

try:
    from poke.poke_model import pokemon as pokemon_model
except:
    from poke_model import pokemon as pokemon_model


@lru_cache(maxsize=16)
def get_pokemon(poke_id: int) -> pokemon_model:
    """ Get a pokemon's data from the database from its ID.

    Args:
        poke_id: ID of the pokemon you want the data for.

    Returns:
        pokemon_model object containing the data for the pokemon found in the DB.

    Raises:
        NoResultFound: If there isn't a pokemon in the DB with the passed in ID.
    """
    with Session(engine) as session:
        poke = session.exec(select(pokemon_model).where(pokemon_model.id == poke_id)).one()
        return poke


def get_total_pokemon() -> int:
    """ Get the total number of pokemon in the database.

    Returns:
        int: Number of pokemon in the database.
    """
    with Session(engine) as session:
        return session.query(pokemon_model).count()


def upsert_pokemon(pokemon: Union[pokemon_model, list[pokemon_model]]) -> None:
    """ Takes an individual, or list of pokemon_models that are to be added or updated in place.

    Args:
        pokemon: pokemon_model objects that are to be created/updated in place in the DB

    """
    with Session(engine) as session:
        if isinstance(pokemon, list):
            # TODO:  add bulk inserts
            raise NotImplementedError

        p = session.exec(select(pokemon_model).where(pokemon_model.id == pokemon.id))

        try:
            p.one()  # see if there was a result for that poke_id
            # TODO: Only update if the values are different than in the DB.
            update(pokemon_model).where(pokemon_model.id == pokemon.id).values(pokemon.__dict__)
        except NoResultFound:
            session.add(pokemon)

        session.commit()
