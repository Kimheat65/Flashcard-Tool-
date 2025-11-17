from dataclasses import dataclass

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
