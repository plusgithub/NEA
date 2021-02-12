from word2number import w2n

#w2n.word_to_num
OPERANDS = {
    "plus": '+',
    "minus": '-',
    "times": '*',
    "divided by": '/',
    "to the power of": '**',
    "over": '/',
    "multiplied by": '*'
}

def calculate(input):
    input2 = input.get_string().replace('?', '')
    for i in OPERANDS:
        input2 = input2.replace(i, OPERANDS[i])
    print(input2)
    for o in input2.split():
        try:
            input2 = input2.replace(o, w2n.word_to_num(o))
            print(input2)
        except:
            if (input2) == '+' or (input2) =='-' or (input2) == '*' or (input2) == '/':
                continue
            else:
                input2 = input2.replace(o, '')

    string = eval(input2)
    return string
