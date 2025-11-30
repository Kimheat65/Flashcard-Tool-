# app.py
import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from quiz_app.quiz_app import (
    Flashcard,
    load_questions_from_file,
    append_cards_to_manual_log,
    manual_entry,
    build_question_pool,
)

app = Flask(__name__)
app.secret_key = "supersecret"

# ---------- Folders ----------
SETS_FOLDER = "flashcard_sets"
if not os.path.exists(SETS_FOLDER):
    os.makedirs(SETS_FOLDER)

# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")


# ---------------- Upload a TXT set ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".txt"):
            set_name = file.filename.replace(".txt", "")
            lines = file.read().decode("utf-8").splitlines()
            cards = []
            for line in lines:
                if "|" in line:
                    q, a = line.split("|", 1)
                    cards.append(Flashcard(question=q.strip(), answer=a.strip()))
            file_path = os.path.join(SETS_FOLDER, f"{set_name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([c.__dict__ for c in cards], f, indent=4)
            flash(f"Set '{set_name}' uploaded successfully!", "success")
            return redirect(url_for("select_quiz_set"))
        else:
            flash("Invalid file. Must be a .txt file with Q|A separated by '|'.", "danger")
    return render_template("upload.html")


# ---------------- Select a Set to Add Questions ----------------
@app.route("/select_set", methods=["GET", "POST"])
def select_set():
    sets = [f.replace(".json", "") for f in os.listdir(SETS_FOLDER) if f.endswith(".json")]

    if request.method == "POST":
        chosen_set = request.form.get("set_name")
        new_set = request.form.get("new_set_name", "").strip()
        if new_set:
            # Create new empty set if it doesn't exist
            file_path = os.path.join(SETS_FOLDER, f"{new_set}.json")
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    json.dump([], f)
            chosen_set = new_set

        if chosen_set:
            session["current_set"] = chosen_set
            return redirect(url_for("add_question"))

    return render_template("select_set.html", sets=sets)


# ---------------- Manual Add Questions ----------------
@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    set_name = session.get("current_set")
    if not set_name:
        flash("Please select a set first.", "warning")
        return redirect(url_for("select_set"))

    file_path = os.path.join(SETS_FOLDER, f"{set_name}.json")
    cards = load_questions_from_file(file_path)

    if request.method == "POST":
        q = request.form.get("question")
        a = request.form.get("answer")
        if q and a:
            card = Flashcard(question=q.strip(), answer=a.strip())
            cards.append(card)
            append_cards_to_manual_log([card])
            with open(file_path, "w") as f:
                json.dump([c.__dict__ for c in cards], f, indent=4)
            flash("Question added!", "success")
            return redirect(url_for("add_question"))
        else:
            flash("Both question and answer are required.", "danger")

    return render_template("add_question.html", set_name=set_name, cards=cards)


# ---------------- Select Quiz Set ----------------
@app.route("/select_quiz_set", methods=["GET", "POST"])
def select_quiz_set():
    sets = [f.replace(".json", "") for f in os.listdir(SETS_FOLDER) if f.endswith(".json")]
    if request.method == "POST":
        chosen = request.form.get("set_name")
        if chosen:
            session["quiz_set"] = chosen
            return redirect(url_for("start_quiz"))
    return render_template("select_quiz_set.html", sets=sets)


# ---------------- Start Quiz ----------------
@app.route("/start")
def start_quiz():
    set_name = session.get("quiz_set")
    if not set_name:
        flash("Please select a set first.", "warning")
        return redirect(url_for("select_quiz_set"))

    file_path = os.path.join(SETS_FOLDER, f"{set_name}.json")
    cards = load_questions_from_file(file_path)
    pool = build_question_pool(cards)
    random.shuffle(pool)

    session["quiz_pool"] = [c.__dict__ for c in pool]  # store pool in session
    session["index"] = 0
    session["score"] = 0
    session["round_number"] = 1
    return redirect(url_for("question"))


# ---------------- Quiz Question ----------------
@app.route("/question", methods=["GET", "POST"])
def question():
    index = session.get("index", 0)
    pool_dicts = session.get("quiz_pool", [])
    if not pool_dicts:
        flash("No quiz loaded.", "danger")
        return redirect(url_for("home"))

    pool = [Flashcard(**c) for c in pool_dicts]

    if request.method == "POST":
        action = request.form.get("action")
        if action == "quit":
            return redirect(url_for("result"))

        user_answer = request.form.get("answer", "").strip()
        card = pool[index]
        card.times_seen += 1
        session["index"] += 1

        if user_answer.lower() == card.answer.lower():
            card.times_correct += 1
            session["score"] += 1
            flash("✅ Correct!", "success")
        else:
            flash(f"❌ Incorrect! Correct answer: {card.answer}", "danger")

        session["quiz_pool"] = [c.__dict__ for c in pool]

        if session["index"] >= len(pool):
            return redirect(url_for("result"))
        else:
            return redirect(url_for("question"))

    return render_template("question.html", card=pool[index], current=index+1, total=len(pool))


# ---------------- Result ----------------
@app.route("/result")
def result():
    pool_dicts = session.get("quiz_pool", [])
    pool = [Flashcard(**c) for c in pool_dicts]
    score = session.get("score", 0)
    total = len(pool)
    round_number = session.get("round_number", 1)
    quiz_name = session.get("quiz_set", "unknown")
    percent = (score / total) * 100 if total > 0 else 0

    # Optional: record session result (can reuse console function)
    # record_session_result(quiz_name, round_number, total, score, percent)

    # Clear session
    session.pop("quiz_pool", None)
    session.pop("index", None)
    session.pop("score", None)
    session.pop("quiz_set", None)

    return render_template("result.html", score=score, total=total, percent=percent)


# ---------- Run Flask ----------
if __name__ == "__main__":
    app.run(debug=True)
