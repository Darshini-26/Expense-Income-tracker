from fastapi import FastAPI

app=FastAPI()

@app.get("/{id}")
def income(id: int):
    return{"message":f"hi{id}"}
