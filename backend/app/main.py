import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .routers import auth, trucks, trips, expenses, documents, stats
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Truck Audit App')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(trucks.router)
app.include_router(trips.router)
app.include_router(expenses.router)
app.include_router(documents.router)
app.include_router(stats.router)

@app.get('/api/health')
def health():
    return {'status': 'ok'}

# Serve SPA - frontend build should be placed into ../frontend/dist when building
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'))
if os.path.isdir(BUILD_DIR):
    app.mount('/assets', StaticFiles(directory=os.path.join(BUILD_DIR, 'assets')), name='assets')

@app.get('/{full_path:path}')
def spa(full_path: str):
    index_path = os.path.abspath(os.path.join(BUILD_DIR, 'index.html'))
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {'message': 'Frontend not built. Run frontend build.'}
