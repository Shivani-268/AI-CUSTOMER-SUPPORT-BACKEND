import httpx

async def get_weather(location: str) -> str:
    """Fetches real-time weather using a free open api."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://wttr.in/{location}?format=j1")
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                return f"Weather in {location}: {current['temp_C']}°C, {current['weatherDesc'][0]['value']}."
        except Exception:
            pass
        return f"Could not fetch weather for {location}."

async def get_order_status(order_id: str) -> str:
    """Simulates a secure database lookup for order information."""
    mock_database = {"145": "Delivered yesterday", "146": "In transit"}
    status = mock_database.get(order_id, "Order reference number not found.")
    return f"Order #{order_id} tracking status: {status}"

# This list tells OpenAI exactly what functions we have, and what variables they expect
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather details for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string", "description": "The city name, e.g., Hyderabad"}},
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Fetch delivery information using an order number identifier.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string", "description": "The numeric order ID, e.g., 145"}},
                "required": ["order_id"],
            },
        },
    }
]