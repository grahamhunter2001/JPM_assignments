def is_new_word(current_char, prev_char):
    if (current_char.islower() and prev_char.isupper()) or prev_char == "":
        return True
    else:
        return False


def func(inp_str):
    words = []
    prev_char = ""
    word = ""
    for char in inp_str:
        if is_new_word(char, prev_char):
            if len(word)>0: words.append(word[:len(word) - 1])
            word = prev_char + char
        else:
            word += char
        prev_char = char
    words.append(word[:len(word)])
    print('_'.join(words))

func("AAAABbbb")