import subprocess
import constantes
import time
from Pila import Pila
import os

simbolos          = constantes.CONSTANT_S
flecha            = constantes.CONSTANT_F
operadoresunarios = constantes.CONSTANT_U

def obtenerConstruccionThompson (expresionInfija):
    print(expresionInfija)
    expresionInfija = preprocesarCadena(expresionInfija)
    expresionPostFijaList = obtenerExpresionPostFija(expresionInfija)
    listaDeTuplas = evaluarExpresion(expresionPostFijaList)
    obtenerArchivo(listaDeTuplas)

def evaluarExpresion (expresionPostFijaList):

    pila = Pila()
    listaFinal = []
    contador = 1

    for caracter in expresionPostFijaList:

        if caracter in simbolos:

            listaDeOperandos = obtenerListaDeOperandos(pila,caracter)
            inicialA,finalA,inicialB,finalB = _obtenerEstadoInicialYFinal(listaDeOperandos)



            if len(listaDeOperandos) > 1:

                if caracter == "|":
                    resultado = unirListas(listaDeOperandos,obtenerInstruccionesDeOperadoresNoUnitarios(caracter,contador,[inicialA,inicialB],[finalA,finalB],listaDeOperandos))
                    contador+=2
                else:
                    resultado = obtenerInstruccionesDeOperadoresNoUnitarios(caracter,contador,[inicialA,inicialB],[finalA,finalB],listaDeOperandos)
                    #contador-=1
            else:

                resultado = obtenerInstruccionesDeOperadoresUnitarios(listaDeOperandos,contador,[inicialA],[finalA],caracter)
                contador+=2

            pila.incluir(resultado)


        else:
            tuplaTemporal = [(str(contador), str((contador+1)), caracter)]
            contador+=2
            pila.incluir(tuplaTemporal)

    listaFinal = pila.extraer()

    return [listaFinal]

def obtenerListaDeOperandos (pila, operador):

    listaDeOperandos = []

    elemento = ()

    for i in range(1 if operador in operadoresunarios  else 2):

        elemento = pila.extraer()

        listaDeOperandos.append(elemento)


    return listaDeOperandos

def _obtenerEstadoInicialYFinal (listaDeOperandos):

    listaDeNumerosA = []
    listaDeNumerosB = []

    j = 0

    for operando in listaDeOperandos:
        for tupla in operando:
            for i in range(len(tupla)-1):

                if j == 0:

                    listaDeNumerosA.append(int(tupla[i]))

                else:

                    listaDeNumerosB.append(int(tupla[i]))
        j+=1

    listaDeNumerosA = list(sorted(set(listaDeNumerosA)))

    listaDeNumerosB = list(sorted(set(listaDeNumerosB)))

    if len(listaDeOperandos) > 1:

        finalA = max(listaDeNumerosA)

        finalB  = max(listaDeNumerosB)

        inicialA = finalA-1

        inicialB = finalB-1

    else:

        finalA = max(listaDeNumerosA)

        inicialA = finalA-1

        finalB = 0

        inicialB = 0


    return inicialA,finalA,inicialB,finalB

def obtenerExpresionPostFija (expresionInfija):
    miComando = 'java App "'+expresionInfija+'"'
    tempStr = subprocess.check_output(miComando, shell=True)
    return list(tempStr.decode("utf-8").strip())

def unirListas (llistaUno, listaDos):
    listaF = []

    for i in llistaUno:
        for elemento in i:
            listaF.append(elemento)
    for i in listaDos:
        listaF.append(i)
    return sorted(set(listaF))

def obtenerEstadoInicialYFinal (lista, caracter):
    inicial = 0
    final = 0

    listaAuxiliar = []

    for tupla in lista:

        for j in range(2):
            listaAuxiliar.append(int(tupla[j]))

    listaAuxiliar = sorted(set(listaAuxiliar))

    final = max(listaAuxiliar)

    listaAuxiliar.pop()

    if caracter == "*" or caracter == "+":
        inicial = max(listaAuxiliar)
    elif caracter == "|" or caracter == ".":
        inicial = min(listaAuxiliar)




    return inicial, final

