from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
import random, uuid, datetime, logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
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
        "options": ["Ginger", "Shrimp Paste", "Korean Chili Paste"],
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

        log = session.get('learning_log', [])
        log.append({
            "index": index,
            "type": item['type'],
            "name": item.get('name', 'quiz'),
            "timestamp": datetime.datetime.now().isoformat()
        })
        session['learning_log'] = log

        selected = None
        is_correct = None

        if item['type'] == 'quiz':
            answers = session.get('quiz_answers', {})
            results = session.get('quiz_results', {})
            submitted = set(session.get('quiz_submitted', []))

            if str(index) in submitted:
                selected = answers.get(str(index))
                is_correct = results.get(str(index))
            else:
                selected = None
                is_correct = None

        return render_template(
            template,
            item=item,
            index=index,
            total=len(items),
            selected=selected,
            is_correct=is_correct,
            is_last=(index == len(items) - 1)
        )
    
    logging.debug("SESSION DEBUG")
    logging.debug("quiz_answers: %s", session.get('quiz_answers'))
    logging.debug("quiz_results: %s", session.get('quiz_results'))
    logging.debug("current index: %s", index)

    return redirect('/learn/0')

@app.route('/learn')
def learn_redirect():
    return redirect('/learn/0')

@app.route('/pop-quiz-result/<int:index>', methods=['POST'])
def pop_quiz_result(index):
    selected = request.form.get("answer")
    correct = items[index]["answer"]

    if not selected:

        return render_template(
            'pop-quiz.html',
            item=items[index],
            index=index,
            total=len(items),
            selected=None,
            is_correct=None,
            is_last=(index == len(items) - 1)
        )

    is_correct = selected == correct
    is_last = index == len(items) - 1

    answers = session.get('quiz_answers', {})
    answers[str(index)] = selected
    session['quiz_answers'] = answers

    results = session.get('quiz_results', {})
    results[str(index)] = is_correct
    session['quiz_results'] = results

    submitted = session.get('quiz_submitted', set())
    submitted = set(submitted) if isinstance(submitted, list) else submitted
    submitted.add(str(index))
    session['quiz_submitted'] = list(submitted)

    if 'quiz_log' not in session:
        session['quiz_log'] = []

    log = session['quiz_log']
    log.append({
        "index": index,
        "question": items[index].get("question", "Unknown"),
        "selected": selected,
        "correct": correct,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })
    session['quiz_log'] = log

    logging.debug("[POP QUIZ] User submitted: %s", log[-1])

    return render_template(
        'pop-quiz.html',
        item=items[index],
        index=index,
        total=len(items),
        selected=selected,
        is_correct=is_correct,
        is_last=is_last
    )

@app.route('/reset-quiz/<int:index>')
def reset_quiz(index):

    if 'quiz_answers' in session:
        session['quiz_answers'].pop(str(index), None)
    if 'quiz_results' in session:
        session['quiz_results'].pop(str(index), None)
    session.modified = True
    return redirect(url_for('learn', index=index))

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
    
@app.route('/quiz/easy')
def easy_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]

    if len(flashcards) < 5:
        raise ValueError("Not enough flashcards")
    selected_items = random.sample(flashcards, 5)

    labels = selected_items.copy()
    images = selected_items.copy()
    random.shuffle(labels)
    random.shuffle(images)

    return render_template("easy_quiz.html", labels=labels, images=images)


@app.route("/quiz/easy/result")
def easy_quiz_results():
    time_left_str = request.args.get("time", "1:00") 
    misses = request.args.get("misses", "0")

    try:
        minutes, seconds = map(int, time_left_str.split(":"))
        time_left = minutes * 60 + seconds
        time_taken = 60 - time_left
    except ValueError:
        time_taken = 60 

    return render_template("easy_result.html", time_taken=time_taken, misses=misses)

@app.route('/quiz/easy/failed')
def easy_quiz_failed():
    time_taken = request.args.get("time", "1:00")
    misses = request.args.get("misses", "0")
    return render_template("failed_quiz.html", time_taken=time_taken, misses=misses, level="easy")

