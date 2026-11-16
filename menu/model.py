from pydantic import BaseModel

class MenuItem(BaseModel):
    id:int
    name: str
    category: str
    price : int
    available : bool
    
class MenuResponse(BaseModel):
    status : str = "Sucess"
    count: int
    items: list[MenuItem]