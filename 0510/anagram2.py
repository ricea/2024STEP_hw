import sys
from collections import Counter
import os

def better_solution(random_word, dictionary):
    if random_word == "":
        print("Enter at least one letter")
        return -1
    if len(random_word) >= 30:
        print("Enter words with 1-30 letters.")
        return -1

    random_word_counter = Counter(random_word)
    print(random_word_counter)

    # check if the random word is a subset for each word in dictionary 
    ans = []
    for score, word in dictionary:
        letter_count = Counter(word)
        print(letter_count)
        is_subset = True
        for letter in letter_count:
            print(letter)
            if letter_count[letter] > random_word_counter[letter]:
                is_subset = False
                break
        if not is_subset:
            continue
        # print("append", word)
        ans.append((score, word))

    return ans

# altered better solution so that it will check the dictionary 
# from the largest score and if it finds a word it stops searching and returns at that point
def best_solution(random_word, dictionary):
    if random_word == "":
        print("Enter at least one letter")
        return -1
    if len(random_word) >= 10**9:
        print("Enter words with 1-10^9 letters.")
        return -1

    random_word_counter = Counter(random_word)
    print(random_word_counter)

    # check if the random word is a subset for each word in dictionary 
    ans = []
    for score, word in dictionary:
        letter_count = Counter(word)
        print(letter_count)
        is_subset = True
        for letter in letter_count:
            print(letter)
            if letter_count[letter] > random_word_counter[letter]:
                is_subset = False
                break
        if not is_subset:
            continue
        # print("append", word)
        ans.append((score, word))
        return ans

    return ans

def main():
    n = len(sys.argv)
    if n != 2:
        print("one word should be passed as file for anagram search")
    print(sys.argv[1])
    
    # adds the words in words.txt to a list and sorts from the highest score to the lowest
    file = open("words.txt", "r")
    dictionary = []
    for line in file.readlines():
        word = line.strip()
        score = calc_score(word)
        dictionary.append((score, line.strip()))
    dictionary = sorted(dictionary,reverse=True)

    words = []
    filename = sys.argv[1]
    file = open(filename, "r")
    for line in file.readlines():
        words.append(line.strip())
    print("words: ", words)

    final_score = 0

    output_filename = filename + "_output.txt"
    if os.path.exists(output_filename):
        os.remove(output_filename)

    for word in words:
        print(word)
        # ans = better_solution(word, dictionary)
        ans = best_solution(word, dictionary)
        if len(ans) == 0:
            f.write("not found\n")
        else:
            with open(output_filename, mode="a") as f:
                f.write(f"{ans[-1][0]}, {ans[-1][1]}\n")
            final_score += ans[-1][0]

    print(final_score)

def calc_score(word):
    score = 0
    for letter in word:
        if letter in ["a", "e", "h", "i", "n", "o", "r", "s", "t"]:
            score += 1
        elif letter in ["c", "d", "l", "m", "u"]:
            score += 2
        elif letter in ["b", "f", "g", "p", "v", "w", "y"]:
            score += 3
        elif letter in ["j", "k", "q", "x", "z"]:
            score += 4
        else:
            print("calc_score error: unknown letter in ", word)
            sys.exit(1)
    return score

## define the dictionary with the scores for each letter
# letter_scores = {
#     "a": 1, "e": 1, "h": 1, "i": 1, "n": 1, "o": 1, "r": 1, "s": 1, "t": 1,
#     "c": 2, "d": 2, "l": 2, "m": 2, "u": 2,
#     "b": 3, "f": 3, "g": 3, "p": 3, "v": 3, "w": 3, "y": 3,
#     "j": 4, "k": 4, "q": 4, "x": 4, "z": 4
# }

if __name__ == "__main__":
    main()