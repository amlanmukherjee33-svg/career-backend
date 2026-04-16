from flask_cors import CORS
from flask import Flask, request, jsonify
from openai import OpenAI

# 🔑 Put your API key here
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    resume = data.get("resume", "")
    role = data.get("role", "")
    level = data.get("level", "")

    prompt = f"""
You are a top career coach and resume expert.

Analyze this resume for a {level} {role}.

Give:
1. Score out of 100
2. Strengths (bullet points)
3. Weaknesses (bullet points)
4. Specific improvements (actionable)
5. Final hiring verdict

Resume:
{resume}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume reviewer. Be clear, structured, and high quality."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json

    question = data.get("question", "")
    role = data.get("role", "")
    level = data.get("level", "")

    prompt = f"""
You are a helpful career coach.

User role: {role}
User level: {level}

Question: {question}

Give a clear, practical, step-by-step answer.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful career mentor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)