from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = [
    {
        "question": "Which of the following is NOT in Kimchi?",
        "options": ["Ginger", "Fish sauce", "Korean Chili Paste"],
        "answer": "Korean Chili Paste"
    },
    {
        "question": "Which of the following is in Pajeon?",
        "options": ["Radish", "Fish sauce", "Sugar"],
        "answer": "Sugar"
    },
    {
        "question": "Which of the following is NOT in Gimbap?",
        "options": ["Radish", "Sesame oil", "Garlic"],
        "answer": "Garlic"
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
