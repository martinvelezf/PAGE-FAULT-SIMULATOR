# Project: Simulator 
# Program name: simulator.py
# Authors: Aguilera Mauricio && Pilliza Gissela
# Last Date updated: 14 Nov 2018

import sys

#Definition of number of pages and bytes in each one
pages = 32
legth = 512

# Section of classes and objects to use 
class Process:
    def __init__ (self, a, b, c, d):
        self.process = a
        self.di = b
        self.dm = c
        self.tipo = d

class Version:
    def __init__ (self, a = -1, b = -1, c = -1, d = -1,e=0):
        self.process = a
        self.logicpage = b 
        self.reference = c 
        self.dirty = d 
        self.clock = e 

# Section of Functions

def InitializeList():
    L = [ ]
    for i in range(pages):
        L.append(Version())
    return L

def ReadFile(nombre,c):
    L = []
    file = open(nombre,'r')
    cont = 0
    for proceso in file:
        if cont < c: 
            proceso = proceso[:-1].split(' ')
            d = 0
            if proceso[3] == 'W':
                d = 1
            L.append(Process(int(proceso[0]),int(proceso[1]),int(proceso[2]),d))
        cont+=1
    file.close
    return L

def RefreshRef(L):
    for proc in L:
        proc.reference = 0
    return L

def IsDirtyPos(L):
    enc = esc = False
    rd = [(0,0),(0,1),(1,0),(1,1)]
    i = 0
    while i < 4 and not enc:
        pos = 0
        while not enc and pos<len(L):
            if (L[pos].reference,L[pos].dirty) == rd[i]:
                enc = True
                if L[pos].dirty == 1:
                    esc = True
            else:
                pos+=1
        i+=1
    return pos , esc

def BuscandoEstaProceso(L,P):
    ext1 = ext2 = False
    i = 0
    while not ext1 and i < len(L):
        if L[i].process == P.process and L[i].logicpage == P.di // legth:
            ext1 = True
        else:
            i+=1
    j = 0
    while not ext2 and j < len(L):
        if L[j].process == P.process and L[j].logicpage  == P.dm // legth:
            ext2 = True
        else:
            j+=1
    return  i, j , ext1 ,ext2

def TablaEstaLlena(L):
    i = 0
    llena = True
    while i<pages and llena:
        if L[i].process == -1:
            llena = False
        else:
            i+=1 
    return i , llena

def BuscandoClockMenor(L):
    menor = 0
    for i in range(len(L)):
        if L[i].clock < L[menor].clock:
            menor = i
    return menor

def DevolverPosicionVersion2(L):
    pos=BuscandoClockMenor(L)
    return pos, L[pos].dirty or 0

