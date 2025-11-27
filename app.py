
from flask import Flask, render_template, request, redirect, url_for, session
from quiz_app.quiz_app import load_questions_from_file

app = Flask(__name__)
app.secret_key = "supersecret"  # Required for session handling

QUESTIONS_FILE = "quiz_app/questions.txt"
cards = load_questions_from_file(QUESTIONS_FILE)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_quiz():
    # Initialize session variables
    session['index'] = 0
    session['score'] = 0
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    index = session.get('index')

    # If quiz hasn't started, redirect to home
    if index is None:
        return redirect(url_for('home'))

    # Handle answer submission
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = cards[index].answer
        if user_answer.strip().lower() == correct_answer.strip().lower():
            session['score'] += 1

        # Move to next question
        index += 1
        session['index'] = index

        # If no more questions, go to result page
        if index >= len(cards):
            return redirect(url_for('result'))

    return render_template('question.html', card=cards[index])

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(cards)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)

