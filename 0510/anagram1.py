import sys
# sys.setrecursionlimit(10000)

def better_solution(random_word, dictionary):
    if random_word == "":
        print("Enter at least one letter")
        return -1
    sorted_random_word = sorted(random_word)
    if len(sorted_random_word) >= 30:
        print("Enter words with 1-30 letters.")
        return -1
    print(sorted_random_word)

    new_dict = []
    for word in dictionary:
        new_dict.append((sorted(word), word))
    new_dict = sorted(new_dict)

    anagram = bin_search(sorted_random_word, new_dict, 0, len(new_dict))
    return anagram

def bin_search(sorted_word, sorted_dictionary, l, r):
    while l < r:
        m = (l + r) // 2
        # print(sorted_dictionary[m])
        if sorted_word < sorted_dictionary[m][0]:
            r = m - 1
        elif sorted_word == sorted_dictionary[m][0]:
            return sorted_dictionary[m][1]
        else:
            l = m + 1
    return -1

def main():
    n = len(sys.argv)
    if n != 2:
        print("one word should be passed as word for anagram search")
    print(sys.argv[1])
    
    file = open("words.txt", "r")
    dictionary = []
    for line in file.readlines():
        dictionary.append(line.strip())

    ans = better_solution(sys.argv[1], dictionary)

    if ans == -1:
        print("Nothing found")
    else: 
        print(ans)

if __name__ == "__main__":
    main()