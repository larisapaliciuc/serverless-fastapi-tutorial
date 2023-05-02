from enum import Enum
from mangum import Mangum
from typing import Annotated
from pydantic import BaseModel
from fastapi import (
    BackgroundTasks, 
    FastAPI, 
    HTTPException, 
    Path, 
    Query,
)
from helpers import write_log


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set() 


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


app = FastAPI()
handler = Mangum(app)

fake_items = ['Foo', 'Loololo', 'Ananaa']

@app.get('/')
async def hello_world():
    return 'Hello World'

@app.get('/items/')
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items[skip: skip + limit]

@app.post('/items/')
async def create_item(item: Item):
    return item

@app.get("/items/{item}")
async def read_item( item: Annotated[str, Path(title='The name of the item')], background_tasks: BackgroundTasks, short: Annotated[bool | None, Query(title='Short or long description')] = False, q: str | None = None):
    
    background_tasks.add_task(write_log, message=f'Somebody just requested this item {item}\n')
    if item not in fake_items:
        raise HTTPException(
            status_code=404,
            detail='Item was not found in fake items list'
        )
    
    ret = dict()
    ret['item'] = item

    if q:
        ret.update({"q": q})

    if not short:
        ret.update(
            {"description": "This is an amazing item that has a long description"}
        )
    else:
        ret.update(
            {"description": "This is a short description"}
        )

    return ret