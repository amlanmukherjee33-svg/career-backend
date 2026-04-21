from flask_cors import CORS
from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

# 🔑 API Key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)


# ✅ HEALTH CHECK
@app.route('/', methods=['GET'])
def home():
    return "Server is running", 200


# ✅ TEST ROUTE (VERY IMPORTANT)
@app.route('/test', methods=['GET'])
def test():
    return "NEW CODE IS LIVE"


# ✅ RESUME ANALYZER
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json

        resume = data.get("resume", "")
        role = data.get("role", "")
        level = data.get("level", "")

        prompt = f"""
You are a strict ATS resume reviewer.

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
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ CAREER ENGINE (FINAL)
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json

        question = data.get("question", "")
        careers = data.get("careers", [])

        prompt = f"""
You are an expert AI career coach.

User Profile:
{question}

Available Careers:
{careers}

Return ONLY a valid JSON array (no explanation, no markdown).

FORMAT:
[
  {{
    "career": "exact career name from list",
    "fitScore": 1-10,
    "reason": "2-3 line personalized explanation",

    "skillsNeeded": ["skill 1", "skill 2", "skill 3"],
    "roadmap": [
      "Step 1: ...",
      "Step 2: ...",
      "Step 3: ..."
    ],
    "projects": [
      "Project idea 1",
      "Project idea 2"
    ],
    "salaryRange": "₹5L - ₹20L",
    "tips": [
      "Tip 1",
      "Tip 2"
    ]
  }}
]

RULES:
- ONLY JSON
- NO explanation text outside JSON
- No empty fields
- Select BEST 3 careers
- Be practical and detailed
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return ONLY JSON array."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        result = response.choices[0].message.content.strip()
        print("RAW AI OUTPUT:", result)

        try:
            parsed = json.loads(result)

            if not isinstance(parsed, list):
                raise Exception("Response is not a list")

            return jsonify(parsed)

        except Exception:
            return jsonify({
                "error": "Invalid JSON from AI",
                "raw": result
            })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)