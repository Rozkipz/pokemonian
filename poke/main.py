from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.exc import NoResultFound
import poke.interface as interface
from poke.poke_model import pokemon as pokemon_model

app = FastAPI()


@app.get("/")
async def root():
    """ GET / endpoint. Returns a 404.

    Returns:
        404 json response.
    """
    return JSONResponse(status_code=404, content={"message": "Resource not found."})


@app.get("/pokemon/{poke_id}")
async def pokemon_get(poke_id: int) -> Union[pokemon_model, JSONResponse]:
    """ GET /pokemon/{poke_id} endpoint. Pass in a pokemon id and it will return that pokemon's stats.

    Args:
        poke_id: ID of a pokemon

    Returns:
        pokemon_model object containing pokemon data.

    Raises:
         404 json response if the pokemon isn't found.
    """
    try:
        poke = interface.get_pokemon(poke_id)
        return poke
    except NoResultFound:
        return JSONResponse(status_code=404, content={"message": "Pokemon not found."})


@app.get("/pokemon/random/")
async def pokemon_random() -> Union[pokemon_model, JSONResponse]:
    """ GET /pokemon/random/ endpoint. Gets a random pokemon from the list of pokemon in the DB.

    Returns:
        pokemon_model object containing pokemon data.

    Raises:
         404 json response if the pokemon isn't found.

    """
    try:
        poke = interface.get_random_pokemon()
        return poke
    except NoResultFound:
        return JSONResponse(status_code=404, content={"message": "Pokemon not found."})


@app.get("/pokemon/")
async def pokemon() -> RedirectResponse:
    """ GET /pokemon/ endpoint. Get requests redirect to the /pokemon/random/ endpoint.

    Returns:
        RedirectResponse: Redirect response that points to the random endpoint.
    """
    return RedirectResponse("/pokemon/random/", status_code=303)


@app.post("/pokemon")
async def upsert_pokemon(poke: pokemon_model) -> Union[pokemon_model, JSONResponse]:
    """
    ***EXPERIMENTAL***

    POST /pokemon/ endpoint. POSTing a pokemon object to this endpoint will try to upsert that pokemon into the db.

    Args:
        poke: pokemon_model object that came from the POST request

    Returns:
        The pokemon_model object that was POSTed to the endpoint

    Raises:
        Json response with a 500 status code, and message describing the issue.
    """
    try:
        interface.upsert_pokemon(poke)
        return JSONResponse(status_code=201, content={"pokemon": poke})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": e})
