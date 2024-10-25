from fastapi import FastAPI

app=FastAPI()

@app.get("/{d}")
def income(d: int):
    return{"message":f"hello{d}"}
