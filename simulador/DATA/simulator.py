# Project: Simulator
# Program name: simulator.py
# Authors: Aguilera Mauricio && Pilliza Gissela
# Last Date updated: 14 Nov 2018

import sys

#Definition of number of pages and bytes in each one
page_num = 32
size = 512

# Section of classes and objects to use

class Process:
    def __init__ (self, processo, i, m, t):
        self.process = processo
        self.di = i
        self.dm = m
        self.type = t
class Version:
    def __init__ (self, processo = -1, paginalogica = -1, referencia = -1, sucio = -1, cloc = -1):
        self.process = processo
        self.logicpage = paginalogica
        self.reference = referencia
        self.dirty = sucio
        self.clock = cloc

# Functions Section

def CreateMemoryList():
    L = [ ]
    for i in range(page_num):
        L.append(Version())
    return L

def LoadingFile(name):
    L = []
    cont = 0
    try:
        file = open(name,'r')
        for processo in file:
            processo = processo[:-1].split(' ')
            d = 0
            cont=cont +1
            if processo[3] == 'W':
                d = 1
            L.append(Process(int(processo[0]),int(processo[1]) //size,int(processo[2]) // size,d))
        print cont
    except:
        print 'Error: Loading wrong text file'
        return 1
    return L

def RefreshRef(L):
    for proc in L:
        proc.reference = 0
    return L

def Search(L):
    enc = False
    pares = [(0,0),(0,1),(1,0),(1,1)]
    i = 0
    while i < 4 and not enc:
        pos = 0
        while not enc and pos<len(L):
            enc = (L[pos].reference,L[pos].dirty) == pares[i]
            pos+=1
        i+=1
    return pos - 1

def SearchProcess(L,P):
    ext1 = ext2 = False
    i = 0
    while not ext1 and i < len(L):
        ext1 = L[i].process == P.process and L[i].logicpage == P.di
        i+=1
    j = 0
    while not ext2 and j < len(L):
        ext2 = L[j].process == P.process and L[j].logicpage  == P.dm
        j+=1
    return  i-1, j-1 , ext1 ,ext2

def IsFull(L):
    i = 0
    full = True
    while i<page_num and full:
        full = L[i].process != -1
        i+=1
    return i - 1 , full

def SearchMinorClock(L):
    menor = 0
    for i in range(len(L)):
        if L[i].clock < L[menor].clock:
            menor = i
    return menor

def UpdateVersion(L_Process,L_memory,version,debug):
    contInstruc = cont = 1
    contFaults = contWritings = 0
    if version == 1:
        for processo in L_Process:
            pos_di,pos_dm, ext1, ext2 = SearchProcess(L_memory,processo)
            if not ext1:
                contFaults+=1
                pos_Aux_1 , full= IsFull(L_memory)
                if not full:
                    L_memory[pos_Aux_1] = Version(processo.process,processo.di,1,0,cont)
                    print pos_Aux_1
                else:
                    pos_Aux_2 = Search(L_memory)
                    if debug:
                        print cont,'\t',pos_Aux_2,'\t',L_memory[pos_Aux_2].process,'\t',L_memory[pos_Aux_2].logicpage,'\t',L_memory[pos_Aux_2].dirty
                    contWritings+=L_memory[pos_Aux_2].dirty
                    L_memory[pos_Aux_2] = Version(processo.process,processo.di,1,0,cont)
            else:
                L_memory[pos_di] = Version(processo.process,processo.di,1,L_memory[pos_di].dirty ,cont)
            pos_di,pos_dm, ext1, ext2 = SearchProcess(L_memory,processo)
            if not ext2:
                contFaults+=1
                pos_Aux_1 , full= IsFull(L_memory)
                if not full:
                    L_memory[pos_Aux_1] = Version(processo.process,processo.dm,1,processo.type,cont)
                else:
                    pos_Aux_2 = Search(L_memory)
                    if debug:
                        print cont,'\t',pos_Aux_2,'\t',L_memory[pos_Aux_2].process,'\t',L_memory[pos_Aux_2].logicpage,'\t',L_memory[pos_Aux_2].dirty
                    contWritings += L_memory[pos_Aux_2].dirty
                    L_memory[pos_Aux_2] = Version(processo.process,processo.dm,1,processo.type,cont)
            else:
                L_memory[pos_dm] = Version(processo.process,processo.dm,1,L_memory[pos_dm].dirty or processo.type,cont)
            cont+=1
            if contInstruc == 200:
                L_memory = RefreshRef(L_memory)
                contInstruc = 0
            contInstruc+=1
    elif version == 2:
        for processo in L_Process:
            pos_di,pos_dm, ext1, ext2 = SearchProcess(L_memory,processo)
            if not ext1:
                contFaults+=1
                pos_Aux_1 , full= IsFull(L_memory)
                if not full:
                    L_memory[pos_Aux_1] = Version(processo.process,processo.di,1,0,cont)
                else:
                    pos_Aux_2= SearchMinorClock(L_memory)
                    if debug:
                            print cont,'\t',pos_Aux_2,'\t',L_memory[pos_Aux_2].process,'\t',L_memory[pos_Aux_2].logicpage,'\t',L_memory[pos_Aux_2].dirty
                    contWritings += L_memory[pos_Aux_2].dirty
                    L_memory[pos_Aux_2] = Version(processo.process,processo.di,1,0,cont)
            else:
                L_memory[pos_di] = Version(processo.process,processo.di,1,L_memory[pos_di].dirty or 0,cont)

            pos_di,pos_dm, ext1, ext2 = SearchProcess(L_memory,processo)
            if not ext2:
                contFaults+=1
                pos_Aux_1 , full= IsFull(L_memory)
                if not full:
                    L_memory[pos_Aux_1] = Version(processo.process,processo.dm,1,processo.type,cont)
                else:
                    pos_Aux_2 = SearchMinorClock(L_memory)
                    if debug:
                            print cont,'\t',pos_Aux_2,'\t',L_memory[pos_Aux_2].process,'\t',L_memory[pos_Aux_2].logicpage,'\t',L_memory[pos_Aux_2].dirty
                    contWritings+=L_memory[pos_Aux_2].dirty
                    L_memory[pos_Aux_2] = Version(processo.process,processo.dm,1,processo.type,cont)
            else:
                L_memory[pos_dm] = Version(processo.process,processo.dm,1,L_memory[pos_dm].dirty or processo.type,cont)
            if contInstruc == 200:
                L_memory = RefreshRef(L_memory)
                contInstruc = 0
            contInstruc+=1
            cont+=1
    else:
        print "Error: Wrong Version."
    return contFaults, contWritings, L_memory

def main(P):
    l = len(P)
    if l==3:
        P.append('0')
    if l > 2 :
        File = LoadingFile(P[1])
        if File != 1:
            c_Faults, c_Writings, _ =  UpdateVersion(File,CreateMemoryList(),int(P[2]),int(P[3]))
            print '---------------------------------------------------------------------------------'
            print '| File Name\t| Lines\t\t| Version\t| Faults\t| Writings\t|'
            print '---------------------------------------------------------------------------------'
            print '|',P[1],'\t|',len(File),'\t|',P[2],'\t\t|',c_Faults,'\t\t|',c_Writings,'\t\t|'
            print '---------------------------------------------------------------------------------'
#            print 'File Name: ',P[1],'\tVersion: ',P[2],'\tFaults: ',c_Faults,'\tWritings: ',c_Writings
    elif l == 2:
        print 'Error: Put the version number (options 1/2). '
    else:
        print """------------------------------  M   E  N  U  -----------------------------
Parameter 1 : Data File Name
Parameter 2 : Version(1/2)
Parameter 3 : Debug(1/0)
Parameter 4 : Number of procces lines desired to show."""

main(sys.argv)
