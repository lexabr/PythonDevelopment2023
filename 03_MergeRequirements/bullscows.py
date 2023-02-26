from typing import Tuple

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    cows = len(set(guess) & set(secret))
    bulls = 0
    for g, s in zip(guess, secret):
        if g == s:
            bulls += 1
    return bulls, cows
