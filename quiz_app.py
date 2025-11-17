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

    Example file:

        What is the capital of France?
        Paris

        What is 2 + 2?
        4
    """
    cards: List[Flashcard] = []

    # Read all lines and strip whitespace
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    i = 0
    while i < len(lines):
        line = lines[i]

        # If this line looks like a question
        if line.endswith("?"):
            question = line
            answer = ""

            # Assume the next line is the answer (if it exists)
            if i + 1 < len(lines):
                answer = lines[i + 1].strip()
                i += 1  # skip the answer line in the next loop

            cards.append(Flashcard(question=question, answer=answer))

        i += 1

    return cards


def main():
    """Temporary test for file loading."""
    path = "questions.txt"
    try:
        cards = load_questions_from_file(path)
    except FileNotFoundError:
        print(f"Could not find file: {path}")
        return

    if not cards:
        print("No questions were found. Check your file format.")
        return

    print(f"Loaded {len(cards)} questions:\n")
    for idx, card in enumerate(cards, start=1):
        print(f"{idx}. Q: {card.question}")
        print(f"   A: {card.answer}\n")


if __name__ == "__main__":
    main()
