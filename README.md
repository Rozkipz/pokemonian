# Pokemonian

### Overview:

This is a small program that crawls [pokeapi.co](https://pokeapi.co) for pokemon and stores them in a postgres DB. It then provides an API to access these pokemon. 

### Usage:
Easiest way of running this is using [just](https://github.com/casey/just). This is a tool used to run commands, similar to make. You can of course run the commands yourself that are in the justfile, but you'll have to substitute in the `{{image_name}}` and `{{args}}`.

You will also need Docker and docker-compose to be able to run Pokemonian.

* `just run` - Just runs the crawler and api.

Once the crawler has populated the DB, you can access the api with:
* `curl -L 0.0.0.0:8000/pokemon/` - Gets a redirect to `/pokemon/random/` and gets a random pokemon.
* `curl -L 0.0.0.0:8000/pokemon/{id}` - Gets a specific pokemon.
* `curl -d '{"id":10000, "name":"randomamon", "url":"get.pokemon/10000"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:8000/pokemon` - This creates a new pokemon with the data passed in from the json. The keys must match the pokemon model object.

Development: 
* `just debug` - Runs the crawler and API, and the crawler will output debug logs.
* `just update_reqs` - Update the poetry lockfile if you change the requirements.
* `just test` - Runs the test suite
* `just _remove_postgres_db` - Delete the contents of the DB (including the table).

---

Database schema:

| pokemon | type          |
|:--------|:--------------|
| id (PK) | int           |
| name    | str           |
| url     | str           |
| height  | optional(int) |
| weight  | optional(int) |
| speed   | optional(int) |