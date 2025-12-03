import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecret"

SETS_FOLDER = "flashcard_sets"
os.makedirs(SETS_FOLDER, exist_ok=True)

# ---------- Helper functions ----------

def load_questions(file_path):
    """Load questions from a .txt or .json file into a list of dicts."""
    if not os.path.exists(file_path):
        return []

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        cards = []
        i = 0
        while i < len(lines):
            if lines[i].endswith("?"):
                question = lines[i]
                answer = lines[i + 1] if i + 1 < len(lines) else ""
                cards.append({"question": question, "answer": answer})
                i += 2
            else:
                i += 1
        return cards
    elif file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_questions(file_path, cards):
    """Save list of question dicts to JSON."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4)

# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

# ---------- Upload Questions File ----------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".txt"):
            set_name = file.filename.replace(".txt", "")
            file_path = os.path.join(SETS_FOLDER, f"{set_name}.txt")
            file.save(file_path)
            flash(f"Set '{set_name}' uploaded successfully!", "success")
            return redirect(url_for("select_quiz_set"))
        else:
            flash("Invalid file. Must be a .txt file with questions ending in '?' and answers on the next line.", "danger")
    return render_template("upload.html")

# ---------- Add Your Own Question ----------
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    sets = [f.replace('.json', '') for f in os.listdir(SETS_FOLDER) if f.endswith('.json')]

    if request.method == 'POST':
        existing_set = request.form.get('existing_set')
        new_set_name = request.form.get('new_set_name').strip()
        question = request.form.get('question').strip()
        answer = request.form.get('answer').strip()

        if not question or not answer:
            flash("Question and answer required!", "danger")
            return redirect(url_for('add_question'))

        # Determine filename
        if new_set_name:
            filename = f"{new_set_name}.json"
        elif existing_set:
            filename = f"{existing_set}.json"
        else:
            flash("Please select or name a set.", "danger")
            return redirect(url_for('add_question'))

        filepath = os.path.join(SETS_FOLDER, filename)

        # Load or create properly structured JSON
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # If file is a list, convert it to our standard structure
            if isinstance(data, list):
                data = {"questions": data}
        else:
            data = {"questions": []}

        # Save new question
        data["questions"].append({
            "question": question,
            "answer": answer
        })

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        flash("Question added successfully!", "success")
        return redirect(url_for('add_question'))

    return render_template('add_question.html', sets=sets)

# ---------- Select Quiz Set ----------
@app.route("/select_quiz_set", methods=["GET", "POST"])
def select_quiz_set():
    # Get all available sets (.txt)
    sets = [
    f.replace(".txt", "").replace(".json", "")
    for f in os.listdir(SETS_FOLDER)
    if f.endswith(".txt") or f.endswith(".json")
]


    if request.method == "POST":
        chosen = request.form.get("set_name")
        if chosen:
            session["quiz_set"] = chosen
            return redirect(url_for("start_quiz"))
        else:
            flash("Please select a set.", "danger")

    return render_template("select_quiz_set.html", sets=sets)
# ---------- Start Quiz ----------
@app.route("/start", methods=["GET"])
def start_quiz():
    set_name = session.get("quiz_set")
    if not set_name:
        flash("Please select a set first.", "warning")
        return redirect(url_for("select_quiz_set"))

    txt_path = os.path.join(SETS_FOLDER, f"{set_name}.txt")
    json_path = os.path.join(SETS_FOLDER, f"{set_name}.json")

    file_path = txt_path if os.path.exists(txt_path) else json_path

    cards = load_questions(file_path)

    # Convert {"questions": [...]} to list
    if isinstance(cards, dict) and "questions" in cards:
        cards = cards["questions"]

    if not cards:
        flash("This set has no questions or the format is incorrect.", "danger")
        return redirect(url_for("select_quiz_set"))
    random.shuffle(cards)
    
    
    session["quiz_pool"] = cards
    session["index"] = 0
    session["score"] = 0
    session["wrong_questions"] = []

    return redirect(url_for("question"))


# ---------- Quiz Question ----------
@app.route("/question", methods=["GET", "POST"])
def question():
    index = session.get("index", 0)
    pool = session.get("quiz_pool", [])
    wrong_questions = session.get("wrong_questions", [])

    if not pool or index >= len(pool):
        return redirect(url_for("result"))

    card = pool[index]

    if request.method == "POST":
        action = request.form.get("action")
        if action == "quit":
            flash("Quiz stopped. Returning to home.", "info")
            session.pop("quiz_pool", None)
            session.pop("index", None)
            session.pop("wrong_questions", None)
            session.pop("score", None)
            return redirect(url_for("home"))

        # Otherwise, handle answer submission
        user_answer = request.form.get("answer", "").strip()
        if user_answer.lower() == card["answer"].lower():
            session["score"] += 1
            flash("✅ Correct!", "success")
        else:
            flash(f"❌ Incorrect! Correct answer: {card['answer']}", "danger")
            wrong_questions.append(card)

        session["index"] = index + 1
        session["wrong_questions"] = wrong_questions

        # Repeat missed questions if at end
        if session["index"] >= len(pool):
            if wrong_questions:
                flash("Repeating missed questions...", "info")
                session["quiz_pool"] = wrong_questions
                session["index"] = 0
                session["wrong_questions"] = []
            else:
                return redirect(url_for("result"))

        return redirect(url_for("question"))

    return render_template("question.html", card=card, current=index + 1, total=len(pool))

# ---------- Result ----------
@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("quiz_pool", []))
    percent = (score / total) * 100 if total > 0 else 0

    session.clear()
    return render_template("result.html", score=score, total=total, percent=percent)

if __name__ == "__main__":
    app.run(debug=True)
