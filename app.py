from flask import Flask, render_template, request, redirect, url_for, session
from quiz_app.quiz_app import load_questions_from_file
import os
import random
import json


app = Flask(__name__)
app.secret_key = "supersecret"

QUESTIONS_FILE = "quiz_app/questions.txt"
cards = load_questions_from_file(QUESTIONS_FILE)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_quiz():
    global cards
    random.shuffle(cards)           # randomize the question order
    session['index'] = 0
    session['score'] = 0
    return redirect(url_for('question'))


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/question', methods=['GET', 'POST'])
def question():
    index = session.get('index')

    if index is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get("action")  # Detect which button was clicked

        # If user selected Quit, immediately end the quiz
        if action == "quit":
            return redirect(url_for('result'))

        # Otherwise continue normally (Next button)
        user_answer = request.form.get('answer')
        correct_answer = cards[index].answer

        if user_answer and user_answer.strip().lower() == correct_answer.strip().lower():
            session['score'] += 1

        index += 1
        session['index'] = index

        if index >= len(cards):
            return redirect(url_for('result'))

    return render_template(
        'question.html',
        card=cards[index],
        current=index + 1,
        total=len(cards)
    )

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(cards)
    session.clear()  # reset quiz state
    return render_template('result.html', score=score, total=total)


# --------------------------
# FILE UPLOAD ROUTE
# --------------------------
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename.endswith(".txt"):
            # Read uploaded questions
            lines = file.read().decode("utf-8").strip().split("\n")
            uploaded_cards = []

            for line in lines:
                if "|" in line:
                    q, a = line.split("|")
                    uploaded_cards.append(Card(q.strip(), a.strip()))

            # Save to session so quiz uses only uploaded questions
            session['custom_cards'] = [(c.question, c.answer) for c in uploaded_cards]

            return redirect(url_for('start_custom_quiz'))

    return render_template('upload.html')

@app.route('/start_custom')
def start_custom_quiz():
    session['index'] = 0
    session['score'] = 0
    return redirect(url_for('custom_question'))

@app.route('/custom_question', methods=['GET', 'POST'])
def custom_question():
    index = session.get('index')
    
    custom_cards_data = session.get('custom_cards')
    if not custom_cards_data:
        return redirect(url_for('home'))

    custom_cards = [Card(q, a) for q, a in custom_cards_data]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = custom_cards[index].answer

        if user_answer.strip().lower() == correct_answer.strip().lower():
            session['score'] += 1

        session['index'] += 1
        index += 1

        if index >= len(custom_cards):
            return redirect(url_for('result'))

    return render_template(
        "question.html",
        card=custom_cards[index],
        current=index + 1,
        total=len(custom_cards)
    )



# --------------------------
# MANUAL ADD QUESTION ROUTE
# --------------------------

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    return render_template('add_question.html')

@app.route("/save_question", methods=["POST"])
def save_question():
    question = request.form["question"]
    answer = request.form["answer"]

    set_name = session.get("current_set")
    if not set_name:
        return redirect("/")   # no set selected

    file_path = f"flashcard_sets/{set_name}.json"

    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add new question
    data.append({"question": question, "answer": answer})

    # Save back to file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return redirect("/add_question")


@app.route("/select_set", methods=["GET", "POST"])
def select_set():
    # Ensure folder exists
    if not os.path.exists("flashcard_sets"):
        os.makedirs("flashcard_sets")

    if request.method == "POST":
        selected = request.form.get("set_name")
        new_set = request.form.get("new_set_name")

        if new_set:
            selected = new_set
            open(f"flashcard_sets/{selected}.json", "w").write("[]")

        session["current_set"] = selected
        return redirect("/add")

    # For GET request → load sets
    sets = os.listdir("flashcard_sets")
    sets = [s.replace(".json", "") for s in sets]
    return render_template("select_set.html", sets=sets)


@app.route("/choose_set")
def choose_set():
    sets = [f.replace(".json", "") for f in os.listdir("flashcard_sets") if f.endswith(".json")]
    return render_template("select_set.html", sets=sets)

if __name__ == '__main__':
    app.run(debug=True)
