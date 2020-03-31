import subprocess
import time
import constantes
import os
from Pila import Pila
import anytree
from anytree import Node, RenderTree

simbolos           = constantes.CONSTANT_S
flecha             = constantes.CONSTANT_F
operadoresunarios  = constantes.CONSTANT_U
simboloDeExtension = constantes.CONSTANT_E


def obtenerImagen(diccionarioDeRelacion,listaDeTransiciones):

    str1 = "digraph AFN{"+"\n"
    str2 = "rankdir = LR;"+"\n"
    str3 = 'node[shape=circle, style="filled", fixedsize=true,width=0.2, color="#FFF7A8", fontsize=8]'+"\n"

    str4 = 'F[color="blue", shape="doublecircle", style="filled"]';
    str5 = 'I[color="white", shape="doublecircle", style="filled", fontcolor="white"]';

    str6 = "edge [ fontname=Arial, fontcolor=blue, fontsize=8 ];"+"\n"
    str7 = 'node [style=filled fillcolor="#00ff005f"];'+"\n"
    str9 = "}"

    lista = [str1,str2,str3,str4,str5,str6,str7]

    f = open("input.dot", "w")

    for _str in lista:
        f.write(_str)

    estadosIniciales = []

    for llave,valor in diccionarioDeRelacion.items():
        if 'I' in valor:
            estadosIniciales.append(valor)


    for estado in estadosIniciales:
        if 'IF' in estado:
            str10 = 'I -> F [label = "Inicial", color="blue"]'
        else:
            str10 = 'I -> '+ str(estado)+' [label = "Inicial", color="blue"]'

        f.write(str10)

    for transicion in listaDeTransiciones:
        estadoActual = str(transicion[0])
        simbolo = str(transicion[1])
        estadoSiguiente = str(transicion[2])

        if 'F' not in estadoSiguiente and 'F' not in estadoActual:
            str8 = estadoActual+' -> '+ estadoSiguiente+' [label = "'+simbolo+'", color="red"]'
        elif 'F' in estadoSiguiente and 'F' in estadoActual:
            str8 = 'F -> F [label = "'+simbolo+'", color="red"]'
        elif 'F' in estadoSiguiente:
            str8 = estadoActual+' -> F [label = "'+simbolo+'", color="red"]'
        elif 'F' in estadoActual:
            str8 = 'F -> '+ estadoSiguiente+' [label = "'+simbolo+'", color="red"]'
        f.write(str8)



    f.write(str9)
    f.close()
    subprocess.call("dot -Tpng input.dot > AFD.png", shell=True)

def construirSubArbol(listaDeOperandos, operador):

    operandoA = listaDeOperandos[0]
    operandoB = []
    _str = 'Nada'

    if len(listaDeOperandos) > 1:

        operandoB = listaDeOperandos[1]

        return [[operador,0,0,0], operandoB, operandoA]

    else:

        return [[operador,0,0,0], operandoA, [_str,[],[]]]

def construirArbol(expresionPostFija):

    pila = Pila()

    contador = 1

    for elemento in expresionPostFija:

        if elemento in simbolos:

            numeroDeOperandos = 1 if elemento in operadoresunarios  else 2

            aux = numeroDeOperandos

            listaDeOperandos = []

            while aux != 0:

                operando = pila.extraer()

                listaDeOperandos.append(operando)

                aux-=1

            resultado = construirSubArbol(listaDeOperandos, elemento)

            pila.incluir(resultado)

        else:

            if elemento == 'e':

                nuevoElemento = [[elemento,True,[],[]],[],[]]

            else:

                nuevoElemento = [[elemento,False,[contador],[contador]],[],[]]


            pila.incluir(nuevoElemento)
            contador+=1

    return pila.extraer()

def obtenerExpresionPostFija (expresionInfija):
    miComando = 'java App "'+expresionInfija+'"'
    tempStr = subprocess.check_output(miComando, shell=True)
    return list(str(tempStr.decode("utf-8").strip()))

def extenderExpresionRegular(expresionInfija):
    return '('+expresionInfija+').'+simboloDeExtension

def calcularAnulables(Arbol):

    nodoRaiz = Arbol[0]

    if str(nodoRaiz[0]) in simbolos:

        hijoIzquierdo = Arbol[1]
        hijoDerecho = Arbol[2]

        calcularAnulables(hijoIzquierdo)
        calcularAnulables(hijoDerecho)

        valorAnulableA = hijoIzquierdo[0][1]
        valorANulableB = hijoDerecho  [0][1]

        operador = nodoRaiz[0]

        if operador == '|':
            nodoRaiz[1] = True if valorAnulableA or valorANulableB else False
        elif operador == '.':
            nodoRaiz[1] = True if valorAnulableA and valorANulableB else False
        elif operador == '*':
            nodoRaiz[1] = True
        elif operador == '+':
            nodoRaiz[1] = True if valorAnulableA else False

        Arbol[0] = nodoRaiz

    return Arbol

