from typing import Tuple, List
import random
import argparse

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    cows = len(set(guess) & set(secret))
    bulls = 0
    for g, s in zip(guess, secret):
        if g == s:
            bulls += 1
    return bulls, cows


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def ask(prompt: str, valid: List[str] = None) -> str:
    inp = input(prompt)
    while valid is not None and inp not in valid:
        inp = input(prompt)
    return inp


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    hidden_word = random.choice(words)
    tries_cnt = 1

    while (inp := ask("Введите слово: ", words)) != hidden_word:
        bulls, cows = bullscows(inp, hidden_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        tries_cnt += 1
    bulls, cows = bullscows(inp, hidden_word)
    inform("Быки: {}, Коровы: {}", bulls, cows)

    return tries_cnt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Bulls and cows game")
    parser.add_argument("path_to_words", type=str)
    parser.add_argument("length", type=int, default=5, nargs="?")
    args = parser.parse_args()
