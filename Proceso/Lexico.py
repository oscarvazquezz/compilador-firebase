import ply.lex as lex
import pandas as pd

# resultado del analisis
resultado_lexema = []
bandera = False
 
tokens = (
    'ASIGNAR',  
    'LLAIZQ',
    'LLADER',
    'DOBLEPUNTO',
    'COMA',
    'COMILLA',
    'TEXT',
    'DECIMAL',
    'ENTERO'
)

t_ASIGNAR = r'='
t_COMILLA= r'\'|\"'
t_DOBLEPUNTO = ':'
t_COMA = r'\,'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_ignore =' \n'

def t_DECIMAL(t):
    r'[0-9]*[.][0-9]*'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TEXT(t):
    r'[a-zA-Z_ ][a-zA-z_0-9 ]*'
    t.type = 'TEXT'
    return t

def t_error( t):
    global resultado_lexema
    global bandera
    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),
                                                                      str(t.lexpos))
    resultado_lexema.append([401,"Error" ,str(t.value)])
    t.lexer.skip(1)

# Prueba de ingreso
def prueba(data):
    global resultado_lexema
    global bandera

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    counter = 0
    while True:
        tok = analizador.token()
        counter+=1
        if not tok:
            break
        id = str(tok.lineno)+""+str(counter)
        
        resultado_lexema.append([id,str(tok.type) ,str(tok.value)])

    return  pd.DataFrame(resultado_lexema,columns=["ID","Token","Chain"])

analizador = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("ingrese: ")
        prueba(data)
        print(resultado_lexema)