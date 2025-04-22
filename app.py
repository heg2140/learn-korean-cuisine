from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

items = [
    {
        "name": "Kimchi",
        "audio": "audio/kimchi.mp3",
        "ingredients": [
            "1. Brined Napa Cabbage",
            "2. Daikon Radish",
            "3. Korean Chili Powder",
            "4. Rice Flour",
            "5. Shrimp Paste",
            "6. Garlic",
            "7. Ginger"
        ],
        "image": "https://english.visitkorea.or.kr/public/images/foodtrip/k-food-img/img_kfood_view_374.jpg"
    },
    {
        "name": "Pajeon",
        "audio": "audio/pajeon.mp3",
        "ingredients": [
            "1. Green Onions",
            "2. Flour",
            "3. Water",
            "4. Soybean Paste",
            "5. Sugar",
            "6. Vegetable Oil"
        ],
        "image": "https://english.visitkorea.or.kr/public/images/foodtrip/k-food-img/img_kfood_view_200.jpg"
    },
    {
        "name": "Gimbap",
        "audio": "audio/gimbap.mp3",
        "ingredients": [
            "1. Rice",
            "2. Seaweed",
            "3. Carrot",
            "4. Spinach",
            "5. Fish Sauce",
            "6. Pickled Radish",
            "7. Sesame Oil"
        ],
        "image": "https://english.visitkorea.or.kr/public/images/foodtrip/k-food-img/img_kfood_view_183.jpg"
    },
    {
        "name": "Japchae",
        "audio": "audio/japchae.mp3",
        "ingredients": [
            "1. Sweet Potato Starch Noodles",
            "2. Beef",
            "3. Carrot",
            "4. Spinach",
            "5. Onion",
            "6. Bell Pepper",
            "7. Shitake Mushroom"
        ],
        "image": "https://english.visitkorea.or.kr/public/images/foodtrip/k-food-img/img_kfood_view_363.jpg"
    },
    {
        "name": "Bulgogi",
        "audio": "audio/bulgogi.mp3",
        "ingredients": [
            "1. Beef",
            "2. Garlic",
            "3. Green Onion",
            "4. Soy Sauce",
            "5. Sugar",
            "6. Sesame Oil",
            "7. Sesame Seeds"
        ],
        "image": "https://english.visitkorea.or.kr/public/images/foodtrip/k-food-img/img_kfood_view_106.jpg"
    } 
]

questions = [
    {
        "question": "Which of the following is NOT in Kimchi?",
        "options": ["Ginger", "Fish sauce", "Korean Chili Paste"],
        "answer": "Korean Chili Paste"
    },
    {
        "question": "Which of the following is in Pajeon?",
        "options": ["Radish", "Sugar", "Fish sauce"],
        "answer": "Sugar"
    },
    {
        "question": "Which of the following is NOT in Gimbap?",
        "options": ["Radish", "Sesame oil", "Garlic"],
        "answer": "Garlic"
    },
    {
        "question": "Which of the following is in Japchae?",
        "options": ["Spinach", "Pork", "Ginger"],
        "answer": "Spinach"
    },
    {
        "question": "Which of the following is NOT in Bulgogi?",
        "options": ["Soy Sauce", "Rice Flour", "Sesame Seeds"],
        "answer": "Rice Flour"
    }
]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/learn')
def learn():
    return render_template("learn.html")

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        qid = int(request.form["qid"])
        selected = request.form["choice"]
        correct = questions[qid]["answer"]
        return render_template("result.html", correct=correct, selected=selected, qid=qid)
    else:
        qid = int(request.args.get("qid", 0))
        if qid >= len(questions):
            return render_template("result.html", final=True)
        return render_template("quiz.html", question=questions[qid], qid=qid)

if __name__ == '__main__':
    app.run(debug=True)
