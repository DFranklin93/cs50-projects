from cs50 import get_string
from sys import argv


def main():

    if len(argv) != 2:
        exit("Usage: python bleep.py infile")
        return 1

    # set the argument to a var of infile
    infile = argv[1]

    # set that to a var of open_infile in able to read said file
    open_infile = open(infile, 'r')

    # read said file line by line
    line_by_line = open_infile.readlines()

    # set an array for each of the words within the file
    # to be placed in
    bannedWords = []

    # go through each word within the file and
    # add it to the above empty array
    for words in line_by_line:
        # strip each word since \n is tagged on each word
        bannedWords.append(words.strip())
    # change the array into a list
    bannedWords = list(bannedWords)

    # get user input then lower it in order to check words later
    userInput = get_string("Input some banned word: ").lower()

    # take user's input and change from single string
    # to multiple strings
    token = userInput.split(' ')

    # For loop created based of length of token string
    for i in range(len(token)):
        # For loop created based of length of bannedWords
        for j in range(len(bannedWords)):
            # If a token is the same as a bannedWord replace it was ***
            if token[i] == bannedWords[j]:
                # Turn token into list in order to deal with each character
                token[i] = list(token[i])
                # Loops through length of bannedWord token
                for k in range(len(token[i])):
                    # Replaces each char with *
                    token[i][k] = '*'
                # Sticks the word back together
                token[i] = ''.join(token[i])
    # Sticks all tokens back together and capitalizes
    token = ' '.join(token).capitalize()

    print(token)
if __name__ == "__main__":
    main()
