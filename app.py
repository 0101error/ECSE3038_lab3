from fastapi import FastAPI , Response,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, ValidationError
from uuid import UUID, uuid4

app = FastAPI()

tanks = []

class Tank(BaseModel):
    id: UUID = Field (default_factory= uuid4) 
    location: str
    lat: float
    long: float

class Tank_Update(BaseModel):
    location: str| None = None
    lat: float| None = None
    long: float| None = None

#Get Handler Request 
@app.get("/tank")
def get_exsisting_tanks():
    return tanks

#Get Handler Request 
@app.get("/tank/{id}")
def get_specific_tanks(id: str):
    for tank in tanks:
        if "id" in tank and str(tank["id"]) == id:
            return tank
    raise HTTPException(status_code=404, detail="Tank Not Found")

#Post Handler Request 
@app.post("/tank")
def create_new_tanks(tank:Tank):
        
        new_tank = {
            "id": str(uuid4()),
            "location": tank.location,
            "lat": tank.lat,
            "long": tank.long
        }

        tanks.append(new_tank)
        return new_tank

@app.patch("/tank/{id}")
async def update_tank_alternative(id: UUID, tank_update: Tank_Update):
   
    for tank_index, tank in enumerate(tanks): 

        if "id" in tank and UUID(str(tank["id"])) == id:
            updated_fields = tank_update.dict(exclude_unset=True) 

            for field, value in updated_fields.items():
                tank[field] = value

            return tanks[tank_index] 
    raise HTTPException(status_code=404, detail="Tank not found")

#Delete Handler Request
@app.delete("/tank/{id}")
def delete_prson(id:UUID):
    for tank in tanks:
         if "id" in tank and UUID(str(tank["id"])) == id:
            tanks.remove(tank)
            return Response(status_code =204)
    raise HTTPException(status_code=404, detail="Tank not found")