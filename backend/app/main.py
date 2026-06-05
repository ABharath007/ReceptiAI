from fastapi import FastAPI

app = FastAPI(
    title="ReceptiAI",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to ReceptiAI!"}