def calcularPrimeros(Arbol):

    nodoRaiz = Arbol[0]

    if str(nodoRaiz[0]) in simbolos:

        hijoIzquierdo = Arbol[1]
        hijoDerecho   = Arbol[2]
        calcularPrimeros(hijoIzquierdo)
        calcularPrimeros(hijoDerecho)
        primerosDeNodoA = set(hijoIzquierdo[0][2])
        primerosDeNodoB = set(hijoDerecho[0][2])
        valorAnulableA = hijoIzquierdo[0][1]
        operador = nodoRaiz[0]

        primerosDeNodo = []

        if operador == '|':

            primerosDeNodo = list(primerosDeNodoA.union(primerosDeNodoB))

        elif operador == '.':

            if valorAnulableA:
                primerosDeNodo = list(primerosDeNodoA.union(primerosDeNodoB))

            else:
                primerosDeNodo = list(primerosDeNodoA)

        elif operador == '*' or operador == '+':

            primerosDeNodo = list(primerosDeNodoA)

        nodoRaiz[2] = primerosDeNodo
        Arbol[0] = nodoRaiz

    return Arbol

def calcularUltimos(Arbol):

    nodoRaiz = Arbol[0]

    if str(nodoRaiz[0]) in simbolos:

        hijoIzquierdo = Arbol[1]
        hijoDerecho = Arbol[2]

        calcularUltimos(hijoIzquierdo)
        calcularUltimos(hijoDerecho)

        ultimosDeNodoA = set(hijoIzquierdo[0][3])
        ultimosDeNodoB = set(hijoDerecho[0][3])
        valorAnulableB = hijoDerecho[0][1]

        operador = nodoRaiz[0]

        ultimosDeNodo = []

        if operador == '|':

            ultimosDeNodo = list(ultimosDeNodoA.union(ultimosDeNodoB))

        elif operador == '.':

            if valorAnulableB:

                ultimosDeNodo = list(ultimosDeNodoA.union(ultimosDeNodoB))

            else:

                ultimosDeNodo = list(ultimosDeNodoB)

        elif operador == '*' or operador == '+':

            ultimosDeNodo = list(ultimosDeNodoA)

        nodoRaiz[3] = ultimosDeNodo

        Arbol[0] = nodoRaiz

    return Arbol

def obtenerPlantillaDeTablaDeSiguientes(expresionPostFija):

    elementos  = [elemento for elemento in expresionPostFija if elemento not in simbolos]

    n = len(elementos)

    iteraciones= [i+1 for i in range(n)]
    siguientes = [[]  for i in range(n)]

    return [elementos, iteraciones, siguientes]

def calcularSiguientes(tablaDeSiguientes, Arbol):

    nodoRaiz = Arbol[0]

    if str(nodoRaiz[0]) in simbolos:

        hijoIzquierdo = Arbol[1]
        hijoDerecho = Arbol[2]

        calcularSiguientes(tablaDeSiguientes, hijoIzquierdo)
        calcularSiguientes(tablaDeSiguientes, hijoDerecho  )

        ultimosDeNodoA  = hijoIzquierdo[0][3] #C1
        primerosDeNodoA = hijoIzquierdo[0][2] #C1
        primerosDeNodoB = hijoDerecho[0][2]
        operador = str(nodoRaiz[0])
        #print(hijoIzquierdo)
        #print(hijoDerecho)

        siguientes = tablaDeSiguientes[2]

        if operador == '*' or operador == '+':

            for elementoA in ultimosDeNodoA:
                for elementoB in primerosDeNodoA:
                    siguientes[elementoA-1].append(elementoB)


        elif operador == '.':

            for elementoA in ultimosDeNodoA:
                for elementoB in primerosDeNodoB:
                    siguientes[elementoA-1].append(elementoB)

        tablaDeSiguientes[2] = siguientes

    return tablaDeSiguientes

def construirAutomata(nodoRaiz,tablaDeSiguientes):

    listaDeTransiciones = []

    estadoInicial = nodoRaiz[2]

    listaDeEstados = [estadoInicial]

    for estadoActual in listaDeEstados:

        diccionarioTemporal = {}

        for elemento in estadoActual:

            llave = tablaDeSiguientes[0][elemento-1]

            if llave not in diccionarioTemporal:

                diccionarioTemporal[llave] =[tablaDeSiguientes[2][elemento-1]]

            else:

                listaExistente = diccionarioTemporal[llave]
                listaExistente.append(tablaDeSiguientes[2][elemento-1])
                diccionarioTemporal[llave] = listaExistente

        diccionarioDeTransiciones = {}

        for llave,valor in diccionarioTemporal.items():

            resultadoDeUnion = list(set().union(*valor))

            if resultadoDeUnion not in listaDeEstados and len(resultadoDeUnion) > 0:

                listaDeEstados.append(resultadoDeUnion)


            if len(resultadoDeUnion) > 0:

                listaDeTransiciones.append([estadoActual,llave,resultadoDeUnion])

    return listaDeEstados, listaDeTransiciones