@app.route('/quiz/easy/result', methods=['POST'])
def submit_easy_quiz_answer():
    index = request.form.get("index") 
    selected = request.form.get("answer")  
    correct = get_correct_answer(index)  
    is_correct = selected == correct

    if 'easy_quiz_log' not in session:
        session['easy_quiz_log'] = []

    log = session['easy_quiz_log']
    log.append({
        "index": index,
        "selected": selected,
        "correct": correct,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })
    session['easy_quiz_log'] = log 

    logging.debug("[LOGGED] Easy quiz entry: %s", log[-1])
    return redirect(url_for('easy_quiz_result_page'))

@app.route('/quiz/easy/log-answer', methods=['POST'])
def log_easy_quiz_answer():
    data = request.get_json()

    match_id = data.get("match_id")
    source_type = data.get("source_type")
    target_type = data.get("target_type")
    is_correct = data.get("is_correct")

    if 'easy_quiz_log' not in session:
        session['easy_quiz_log'] = []

    session['easy_quiz_log'].append({
        "match_id": match_id,
        "source_type": source_type,
        "target_type": target_type,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })

    session.modified = True 

    logging.debug("[LOGGED] Easy quiz match: %s", session['easy_quiz_log'][-1])

    return jsonify(success=True)

@app.route('/quiz/easy/store-result', methods=['POST'])
def store_easy_quiz_result():
    data = request.get_json()

    outcome = data.get("outcome")             
    time = data.get("time")                   
    misses = data.get("misses")               
    matches = data.get("matches")             

    session["easy_quiz_outcome"] = outcome
    session["easy_quiz_time"] = time
    session["easy_quiz_misses"] = misses
    session["easy_quiz_matches"] = matches
    session.modified = True

    import logging
    logging.debug(f"[EASY QUIZ COMPLETE] Outcome: {outcome}, Time: {time}, Misses: {misses}, Matches: {matches}")

    return jsonify(success=True)

@app.route('/quiz/medium')
def medium_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]

    selected_items = random.sample(flashcards, 5)

    labels = selected_items.copy()
    ingredients = selected_items.copy()
    random.shuffle(labels)
    random.shuffle(ingredients)

    return render_template("medium_quiz.html", labels=labels, images=ingredients)

@app.route('/quiz/medium/result')
def medium_quiz_result():
    time_left_str = request.args.get("time", "1:00")  
    misses = request.args.get("misses", "0")

    try:
        minutes, seconds = map(int, time_left_str.split(":"))
        time_left = minutes * 60 + seconds
        time_taken = 60 - time_left
    except ValueError:
        time_taken = 60  

    return render_template("medium_result.html", time_taken=time_taken, misses=misses)

@app.route('/quiz/medium/failed')
def medium_quiz_failed():
    time_taken = request.args.get("time", "1:00")
    misses = request.args.get("misses", "0")
    return render_template("failed_quiz.html", time_taken=time_taken, misses=misses, level="medium")

@app.route('/quiz/medium/result', methods=['POST'])
def submit_medium_quiz_answer():
    index = request.form.get("index")  
    selected = request.form.get("answer")  
    correct = get_correct_answer(index)  
    is_correct = selected == correct

    if 'medium_quiz_log' not in session:
        session['medium_quiz_log'] = []

    log = session['medium_quiz_log']
    log.append({
        "index": index,
        "selected": selected,
        "correct": correct,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })
    session['medium_quiz_log'] = log  

    logging.debug("[LOGGED] Medium quiz entry: %s", log[-1])
    return redirect(url_for('medium_quiz_result_page'))

@app.route('/quiz/medium/log-answer', methods=['POST'])
def log_medium_quiz_answer():
    data = request.get_json()

    match_id = data.get("match_id")
    source_type = data.get("source_type")
    target_type = data.get("target_type")
    is_correct = data.get("is_correct")

    if 'medium_quiz_log' not in session:
        session['medium_quiz_log'] = []

    session['medium_quiz_log'].append({
        "match_id": match_id,
        "source_type": source_type,
        "target_type": target_type,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })

    session.modified = True  

    logging.debug("[LOGGED] Medium quiz match: %s", session['medium_quiz_log'][-1])

    return jsonify(success=True)

