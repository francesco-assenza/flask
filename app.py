from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Text Generation API is running."

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Lazy-load the model inside the request
        generator = pipeline("text-generation", model="distilgpt2")
        output = generator(prompt, max_length=100, num_return_sequences=1)
        return jsonify({"itinerary": output[0]["generated_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
