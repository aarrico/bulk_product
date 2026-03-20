from fastapi import APIRouter

from app.api.v1 import pokemon, species

api_router = APIRouter()

api_router.include_router(species.router, prefix="/species", tags=["species"])
api_router.include_router(pokemon.router, prefix="/pokemon", tags=["pokemon"])

# Wire up route modules as you build them:
# from app.api.v1 import collection, analysis
# api_router.include_router(collection.router, prefix="/collection", tags=["collection"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