@app.route('/quiz/medium/store-result', methods=['POST'])
def store_medium_quiz_result():
    data = request.get_json()

    outcome = data.get("outcome")             
    time = data.get("time")                  
    misses = data.get("misses")               
    matches = data.get("matches")             

    session["medium_quiz_outcome"] = outcome
    session["medium_quiz_time"] = time
    session["medium_quiz_misses"] = misses
    session["medium_quiz_matches"] = matches
    session.modified = True

    import logging
    logging.debug(f"[MEDIUM QUIZ COMPLETE] Outcome: {outcome}, Time: {time}, Misses: {misses}, Matches: {matches}")

    return jsonify(success=True)

@app.route('/quiz/hard')
def hard_quiz():
    flashcards = [item for item in items if item["type"] == "flashcard"]
    selected = random.sample(flashcards, 5)

    representations = []

    for card in selected:
        match_id = str(uuid.uuid4())

        types = ["name", "image", "audio", "ingredients"]
        chosen_types = random.sample(types, 2)
        draggable_type = chosen_types[0]
        dropzone_type = chosen_types[1]

        if draggable_type == "name":
            draggable_content = card["name"]
        elif draggable_type == "image":
            draggable_content = card["image"]
        elif draggable_type == "audio":
            draggable_content = card["audio"]
        elif draggable_type == "ingredients":
            draggable_content = card["ingredients"]

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
    time_left_str = request.args.get("time", "1:00") 
    misses = request.args.get("misses", "0")

    try:
        minutes, seconds = map(int, time_left_str.split(":"))
        time_left = minutes * 60 + seconds
        time_taken = 60 - time_left
    except ValueError:
        time_taken = 60 
    return render_template("hard_result.html", time_taken=time_taken, misses=misses)

@app.route('/quiz/hard/failed')
def hard_quiz_failed():
    time_taken = request.args.get("time", "1:00")
    misses = request.args.get("misses", "0")
    return render_template("failed_quiz.html", time_taken=time_taken, misses=misses, level="easy")

@app.route('/quiz/hard/result', methods=['POST'])
def submit_quiz_answer():
    index = request.form.get("index")  
    selected = request.form.get("answer")  
    correct = get_correct_answer(index) 
    is_correct = selected == correct

    if 'hard_quiz_log' not in session:
        session['hard_quiz_log'] = []

    log = session['hard_quiz_log']
    log.append({
        "index": index,
        "selected": selected,
        "correct": correct,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })
    session['hard_quiz_log'] = log  
    logging.debug("[LOGGED] Hard quiz entry: %s", log[-1])
    return redirect(url_for('hard_quiz_result_page'))

@app.route('/quiz/hard/log-answer', methods=['POST'])
def log_hard_quiz_answer():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    match_id = data.get("match_id")
    source_type = data.get("source_type")
    target_type = data.get("target_type")
    is_correct = data.get("is_correct")

    if 'hard_quiz_log' not in session:
        session['hard_quiz_log'] = []

    session['hard_quiz_log'].append({
        "match_id": match_id,
        "source_type": source_type,
        "target_type": target_type,
        "is_correct": is_correct,
        "timestamp": datetime.datetime.now().isoformat()
    })

    session.modified = True
    logging.debug("[LOGGED] Medium quiz match: %s", session['medium_quiz_log'][-1])


    return jsonify(success=True)

@app.route('/quiz/hard/store-result', methods=['POST'])
def store_hard_quiz_result():
    data = request.get_json()

    outcome = data.get("outcome")
    time = data.get("time")
    misses = data.get("misses")
    matches = data.get("matches")

    session["hard_quiz_outcome"] = outcome
    session["hard_quiz_time"] = time
    session["hard_quiz_misses"] = misses
    session["hard_quiz_matches"] = matches
    session.modified = True

    logging.debug(f"[QUIZ COMPLETE] Outcome: {outcome}, Time: {time}, Misses: {misses}, Matches: {matches}")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
