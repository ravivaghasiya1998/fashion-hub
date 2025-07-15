from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from fashion_hub_backend.database.db_setup import (
    Base,
    SessionLocal,
    engine,
    setup_db,
)
from fashion_hub_backend.errors import APIBadRequest, APINotFound, DataBaseNotFound
from fashion_hub_backend.interface.fastapi.app_config import RunMode, config
from fashion_hub_backend.interface.fastapi.authentication.routes import authentication_router
from fashion_hub_backend.interface.fastapi.categories.routes import category_router
from fashion_hub_backend.interface.fastapi.order_items.routes import order_item_router
from fashion_hub_backend.interface.fastapi.orders.routes import order_router
from fashion_hub_backend.interface.fastapi.payments.routes import payment_router
from fashion_hub_backend.interface.fastapi.products.routes import product_router
from fashion_hub_backend.interface.fastapi.users.routes import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load expensive code

    # init sql database
    with SessionLocal() as session:
        setup_db(session)

    # create table and fill with defaults
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=lifespan, debug=config.run_mode == RunMode.DEBUG, root_path="/api")

if app.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(authentication_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)
app.include_router(order_item_router)
app.include_router(payment_router)


# Error handlers
@app.exception_handler(APIBadRequest)
def handle_bad_request(request: Request, exc: APIBadRequest):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.model_dump(),
    )


@app.exception_handler(APINotFound)
def handle_not_found(request: Request, exc: APINotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.model_dump(),
    )


@app.exception_handler(DataBaseNotFound)
def handle_database_not_found(request: Request, exc: DataBaseNotFound):
    if app.debug:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=exc.model_dump(),
        )
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
