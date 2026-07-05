from google import genai
from app.config import settings
from app.vectorstore import vector_store

async def generate_rag_response(user_message: str) -> dict:
    # 1. Search the company handbook index
    docs = await vector_store.search(user_message, k=1)
    context = docs[0] if docs else "No relevant context found in documents."

    # 2. Setup instruction guidelines
    system_prompt = f"You are a helpful customer support assistant. Use this documentation context to answer if relevant:\n{context}"
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    try:
        # 3. Request the response using the new SDK syntax
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config={"system_instruction": system_prompt}
        )
        return {"answer": response.text, "tool_used": False}
    except Exception as e:
        return {"answer": f"Gemini API Error: {str(e)}", "tool_used": False}