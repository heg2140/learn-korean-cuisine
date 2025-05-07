from flask import Flask, render_template, request, redirect, flash, url_for
import random, uuid
app = Flask(__name__)
app.secret_key = 'some_secret_key'

items = [
    {
        "type": "flashcard",
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
        "type": "quiz",
        "question": "Which of the following is NOT in Kimchi?",
        "options": ["Ginger", "Fish sauce", "Korean Chili Paste"],
        "answer": "Korean Chili Paste"
    },
    {
        "type": "flashcard",
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
        "type": "quiz",
        "question": "Which of the following is in Pajeon?",
        "options": ["Radish", "Sugar", "Fish sauce"],
        "answer": "Sugar"
    },
    {
        "type": "flashcard",
        "name": "Gimbap",
        "audio": "audio/kimbap.mp3",
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
        "type": "quiz",
        "question": "Which of the following is NOT in Gimbap?",
        "options": ["Radish", "Sesame oil", "Garlic"],
        "answer": "Garlic"
    },
    {
        "type": "flashcard",
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
        "type": "quiz",
        "question": "Which of the following is in Japchae?",
        "options": ["Spinach", "Pork", "Ginger"],
        "answer": "Spinach"
    },
    {
        "type": "flashcard",
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
    },
    {
        "type": "quiz",
        "question": "Which of the following is NOT in Bulgogi?",
        "options": ["Soy Sauce", "Rice Flour", "Sesame Seeds"],
        "answer": "Rice Flour"
    }
]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/learn/<int:index>')
def learn(index):
    if 0 <= index < len(items):
        item = items[index]
        template = 'learn.html' if item['type'] == 'flashcard' else 'pop-quiz.html'
        return render_template(template, item=item, index=index, total=len(items))
    return redirect('/learn/0')

@app.route('/learn')
def learn_redirect():
    return redirect('/learn/0')

@app.route('/pop-quiz-result/<int:index>', methods=['POST'])
def pop_quiz_result(index):
    selected = request.form.get("answer")
    correct = items[index]["answer"]
    is_correct = selected == correct
    is_last = index == len(items) - 1  

    return render_template(
        'pop-quiz.html',
        item=items[index],
        index=index,
        total=len(items),
        selected=selected,
        is_correct=is_correct,
        is_last=is_last
    )

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
    
@app.route('/quiz/easy')
def easy_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]

    # Make sure there are at least 5 flashcards
    if len(flashcards) < 5:
        raise ValueError("Not enough flashcards")

    # Sample 5 flashcards
    selected_items = random.sample(flashcards, 5)

    # Shuffle labels and images separately
    labels = selected_items.copy()
    images = selected_items.copy()
    random.shuffle(labels)
    random.shuffle(images)

    return render_template("easy_quiz.html", labels=labels, images=images)


@app.route("/quiz/easy/result")
def easy_quiz_results():
    time_left_str = request.args.get("time", "1:00")  # format: "mm:ss"
    misses = request.args.get("misses", "0")

    try:
        minutes, seconds = map(int, time_left_str.split(":"))
        time_left = minutes * 60 + seconds
        time_taken = 60 - time_left
    except ValueError:
        time_taken = 60  # fallback if something goes wrong

    return render_template("easy_result.html", time_taken=time_taken, misses=misses)


@app.route('/quiz/medium')
def medium_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]

    # Sample 5 flashcards
    selected_items = random.sample(flashcards, 5)

    # Shuffle labels and images separately
    labels = selected_items.copy()
    ingredients = selected_items.copy()
    random.shuffle(labels)
    random.shuffle(ingredients)

    return render_template("medium_quiz.html", labels=labels, images=ingredients)

@app.route('/quiz/medium/result')
def medium_quiz_result():
    time_left_str = request.args.get("time", "1:00")  # format: "mm:ss"
    misses = request.args.get("misses", "0")

    try:
        minutes, seconds = map(int, time_left_str.split(":"))
        time_left = minutes * 60 + seconds
        time_taken = 60 - time_left
    except ValueError:
        time_taken = 60  # fallback if something goes wrong

    return render_template("medium_result.html", time_taken=time_taken, misses=misses)

@app.route('/quiz/hard')
def hard_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]
    selected = random.sample(flashcards, 5)

    representations = []

    for card in selected:
        match_id = str(uuid.uuid4())

        # Randomly assign roles
        types = ["name", "image", "audio", "ingredients"]
        chosen_types = random.sample(types, 2)
        draggable_type = chosen_types[0]
        dropzone_type = chosen_types[1]

        # Draggable representation
        if draggable_type == "name":
            draggable_content = card["name"]
        elif draggable_type == "image":
            draggable_content = card["image"]
        elif draggable_type == "audio":
            draggable_content = card["audio"]
        elif draggable_type == "ingredients":
            draggable_content = card["ingredients"]

        # Dropzone representation
        if dropzone_type == "name":
            dropzone_content = card["name"]
        elif dropzone_type == "image":
            dropzone_content = card["image"]
        elif dropzone_type == "audio":
            dropzone_content = card["audio"]
        elif dropzone_type == "ingredients":
            dropzone_content = card["ingredients"]

        representations.append({
            "role": "draggable",
            "type": draggable_type,
            "content": draggable_content,
            "match_id": match_id
        })

        representations.append({
            "role": "dropzone",
            "type": dropzone_type,
            "content": dropzone_content,
            "match_id": match_id
        })

    random.shuffle(representations)

    return render_template("hard_quiz.html", cards=representations)


@app.route('/quiz/hard/result')
def hard_quiz_result():
    time_taken = request.args.get("time", "1:00")
    misses = request.args.get("misses", 0)
    return render_template("hard_result.html", time_taken=time_taken, misses=misses)



if __name__ == '__main__':
    app.run(debug=True)
