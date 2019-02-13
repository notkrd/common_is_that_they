import os
import random

import requests


def get_phr_books(phr, api_url='https://api.phrasefinder.io/'):
    r = requests.get(api_url, params={'corpus': 'eng-us', 'query': phr, 'topk': 1})
    return r


def phr_found(phr):
    resp = get_phr_books(phr).json()['phrases']
    if resp:
        return True
    else:
        return False


def read_2grams(ngrams_file='w2_.txt'):
    the_2grams = {}
    first_line = True
    active_w = ''
    with open(os.path.join(os.getcwd(), ngrams_file), encoding='ISO-8859-1') as ngfile:
        for line in ngfile:
            splitline = line.split()
            freq = splitline[0]
            w1 = splitline[1]
            w2 = splitline[2]
            if w1 in the_2grams:
                the_2grams[w1].append((freq, w2))
            else:
                if first_line:
                    first_line = False
                else:
                    the_2grams[active_w].sort()
                active_w = w1
                the_2grams[w1] = [(freq, w2)]
    return the_2grams


def next_word(words, dict_2grams, all_words):
    last_w = words[-1]
    last_3ws = words[-3:]
    if last_w in dict_2grams:
        candidates = [x[1] for x in dict_2grams[last_w]]
        for w in candidates:
            if phr_found(' '.join(last_3ws + [w])):
                pass
            else:
                return w
    return random.choice(all_words)


def make_commons(dict_2grams, all_words, words=["common","is","that","they"], max_words=30, dest_file="common_they.txt"):
    with open(os.path.join(os.getcwd(), dest_file), 'w+') as common_file:
        common_file.write(' '.join(words))
        num_words = len(words)
        while num_words <= max_words:
            try:
                next_w = next_word(words, dict_2grams, all_words)
            except Exception:
                return words
            if next_w:
                words.append(next_w)
                common_file.write(' ' + next_w)
                num_words += 1
            else:
                break
    return words


def main():
    all_2grams = read_2grams()
    all_words = list(all_2grams.keys())
    print(make_commons(all_2grams, all_words))


if __name__ == "__main__":
    main()
