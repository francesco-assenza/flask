# app.py
import os
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Use a smaller, faster model for Render free tier
generator = pipeline("text-generation", model="distilgpt2")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        result = generator(prompt, max_length=200, num_return_sequences=1)
        return jsonify({"itinerary": result[0]["generated_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Text generation API is running."
