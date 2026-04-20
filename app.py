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


# ✅ RESUME ANALYZER (FIXED)
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


# ✅ CAREER ENGINE (FINAL FIX)
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json

        question = data.get("question", "")
        careers = data.get("careers", [])

        prompt = f"""
Return ONLY a valid JSON ARRAY.

User:
{question}

Careers:
{careers}

FORMAT:
[
  {{
    "career": "exact career name from list",
    "fitScore": number (1-10),
    "reason": "short personalized reason",
    "steps": ["step 1", "step 2"],
    "insights": ["insight 1"]
  }}
]

RULES:
- ONLY JSON array
- NO explanation
- NO markdown
- Each career MUST be different
- Select BEST 3 careers only
- Prefer careers that closely match skills and interests
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return ONLY JSON array."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()
        print("RAW AI OUTPUT:", result)

        import json
        parsed = json.loads(result)

        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)