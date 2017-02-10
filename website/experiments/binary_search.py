
ALPHABET = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
            'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22,
            'x': 23, 'y': 24, 'z': 25, ' ': -1}


def numeric_binary_search(num, array):

    low = 0
    high = len(array) - 1
    idx = None

    while low <= high:

        mid = (high + low) / 2
        print 'high: {}, low: {}, array[{}]={}'.format(high, low, mid, array[mid])

        if array[mid] == num:
            idx = mid
            break
        elif array[mid] > num:
            high = mid - 1
        elif array[mid] < num:
            low = mid + 1

    return idx


def letter_binary_search(letter, array):

    low = 0
    high = len(array) - 1
    idx = None
    letter_num = ALPHABET.get(letter)

    if letter_num is None:
        return None

    while low <= high:

        mid = (high + low) / 2
        print 'high: {}, low: {}, array[{}]={}'.format(high, low, mid, array[mid])

        if ALPHABET.get(array[mid]) == letter_num:
            idx = mid
            break
        elif ALPHABET.get(array[mid]) > letter_num:
            high = mid - 1
        elif ALPHABET.get(array[mid]) < letter_num:
            low = mid + 1

    return idx


def string_binary_search(word, array):

    low = 0
    high = len(array) - 1
    idx = None

    while low <= high:

        mid = (low + high) / 2
        print 'high: {}, low: {}, array[{}]={}'.format(high, low, mid, array[mid])

        if array[mid] == word:
            idx = mid
            break
        else:
            for i, letter in enumerate(word):
                if len(array[mid]) < i + 1:
                    # assumes shorter words come first alphabetically: if search word is longer than mid word, move up
                    low = mid + 1
                    break
                lookup_letter_num = ALPHABET[array[mid][i]]
                letter_num = ALPHABET[letter]
                if lookup_letter_num > letter_num:
                    high = mid - 1
                    break
                elif lookup_letter_num < letter_num:
                    low = mid + 1
                    break
            else:
                # if made it through for loop without a break, it's probably b/c the word is too short
                # assumes shorter words come first alphabetically
                high = mid - 1

    return idx

if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]
    #location = numeric_binary_search(14, test)
    letter_test = ['a', 'e', 'g', 'h', 'i', 'l', 'm', 'n', 'r']
    #location = letter_binary_search('e', letter_test)
    words_test = ['apple', 'bananas', 'erin', 'erin is cool', 'llama', 'llamas', 'rat', 'yoyo', 'zoo']
    location = string_binary_search('erin is cool', words_test)
    print location