
import sys
debug=0
tamanopaginas=[]

class Process:
    def __init__ (self, a, b, c, d):
        self.process = a
        self.di = b
        self.ddato = c
        self.type = d

class Page:
    def __init__ (self, a = -1, b = -1, c = -1, d = -1,e=0):
        self.process = a
        self.logicpage = b
        self.reference = c
        self.dirty = d
        self.clock = e
    def IsFull():
        i = 0
        full = True
        while i<len(L) and full:
            full = L[i].process != -1
            i+=1
        return i-1  , full
def PageTable(memoryframe):
    P = [ ]
    for i in range(memoryframe):
        P.append(Page())#crea una lista de la clase con el tam;o de la pagina
    return P

def saveprocess(process,NumeroArchivos):
    l=[]
    for i in range(0,NumeroArchivos):
        l.append(ReadFile0(process[i]))
    return l
def ReadFile0(nombre):
    L = []
    c=0
    file = open(nombre,'r')
    for instruccion in file:
        L.append(instruccion)
        c=c+1
    file.close
    tamanopaginas.append(c)
    return L

def ReadFile(nombre,size):
    L = []
    file = open(nombre,'r')
    for proceso in file:
        proceso = proceso[:-1].split(' ')
        if proceso[3] == 'W':
            d = 1
        else:
            d = 0
        L.append(Process(int(proceso[0]),int(proceso[1]) // size,int(proceso[2]) // size,d))
    file.close
    return L

def Quatum(L,quatum): #esta funcion ordena los procesos por quatum y llama la funcion que los guarda en la page table
    c=0 #contador interno para pasar quatum de lineas
    pos=0
    f= open("temp.txt","w+")
    bool=True
    line=[0]*len(tamanopaginas)#registro de las lineas que se estan leyendo por proceso
    true=0 #sirv
    s=0
    while(True):
        while(line[pos]!=tamanopaginas[pos] and c<quatum):#revisa que no se estes leyendo una pagina fuera de la instruccion
            f.write(L[pos][line[pos]])
            line[pos]=line[pos]+1 #sigue leyendo la siguiente linea
            c=c+1
        c=0
        pos=pos+1 #buscamos el siguiente proceso
        if(pos==len(tamanopaginas)):
            for i in range(0,len(tamanopaginas)):
                bool=line[i]>=tamanopaginas[i] and bool #es la ultima linea del ultimo proceso
            if bool:
                break
            else:
                bool=True
                pos=0 #reiniciamos la lectura de proceso

def readinputfile(name):
    l=[]
    NumeroArchivos=0
    file1 = open(name,"r")
    c=0
    for i in file1:
        if c==0:
            pagesize=int(i)
            if (pagesize<>512 and pagesize<>1024 and pagesize<>2048):
                print "invalid range of values for page size in the file:"+filename
                c=0
                break
        elif c==1:
            memoryframe=int(i)
            if (memoryframe<>16 and memoryframe<>32 and memoryframe<>64):
                print "invalid range of values for memory size in the file:"+filename
                c=0
                break
        elif c==2:
            quatum=int(i)
        elif c==3:
            NumeroArchivos=int(i)
        elif c>3:
            l.append(str(i).replace("\n", ""))
        c=c+1
    file1.close
    if c<4:
        print "Change the file and run the program again"
    print '| Page Size\t| Memory Frame\t| Numero de Archivos\t|'
    print '|    '+str(pagesize)+'\t |  \t'+ str(memoryframe)+'\t  |  \t  '+str(NumeroArchivos)+' \t  |'
    print '-----------------------text files--------------------------------------------'
    stri="|"
    for i in range(NumeroArchivos):
        stri=stri+" "+l[i]+" |"
    print stri
    L=saveprocess(l,NumeroArchivos)
    Quatum(L,quatum)
    LF=ReadFile("temp.txt",pagesize)
    return memoryframe,LF

def CleanTable(L):
    for proc in L:
        proc.reference = 0
    return L

def SearchRefBit(L):
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

def SearchDirDato(L,P):
    ext1 =  False
    i = 0
    while not ext1 and i < len(L):
        ext1 = L[i].process == P.process and L[i].logicpage == P.di
        i+=1
    return  i-1, ext1

def SearchDirI(L,P):
    ext2 = False
    j = 0
    while not ext2 and j < len(L):
        ext2 = L[j].process == P.process and L[j].logicpage  == P.ddato
        j+=1
    return  j-1 ,ext2

def IsFull(Table):
    i = 0
    full = True
    while i<len(Table) and full:
        full = Table[i].process != -1
        i+=1

    return i-1  , full

def SearchClock(Table):
    m = 0
    for i in range(len(Table)):
        if Table[i].clock < Table[m].clock:
            m = i
    return m

def PageFault1(PageTable,id,direccion,dirty,contWritings,debug):
    pos_Aux_1 , full= IsFull(PageTable)
    if not full:
        PageTable[pos_Aux_1] = Page(id,direccion,1,dirty)
    else:
        pos_Aux_2 = SearchRefBit(PageTable)
        if debug:
            print cont,'\t',pos_Aux_2,'\t',PageTable[pos_Aux_2].process,'\t',PageTable[pos_Aux_2].logicpage,'\t',PageTable[pos_Aux_2].dirty
        contWritings+=PageTable[pos_Aux_2].dirty
        PageTable[pos_Aux_2] = Page(id,direccion,1,dirty)
    return contWritings

def PageFault2(PageTable,id,direccion,dirty,contWritings,cont,debug):
    pos_Aux_1 , full= IsFull(PageTable)
    if not full:
        PageTable[pos_Aux_1] = Page(id,direccion,1,dirty,cont)
    else:
        pos_Aux_2 = SearchClock(PageTable)
        if debug:
            print cont,'\t',pos_Aux_2,'\t',PageTable[pos_Aux_2].process,'\t',PageTable[pos_Aux_2].logicpage,'\t',PageTable[pos_Aux_2].dirty
        contWritings+=PageTable[pos_Aux_2].dirty
        PageTable[pos_Aux_2] = Page(id,direccion,1,dirty,cont)
    return contWritings


def Version1(L_Process,PageTable,debug):
    contInstruc = 1
    contFaults = contWritings = 0
    for processo in L_Process:
        pos_di, ext1 = SearchDirDato(PageTable,processo)
        if not ext1:
            contFaults+=1
            contWritings=PageFault1(PageTable,processo.process,processo.di,0,contWritings,debug)
        else:
            PageTable[pos_di] = Page(processo.process,processo.di,1,PageTable[pos_di].dirty)
        pos_dm, ext2 = SearchDirI(PageTable,processo)
        if not ext2:
            contFaults+=1
            contWritings=PageFault1(PageTable,processo.process,processo.ddato,processo.type,contWritings,debug)
        else:
            PageTable[pos_dm] = Page(processo.process,processo.ddato,1,PageTable[pos_dm].dirty or processo.type)
        
        if contInstruc == 200:
            PageTable = CleanTable(PageTable)
            contInstruc = 0
        contInstruc+=1

    return contFaults,contWritings

def Version2(L_Process,PageTable,debug):
    cont = 1
    contFaults = contWritings = 0
    for processo in L_Process:
        pos_di, ext1 = SearchDirDato(PageTable,processo)
        if not ext1:
            contFaults+=1
            contWritings=PageFault2(PageTable,processo.process,processo.di,0,contWritings,cont,debug)
        else:
            PageTable[pos_di] = Page(processo.process,processo.di,1,PageTable[pos_di].dirty or 0,cont)

        pos_dm, ext2 = SearchDirI(PageTable,processo)
        if not ext2:
            contFaults+=1
            contWritings=PageFault2(PageTable,processo.process,processo.ddato,processo.type,contWritings,cont,debug)

        else:
            PageTable[pos_dm] = Page(processo.process,processo.ddato,1,PageTable[pos_dm].dirty or processo.type,cont)
        cont+=1
    return contFaults,contWritings

def UpdatePageTable(L_Process,PageTable,version,debug):
    contInstruc = cont = 1
    contFaults = contWritings = 0
    if version == 1:
        contFaults,contWritings=Version1(L_Process,PageTable,debug)
    elif version == 2:
        contFaults,contWritings=Version2(L_Process,PageTable,debug)
    else:
        print "Error: Wrong Version."
    return contFaults, contWritings

def main(P):
    l = len(P)
    if l==3:
        P.append('0')
    if l >2 :
        memoryframe,L=readinputfile(P[1])
        print '---------------------------------------------------------------------------------'

		#(l,quatum)
        PT= PageTable(memoryframe)
        version=int(P[2])
        debug=int(P[3])
        c_Faults, c_Writings =UpdatePageTable(L,PT,version,debug)
        print '---------------------------------------------------------------------------------'
        print '| File Name\t| Lines\t\t| Version\t| Faults\t| Writings\t|'
        print '---------------------------------------------------------------------------------'
        print '|',P[1],'\t|',len(L),'\t|',P[2],'\t\t|',c_Faults,'\t\t|',c_Writings,'\t\t|'
        print '---------------------------------------------------------------------------------'
        print 'File Name: ',P[1],'\tVersion: ',P[2],'\tFaults: ',c_Faults,'\tWritings: ',c_Writings
    elif l == 2:
        print 'Error: Put the version number (options 1/2). '
    else:
        print " Call the program again with a valid input"

    #print L[0][1]
    #
main(sys.argv)
