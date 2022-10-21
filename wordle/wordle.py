import random
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Iterator, List, Optional

LEN = 5
N_SUGGESTIONS = 6


class GuessResult(Enum):
    GREEN = "g"
    YELLOW = "y"
    GREY = "x"


class Letter:
    def __init__(self):
        self.answer: Optional[str] = None
        self.cannot_be: set(str) = set()

    def good_guess(self, letter: str) -> bool:
        if self.answer:
            return letter == self.answer
        return letter not in self.cannot_be

    def __str__(self):
        return self.answer or "?"


class Word:

    DICT_PATH = Path("/usr/share/dict/american-english")

    def __init__(self):
        self.letters = [Letter() for i in range(LEN)]
        self.cannot_contain = set()
        self.must_contain = set()
        # Cannot random.choice from a set!
        unguessed = [
            w.upper()
            for w in self.DICT_PATH.read_text().splitlines()
            if len(w) == LEN and w.isalpha()
        ]
        random.shuffle(unguessed)
        self.unguessed = deque(unguessed)

    def guessed(self, guess: str, word_result: str) -> None:
        assert len(guess) == LEN
        assert len(word_result) == LEN
        # Convert to list of enums
        word_result: List[GuessResult] = [GuessResult(l) for l in word_result]
        for pos, (letter_guessed, result) in enumerate(zip(guess, word_result)):
            match result:
                case GuessResult.GREEN:
                    self.letters[pos].answer = letter_guessed
                    self.must_contain -= {letter_guessed}
                case GuessResult.YELLOW:
                    self.must_contain.add(letter_guessed)
                    self.cannot_contain -= {letter_guessed}
                    self.letters[pos].cannot_be.add(letter_guessed)
                case GuessResult.GREY:
                    self.cannot_contain.add(letter_guessed)
                    self.must_contain -= {letter_guessed}

    def good_guess(self, guess: str) -> tuple[bool, str]:
        if not len(guess) == LEN:
            return (False, f"Need {LEN} letters, got {len(guess)}")
        letters = {l for (pos, l) in enumerate(guess) if not self.letters[pos].answer}
        # letters = set(guess)
        if forbidden := letters & self.cannot_contain:
            return (False, f"cannot contain {forbidden}")
        if missing := self.must_contain - letters:
            return (False, f"must containt {missing}")
        for (pos, letter_guess) in enumerate(guess):
            if not self.letters[pos].good_guess(letter_guess):
                return (False, f"{letter_guess} wrong for position {pos}")
        return (True, "Go for it, good luck!")

    def suggest(self) -> Iterator[str]:
        yielded = 0
        while yielded < N_SUGGESTIONS:
            guess = self.unguessed.popleft()
            (good, reason) = self.good_guess(guess)
            if good:
                self.unguessed.append(guess)
                yielded += 1
                yield guess

    def __str__(self):
        return "".join(str(letter) for letter in self.letters)

    def report(self) -> str:
        return (
            f"{self}\n"
            f"Cannot contain: {', '.join(sorted(self.cannot_contain))}\n"
            f"Must contain: {', '.join(sorted(self.must_contain))}\n"
        )


def play() -> None:
    word = Word()
    while True:
        print(word.report())
        print(f"Suggestions: {' '.join(word.suggest())}")
        guessed = input("What is your guess? ").upper()
        if not guessed:
            print(f"Suggestions: {' '.join(word.suggest())}")
        good_guess = word.good_guess(guessed)
        print(good_guess[1])
        if good_guess[0]:
            result = input("What was the result? ").lower()
            word.guessed(guessed.upper(), result.lower())
