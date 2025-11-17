import os
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Flashcard:
    question: str
    answer: str
    times_seen: int = 0
    times_correct: int = 0

    @property
    def mistakes(self) -> int:
        """How many times this card has been missed."""
        return max(0, self.times_seen - self.times_correct)


def load_questions_from_file(path: str) -> List[Flashcard]:
    """
    Load Q&A pairs from a plain text file.

    Expected format:
      - Each question is on its own line and ends with a '?'
      - The line immediately following a question is its answer.
      - Blank lines are allowed and ignored.
    """
    cards: List[Flashcard] = []

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


def manual_entry() -> List[Flashcard]:
    """
    Allow the user to manually enter questions and answers.
    """
    print("\n--- Manual Question Entry ---")
    print("Enter your questions and answers.")
    print("Press Enter on an empty question to finish.\n")

    cards: List[Flashcard] = []

    while True:
        q = input("Question (leave blank to finish): ").strip()
        if not q:
            break

        # Ensure the question ends with '?'
        if not q.endswith("?"):
            q += "?"

        a = input("Answer: ").strip()
        cards.append(Flashcard(question=q, answer=a))
        print("Added!\n")

    if not cards:
        print("No questions were added.")
    else:
        print(f"{len(cards)} questions added.\n")

    return cards


def run_quiz(cards: List[Flashcard]) -> None:
    """
    Ask each question in random order, get user answers,
    give immediate feedback, and show a final score.
    """
    if not cards:
        print("No questions available to quiz on.")
        return

    # Make a shuffled copy of the questions
    questions = cards.copy()
    random.shuffle(questions)

    print("\n--- Quiz Started ---")
    print("Type your answer and press Enter.")
    print("Type 'quit' to exit early.\n")

    total = 0
    correct = 0

    for card in questions:
        print(f"Question: {card.question}")
        user_answer = input("Your answer: ").strip()

        if user_answer.lower() in {"quit", "q", "exit"}:
            print("\nEnding quiz early.\n")
            break

        total += 1
        card.times_seen += 1

        if user_answer.strip().lower() == card.answer.strip().lower():
            print("✅ Correct!\n")
            correct += 1
            card.times_correct += 1
        else:
            print("❌ Incorrect.")
            print(f"   Correct answer: {card.answer}\n")

    if total == 0:
        print("No questions were answered.")
        return

    score_percent = (correct / total) * 100
    print("----- Quiz Summary -----")
    print(f"Questions answered: {total}")
    print(f"Correct answers:   {correct}")
    print(f"Score:             {score_percent:.1f}%\n")


def main():
    """Menu that lets user choose how to load questions."""

    print("How would you like to load your questions?")
    print("1) Load from questions.txt")
    print("2) Enter questions manually")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "questions.txt")

        try:
            cards = load_questions_from_file(path)
        except FileNotFoundError:
            print(f"Could not find file: {path}")
            return

    elif choice == "2":
        cards = manual_entry()

    else:
        print("Invalid choice.")
        return

    if not cards:
        print("No questions to display or quiz on.")
        return

    # Run the quiz on the loaded/entered cards
    run_quiz(cards)


if __name__ == "__main__":
    main()
