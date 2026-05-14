from flask import Flask, render_template, request, jsonify
from chatbot import FitnessChatbot

app = Flask(__name__)
app.secret_key = "fitness_chatbot_secret_key"

bot = FitnessChatbot()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        try:
            name = request.form.get("name", "")
            age = int(request.form.get("age"))
            weight = float(request.form.get("weight"))
            height = float(request.form.get("height"))
            goal = request.form.get("goal", "maintain")

            gender = request.form.get("gender", "male")
            activity = request.form.get("activity", "moderate")

            result = bot.calculate_plan(
                age,
                weight,
                height,
                gender,
                activity,
                goal
            )

            plan = f"""
Hello {name},

BMI: {result['BMI']}
BMI Category: {result['BMI Category']}
BMR: {result['BMR']} calories/day
TDEE: {result['TDEE']} calories/day
Target Calories: {result['Target Calories']} calories/day
Protein Intake: {result['Protein Intake']}

Goal: {goal}

Basic Plan:
- Follow your target calories daily
- Take enough protein
- Workout 4–6 days per week
- Walk 6000–10000 steps daily
- Sleep 7–8 hours
- Drink 3–4 liters water daily
"""

            return render_template("index.html", plan=plan)

        except Exception as e:
            return render_template("index.html", plan="Error generating plan: " + str(e))

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "").strip()

        if message == "":
            return jsonify({"reply": "Please type your fitness question."})

        reply = bot.get_response(message)
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)

        age = int(data.get("age"))
        weight = float(data.get("weight"))
        height = float(data.get("height"))
        gender = data.get("gender", "male")
        activity = data.get("activity", "moderate")
        goal = data.get("goal", "maintain")

        result = bot.calculate_plan(age, weight, height, gender, activity, goal)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)