import operator
import sys

ops = {"+":1, "-":1, "*" : 2, "/": 2, "(":4, ")":4,"change":3}
def change(ops:str,value:str)->str: return str(-float(value))

def evaluate(ops:str,first = None,second = None)->str:
    op = {"+":operator.__add__,
          "-":operator.__sub__,
          "*":operator.__mul__,
          "/":operator.__truediv__,
          "change":change(ops,first)}
    if ops == "change":
        return op[ops]
    return str(op[ops](float(first),float(second)))


#---------------------------------------------------------------------------#
# ----------------------------postfix-evalutate-----------------------------#
#---------------------------------------------------------------------------#
def postFixEval(pf:list)->str:
        numbers_stack = []
        result = 0
        index = 0
        while index < len(pf):
            if pf[index].lstrip('-').isdigit():
                numbers_stack.append(pf[index])
            elif pf[index] in ops:                
                if pf[index] == "change":
                    result = evaluate(pf[index], numbers_stack[-1])
                else:
                    result = evaluate(pf[index],numbers_stack[-2],numbers_stack[-1])
                if pf[index] == "change":
                    del numbers_stack[-1:-2:-1]
                else:
                    del numbers_stack[-1:-3:-1]
                numbers_stack.append(result)
            index += 1
        return numbers_stack[0]

def calc(expression):
    simp = "+-"
    op_stack = []
    exp = expression.replace(" ","")
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
            print("index here is ", i)
            check = exp[i] if i == 0 else exp[i-1] #checking for the postion of the numeber if its negative
            print("check here is", check)
            if check in ops:
                if i == 0 and exp[i+1] == "(":
                    op_stack.append("change")
                    i+=1 

                elif not exp[i-1] == ")" and exp[i+1] == "(": #made changes here ----------------------------------------------> i != 0 and
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
                        if not op_stack[m] in ["change", "("] and ops[op_stack[m]] >= ops[exp[i]]:
                            postfix.append(op_stack.pop())
                        elif op_stack[m] == "change" and ops[op_stack[m]] >= ops[exp[i]]:
                            postfix.append(op_stack.pop())
                        else:
                            break
                op_stack.append(exp[i])
            
            elif exp[i] == ")":
                s = len(op_stack)-1
                while op_stack[s] != "(":
                    postfix.append(op_stack.pop())
                    s -= 1
                op_stack.pop()
        i += 1

    #clearing the remaining opertors in the op_stack
    while op_stack:
        postfix.append(op_stack.pop())

    return float(postFixEval(postfix))

def test():
    #assert calc("-53 - -74 - 73 / -88 + 94 / 71 / 64 - 48") == ['-53','-74','-','73','-88','/','-','94','71','/','64','/','+','48','-']
    #assert calc("2 + -2") == 0.0
    #assert calc("(((10)))") == 10.0
    #assert calc("10- 2- -5") == 13.0
    assert calc("-(-(-(-1)))") == 1.0
    #assert calc("(76)-(-50--51*-(95))*(69*-(((-(-43+-9))))/-58)") == 76.0
    assert calc("(-20)+(-22+-4*-(12))+(-31-(((-(57+-64))))*24)") == -193.0
    assert calc("-(-74)+(59-61*-(20))-(57+-(((-(30+-7))))*57)") == -15.0
    #assert calc("1 + 2 * 3 * (5 - (3 - 1)) - 8") == ['1', '2', '3', '*', '5', '3', '1', '-', '-', '*', '+', '8', '-']

try:
    test()
    print("------------------All test ran successfully------------")
except:
    print("-------------------There is an error----------------------")


'''
(-20)+(-22+-4*-(12))+(-31-(((-(57+-64))))*24)
(76)-(-50--51*-(95))*(69*-(((-(-43+-9))))/-58)
(((10)))
2 + -2
1 + 2 * 3 * (5 - (3 - 1)) - 8
10- 2- -5
-7 * -(6 / 3)
(-59) - (-62 + 100 + (64)) + (29 - ((((-16 - 90)))) + -3)
-53 - -74 - 73 / -88 + 94 / 71 / 64 - 48
3 -(-1)
'''
