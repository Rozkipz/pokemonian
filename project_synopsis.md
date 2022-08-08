# Synopsis
A quick overview of some of my thoughts on the stages of the project and future improvements. 


### Design:

* A much better idea to use [Pokebase](https://github.com/PokeAPI/pokebase) over writing our own crawler. (And not only because they have the better name.)
* Two small independent services that share a common interface - the pokemon itself.
* FastAPI seperated into three components:
    - API layer, where all the logic for the API itself is - status codes, headers etc;
    - Data layer which would manipulate or correlate data - Not so much used in this project as it was a bit simple, only the `get_random_pokemon()`
      interface generating a random ID to pass into the next layer.
    - Database layer to separate out the business logic, storing and retrieving data from the database.
* Using a common model between the API and the DB ensures that as soon as a pokemon is seen it is put into this model, meaning that we can be sure that the pokemon object is consistent throughout the system - also gives us type validation on creation.
* FastAPI gives us a quick restful api that can easily be expanded upon in the future if needed.
* Use just to keep useful project commands together in a single space, with explanations for each.

### Integration:

I moved away from a threaded approach to a microservice approach with docker-compose after it came more clear that the two should be more separate than they were. In the future I would completely separate the two in the repo, along with creating a pokemon_model package that could be shared between the two.

### Scaling:

Containerisation means that pokemonian can be easily deployed with a container orchestration program, and could be scaled easily using that. The difficulty with scaling would be the postgres database being in a container on the cluster, and I would move away to either a dedicated server running postgres, or to a cloud variant.

The crawler probably doesn't need to scale, but to do so you could implement a pool/queue of pokemon IDs that need data retrieval after first crawling through the tree, and have crawler instances get from this pool/queue, query the api, and then update the DB.

### Testing

TDD could have been done easily, as during the design we determined what the pokemon model would look like, and what API endpoints would be needed.
Better e2e tests could have been accomplished by changing `test_poke_live_db.py` to create and use a FastAPI object, testing the API right through to the database. Fuzzing could also be added to test for unexpected errors in the API endpoints. Better test coverage overall should also be heavily considered in the future.

### Extras:

In addition to what I've mentioned above, I would also do a few other things on continuation of this project

- Add black pre-commit hook enforcement
- Add mypy pre-commit hook enforcement
- Restructure the repo a bit more, moving out the crawler code into its own microservice, and creating a common Pokemon model package.
- I'd modify the dockerfiles after separating the two services, and create multi-stage builds to house a testing environment for each.
- Async the FastAPI and SQLAlchemy code for better performance.
- Develop a git branching strategy and implement a stronger merging process.

### SQL improvements

For an initial design I created a single Pokemon table and kept some of the data returned from the API there, but if I were to expand the project and store more data, I'd split the database up into several tables that would be linked together using keys.

#### Initial DB schema

##### Pokemon
| field   | type          |
|:--------|:--------------|
| id (PK) | int           |
| name    | str           |
| url     | str           |
| height  | optional(int) |
| weight  | optional(int) |
| speed   | optional(int) |

#### Proposed new design
One way to eliminate the optional attributes (because they don't get populated in the model until after the call to the URL), you could create a single table with just the metadata on the Pokemon, and a table that stores the information on that Pokemon that is retrieved by the API after the initial get:

##### poke_meta
| field   | type          |
|:--------|:--------------|
| id (PK) | int           |
| url     | str           |

##### poke_info 
| field   | type          |
|:--------|:--------------|
| id (FK) | poke_meta.id  |
| name    | str           |
| height  | int           |
| weight  | int           |
| speed   | int           |

Although this fixes the optional fields in the DB, this creates a messier design that is harder to follow through. The cleaner way to fix this issue would be to configure SQLModel to only have an optional parameter for the model and not the DB field, or to create the model after getting all information on the Pokemon, and to keep the original DB design.

If we were going to expand the project to also hold something that was in a many-to-many relationship with a Pokemon, for example attacks that Pokemon can perform, then you'd need to create a bridging table between attacks and Pokemon. I also created a simple ENUM to correspond to the types of attacks that Pokemon might have.

##### type_ENUM
|:------|
| Air   | 
| Water |
| Fire  | 
| Earth |

##### pokemon
| field   | type          |
|:--------|:--------------|
| id (PK) | int           |
| name    | str           |
| url     | str           |
| type    | type_ENUM     |
| height  | int           |
| weight  | int           |
| speed   | int           |

##### attacks

| field   | type          |
|:--------|:--------------|
| id (PK) | int           |
| name    | str           |
| type    | type_ENUM     |

##### pokemon_attacks
| field          | type          |
|:---------------|:--------------|
| poke_id (FK)   | int           |
| attack_id (FK) | int           |
| attack_slot    | int           |

PRIMARY KEY (poke_id, attack_slot)
// As Pokemon can only have one attack in each slot, we can make the composite key based on that, with the assumption that a Pokemon can have multiple of the same attack in different slots.

Using a bridging table in this way allows for both Pokemon and Attacks to be created and stored only once each, and easily associated with each other using the pokemon_attacks table.
