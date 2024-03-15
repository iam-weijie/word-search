import word_search

letter_list = input("Input a list of letters (with no space): ")

words = input("Input the words to search for (use - between the words): ")

print(word_search.word_search_main(letter_list, words))