def obtenerInstruccionesDeOperadoresNoUnitarios(operador, contador, listaDeIniciales, listaDeFinales,listaDeOperandos):

    listaDeTuplas = []

    if operador == ".":

        inicialA, inicialB, finalA, finalB = int(listaDeIniciales[0]),int(listaDeIniciales[1]),int(listaDeFinales[0]),int(listaDeFinales[1])


        operandoA = listaDeOperandos[0]


        operandoB = listaDeOperandos[1]

        listaAux2 = []
        for tupla in operandoA:
            a,b,c = tupla[0],tupla[1],tupla[2]

            if b == str(finalA):
                b = str(inicialB)
            if a == str(finalA):
                a = str(inicialB)

            listaAux2.append((a,b,c))
        operandoA = listaAux2

        listaAux3 = []
        for tupla in operandoB:
            a,b,c = tupla[0],tupla[1],tupla[2]

            if a == str(finalB):
                a = str(finalA)
            if b == str(finalB):
                b = str(finalA)
            listaAux3.append((a,b,c))

        operandoB = listaAux3

        return operandoA+operandoB
    else:

        inicial = contador
        final = contador+1

        for i in range(2):

            listaDeTuplas.append((str(inicial),str(listaDeIniciales[i]),"&epsilon;"))

            listaDeTuplas.append((str(listaDeFinales[i]),str(final),"&epsilon;"))

        return listaDeTuplas

def obtenerInstruccionesDeOperadoresUnitarios  (operador, contador,listaDeIniciales,listaDeFinales,caracter):

    listaDeTuplas = []

    inicialA = str(listaDeIniciales.pop())
    finalA = str(listaDeFinales.pop())

    for operando in operador:
        for tupla in operando:
            listaDeTuplas.append(tupla)

    listaDeTuplas.append((finalA,inicialA,"&epsilon;"))
    listaDeTuplas.append((str(contador), inicialA,"&epsilon;"))
    listaDeTuplas.append((finalA, str(contador+1),"&epsilon;"))

    if caracter == "*":
        listaDeTuplas.append((str(contador), str(contador+1),"&epsilon;"))

    return listaDeTuplas

def obtenerEstadoInicialFinal (listaDeTuplas):
    listaTemporal = []
    for i in range(len(listaDeTuplas)):
        iTupla = listaDeTuplas[i]
        for j in range(len(iTupla)-1):
            listaTemporal.append(listaDeTuplas[i][j])

    listaTemporal = list(set(listaTemporal))

    final = max(listaTemporal)

    posicion = 0

    while posicion < len(listaTemporal):
        if listaTemporal[posicion] == final:
            listaTemporal.pop(posicion)

        posicion+=1

    inicial = max(listaTemporal)

    return  inicial,final

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

    return cadenaFinal

def obtenerArchivo (listaDeTuplas):

    str1 = "digraph AFN{"+"\n"
    str2 = "rankdir = LR;"+"\n"
    str3 = 'node[shape=circle, style="filled", fixedsize=true,width=0.2, color="#FFF7A8", fontsize=8]'+"\n"
    str4 = 'F[color="blue", shape="doublecircle", style="filled"]';
    str5 = 'I[color="white", shape="doublecircle", style="filled", fontcolor="white"]';
    str6 = "edge [ fontname=Arial, fontcolor=blue, fontsize=8 ];"
    str7 = 'node [name = "1"];'+"\n"
    str8 = "}"

    lista = [str1,str2,str3,str4,str5,str6,str7]
    listaTemporal = []
    f = open("input.dot", "w")


    for elemento in listaDeTuplas:
        for tupla in elemento:
            a,b = int(tupla[0]), int(tupla[1])
            listaTemporal.append(a)
            listaTemporal.append(b)

    listaTemporal = list(set(listaTemporal))

    inicial = max(listaTemporal)
    final = inicial - 1

    for m in lista:
        f.write(str(m))

    for elemento in listaDeTuplas:
        for tupla in elemento:
            a,b,c = str(tupla[0]),str(tupla[1]), str(tupla[2])


            if int(a) == final or int(b) == final:
                nuevaStr = b+'->F [label  = "'+c+'", color = "red"]'+"\n"
            else:
                nuevaStr = ''+b+' -> '+''+a+' [label = "'+c+'", color="red"]'+"\n"
            f.write(nuevaStr)


    inicial ='I -> '+str(inicial)+' [label  = "Inicio", color = "red"]'+"\n"
    f.write(inicial)
    f.write(str8)
    f.close()
    subprocess.call("dot -Tpng input.dot > output.png", shell=True)

def probarApp():
    f = open("Expresiones", "r")

    for regex in f:
        obtenerConstruccionThompson(regex.strip())
        time.sleep(1.5)
    f.close()

probarApp()
