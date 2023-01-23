import fastapi

import main

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return main.new_match()
