import operator
import sys

def change(ops:str,value:str)->str: return str(-int(value))

def evaluate(ops:str,first = None,second = None)->str:
    op = {"+":operator.__add__,
          "-":operator.__sub__,
          "*":operator.__mul__,
          "/":operator.__div__,
          "change":change(ops,first)}
    if ops == "change":
        return op[ops]
    return str(op[ops](int(first),int(second)))


def calc(expression):
    ops = {"+":1, "-":1, "*" : 2, "/": 2, "(":4, ")":4,"change":3}
    simp = "+-"
    op_stack = []
    exp = expression.replace(" ","")

    print(exp)
    length = len(exp)
    postfix = []
    number = ""
    i = 0

    #---------------------------------------------------------------------------#
    # -------------------------infix to postfix conversion----------------------#
    #---------------------------------------------------------------------------#
    while(i < length):
        
        if exp[i].isdigit():
            number = exp[i]
            if i <= length - 1:
                for y in range(i + 1, length):
                    if not exp[y].isdigit():
                        i = y-1
                        break
                    number += exp[y]
                
                postfix.append(number)
                i += 1

        elif exp[i] in simp and i >= 0:
            check = exp[i] if i == 0 else exp[i-1] #checking for the postion of the numeber if its negative
            if check in ops:
                if i != 0 and exp[i-1] in ops and exp[i+1] == "(":
                    op_stack.append("change")
                    i += 1
                elif check != ")":
                    number = exp[i]
                    for x in range(i+1,length):
                        if not exp[x] in ops:
                            number += exp[x]
                        else:
                            break
                    postfix.append(number)
                    
                    i = x
        

        if i < length and exp[i] in ops:
            print("opstack: ",op_stack)
            print("my operator is", ops[exp[i]] )
            if exp[i] != ")": 
                if op_stack:
                    for m in range(len(op_stack)-1,-1,-1):
                        if not op_stack[m] in ["change", "("] and  ops[op_stack[m]] >= ops[exp[i]]:
                            print("op_stack:",op_stack)
                            print("popping here", op_stack[-1],"to", exp[i])
                            postfix.append(op_stack.pop())
                        else:
                            break
                op_stack.append(exp[i])
            
            elif exp[i] == ")":
                s = len(op_stack)-1
                print("s is", s)
                while op_stack[s] != "(":

                    print("s here is:", s)
                    postfix.append(op_stack.pop())
                    s -= 1
                op_stack.pop()
        i += 1
        print("postfix: ",postfix)

    #clearing the remaining opertors in the op_stack
    while op_stack:
        postfix.append(op_stack.pop())
        
    print("postfix:",postfix)
    print("op_stack:",op_stack)
    return postfix  #for test
    #---------------------------------------------------------------------------#
    # ----------------------------postfix-evalutate-----------------------------#
    #---------------------------------------------------------------------------#
    

def test():
    assert calc("-53 - -74 - 73 / -88 + 94 / 71 / 64 - 48") == ['-53','-74','-','73','-88','/','-','94','71','/','64','/','+','48','-']
    assert calc("2 + -2") == ['2','-2','+']
    assert calc("(((10)))") == ['10']
    assert calc("10- 2- -5") == ['10','2','-','-5','-']

    assert calc("1 + 2 * 3 * (5 - (3 - 1)) - 8") == ['1', '2', '3', '*', '5', '3', '1', '-', '-', '*', '+', '8', '-']

try:
    test()
    print("------------------All test ran successfully------------")
except:
    print("-------------------There is error----------------------")
'''
(((10)))
2 + -2
1 + 2 * 3 * (5 - (3 - 1)) - 8
10- 2- -5
-7 * -(6 / 3)
(-59) - (-62 + 100 + (64)) + (29 - ((((-16 - 90)))) + -3)
-53 - -74 - 73 / -88 + 94 / 71 / 64 - 48
3 -(-1)
'''