from fastapi import FastAPI
from routes import base, data, nlp


app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)