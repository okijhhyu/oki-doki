import ply.yacc as yacc
from lexer import tokens

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def p_prog(p):
    '''prog : VARS dec_list OF stmt_list CF
            | VARS dec_list def_list OF stmt_list CF'''
    if len(p) == 6:
        p[0] = Node('prog', [p[2], p[4]])
    else:
        p[0] = Node('prog', [p[2], p[3], p[5]])

def p_def_list(p):
    '''def_list : def
               | def_list SC def'''
    if len(p) == 2:
        p[0] = Node('DEF', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_def(p):
    '''def : DEF ID OP dec_list CP OF stmt_list_def CF
            | DEF ID OP dec_list CP OF VARS dec_list stmt_list_def CF'''
    if len(p) == 9:
        p[0] = Node(p[2], [p[4], p[7]])
    else:
        p[0] = Node(p[2], [p[4], p[8], p[9]])

def p_defstmt(p):
    '''defstmt : ID OP args CP'''
    p[0] = Node(p[1], [p[3]])

def p_args(p):
    '''args : arg
            | args SC arg'''
    if len(p) == 2:
        p[0] = Node('args', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_arg(p):
    '''arg : ID
            | NUMBER_INT
            | NUMBER_REAL
            | OP exp CP'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_dec_list(p):
    '''dec_list : dec
               | dec_list SC dec'''
    if len(p) == 2:
        p[0] = Node('VAR', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_dec(p):
    '''dec : type DP OP id_list CP'''
    p[0] = Node('declare', [p[4], p[1]])

def p_type(p):
    '''type : INT
            | REAL
            | STRING'''
    p[0] = Node('type', [p[1]])

def p_id_list(p):
    '''id_list : ID
                | id_list CM ID'''
    if len(p) == 2:
        p[0] = Node('Id', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_list(p):
    '''stmt_list : stmt
                | stmt_list SC stmt'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt(p):
    '''stmt : prisv
            | print
            | while
            | if'''
    if len(p) == 2:
        p[0] = p[1]

def p_stmt_list_if(p):
    '''stmt_list_if : stmt_if
                | stmt_list_if SC stmt_if'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_if(p):
    '''stmt_if : prisv
            | print
            | while
            | if
            | CONTINUE
            | BREAK'''
    if len(p) == 2:
        p[0] = p[1]

def p_stmt_list_def(p):
    '''stmt_list_def : stmt_def
                | stmt_list_def SC stmt_def'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_def(p):
    '''stmt_def : prisv
            | print
            | while
            | if
            | return'''
    if len(p) == 2:
        p[0] = p[1]

def p_return(p):
    '''return : RETURN exp'''
    p[0] = Node(p[1], [p[2]])

def p_prisv(p):
    '''prisv : ID PRISV exp
                | ID PRISV STRING'''
    p[0] = Node('prisv', [p[1], p[3]])

def p_exp(p):
    '''exp : term
            | exp SUM term
            | exp SUB term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_term(p):
    '''term : factor
            | term MUL factor
            | term DIV factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_factor(p):
    '''factor : defstmt
            | ID
            | NUMBER_INT
            | NUMBER_REAL
            | OP exp CP'''
    if len(p) == 2:
        p[0] = p[1]
    else: p[0] = p[2]

def p_print(p):
    '''print : PRINT OP exp CP
                | PRINT OP STRING CP'''
    p[0] = Node('print', [p[3]])

def p_while(p):
    '''while : WHILE bool_exp OF stmt_list CF'''
    p[0] = Node('while', [p[2], p[4]])

def p_if(p):
    '''if : IF bool_exp OF stmt_list_if CF'''
    p[0] = Node('if', [p[2], p[4]])

def p_bool_exp(p):
    '''bool_exp : bool_exp OR bool_exp_term
                | bool_exp_term
                | NOT bool_exp
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_bool_exp_term(p):
    '''bool_exp_term : bool_exp_term AND bool
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_bool(p):
    '''bool : OP exp RAVNO exp CP
            | OP exp MORE exp CP
            | OP exp LESS exp CP'''
    p[0] = Node(p[3], [p[2], p[4]])

def p_error(p):
    print ('Unexpected token:', p)

f = open('program.txt', 'r')
text_input = f.read()
parser = yacc.yacc()
tree = parser.parse(text_input)
print(tree)
simtabs = []
tns = {}
functions = []
def is_float(string): #функцая определения что число с плавающей точкой
    try:
        float(string)
        if (string.isnumeric()):
            return False
        return True
    except ValueError:
        return False

def obhod(tree):
    if (type(tree) != Node):
        return
    elif (tree.type == 'DEF'):
        for j in tree.parts:
            if (len(j.parts) == 2):
                obhod_fun(j, j.type)
                functions.append(j.type)
            elif (len(j.parts) == 3):
                functions.append(j.type)
                for l in j.parts:
                    obhod_fun(l, j.type)
    elif (tree.type == 'declare'): #обход main , чтобы определить переменные
        for i in tree.parts[0].parts:
            simtabs.append((i, tree.parts[1].parts[0], 'main', 0))
        return
    else:
        for i in range(len(tree.parts)):
            obhod(tree.parts[i])

def obhod_fun(tree, fun): #обход функции чтобы определить переменные
    if (type(tree) != Node):
        return
    elif (tree.type == 'declare'):
        for i in tree.parts[0].parts:
            simtabs.append((i, tree.parts[1].parts[0], fun, 0))

    else:
        for i in range(len(tree.parts)):
            obhod_fun(tree.parts[i], fun)

obhod(tree)


def edit_simtabs(simtabs):
    index = 0
    new_simtabs1 = {}
    jo=''
    xy=0
    for i in simtabs:
        new_simtabs1[i[0]] = []
        if i[2] != 'main':
            if jo != i[2]:
                jo = i[2]
                xy=0
            jo = i[2]
            if (i[1]!='real'):
                new_simtabs1[i[0]].append('a' + str(xy))
            else:
                new_simtabs1[i[0]].append('f2'+str(xy))
            xy=xy+1
            new_simtabs1[i[0]].append(i[1])
            new_simtabs1[i[0]].append(i[2])
        else:
            if i[1]=='int' or i[1]=='str':
                new_simtabs1[i[0]].append('s' + str(index))
            else:
                new_simtabs1[i[0]].append('f1' + str(index))
            index=index+1
            new_simtabs1[i[0]].append(i[1])
            new_simtabs1[i[0]].append(i[2])
    return new_simtabs1

simtabs = edit_simtabs(simtabs)
for key in simtabs:
    print(key + ' : ')
    for i in simtabs[key]:
        print('\t' + str(i))


three_address_code = {'main': []}
j = 0
sample = 0
strok = 0

def check_scope(tree, name):
    if name.startswith('if') or (tree.isnumeric()) or (is_float(tree)):
        return True
    if (tree in simtabs.keys()):
        if (simtabs[tree][2] == name):
            return True
        else:
            print('Ошибка области видимости')
            print(tree + ' ' + name)
            return False
    else:
        print('Неверная переменная ' + tree + ' ' + name)
        return False

def global_obhod(tree):

    global strok
    if len(tree.parts) == 3:
        three_address_codeg(tree.parts[0], 'main')
        three_address_codeg(tree.parts[2], 'main')
        for funct in tree.parts[1].parts:
            three_address_code[funct.type] = []
            three_address_codeg(funct, funct.type)
    else:
        three_address_codeg(tree.parts[0], 'main')
        three_address_codeg(tree.parts[1], 'main')
    three_address_code['main'].append('GOTO END')

def function_obhod(tree, name):

    global strok
    if (type(tree) != Node):
        return
    elif (tree.type == 'declare'):
        for i in tree.parts[0].parts:
            three_address_code[name].append('Dec ' + i)
            strok = strok + 1
    elif (tree.type == 'prisv'):
        prisv_three_address_code(tree, name)
        three_address_code[name].append(':= ' + 't' + str(j - 1) + ' ' + tree.parts[0])
        strok = strok + 1
    else:
        for i in range(len(tree.parts)):
            function_obhod(tree.parts[i], name)

def three_address_codeg(tree, name):

    global j, sample, strok
    if (type(tree) != Node and (tree == 'break' or tree == 'continue')):
        three_address_code[name].append(tree)
    elif (type(tree) != Node):
        return
    elif (tree.type == 'prisv'):
        if (type(tree.parts[0]) == str and type(tree.parts[1]) == str):
            if (not check_scope(tree.parts[0], name)):
                return
            three_address_code[name].append(':= ' + tree.parts[1] + ' ' + tree.parts[0])
            strok = strok + 1
        else:
            prisv_three_address_code(tree, name)
            if (not check_scope(tree.parts[0], name)):
                return
            three_address_code[name].append(':= '+'t'+str(j-1)+ ' '+tree.parts[0])
            tns['t'+str(j-1)]=[]
            tns['t'+str(j-1)].append(tree.parts[0])
            print(tns)
            strok = strok + 1
            j = 0
    elif (tree.type == 'if'):
        expression_obhod(tree.parts[0], name)
        ime = 'if'+str(sample)
        sample = sample + 1
        three_address_code[ime] = []
        three_address_code[name].append('IF ' + 't' + str(j - 1) + ' GOTO ' + ime)
        three_address_codeg(tree.parts[1], ime)
        three_address_code[ime].append('GOTO after_if ' +  ime[2:])
        strok = strok + 1
    elif (tree.type == 'while'):
        expression_obhod(tree.parts[0], name)
        ime = 'if'+str(sample)
        sample = sample + 1
        three_address_code[ime] = []
        three_address_code[name].append('IF ' + 't' + str(j - 1) + ' GOTO ' + ime)
        three_address_codeg(tree.parts[1], ime)
        three_address_code[ime].append('GOTO after_while ' + ime[2:])
        strok = strok + 1
    elif (tree.type == 'return'):
        if (name == 'main'):
            print('ОШИБКА : у тебя return не в функции')
        else:
            prisv_three_address_code(tree.parts[0],name)
            three_address_code[name].append('return ' + 't'+str(j-1))
    elif (tree.type == 'print'):
        three_address_code[name].append('print ' + tree.parts[0])

    else:
        for i in range(len(tree.parts)):
            three_address_codeg(tree.parts[i], name)

def prisv_three_address_code(tree, name):
    global j, strok

    if type(tree) != Node:
        if (not check_scope(tree, name)):
            return
        return tree
    elif(tree.type == '*' or tree.type == '/' or tree.type == '+' or tree.type == '-'):

        operand = tree.type
        arg1 = prisv_three_address_code(tree.parts[0], name)
        arg2 = prisv_three_address_code(tree.parts[1], name)
        if arg1 == None and arg2 == None:
            arg1 = 't' + str(j - 2)
            arg2= 't' + str(j-1)
        if arg1 == None:
            arg1 = 't'+str(j-1)
            if not(str('t' + str(j-1)) in tns.keys()):
                tns['t' + str(j)] = []
            tns['t'+str(j-1)].append(arg2)
        if arg2 == None:
            arg2 = 't'+str(j-1)
            if not (str('t' + str(j-1)) in tns.keys()):
                tns['t' + str(j)] = []
            tns['t'+str(j-1)].append(arg1)
        temp = 't' + str(j)

        if not((temp) in tns.keys()):
            tns['t'+str(j)] = []
        tns['t'+str(j)].append(arg1)
        j = j+1
        three_address_code[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        strok = strok + 1
    elif (tree.type in functions):
        string = 'Call ' + tree.type + ' '
        for arg in tree.parts[0].parts:
            string = string + arg + ' '
        temp = 't' + str(j)
        j = j + 1
        string = string + temp
        three_address_code[name].append(string)

    else:
        for i in range(len(tree.parts)):
            prisv_three_address_code(tree.parts[i], name)

def expression_obhod(tree, name):

    global j, strok
    if type(tree) != Node:
        if (not check_scope(tree, name)):
            return
        return tree
    elif(tree.type == 'and' or tree.type == 'or'):
        operand = tree.type
        arg1 = expression_obhod(tree.parts[0], name)
        arg2 = expression_obhod(tree.parts[1], name)
        if arg1 == None and arg2 == None:
            arg1 = 't' + str(j - 2)
            arg2 = 't' + str(j - 1)

        if arg1 == None:
            arg1 = 't'+str(j-1)
            if (str('t'+str(j-1)) in tns.keys()):
                tns['t' + str(j - 1)].append(arg2)
            else:
                tns['t' + str(j-1)] = []
                tns['t' + str(j - 1)].append(arg2)
        if arg2 == None:
            arg2 = 't'+str(j-1)
            if (str('t'+str(j-1)) in tns.keys()):
                tns['t' + str(j-1)].append(arg1)
            else:
                tns['t' + str(j-1)] = []
                tns['t' + str(j-1)].append(arg1)
        temp = 't'+str(j)
        if (temp in tns.keys()):
            tns[temp].append(arg1)
        else:
            tns[temp]=[]
            tns['t' + str(j)].append(arg1)
        j = j+1
        if(str(operand))=='and':
            operand='or'
        else:
            operand = 'and'
        three_address_code[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        strok = strok + 1
    elif (tree.type == 'not'):
        operand = tree.type
        expression_obhod(tree.parts[0], name)
        arg = 't'+str(j-1)
        temp = 't' + str(j)
        j = j + 1
        three_address_code[name].append(str(operand) + ' ' + str(arg) + ' ' + str(temp))
        strok = strok + 1
    elif (tree.type == '>' or tree.type == '<' or tree.type == '='):
        operand = tree.type
        arg1 = prisv_three_address_code(tree.parts[0], name)
        arg2 = prisv_three_address_code(tree.parts[1], name)
        temp = 't' + str(j)
        if(temp in tns.keys()):
            tns[temp].append(arg1)
        else:
            tns[temp]=[]
            tns[temp].append(arg1)
        j = j + 1
        three_address_code[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
        strok = strok + 1
    else:
        for i in range(len(tree.parts)):
            expression_obhod(tree.parts[i], name)


global_obhod(tree)
for key in three_address_code:
    print(key + ' : ')
    for i in three_address_code[key]:
        print('\t' + str(i))



sho = simtabs
def asm(three_address_code, simtabs):


    sample = 0
    skip_count = 0
    flag = False
    f_bc = False
    str_count = 0
    data = ''
    f = open('out.s', 'w')
    data = data + '.data\n\ttrue: .byte 1\n\tfalse: .byte 0\n'
    f.write('.text\n')
    operation=0
    print(sho)
    for i in range (len(tns)):
        print (tns)
        if tns['t'+str(i)][0].isnumeric():
            tns['t'+str(i)]=[]
            tns['t' + str(i)] = 'i'
            simtabs['t' + str(i)] = []
            simtabs['t' + str(i)] = 'int'
        elif is_float(tns['t'+str(i)][0]):
            tns['t'+str(i)]=[]
            tns['t' + str(i)] = 'r'
            simtabs['t' + str(i)] = []
            simtabs['t' + str(i)] = 'real'
        elif tns['t'+str(i)][0] in simtabs and simtabs[tns['t'+str(i)][0]][1]=='int':
            tns['t' + str(i)] = []
            tns['t' + str(i)] = 'i'
            simtabs['t' + str(i)] = []
            simtabs['t' + str(i)] = 'int'
        elif tns['t'+str(i)][0] in simtabs and simtabs[tns['t'+str(i)][0]][1]=='real':
            tns['t'+str(i)]=[]
            tns['t' + str(i)] = 'r'
            simtabs['t' + str(i)] = []
            simtabs['t' + str(i)] = 'real'
        elif tns['t' + str(i)][0] in tns.keys():
            for ki in range (len(tns['t' + str(i)])):
                if tns['t' + str(i)][ki] in tns.keys():
                    u = 0
                elif tns['t' + str(i)][ki].isnumeric():
                    tns['t' + str(i)] = []
                    tns['t' + str(i)] = 'i'
                    simtabs['t' + str(i)] = []
                    simtabs['t' + str(i)] = 'int'
                elif is_float(tns['t' + str(i)][ki]):
                    tns['t' + str(i)] = []
                    tns['t' + str(i)] = 'r'
                    simtabs['t' + str(i)] = []
                    simtabs['t' + str(i)] = 'real'
                elif tns['t' + str(i)][ki] in simtabs.keys() and simtabs[tns['t' + str(i)][ki]][1] == 'int':
                    tns['t' + str(i)] = []
                    tns['t' + str(i)] = 'i'
                    simtabs['t' + str(i)] = []
                    simtabs['t' + str(i)] = 'i'
                elif tns['t' + str(i)][ki] in simtabs.keys() and simtabs[tns['t' + str(i)][ki]][1] == 'real':
                    tns['t' + str(i)] = []
                    tns['t' + str(i)] = 'r'
                    simtabs['t' + str(i)] = []
                    simtabs['t' + str(i)] = 'real'

    for i in range(len(tns)):

        for ki in range(len(tns['t' + str(i)])):
            if tns['t' + str(i)][ki] in tns.keys():
                tns['t' + str(i)]=tns[tns['t' + str(i)][ki]][0]
                break
    for lo in (sho):
        if lo==('t0') :
            break
        tns[lo]=[]
        tns[lo].append(lo)
    for label in three_address_code:
        f.write(label + ':\n')
        for com in three_address_code[label]:
            comex = com.split(' ')
            if ( comex[0] == ':=' ):
                if comex[1].isnumeric() and (simtabs[comex[2]][1] == 'int' or tns[comex[2]][0]=='i'):
                    if (comex[2] in tns.keys() and tns[comex[2]][0]!=comex[2]):
                        f.write('\tli $' + comex[2] + ', ' + comex[1] + '\n')
                    else:
                        f.write('\tli $' + simtabs[comex[2]][0] + ', ' + comex[1] + '\n')
                elif (is_float(comex[1]) and (simtabs[comex[2]][1] == 'real' or tns[comex[2]][0]=='r')):
                    if (comex[2] in tns.keys() and tns[comex[2]][0]!=comex[2]):
                        f.write('\tla $' + comex[2] + ', drob' + comex[1] + '\n')
                    else:
                        f.write('\tli.s $' + simtabs[comex[2]][0] + ', ' + comex[1] + '\n')
                elif comex[1].startswith('\"') and comex[1].endswith('\"') and (simtabs[comex[2]][1] == 'str'):
                    data = data + '\t' + comex[2] + ': .asciiz ' + comex[1] +'\n'

                elif(comex[1] in simtabs.keys() ):
                    if (comex[1] in tns.keys() and tns[comex[1]][0]!=comex[1]):
                        if (comex[2] in tns.keys() and tns[comex[2]][0]!=comex[2]):
                            if tns[comex[1]][0]=='r':

                                f.write('\tmov.s $f' +  comex[2][1:] + ', $f' + comex[1][1:] + '\n')
                            else:
                                f.write('\tmove $' + comex[2] + ', $f' + comex[1] + '\n')
                        elif comex[2] in simtabs.keys():
                            if tns[comex[1]][0] == 'r':
                                if (simtabs[comex[2]][1]=='int'):
                                    f.write('\tmove $' + simtabs[comex[2]][0] + ', $' + comex[1] + '\n')
                                else:
                                    f.write('\tmov.s $' + simtabs[comex[2]][0] + ', $f' + comex[1][1:] + '\n')
                            else:
                                if (simtabs[comex[2]][1]=='real'):
                                    f.write('\tmov.s $' + simtabs[comex[2]][0] + ', $f' + comex[1][1:] + '\n')
                                else:
                                    f.write('\tmove $' + simtabs[comex[2]][0] + ', $' + comex[1] + '\n')
                    elif (comex[1] in simtabs.keys()):
                        if (comex[2] in simtabs.keys()):
                            if simtabs[comex[2]][1] =='real':
                                f.write('\tmov.s $' + simtabs[comex[2]][0] + ', $' + simtabs[comex[1]][0] + '\n')
                            else:
                                f.write('\tmove $' + simtabs[comex[2]][0] + ', $' + simtabs[comex[1]][0] + '\n')



                else:
                    if (comex[2] in simtabs.keys()):
                        f.write('\tmove $' + comex[2] + ', $' + comex[1] + '\n')
                    elif (comex[2] in simtabs.keys()):
                        f.write('\tmove $' + simtabs[comex[2]][0] + ', $' + comex[1] +'\n')
                    else:
                        f.write('\tmove $' + comex[2] + ', $' + comex[1] + '\n')

            elif ( comex[0] == '*' ):
                            operation = operation+1
                            if comex[1].isnumeric():
                                if operation>2:
                                    f.write('\tli $t0, '+ comex[1] + '\n')
                                    arg1 = '$t0'
                                else:
                                    f.write('\tli $t4, '+ comex[1] + '\n')
                                    arg1 = '$t4'
                                if comex[2].isnumeric():
                                    if operation > 2:
                                        f.write('\tli $t1, ' + comex[2] + '\n')
                                        arg2 = '$t1'
                                    else:
                                        f.write('\tli $t5, ' + comex[2] + '\n')
                                        arg2 = '$t5'
                                    f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                    f.write('\tmflo $' + comex[3] + '\n')
                                elif comex[2] in simtabs.keys():
                                    if(comex[2] in simtabs and simtabs[comex[2]][1]=='int'):
                                        arg2 = '$'+ simtabs[comex[2]][0]
                                        f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                    elif (tns[comex[2]][0] == 'i'):
                                        arg2 = '$' + comex[2]
                                        f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                else:
                                    print('error неверный тип')
                                    return

                            elif comex[1] in simtabs.keys():

                                if ((comex[1] in simtabs and simtabs[comex[1]][1] == 'int')or(tns[comex[1]][0] == 'i' and comex[1] in tns)):
                                    if (comex[1] in simtabs and simtabs[comex[1]][1] == 'int'):
                                        arg1 = '$' + simtabs[comex[1]][0]
                                    else:
                                        arg1 = '' + comex[1][1:]

                                    if comex[2].isnumeric():
                                        f.write('\tli $t1, '+ comex[2]+ '\n')
                                        arg2 = '$t1'
                                        f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                    elif comex[2] in simtabs.keys():
                                        if (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                                            arg2 = '$' + simtabs[comex[2]][0]
                                            f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                            f.write('\tmflo $' + comex[3] + '\n')
                                        elif (tns[comex[2]][0] == 'i' and comex[2] in tns):
                                            arg2 = '$' + comex[2]
                                            f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                                            f.write('\tmflo $' + comex[3] + '\n')
                                elif (comex[1] in simtabs and simtabs[comex[1]][1] == 'real'):
                                    arg1 = '$' + simtabs[comex[1]][0]
                                else:
                                    chislo = comex[1][1:]
                                    arg1 = '$f' + str(chislo)
                                if is_float(comex[2]):
                                    f.write('\tli.s $f1, ' + comex[2] + '\n')
                                    arg2 = '$f1'
                                    f.write('\tmul.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                                    arg2 = '$' + simtabs[comex[2]][0]
                                    chislo = comex[3][1:]
                                    f.write('\tmul.s $f' + str(chislo) + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                                    chislo = comex[2][1:]
                                    arg2 = '$f' + str(chislo)
                                    f.write('\tmul.s $f' + comex[3][1:] + ', ' + arg1 +', $f' + str(comex[2][1:]) +  '\n')
                            elif is_float(comex[1]):
                                f.write('\tli.s $f0, ' + comex[1] + '\n')
                                arg1 = '$f0'
                                if is_float(comex[2]):
                                    f.write('\tli.s $f, ' + comex[2] + '\n')
                                    arg2 = '$f1'
                                    f.write('\tmul.s $f'+ comex[3][1:]+', '  + arg1 + ', ' + arg2 + '\n')
                                elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                                    arg2 = '$' + simtabs[comex[2]][0]
                                    f.write('\tmul.s $f'+ comex[3][1:]+', ' + arg1 + ', ' + arg2 + '\n')
                                elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                                    chislo = comex[2][1:]
                                    arg2 = '$f' +str(chislo)
                                    f.write('\tmul.s '+ comex[3][1:]+', '  + arg1 + ', ' + arg2 + '\n')
                            else:
                                print('error неверный тип')
                                return
            elif ( comex[0] == '/' ):
                            operation = operation + 1

                            if comex[1].isnumeric():
                                if operation > 2:
                                    f.write('\tli $t0, ' + comex[1] + '\n')
                                    arg1 = '$t0'
                                else:
                                    f.write('\tli $t4, ' + comex[1] + '\n')
                                    arg1 = '$t4'
                                if comex[2].isnumeric():
                                    if operation > 2:
                                        f.write('\tli $t1, ' + comex[2] + '\n')
                                        arg2 = '$t1'
                                    else:
                                        f.write('\tli $t5, ' + comex[2] + '\n')
                                        arg2 = '$t5'
                                    f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                    f.write('\tmflo $' + comex[3] + '\n')
                                elif comex[2] in simtabs.keys():
                                    if(comex[2] in simtabs and simtabs[comex[2]][1]=='int'):
                                        arg2 = '$'+simtabs[comex[2]][0]
                                        f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                    elif (tns[comex[2]][0] == 'i'):
                                        arg2 = '$' + comex[2]
                                        f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                else:
                                    print('error неверный тип')
                                    return
                            elif comex[1] in simtabs.keys():
                                if((comex[1] in simtabs and simtabs[comex[1]][1]=='int')or( tns[comex[1]][0]=='i' and comex[1] in tns)):
                                    if (comex[1] in simtabs and simtabs[comex[1]][1]=='int' ):
                                        arg1 = '$' + simtabs[comex[1]][0]
                                    else:
                                        arg1 = '$' + comex[1]
                                    if comex[2].isnumeric():
                                        f.write('\tli $t1, '+ comex[2]+ '\n')
                                        arg2 = '$t1'
                                        f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                    elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                                        arg2 = '$' + simtabs[comex[2]][0]
                                        f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                    elif (tns[comex[2]][0] == 'i' and comex[2] in tns):
                                        arg2 = '$' + comex[2]
                                        f.write('\tdiv ' + arg1 + ', ' + arg2 + '\n')
                                        f.write('\tmflo $' + comex[3] + '\n')
                                elif ((comex[1] in simtabs and simtabs[comex[1]][1] == 'real') or (tns[comex[1]][0] == 'r' and comex[1] in tns)):
                                    if (comex[1] in simtabs and simtabs[comex[1]][1] == 'real'):
                                        arg1 = '$' + simtabs[comex[1]][0]
                                    else:
                                        arg1 = '$f' + str(2)
                                    if is_float(comex[2]):
                                        f.write('\tli.s $f1, ' + comex[2] + '\n')
                                        arg2 = '$f1'
                                        f.write('\tdiv.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                                    elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                                        arg2 = '$' + simtabs[comex[2]][0]
                                        f.write('\tdiv.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                                    else:
                                        arg2 = '$f' + comex[2][1:]
                                        f.write('\tdiv.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif is_float(comex[1]):
                                if operation>2:
                                    f.write('\tli.s $f0, ' + comex[1] + '\n')
                                    arg1 = '$f0'
                                else:
                                    f.write('\tli.s $f4, ' + comex[1] + '\n')
                                    arg1 = '$f4'
                                if is_float(comex[2]):
                                    if operation > 2:
                                        f.write('\tli.s $f1, ' + comex[2] + '\n')
                                        arg2 = '$f0'
                                    else:
                                        f.write('\tli.s $f5, ' + comex[2] + '\n')
                                        arg2 = '$f4'
                                    f.write('\tdiv.s $f'  + comex[3][1:]+', '+ arg1 + ', ' + arg2 + '\n')
                                elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                                    arg2 = '$' + simtabs[comex[2]][0]
                                    f.write('\tdiv.s $f' + comex[3][1:]+', ' + arg1 + ', ' + arg2 + '\n')
                                elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                                    arg2 = '$f' + comex[2][1:]
                                    f.write('\tdiv.s $f' + comex[3][1:]+', ' + arg1 + ', ' + arg2 + '\n')
                                else:
                                    print('error неверный тип')
                                    return
            elif (comex[0] == '+'):
                operation = operation + 1
                if comex[1].isnumeric():
                    if operation > 2:
                        f.write('\tli $t0, ' + comex[1] + '\n')
                        arg1 = '$t0'
                    else:
                        f.write('\tli $t4, ' + comex[1] + '\n')
                        arg1 = '$t4'
                    if comex[2].isnumeric():
                        if operation > 2:
                            f.write('\tli $t1, ' + comex[2] + '\n')
                            arg1 = '$t1'
                        else:
                            f.write('\tli $t5, ' + comex[2] + '\n')
                            arg1 = '$t5'
                        f.write('\taddu $'+ comex[3] +', '+ arg1 + ', ' + arg2 + '\n')
                    elif comex[2] in simtabs.keys():
                        if (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\taddu $'+ comex[3] +', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'i'):
                            arg2 = '$' + comex[2]
                            f.write('\taddu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                elif comex[1] in simtabs.keys():
                    if ((comex[1] in simtabs and simtabs[comex[1]][1] == 'int') or (
                            tns[comex[1]][0] == 'i' and comex[1] in tns)):
                        if (comex[1] in simtabs and simtabs[comex[1]][1] == 'int'):
                            arg1 = '$' + simtabs[comex[1]][0]
                        else:
                            arg1 = '$' + comex[1]
                        if comex[2].isnumeric():
                            f.write('\tli $t1, ' + comex[2] + '\n')
                            arg2 = '$t1'
                            f.write('\taddu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\taddu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'i' and comex[2] in tns):
                            arg2 = '$' + comex[2]
                            f.write('\taddu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif ((comex[1] in simtabs and simtabs[comex[1]][1] == 'real') or (
                            tns[comex[1]][0] == 'r' and comex[1] in tns)):
                        if (comex[1] in simtabs and simtabs[comex[1]][1] == 'real'):
                            arg1 = '$' + simtabs[comex[1]][0]
                        else:
                            arg1 = '$f' + comex[1][1:]
                        if is_float(comex[2]):
                            f.write('\tli.s $f1, ' + comex[2] + '\n')
                            arg2 = '$f1'
                            f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                            arg2 = '$f' + comex[2][1:]
                            f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        else:
                            print('error неверный тип')
                            return
                elif is_float(comex[1]):
                    f.write('\tli.s $f0, ' + comex[1] + '\n')
                    arg1 = '$f0'
                    if is_float(comex[2]):
                        f.write('\tli.s $f1, ' + comex[2] + '\n')
                        arg2 = '$f1'
                        f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                        arg2 = '$' + simtabs[comex[2]][0]
                        f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                        arg2 = '$f' + comex[2][1:]
                        f.write('\tadd.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                    else:
                        print('error неверный тип')
                        return
            elif (comex[0] == '-'):
                operation = operation + 1
                if comex[1].isnumeric():

                    if operation > 2:
                        f.write('\tli $t0, ' + comex[1] + '\n')
                        arg1 = '$t0'
                    else:
                        f.write('\tli $t4, ' + comex[1] + '\n')
                        arg1 = '$t4'
                    if comex[2].isnumeric():
                        if operation > 2:
                            f.write('\tli $t1, ' + comex[2] + '\n')
                            arg1 = '$t1'
                        else:
                            f.write('\tli $t5, ' + comex[2] + '\n')
                            arg1 = '$t5'
                        f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif comex[2] in simtabs.keys():
                        if (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'i'):
                            arg2 = '$' + comex[2]
                            f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                    else:
                        print('error неверный тип')
                        return
                elif comex[1] in simtabs.keys():

                    if ((comex[1] in simtabs and simtabs[comex[1]][1] == 'int') or (
                            tns[comex[1]][0] == 'i' and comex[1] in tns)):
                        if (comex[1] in simtabs and simtabs[comex[1]][1] == 'int'):
                            arg1 = '$' + simtabs[comex[1]][0]
                        else:
                            arg1 = '$' + comex[1]
                        if comex[2].isnumeric():
                            f.write('\tli $t1, ' + comex[2] + '\n')
                            arg2 = '$t1'
                            f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'int'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'i' and comex[2] in tns):
                            arg2 = '$' + comex[2]
                            f.write('\tsubu $' + comex[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif ((comex[1] in simtabs and simtabs[comex[1]][1] == 'real') or (
                            tns[comex[1]][0] == 'r' and comex[1] in tns)):
                        if (comex[1] in simtabs and simtabs[comex[1]][1] == 'real'):
                            arg1 = '$' + simtabs[comex[1]][0]
                        else:
                            arg1 = '$f' + comex[1][1:]
                        if is_float(comex[2]):
                            f.write('\tli.s $f1, ' + comex[2] + '\n')
                            arg2 = '$f1'
                            f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                            arg2 = '$' + simtabs[comex[2]][0]
                            f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                            arg2 = '$f' + comex[2][1:]
                            f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        else:
                            print('error неверный тип')
                            return
                elif is_float(comex[1]):

                    if operation > 5:
                        f.write('\tli.s $f0, ' + comex[1] + '\n')
                        arg1 = '$f0'
                    else:
                        f.write('\tli.s $f4, ' + comex[1] + '\n')
                        arg1 = '$f4'
                    if is_float(comex[2]):
                        if operation > 5:
                            f.write('\tli.s $f0, ' + comex[2] + '\n')
                            arg2 = '$f0'
                        else:
                            f.write('\tli.s $f4, ' + comex[2] + '\n')
                            arg2 = '$f5'
                        f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif (comex[2] in simtabs and simtabs[comex[2]][1] == 'real'):
                        arg2 = '$' + simtabs[comex[2]][0]
                        f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                    elif (tns[comex[2]][0] == 'r' and comex[2] in tns):
                        arg2 = '$f' + comex[2][1:]
                        f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

                    else:
                        arg2 = '$f' + comex[2][1:]
                        f.write('\tsub.s $f' + comex[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

            elif (comex[0] == '<' or comex[0] == '>'
                    or comex[0] == '='):
                if flag == False:
                    L = 'L' + str(sample)
                    sample = sample + 1
                    flag = True
                    f.write(L + ':\n')
                if comex[0] == '<':
                    f.write('\tla $' + comex[3] + ', false\n')
                    f.write('\tbge $' + simtabs[comex[1]][0] + ', $' + simtabs[comex[2]][0] + ', SKIP'+str(skip_count) + '\n')
                    f.write('\tla $' + comex[3] + ', true\n')
                    f.write('SKIP'+str(skip_count) + ':\n')
                    skip_count = skip_count + 1
                elif comex[0] == '>':
                    f.write('\tla $' + comex[3] + ', false\n')
                    f.write('\tble $' + simtabs[comex[1]][0] + ', $' + simtabs[comex[2]][0] + ', SKIP'+str(skip_count) + '\n')
                    f.write('\tla $' + comex[3] + ', true\n')
                    f.write('SKIP'+str(skip_count) + ':\n')
                    skip_count = skip_count + 1
                elif comex[0] == '=':
                    f.write('\tla $' + comex[3] + ', false\n')
                    f.write('\tbne $' + simtabs[comex[1]][0] + ', $' + simtabs[comex[2]][0] + ', SKIP'+str(skip_count) + '\n')
                    f.write('\tla $' + comex[3] + ', true\n')
                    f.write('SKIP'+str(skip_count) + ':\n')
                    skip_count = skip_count + 1
            elif (comex[0] == 'and' or comex[0] == 'or'):
                f.write('\t' + comex[0] + ' $' + comex[3] + ', $' + comex[1] + ', $' + comex[2] + '\n')
            elif (comex[0] == 'not'):
                index = comex[2][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ' false\n')
                f.write('\tnor $' + comex[2] + ', $' + comex[1] + ', $' + temp + '\n')
            elif (comex[0] == 'IF'):
                flag = False
                index = comex[1][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ', true\n')
                f.write('\tbeq $' + temp + ', $' + comex[1] + ', ' + comex[3] + '\n')
                f.write('\tj L' + str(sample) + '\n')
                f.write('L' + str(sample) + ':\n')
                sample = sample + 1
            elif (comex[0] == 'GOTO'):
                if (comex[1] == 'after_if'):
                    if f_bc == False:
                        print('after false')
                        if (int(comex[2])>0):
                            f.write('\tj L' + str(int(comex[2])+2) + '\n')
                        else:
                            f.write('\tj L' + str(int(comex[2])+1) + '\n')
                elif (comex[1] == 'after_while'):
                    if (int(comex[2])>0):
                        f.write('\tj L' + str(sample - 1 -int(comex[2])) + '\n')
                    else:
                        if sample==2:
                            f.write('\tj L' + str(sample - 2) + '\n')
                        else:
                            f.write('\tj L' + str(sample - 4 - int(comex[2])) + '\n')
                else:
                    f.write('\tj ' + comex[1] + '\n')
            elif (comex[0] == 'break'):
                f.write('\tj L' + str(sample - 3) + '\n')
                f_bc = True
            elif (comex[0] == 'continue'):
                f.write('\tj L' + str(sample - 4) + '\n')
                f_bc = True
            elif (comex[0] == 'print'):
                if (comex[1].startswith('\"') and comex[1].endswith('\"')):
                    data=data +'\tstr'+str(str_count) + ': .asciiz '+comex[1]+'\n'
                    str_count = str_count+1
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, '+'str'+str(str_count-1)+'\n')
                    f.write('\tsyscall\n')
                elif (comex[1] in simtabs and simtabs[comex[1]][1] == 'str'):
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + comex[1] + '\n')
                    f.write('\tsyscall\n')
                elif (comex[1].isnumeric()):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, '+comex[1] + '\n')
                    f.write('\tsyscall\n')
                    data = data + '\tstrZero' + r': .asciiz "\n"'  + '\n'
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + 'strZero' + '\n')
                    f.write('\tsyscall\n')
                elif (is_float(comex[1])):
                    f.write('\tli $v0, 2\n')
                    f.write('\tli.s $f12, ' + comex[1] + '\n')
                    f.write('\tsyscall\n')
                elif (comex[1] in simtabs and simtabs[comex[1]][1] == 'int'):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, ' + '($' + simtabs[comex[1]][0] + ')\n')
                    f.write('\tsyscall\n')
                elif (comex[1] in simtabs and simtabs[comex[1]][1] == 'real'):
                    f.write('\tli $v0, 2\n')
                    f.write('\tmov.s $f12, $' + simtabs[comex[1]][0] + '\n')
                    f.write('\tsyscall\n')

            elif (comex[0] == 'return'):
                f.write('\tmove $t9, $t' + str(int(comex[1][1:])+1) + '\n' )
                f.write('\tjr $ra\n')

            elif (comex[0] == 'Call'):
                args = comex[2:len(comex)-1]
                print(args)
                for i in range(len(args)):
                    if (simtabs[args[i]][1]=='real'):
                        f.write('\tmov.s $f2' + str(i) + ', $' + simtabs[args[i]][0] + '\n')
                    else:
                        f.write('\tmove $a' + str(i) + ', $' + simtabs[args[i]][0] + '\n')
                f.write('\tjal ' + comex[1] + '\n')
                f.write('\tmove $' + comex[len(comex)-1] + ', $t9\n')



















    f.write('END:\n')
    f.close()
    f = open('out.s', 'r')
    text = f.read()
    f.close()
    f = open('out.s', 'w')
    f.write(data)
    f.write(text)
    f.close()



asm(three_address_code, simtabs)
