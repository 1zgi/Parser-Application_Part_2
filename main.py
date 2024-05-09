class Node:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.leftChild = left
        self.rightChild = right


error = False
next_token = '%'


def lex():
    global next_token
    with open("input.txt", "r") as file:
        while True:
            next_char = file.read(1)
            if not next_char:
                next_token = '$'
                break
            if next_char.strip():
                next_token = next_char
                break


def unconsumed_input():
    with open("input.txt", "r") as file:
        return file.read()


def main():
    global error, next_token
    theTree = G()
    if not error:
        printTree(theTree)
        value = evaluate(theTree)
        print("The value is", value)
    else:
        print("input not parsed correctly")


def G():
    global error, next_token
    lex()
    print("G -> E")
    tree = E()
    if next_token == '$' and not error:
        print("success")
        return tree
    else:
        print("failure: unconsumed input=", unconsumed_input())
        return None


def E():
    global error, next_token
    if error:
        return None
    print("E -> T R")
    temp = T()
    return R(temp)


def R(tree):
    global error, next_token
    if error:
        return None
    temp1, temp2 = None, None
    if next_token == '+':
        print("R -> + T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('+', tree, temp2)
    elif next_token == '-':
        print("R -> - T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('-', tree, temp2)
    else:
        print("R->e")
        return tree


def T():
    global error
    if error:
        return None
    print(" T -> F S")
    temp = F()
    return S(temp)


def S(tree):
    global error, next_token
    if error:
        return None
    temp1, temp2 = None, None
    if next_token == '*':
        print("S -> * F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('*', tree, temp2)
    elif next_token == '/':
        print("S -> / F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('/', tree, temp2)
    else:
        print("S -> e")
        return tree


def F():
    global error, next_token
    if error:
        return None
    temp = None
    if next_token == '(':
        print("F->( E )")
        lex()
        temp = E()
        if next_token == ')':
            lex()
            return temp
        else:
            error = True
            print("error: unexpected token ", next_token)
            print("unconsumed_input ", unconsumed_input())
            return None
    elif next_token in ['a', 'b', 'c', 'd']:
        print("F->M")
        return M()
    elif next_token in ['0', '1', '2', '3']:
        print("F->N")
        return N()
    else:
        error = True
        print("error: unexpected token ", next_token)
        print("unconsumed_input ", unconsumed_input())
        return None


def M():
    global error, next_token
    prev_token = next_token
    if error:
        return None
    if next_token in ['a', 'b', 'c', 'd']:
        print("M->", next_token)
        lex()
        return Node(prev_token)
    else:
        error = True
        print("error: unexpected token ", next_token)
        print("unconsumed_input ", unconsumed_input())
        return None


def N():
    global error, next_token
    prev_token = next_token
    if error:
        return None
    if next_token in ['0', '1', '2', '3']:
        print("N->", next_token)
        lex()
        return Node(prev_token)
    else:
        error = True
        print("error: unexpected token ", next_token)
        print("unconsumed_input ", unconsumed_input())
        return None


def printTree(tree):
    if tree is None:
        return
    printTree(tree.leftChild)
    printTree(tree.rightChild)
    print(tree.symbol, end=' ')


def evaluate(tree):
    if tree is None:
        return -1
    if tree.symbol == 'a':
        return 10
    elif tree.symbol == 'b':
        return 20
    elif tree.symbol == 'c':
        return 30
    elif tree.symbol == 'd':
        return 40
    elif tree.symbol in ['0', '1', '2', '3']:
        return int(tree.symbol)
    elif tree.symbol == '+':
        return evaluate(tree.leftChild) + evaluate(tree.rightChild)
    elif tree.symbol == '-':
        return evaluate(tree.leftChild) - evaluate(tree.rightChild)
    elif tree.symbol == '*':
        return evaluate(tree.leftChild) * evaluate(tree.rightChild)
    elif tree.symbol == '/':
        return evaluate(tree.leftChild) / evaluate(tree.rightChild)


if __name__ == "__main__":
    main()
