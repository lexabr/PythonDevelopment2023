from typing import Tuple

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    cows = len(set(guess) & set(secret))
    bulls = 0
    for g, s in zip(guess, secret):
        if g == s:
            bulls += 1
    return bulls, cows


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
