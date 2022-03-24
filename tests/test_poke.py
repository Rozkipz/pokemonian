import unittest

import os

os.environ.update(DB_CONN="postgresql://postgres:postgres@host.docker.internal:5432/postgres")

import poke.interface as interface
from poke.poke_model import pokemon as pokemon_model

TOTAL_POKEMON = 5


class FakeDatabaseInterface():
    def __init__(self):
        self.pokes = {}
        self.max_pokes = TOTAL_POKEMON + 1  # Don't zero index IDs, so create an extra poke for the zeroth we lost
        for i in range(1, self.max_pokes):
            self.pokes[i] = pokemon_model(id=i, name=f"testamon_{i}", url=f"random.url/{i}")

    def get_pokemon(self, poke_id: int):
        return self.pokes[poke_id]

    def get_total_pokemon(self):
        return self.max_pokes

    def upsert_pokemon(self, poke: pokemon_model):
        self.pokes[poke.id] = poke


fake_database_interface = FakeDatabaseInterface()
interface.database_interfaces = fake_database_interface


class TestInterfaces(unittest.TestCase):
    def test_interface_get(self):
        db_poke = interface.get_pokemon(1)

        assert db_poke.id == fake_database_interface.pokes.get(1).id
        assert db_poke.name == fake_database_interface.pokes.get(1).name
        assert db_poke.url == fake_database_interface.pokes.get(1).url

    def test_random_get(self):
        random_poke = interface.get_random_pokemon()

        assert random_poke.id in range(1, TOTAL_POKEMON + 1)
        assert random_poke.id == fake_database_interface.pokes.get(random_poke.id).id
        assert random_poke.name == fake_database_interface.pokes.get(random_poke.id).name
        assert random_poke.url == fake_database_interface.pokes.get(random_poke.id).url

    def test_insert(self):
        new_poke_id = 10
        new_poke = pokemon_model(id=new_poke_id, name="insertamon", speed=123)

        interface.upsert_pokemon(new_poke)
        get_poke_back = interface.get_pokemon(new_poke_id)

        assert get_poke_back.id == new_poke.id
        assert get_poke_back.name == new_poke.name
        assert get_poke_back.speed == new_poke.speed
