import ply.yacc as yacc
from Proceso.Lexico import *

resultado_gramatica = []
listaVariable = []
banderVerific  = False 

precedence = (
    ('left','ASIGNAR','LLAIZQ','LLADER'),
    ('left','DOBLEPUNTO','COMA')
)

def p_expresion_logicas(t):
    '''
    expresion : COMILLA TEXT COMILLA DOBLEPUNTO LLAIZQ expresion LLADER
              | COMILLA TEXT COMILLA DOBLEPUNTO LLAIZQ expresion COMA expresion LLADER
              | COMILLA TEXT COMILLA DOBLEPUNTO LLAIZQ expresion COMA expresion COMA expresion LLADER
    '''
    global banderVerific
    banderVerific = True
    t[0]= (t[5],t[6],t[7])

def p_expresion_logicas_evaluar(t):
    '''
    expresion : COMILLA TEXT COMILLA DOBLEPUNTO COMILLA TEXT COMILLA COMA expresion
              | COMILLA TEXT COMILLA DOBLEPUNTO COMILLA TEXT COMILLA
              | COMILLA TEXT COMILLA DOBLEPUNTO ENTERO 
              | COMILLA TEXT COMILLA DOBLEPUNTO ENTERO COMA expresion
              | COMILLA TEXT COMILLA DOBLEPUNTO DECIMAL
              | COMILLA TEXT COMILLA DOBLEPUNTO DECIMAL COMA expresion

              | expresion COMILLA TEXT COMILLA DOBLEPUNTO LLAIZQ expresion LLADER
              | expresion COMILLA TEXT COMILLA DOBLEPUNTO LLAIZQ expresion LLADER COMA expresion
            
    '''
    global listaVariable
    t[0] = t[2]
    listaVariable.append(t[2])
    

def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

def p_error(t):
    global resultado_gramatica
    global banderVerific
    banderVerific = False
    if t:
        resultado = "syntax type error {} in value  =  {}".format( str(t.type),str(t.value))
    else:
        resultado = "Syntax error {}".format(t)
    resultado_gramatica.append(resultado)

parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    global listaVariable
    global banderVerific
    resultado_gramatica.clear()
    
    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else: print("")
    
    visited = set()
    dup = [x for x in listaVariable if x in visited or (visited.add(x) or False)]
    listaVariable.clear()
    if len(dup) >= 1:
        banderVerific = False
        return (resultado_gramatica,banderVerific,dup)
    else:
        return (resultado_gramatica,banderVerific)