#
#

def most_frequent_character(s):
    char_count = {}

    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    max_count = 0
    max_char = None
    for char, count in char_count.items():
        if count > max_count:
            max_count = count
            max_char = char

    return max_char

user_string = input("Enter a string: ")
result = most_frequent_character(user_string)
print(f"The most frequent character is: {result}")
