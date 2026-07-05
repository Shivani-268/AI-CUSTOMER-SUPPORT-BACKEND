import traceback
from fastapi import FastAPI
from app.vectorstore import vector_store
from app.routes import router

app = FastAPI()

# Mount our router so endpoints like /chat work!
app.include_router(router)

@app.on_event("startup")
async def startup():
    try:
        print("Starting services...")

        # Added 'await' here since initialize_store is now cleanly async!
        await vector_store.initialize_store("faq.txt")

        print("All services connected successfully")

    except Exception as e:
        print("❌ Startup Error:", str(e))
        traceback.print_exc()