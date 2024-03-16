from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Привет, Саня! Это будущая заготовка для тг-бота, сделанная на fastapi"}