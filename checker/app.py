

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyA600mEDtL7Dh7_oaQd3AM8cq2oYbN6DIA")

@app.route("/")
def index():
    return render_template("bot.html")

@app.route("/check_symptoms", methods=["POST"])
def check_symptoms():
    user_input = request.json.get("symptoms", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter some symptoms to analyze."})

    prompt = f"""
    You are a diabetes specialist. A patient reports these symptoms: {user_input}.
    
    Provide the response in this structured format:
    
    Diabetes Type: [Mention Type 1, Type 2, or Gestational Diabetes]
    Stage: [Indicate Early, Moderate, or Severe]
    Home Care Advice: [Provide simple care instructions]
    Consultation: "Book a doctor appointment here: /book-appointment"
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)
