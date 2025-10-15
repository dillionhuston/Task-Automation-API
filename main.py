from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib
import sys

app = FastAPI(title="Task Automation API", version="1.0.0")

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Setup ---
try:
    from app.models.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print(" Database tables created")
except Exception as e:
    print(f" Database initialization failed: {e}")
    sys.exit(1)

# --- Dynamic Router Loading ---
ROUTER_PATHS = {
   "auth": "routers.auth",
    "tasks": "routers.tasks",
    "files": "routers.files",
    "admin": "routers.admin",

}

loaded_routers = []

for name, path in ROUTER_PATHS.items():
    try:
        module = importlib.import_module(path)
        app.include_router(module.router, prefix=f"/{name}", tags=[name])
        loaded_routers.append(name)
        print(f" {name.capitalize()} router loaded at /{name}")
    except Exception as e:
        print(f"❌ Failed to load {name} router: {e}")

# --- Routes ---
@app.get("/")
def root():
    return {
        "message": "Task Automation API - Live on Railway!",
        "version": app.version,
        "base_url": "https://reliable-fulfillment.railway.app",
        "docs": "/docs",
        "auth_prefix": "/auth",
    }

@app.get("/health")
def health():
    return {"success": True, "status": "healthy"}

@app.get("/debug/routes")
def debug_routes():
    return {
        "loaded_routers": loaded_routers,
        "routes": [
            {
                "path": route.path,
                "methods": list(route.methods),
                "tags": getattr(route, "tags", []),
            }
            for route in app.routes
            if hasattr(route, "path")
        ],
    }

print(" FastAPI app starting...")
print(f" Loaded routers: {loaded_routers}")

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

