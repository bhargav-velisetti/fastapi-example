import os 
import json 
import uuid
import time
from memory_profiler import profile
from fastapi import FastAPI
from pydantic import BaseModel
from util import upsert_spanner_async

project = os.getenv('project') 
instance = os.getenv('instance')
database = os.getenv('database')


app = FastAPI()

class Upsert_Data(BaseModel):
    table: str 
    columns: list
    values: list


@app.post("/")
async def upsert_to_spanner(upsert_data: Upsert_Data):
   try:
       upsert_spanner_async(project, instance, database, upsert_data.table, upsert_data.columns, upsert_data.values)
       return {"message": "Success"}
   except Exception as e:
       return {"message": f"Error: {str(e)}"}
