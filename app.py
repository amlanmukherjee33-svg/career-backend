from flask_cors import CORS
from flask import Flask, request, jsonify
from openai import OpenAI

# 🔑 Put your API key here
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Server is running", 200


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    resume = data.get("resume", "")
    role = data.get("role", "")
    level = data.get("level", "")

    prompt = f"""
You are a strict ATS resume reviewer.

You MUST follow this exact format.

User:
Role: {role}
Level: {level}

Resume:
{resume}

OUTPUT FORMAT:

### 📊 SCORE:
Score: X/100

### 💪 STRENGTHS:
- Point 1
- Point 2

### ⚠️ WEAKNESSES:
- Point 1
- Point 2

### 🚀 IMPROVEMENTS:
- Action 1
- Action 2

### 🎯 FINAL VERDICT:
(Short hiring decision)

RULES:
- Use ONLY this format
- Use "-" for bullets
- Use headings with ###
- No extra explanation outside sections
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
You are a strict career coach.

You MUST follow this exact format. No deviation.

User:
Role: {role}
Level: {level}

Question:
{question}

OUTPUT FORMAT:

### 🔥 MAIN ANSWER:
(1–2 line summary)

### 📌 STEPS:
- Step 1: ...
- Step 2: ...
- Step 3: ...

### 🎯 KEY INSIGHTS:
- Insight 1
- Insight 2

### ⚠️ MISTAKES TO AVOID:
- Mistake 1
- Mistake 2

RULES:
- Use ONLY this format
- Use bullet points with "-"
- Use headings starting with ###
- No extra text outside sections
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