def apodarEstados(listaDeEstados,listaDeTransiciones,estadoInicial,valorEstadoFinal):

    preCadena = 'E'
    diccionarioTemporal = {}
    contador = 0

    for estado in listaDeEstados:

        if estado == estadoInicial and valorEstadoFinal in estado:

            diccionarioTemporal[str(estado)] = preCadena+'IF'+str(contador)

        elif estado == estadoInicial:

            diccionarioTemporal[str(estado)] = preCadena+'I'+str(contador)

        elif valorEstadoFinal in estado:

            diccionarioTemporal[str(estado)] = preCadena+'F'+str(contador)

        else:

            diccionarioTemporal[str(estado)] = preCadena+str(contador)

        contador+=1

    for transicion in listaDeTransiciones:

        estadoActual = str(transicion[0])
        estadoSiguiente = str(transicion[2])

        transicion[0] = diccionarioTemporal[estadoActual]
        transicion[2] = diccionarioTemporal[estadoSiguiente]

    return diccionarioTemporal,listaDeTransiciones

def obtenerArchivoDeRelacionDeEstados(diccionarioDeRelacion):

    f = open('relacionDeEstados.txt','w')
    _str = ""

    for llave,valor in diccionarioDeRelacion.items():
        if 'F' in valor:
            _str = "F = "+ llave+"\n"
        else:
            _str = valor +" = "+ llave+"\n"

        f.write(_str)

    f.close()

def preprocesarCadena (expresionInfija):
    cadenaTemporal  = expresionInfija
    cadenaFinal = ""
    listaTemporal = []
    if len(cadenaTemporal) > 1:
        for i in range(len(cadenaTemporal)):

            try:

                caracteri_0 = cadenaTemporal[i]
                caracteri_1 = cadenaTemporal[i+1]

                if caracteri_0 not in simbolos and caracteri_1 not in simbolos and caracteri_1 != ')' and caracteri_1 != '(' and caracteri_0 != ')' and caracteri_0 != '(':

                    if len(cadenaFinal) > 0:
                        cadenaFinal+= ("."+caracteri_1)
                    else:
                        cadenaFinal+= (caracteri_0+"."+caracteri_1)

                elif (caracteri_0 == ")" and (caracteri_1 == "(" or caracteri_1 not in simbolos)) and (caracteri_0 != ")" and caracteri_1 != ")"):

                    if len(cadenaFinal) > 0:

                        cadenaFinal+= ("."+caracteri_1)

                    else:
                        cadenaFinal+= (caracteri_0+"."+caracteri_1)

                elif (caracteri_0 not in simbolos and caracteri_0 != "(") and caracteri_1 == "(":

                    if len(cadenaFinal) > 0:

                        cadenaFinal+= ("."+caracteri_1)

                    else:
                        cadenaFinal+= (caracteri_0+"."+caracteri_1)
                else:

                    if (caracteri_0 == "*" or caracteri_0 == "+") and caracteri_1 not in simbolos and caracteri_1 != "(" and caracteri_1 != ")":
                        if len(cadenaFinal) > 0:

                            cadenaFinal+= "."+caracteri_1

                        else:
                            cadenaFinal+= (caracteri_0+"."+caracteri_1)
                    else:
                        if len(cadenaFinal) > 0:

                            cadenaFinal+= caracteri_1

                        else:
                            cadenaFinal+= (caracteri_0+caracteri_1)

            except:
                pass

        return cadenaFinal
    else:
        return expresionInfija

def obtenerAFD(expresionInfija):
    print(expresionInfija)
    expresionInfija   = preprocesarCadena(expresionInfija)
    expresionInfija   = extenderExpresionRegular(expresionInfija)
    expresionPostFija = obtenerExpresionPostFija(expresionInfija)
    Arbol = construirArbol(expresionPostFija)
    Arbol = calcularAnulables(Arbol)
    Arbol = calcularPrimeros(Arbol)
    Arbol = calcularUltimos(Arbol)
    tablaDeSiguientes = obtenerPlantillaDeTablaDeSiguientes(expresionPostFija)
    tablaDeSiguientes = calcularSiguientes(tablaDeSiguientes, Arbol)
    listaDeEstados, listaDeTransiciones = construirAutomata(Arbol[0], tablaDeSiguientes)
    diccionarioDeRelacion, listaDeTransiciones = apodarEstados(listaDeEstados, listaDeTransiciones,Arbol[0][2], len(tablaDeSiguientes[0]))
    obtenerArchivoDeRelacionDeEstados(diccionarioDeRelacion)
    obtenerImagen(diccionarioDeRelacion,listaDeTransiciones)

def probarApp():
    f = open("Expresiones", "r")

    for regex in f:
        obtenerAFD(regex.strip())
        time.sleep(1.5)
    f.close()

probarApp()
