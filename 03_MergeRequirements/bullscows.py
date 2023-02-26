from typing import Tuple, List
import random
import argparse
import urllib.request
import urllib.error
import cowsay

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    cows = len(set(guess) & set(secret))
    bulls = 0
    for g, s in zip(guess, secret):
        if g == s:
            bulls += 1
    return bulls, cows


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows),
                        cow=random.choice(cowsay.list_cows())))


def ask(prompt: str, valid: List[str] = None) -> str:
    inp = input(cowsay.cowsay(prompt, cow=random.choice(cowsay.list_cows())))
    while valid is not None and inp not in valid:
        inp = input(cowsay.cowsay(prompt, cow=random.choice(cowsay.list_cows())))
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


def start_game(path_to_words: str, length: int) -> None:
    def process_str(s):
        if isinstance(s, str):
            return s.strip()
        else:
            return s.decode('utf-8').strip()

    try:
        if path_to_words.startswith("https://"):
            file = urllib.request.urlopen(path_to_words)
        else:
            file = open(path_to_words)
        words = list(filter(lambda x: len(x) == length, map(process_str, file.readlines())))

    except urllib.error.HTTPError:
        print("Wrong URL")
        return
    except FileNotFoundError:
        print("Wrong filepath")
        return
    except BaseException:
        print("Something is wrong")
        return
    
    print(f"Won with {gameplay(ask, inform, words)} attempts")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Bulls and cows game")
    parser.add_argument("path_to_words", type=str)
    parser.add_argument("length", type=int, default=5, nargs="?")
    args = parser.parse_args()

    start_game(args.path_to_words, args.length)