def ActualizarVersion(L_Procesos,Lv,version,debug):
    contInstrucciones = cont = 1
    contFallos = contEscritura = 0
    if version == 1:
        for proceso in L_Procesos:
            pos_di,pos_dm, ext1, ext2 = BuscandoEstaProceso(Lv,proceso)

            if not ext1:
                contFallos+=1
                pos_Aux_1 , llena= TablaEstaLlena(Lv)
                if not llena:
                    Lv[pos_Aux_1] = Version(proceso.process,proceso.di//legth,1,0,cont)
                else:
                    pos_Aux_2, escritura = IsDirtyPos(Lv)
                    if debug:
                        print cont,'\t',pos_Aux_2,'\t',Lv[pos_Aux_2].process,'\t',Lv[pos_Aux_2].logicpage,'\t',Lv[pos_Aux_2].dirty
                    if escritura:
                        contEscritura+=1
                    Lv[pos_Aux_2] = Version(proceso.process,proceso.di//legth,1,0,cont)
            else:
                Lv[pos_di] = Version(proceso.process,proceso.di//legth,1,Lv[pos_di].dirty or 0,cont)
            
            pos_di,pos_dm, ext1, ext2 = BuscandoEstaProceso(Lv,proceso)
            if not ext2:
                contFallos+=1
                pos_Aux_1 , llena= TablaEstaLlena(Lv)
                if not llena:
                    Lv[pos_Aux_1] = Version(proceso.process,proceso.dm//legth,1,proceso.tipo,cont)
                else:
                    pos_Aux_2, escritura = IsDirtyPos(Lv)
                    if debug:
                        print cont,'\t',pos_Aux_2,'\t',Lv[pos_Aux_2].process,'\t',Lv[pos_Aux_2].logicpage,'\t',Lv[pos_Aux_2].dirty
                    if escritura:
                        contEscritura+=1
                    Lv[pos_Aux_2] = Version(proceso.process,proceso.dm//legth,1,proceso.tipo,cont)
            else:
                Lv[pos_dm] = Version(proceso.process,proceso.dm//legth,1,Lv[pos_dm].dirty or proceso.tipo,cont)
            cont+=1
            if contInstrucciones == 200:
                Lv = RefreshRef(Lv)
                contInstrucciones = 0
            contInstrucciones+=1
    elif version == 2:
        for proceso in L_Procesos:
            pos_di,pos_dm, ext1, ext2 = BuscandoEstaProceso(Lv,proceso)
            if not ext1:
                contFallos+=1
                pos_Aux_1 , llena= TablaEstaLlena(Lv)
                if not llena:
                    Lv[pos_Aux_1] = Version(proceso.process,proceso.di//legth,1,0,cont)
                else:
                    pos_Aux_2, escritura = DevolverPosicionVersion2(Lv)
                    if debug:
                            print cont,'\t',pos_Aux_2,'\t',Lv[pos_Aux_2].process,'\t',Lv[pos_Aux_2].logicpage,'\t',Lv[pos_Aux_2].dirty
                    if escritura:
                        contEscritura+=1
                    Lv[pos_Aux_2] = Version(proceso.process,proceso.di//legth,1,0,cont)
            else:
                Lv[pos_di] = Version(proceso.process,proceso.di//legth,1,Lv[pos_di].dirty or 0,cont)
            
            pos_di,pos_dm, ext1, ext2 = BuscandoEstaProceso(Lv,proceso)
            if not ext2:
                contFallos+=1
                pos_Aux_1 , llena= TablaEstaLlena(Lv)
                if not llena:
                    Lv[pos_Aux_1] = Version(proceso.process,proceso.dm//legth,1,proceso.tipo,cont)
                else:
                    pos_Aux_2, escritura = DevolverPosicionVersion2(Lv)
                    if debug:
                            print cont,'\t',pos_Aux_2,'\t',Lv[pos_Aux_2].process,'\t',Lv[pos_Aux_2].logicpage,'\t',Lv[pos_Aux_2].dirty
                    if escritura:
                        contEscritura+=1
                    Lv[pos_Aux_2] = Version(proceso.process,proceso.dm//legth,1,proceso.tipo,cont)
            else:
                Lv[pos_dm] = Version(proceso.process,proceso.dm//legth,1,Lv[pos_dm].dirty or proceso.tipo,cont)
            if contInstrucciones == 200:
                Lv = RefreshRef(Lv)
                contInstrucciones = 0
            contInstrucciones+=1
            cont+=1
    else:
        print "Error: Wrong Version."
    return contFallos, contEscritura, Lv


def main(P):
    l = len(P)
    if l==3:
        P.append('0')
        P.append('50000')
    elif l == 4:
        P.append('50000')
    if l > 2 :
        c_Fallos, c_Escrituras, _ =  ActualizarVersion(ReadFile(P[1],int(P[4])),InitializeList(),int(P[2]),int(P[3]))
        print 'File: ',P[1],'\tVersion: ',P[2],'\tFaults: ',c_Fallos,'\tWritings: ',c_Escrituras
    elif l == 2:
        print 'Error: Put the version number option (1/2) '
    else:
        print """Menu:
PArameters 1 : Data File Name
PArameters 2 : Version(1/2)
PArameters 3 : Debug(1/0) ( 0 by default)
PArameters 4 : Number of procces lines to show (all lines by default)"""
main(sys.argv)