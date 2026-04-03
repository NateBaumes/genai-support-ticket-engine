from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.tickets import routes as ticket_routes
from app.database import init_db

app = FastAPI(title="GenAI Support Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_routes.router, prefix="/api/tickets", tags=["tickets"])

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Database initialized")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
