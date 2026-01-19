from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.finance_router import router as finance_router

app = FastAPI(title="AI Financial Report Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router, prefix="/api/auth")
app.include_router(finance_router, prefix="/api/finance")

@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
def health_check():
    return {"status": "ok"}
