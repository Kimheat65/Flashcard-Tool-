"""
OIM3640 Final Project - Q&A Practice Tool

This program lets users practice custom question-and-answer sets.
Users can:
- Load questions from a text file (questions.txt)
- Enter questions manually
- Take randomized quizzes with instant feedback
- Get repeated practice on missed questions
- Track performance over multiple rounds and sessions
- Automatically log all manually entered questions to a master file
- Load and quiz on all manually logged questions (manual_questions_log.txt)
"""

import os
import json
import random
from dataclasses import dataclass
from typing import List, Dict, Any

# Base directory (folder where this file lives)
BASE_DIR = os.path.dirname(__file__)

# File to store quiz performance results
RESULTS_FILE = os.path.join(BASE_DIR, "quiz_results.json")

# File to store ALL manually entered questions (append-only log)
MANUAL_LOG_FILE = os.path.join(BASE_DIR, "manual_questions_log.txt")


# ---------- Data model ----------

@dataclass
class Flashcard:
    question: str
    answer: str
    times_seen: int = 0
    times_correct: int = 0

    @property
    def mistakes(self) -> int:
        """How many times this card has been missed overall."""
        return max(0, self.times_seen - self.times_correct)


# ---------- Loading & saving questions ----------

def load_questions_from_file(path: str) -> List[Flashcard]:
    """
    Load Q&A pairs from a plain text file.

    Expected format:
      - Each question is on its own line and ends with a '?'
      - The line immediately following a question is its answer.
      - Blank lines are allowed and ignored.
    """
    cards: List[Flashcard] = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"File does not exist: {path}")

    # Read file lines and strip whitespace
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    # Remove blank lines
    lines = [line for line in lines if line]

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.endswith("?"):
            question = line
            answer = ""

            # The next line should be the answer
            if i + 1 < len(lines):
                answer = lines[i + 1].strip()
                i += 1  # skip answer line

            cards.append(Flashcard(question=question, answer=answer))

        i += 1

    return cards


def append_cards_to_manual_log(cards: List[Flashcard]) -> None:
    """
    Append a list of Flashcards to the master manual log file
    in the same format used by load_questions_from_file:

        Question?
        Answer

    (blank line between pairs)

    This file will grow over time as more users manually enter questions.
    """
    with open(MANUAL_LOG_FILE, "a", encoding="utf-8") as f:
        for card in cards:
            f.write(card.question.strip() + "\n")
            f.write(card.answer.strip() + "\n\n")

    print(f"Logged {len(cards)} manually entered questions to {MANUAL_LOG_FILE}")


def manual_entry() -> List[Flashcard]:
    """
    Allow the user to manually enter questions and answers.
    After each Q/A pair, ask if they want to add another.
    Automatically logs all manually entered questions to MANUAL_LOG_FILE.
    """
    print("\n--- Manual Question Entry ---")
    print("Enter your questions and answers.")
    print("After each question, you'll be asked if you want to add another.\n")

    cards: List[Flashcard] = []

    while True:
        q = input("Question (or press Enter to stop): ").strip()
        if not q:
            # user pressed Enter with no text -> stop adding
            break

        # Ensure the question ends with '?'
        if not q.endswith("?"):
            q += "?"

        a = input("Answer: ").strip()
        cards.append(Flashcard(question=q, answer=a))
        print("Added!\n")

        cont = input("Do you want to add another question? (y/n): ").strip().lower()
        if cont != "y":
            break

    if not cards:
        print("No questions were added.")
        return cards

    print(f"{len(cards)} questions added.\n")

    # Always log these questions to the master manual log file
    append_cards_to_manual_log(cards)

    return cards


# ---------- Persistence: saving & loading results ----------

def load_results() -> Dict[str, Any]:
    """Load past quiz results from disk if available."""
    if not os.path.exists(RESULTS_FILE):
        return {}

    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_results(all_results: Dict[str, Any]) -> None:
    """Save all quiz results to disk."""
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)


def record_session_result(
    quiz_name: str,
    round_number: int,
    total_questions: int,
    correct_answers: int,
    score_percent: float,
) -> None:
    """Append a new session result for this quiz."""
    all_results = load_results()
    session_data = {
        "round": round_number,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percent": score_percent,
    }
    all_results.setdefault(quiz_name, []).append(session_data)
    save_results(all_results)


def show_previous_results(quiz_name: str) -> None:
    """Print previous results for this quiz if they exist."""
    all_results = load_results()
    sessions = all_results.get(quiz_name)
    if not sessions:
        return

    print("\nPrevious sessions for this quiz:")
    for s in sessions:
        print(
            f"  Round {s['round']}: "
            f"{s['correct_answers']}/{s['total_questions']} "
            f"({s['score_percent']:.1f}%)"
        )
    print()


# ---------- Adaptive weighting ----------

