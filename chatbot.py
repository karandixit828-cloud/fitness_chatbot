from groq import Groq


class FitnessChatbot:
    def __init__(self):
        self.client = Groq(
            api_key="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"
        )

    def get_response(self, message):
        return self.ask_ai(message)

    def ask_ai(self, user_message):
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are an advanced fitness chatbot.
Answer only fitness-related questions.

Topics allowed:
diet, workout, gym, protein, calories, fat loss, muscle gain,
supplements, cardio, BMI, BMR, TDEE, exercises, recovery, sleep, hydration.

Use simple practical language.
Use Indian diet examples when helpful.
For non-fitness questions say: I can only answer fitness-related questions.
Do not give medical diagnosis.
"""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=600
            )

            return response.choices[0].message.content

        except Exception as e:
            return "API Error: " + str(e)

    def calculate_plan(self, age, weight, height, gender, activity, goal):
        bmi = self.calculate_bmi(weight, height)
        bmr = self.calculate_bmr(age, weight, height, gender)
        tdee = self.calculate_tdee(bmr, activity)

        if goal.lower() in ["loss", "weight loss", "fat loss"]:
            target_calories = tdee - 500
        elif goal.lower() in ["gain", "muscle gain", "weight gain"]:
            target_calories = tdee + 300
        else:
            target_calories = tdee

        protein_min = round(weight * 1.6)
        protein_max = round(weight * 2.2)

        return {
            "BMI": round(bmi, 2),
            "BMI Category": self.bmi_category(bmi),
            "BMR": round(bmr),
            "TDEE": round(tdee),
            "Target Calories": round(target_calories),
            "Protein Intake": f"{protein_min}g - {protein_max}g per day"
        }

    def calculate_bmi(self, weight, height):
        height_meter = height / 100
        return weight / (height_meter * height_meter)

    def bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def calculate_bmr(self, age, weight, height, gender):
        if gender.lower() == "female":
            return 10 * weight + 6.25 * height - 5 * age - 161
        return 10 * weight + 6.25 * height - 5 * age + 5

    def calculate_tdee(self, bmr, activity):
        levels = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very active": 1.9
        }
        return bmr * levels.get(activity.lower(), 1.55)