from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/videos", StaticFiles(directory="videos"), name="videos")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "you api key")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_ai(prompt: str = Form(...)):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_API_URL, headers=headers, json=data)
        result = response.json()
    print("OpenRouter API response:", result)  # Debug print
    ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "No response from AI.")
    return JSONResponse({"response": ai_response})
