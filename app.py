from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()


tanks = []
tank_id_counter = 1 

class Tank(BaseModel): 
    location: str
    lat: float
    long: float
    id: Optional[str] = None

class UpdateTank(BaseModel):
    location: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None


@app.get("/tank", response_model=List[Tank])
async def get_tanks():
    return tanks  

# GET /tank/{tank_id} - Get Single Tank by ID
@app.get("/tank/{tank_id}", response_model=Tank)
async def get_tank_by_id(tank_id: str):
    for tank in tanks:
        if tank['id'] == tank_id:
            return tank  
    raise HTTPException(status_code=404, detail="Tank not found")


# POST /tank - Create New Tank
@app.post("/tank", response_model=Tank, status_code=201)
async def create_tank(tank: Tank):  
    global tank_id_counter  

    tank_dict = tank.dict()  
    tank_id = str(uuid.uuid4())  
    tank_dict['id'] = tank_id  
    tanks.append(tank_dict) 
    return tank_dict 

# PATCH /tank/{tank_id} - Update Tank Information (SIMPLIFIED VERSION for Beginners)
@app.patch("/tank/{tank_id}")
async def update_tank(tank_id: str, updates: dict): 
    tank_to_update = None
    tank_index = -1
    for index, tank in enumerate(tanks):
        if tank['id'] == tank_id:
            tank_to_update = tank
            tank_index = index
            break

    if not tank_to_update:
        raise HTTPException(status_code=404, detail="Tank not found (Simplified Update)")

   
    if "location" in updates:
        tank_to_update['location'] = updates['location']

    return tank_to_update 


# DELETE /tank/{tank_id} - Delete Tank
@app.delete("/tank/{tank_id}", status_code=204)  
async def delete_tank(tank_id: str):
  
    tank_to_delete = None
    tank_index = -1
    for index, tank in enumerate(tanks):
        if tank['id'] == tank_id:
            tank_to_delete = tank
            tank_index = index
            break

    if not tank_to_delete:
        raise HTTPException(status_code=404, detail="Tank not found")

    tanks.pop(tank_index)  
    return  