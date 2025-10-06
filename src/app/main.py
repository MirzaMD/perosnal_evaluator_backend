from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from src.models.schema import MainSchema
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
GEMINI_KEY = os.getenv("GEMINI_KEY")

client = AsyncIOMotorClient(MONGO_URL)
db = client["personality_evaluator_db"]
responses = db["responses"]

genai.configure(api_key=GEMINI_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001","http://localhost:3002","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)

gemini_model = genai.GenerativeModel("models/gemini-2.5-pro")

@app.post("/api/personality_evaluator")
async def analysis(item: MainSchema):
    try:
        # Combine all Q&A into one prompt
        combined_prompt = ""
        for qa in item.info:  # iterate over the list
            combined_prompt += f"Q: {qa.q}\nA: {qa.a}\n"

        prompt = f"Analyze the personality based on these Q&As:\n{combined_prompt}\nProvide a concise personality summary."

        # Generate personality summary
        response = gemini_model.generate_content(prompt)
        personality_summary = response.text

        # Update the schema instance
        item.personality_summary = personality_summary

        # Store in MongoDB
        await responses.insert_one(item.model_dump())

        return {"personality_summary": personality_summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


