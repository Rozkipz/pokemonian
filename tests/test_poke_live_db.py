import unittest

import os

os.environ.update(DB_CONN="postgresql://postgres:postgres@host.docker.internal:5432/postgres")

import poke.database_interface as database_interface
from poke.poke_model import pokemon as pokemon_model


class TestInterfaces(unittest.TestCase):
    def setUp(self):
        self.pokes = {}
        for i in range(5):
            self.pokes[i] = pokemon_model(id=i, name=f"testamon_the_{i}", url=f"random.url/{i}")

    def test_insert_get(self):
        # Todo: split this into two tests, one to insert and one to get.
        database_interface.upsert_pokemon(self.pokes.get(1))
        db_poke = database_interface.get_pokemon(self.pokes.get(1).id)

        assert db_poke.id == self.pokes.get(1).id
        assert db_poke.name == self.pokes.get(1).name
        assert db_poke.url == self.pokes.get(1).url

    def test_get_count(self):
        database_interface.upsert_pokemon(self.pokes.get(1))
        database_interface.upsert_pokemon(self.pokes.get(2))
        database_interface.upsert_pokemon(self.pokes.get(3))

        count = database_interface.get_total_pokemon()
        assert count == 3
