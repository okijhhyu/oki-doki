from rply import LexerGenerator
from ply import lex

# Список лексем. Обязателен.

reserved = {
        'def':'DEF',
        'return':'RETURN',
        'and':'AND',
        'or':'OR',
        'not':'NOT',
        'print':'PRINT',
        'while':'WHILE',
        # if
        'if':'IF',
        # break
        'break':'BREAK',
        # continue
        'continue':'CONTINUE',
        # int
        'int':'INT',
        # real
        'real':'REAL',
        # BOOLEAN
        'boolean':'BOOLEAN',
        # var
        'vars':'VARS',
        'str':'STRING'
}

tokens = list(reserved.values()) + [
        'RAVNO',
        'DP',
        'CM',
        'OP',
        'CP',
        # Фигурные скобки
        'OF',
        'CF',
        # Присваивание
        'PRISV',
        # Точка с запятой
        'SC',
        # Операторы
        'SUM',
        'SUB',
        'MUL',
        'DIV',
        # Больше - меньше
        'MORE',
        'LESS',
        # Числа int
        'NUMBER_INT',
        #'NUM',
        # Числа real
        'NUMBER_REAL',
        # Игнорируем пробелы
        #Переменная
        'ID',
        ]



# Регулярные выражения для выделения лексем.
t_DP = r'\:'
t_RAVNO = r'\='
t_PRINT = r'print'
# Скобки
t_OP = r'\('
t_CP = r'\)'
t_CM = r'\,'
# Фигурные скобки
t_OF = r'\{'
t_CF = r'\}'
# Присваивание
t_PRISV = r'\:='
# Точка с запятой
t_SC = r'\;'
# Операторы
t_SUM = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
# Больше - меньше
t_MORE = r'\>'
t_LESS = r'\<'
# Числа int
t_NUMBER_INT = r'\d+'
# Числа real
t_NUMBER_REAL = r'\d+\.\d+'
# Числа str
t_STRING = r'\"[^\'\n]*\"'

# Регулярное выражение, требующее дополнительных действий.

def t_comment(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# Правило трассировки номеров строк.

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)



# Строка, содержащая игнорируемые символы (пробелы и символы табуляции).

t_ignore  = ' \t'



# Правило обработки ошибок

def t_error(t):
    print ("Недопустимый символ '%s'" % t.value[0])
    #t.skip(1)



lex.lex()



