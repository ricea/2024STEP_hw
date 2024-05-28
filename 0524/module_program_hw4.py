#! /usr/bin/python3
#define abs function
def abs(x):
    if x < 0:
        return -x
    else:
        return x

# define round function
def round(x):
    if x >= 0:
        if x - int(x) >= 0.5:
            return int(x) + 1
        else:
            return int(x)
    else:
        if x - int(x) <= -0.5:
            return int(x) - 1
        else:
            return int(x)

# chage to read negative number also
def read_number(line, index):
    number = 0
    is_negative = False
    if line[index] == '-':
        is_negative = True
        index += 1
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    if is_negative:
        number = -number
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_parenthesis_left(line, index):
    token = {'type': 'PARENTHESIS_LEFT'}
    return token, index + 1

def read_parenthesis_right(line, index):
    token = {'type': 'PARENTHESIS_RIGHT'}
    return token, index + 1

def create_number_token(number):
    token = {'type': 'NUMBER', 'number': number}
    return token

def create_plus_token():
    token = {'type': 'PLUS'}
    return token

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_parenthesis_left(line, index)
        elif line[index] == ')':
            (token, index) = read_parenthesis_right(line, index)
        elif line[index:index+3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index:index+3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index:index+5] == 'round':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# evaluate () function added abs, int, round
def evaluate_parentheses(tokens):
    new_tokens = tokens
    num_parentheses = sum(1 for token in tokens if token['type'] == 'PARENTHESIS_LEFT')
    
    # if there are no parentheses
    if num_parentheses == 0:
        return new_tokens

    while num_parentheses > 0:
        start_index = None
        end_index = None

        # find the innermost parentheses' indices
        for index, token in enumerate(new_tokens):
            if token['type'] == 'PARENTHESIS_LEFT':
                start_index = index
            elif token['type'] == 'PARENTHESIS_RIGHT':
                end_index = index
                break
        
        if start_index is not None and end_index is not None:
            inner_tokens = new_tokens[start_index + 1:end_index]
            evaluated_inner = evaluate(evaluate_mul_and_div(inner_tokens))
            # if outside of the parentheses are either abs, int, or round
            if start_index > 0 and (new_tokens[start_index - 1]['type'] == 'ABS' or new_tokens[start_index - 1]['type'] == 'INT' or new_tokens[start_index - 1]['type'] == 'ROUND'):
                if new_tokens[start_index - 1]['type'] == 'ABS':
                    evaluated_inner = abs(evaluated_inner)
                elif new_tokens[start_index - 1]['type'] == 'INT':
                    evaluated_inner = int(evaluated_inner)
                elif new_tokens[start_index - 1]['type'] == 'ROUND':
                    evaluated_inner = round(evaluated_inner)
                start_index -= 1
            if start_index == -1:
                start_index = 0
            new_tokens[start_index] = create_plus_token()
            new_tokens[start_index + 1] = create_number_token(evaluated_inner)
            new_tokens = new_tokens[:start_index + 2] + new_tokens[end_index + 1:]
            num_parentheses -= 1
        else:
            break
    return new_tokens

# calculates the multiplication and division first
def evaluate_mul_and_div(tokens):
    new_tokens = []
    paragraph = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens.append({'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                paragraph *= tokens[index]['number']
                if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                    token = create_number_token(paragraph)
                    plus_token = create_plus_token()
                    new_tokens.append(plus_token)
                    new_tokens.append(token)
            elif tokens[index - 1]['type'] == 'DIVIDE':
                paragraph /= tokens[index]['number']
                if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                    token = create_number_token(paragraph)
                    plus_token = create_plus_token()
                    new_tokens.append(plus_token)
                    new_tokens.append(token)
            elif tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS': # either + or -
                if index >=2 and tokens[index - 2]['type'] == 'MULTIPLY' or tokens[index - 2]['type'] == 'DIVIDE': # if there is a multiplication or division before the number
                    paragraph *= tokens[index]['number']
                    if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                        token = create_number_token(paragraph)
                        plus_token = create_plus_token()
                        new_tokens.append(plus_token)
                        new_tokens.append(token)
                else:
                    paragraph = tokens[index]['number']
                    if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                        new_tokens.extend(tokens[index - 1: index + 1])
            else:
                print('Invalid syntax in evaluate_mul_and_div')
                exit(1)
        index += 1
    return new_tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax in evaluate')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    tokens = evaluate_parentheses(tokens)
    tokens = evaluate_mul_and_div(tokens)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :) # added parentheses test
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2.1-3.0")
    test("2*4/2+1+2*1")
    test("2*4/2+1+2*1-1")
    test("((2+2)+1)")
    test("((2+2)*3)")
    test("((2+2)*3)+1")
    test("((2+2)*3)+1+1")
    test("abs(-1)")
    test("round(1.5)")
    test("int(1.5)")
    test("int(-1.6)")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4)))+1)")
    test("round(1.5)+int(1.5)")
    test("round(-1.5+int(1.5))*int(1.5)")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens = evaluate_parentheses(tokens)
    tokens_without_mul_and_div = evaluate_mul_and_div(tokens)
    print("tokens = %s" % tokens_without_mul_and_div)
    answer = evaluate(tokens_without_mul_and_div)
    print("answer = %f\n" % answer)