def build_question_pool(cards: List[Flashcard]) -> List[Flashcard]:
    """
    Build a pool of questions for a round.

    - Each question appears at least once.
    - Questions with more mistakes appear extra times (up to 3 extra),
      which increases the chance they are asked again in this round.
    """
    pool: List[Flashcard] = []
    for card in cards:
        copies = 1
        if card.mistakes > 0:
            copies += min(card.mistakes, 3)
        pool.extend([card] * copies)

    random.shuffle(pool)
    return pool


# ---------- Quiz session with 80% rule & adaptive practice ----------

def run_quiz_session(cards: List[Flashcard], quiz_name: str) -> None:
    if not cards:
        print("No questions available. Exiting.")
        return

    show_previous_results(quiz_name)

    round_number = 1

    while True:
        print("\n==============================")
        print(f"        QUIZ ROUND {round_number}")
        print("==============================")

        pool = build_question_pool(cards)

        total_asked = 0
        correct_this_round = 0
        incorrect_details = []

        for card in pool:
            print(f"\nQuestion: {card.question}")
            user_answer = input("Your answer (or type 'quit' to stop): ").strip()

            if user_answer.lower() in {"quit", "q", "exit"}:
                print("\nEnding this round early.")
                if total_asked == 0:
                    print("No questions were answered. Goodbye!")
                    return
                break

            card.times_seen += 1
            total_asked += 1

            if user_answer.strip().lower() == card.answer.strip().lower():
                print("✅ Correct!")
                card.times_correct += 1
                correct_this_round += 1
            else:
                print("❌ Incorrect.")
                print(f"   Correct answer: {card.answer}")
                incorrect_details.append((card, user_answer))

        if total_asked == 0:
            print("No questions were answered. Goodbye!")
            return

        score_percent = (correct_this_round / total_asked) * 100

        print("\n---------- Round Summary ----------")
        print(f"Questions answered: {total_asked}")
        print(f"Correct answers:   {correct_this_round}")
        print(f"Score:             {score_percent:.1f}%")

        if incorrect_details:
            print("\nQuestions you missed this round:")
            for card, user_answer in incorrect_details:
                print(f"- {card.question}")
                print(f"  Your answer:  {user_answer}")
                print(f"  Correct:      {card.answer}")
        else:
            print("\nPerfect round! 🎉 Great job!")

        # Save this round's result
        record_session_result(
            quiz_name=quiz_name,
            round_number=round_number,
            total_questions=total_asked,
            correct_answers=correct_this_round,
            score_percent=score_percent,
        )

        # 80% rule
        if score_percent >= 80.0:
            print("\nYou scored at least 80%. Nice work! 🎯")
            break
        else:
            print(
                "\nYour score is below 80%. "
                "We'll prioritize the questions you missed in the next round."
            )
            cont = input("Press Enter to continue or type 'q' to quit: ").strip().lower()
            if cont == "q":
                print("Okay, stopping here. Keep practicing next time!")
                break

        round_number += 1


# ---------- Main menu (looping) ----------

def main():
    """Looping menu to load questions and start quizzes."""

    # Ask once per run which quiz name to use for saving results
    quiz_name = input(
        "Enter a name for this quiz (e.g., 'exam1', 'bio_midterm'): "
    ).strip() or "default_quiz"

    while True:
        print("\nHow would you like to load your questions?")
        print("1) Load from questions.txt")
        print("2) Enter questions manually")
        print("3) Load from manual_questions_log.txt")
        print("q) Quit")
        choice = input("Choose 1, 2, 3, or q: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        cards: List[Flashcard] = []

        if choice == "1":
            path = os.path.join(BASE_DIR, "questions.txt")
            try:
                cards = load_questions_from_file(path)
            except FileNotFoundError:
                print(f"Could not find file: {path}")
                continue

        elif choice == "2":
            # Manual entry (always logged)
            cards = manual_entry()

            if not cards:
                print("No questions entered. Returning to main menu.")
                continue

            # Ask what to do next
            print("\nWhat would you like to do next?")
            print("1) Start a quiz with these questions now")
            print("2) Return to main menu (questions are still saved to the manual log)")
            sub = input("Choose 1 or 2: ").strip()

            if sub == "2":
                # Do not quiz now; loop back to main menu
                cards = []
                print("Returning to main menu...")
                continue
            elif sub != "1":
                print("Invalid choice. Returning to main menu.")
                cards = []
                continue

            # If sub == "1", we keep 'cards' and fall through to run_quiz_session

        elif choice == "3":
            path = MANUAL_LOG_FILE
            if not os.path.exists(path):
                print(
                    f"No manual log file found at {path}. "
                    "Try entering questions manually first (option 2)."
                )
                continue
            try:
                cards = load_questions_from_file(path)
            except FileNotFoundError:
                print(f"Could not find file: {path}")
                continue

        else:
            print("Invalid choice. Please choose 1, 2, 3, or q.")
            continue

        if not cards:
            print("No questions to quiz on.")
            continue

        # Run the full quiz session (with 80% rule + adaptive weighting)
        run_quiz_session(cards, quiz_name)

        # After a quiz, ask if they want to go back to the main menu
        again = input(
            "\nReturn to the main menu for another action? (y/n): "
        ).strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
