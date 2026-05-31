# -*- coding: cp1252 -*
'''
Examen final - Intro a la Progra 0769
Facultad de Ingenieria
Universidad de San Carlos de Guatemala

1er Semestre 2014 - Seccion "N"
Ing. Ivan Rene Morales

 
'''


import socket, time,random


class juego(object):
    
    def __init__(self,tipo,tamX,tamY,maxBarcos,maxPosi,archivo,bot=-1):
        self.tamX=tamX 
        self.tamY=tamY
        self.archivo=archivo  
        self.maxBarcos=maxBarcos
        self.maxPosi=maxPosi
        self.listaBarcos=[]
        self.Nbarcos=0
        self.mapaPrincipal=self.creaMapaPrincipal(tamX,tamY)
        self.creaBarcos(archivo)
        self.mapaSecundario=self.creaMapaSecundario(tamX,tamY)
        self.tipo=tipo
        self.conex=None
        self.enchufe=None
        self.tamBuffer=20
        self.fijarY=-1
        self.BOT=bot
        self.ut=-1
        self.fijaX=0
        self.fijaY=0
        self.utX=0
        self.utY=0
        self.tiro=self.cTiro=self.res='000'
        self.GAME_OVER='XXX'
        self.ntBot=0
        self.botD=-1
        self.tirosBot=[]
        
    
    def serverConec(self,TCP_IP,TCP_PORT):#conecta al servidor
        self.enchufe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Abrir socket
        self.enchufe.bind((TCP_IP, TCP_PORT)) #Levantar el servidor
        self.enchufe.listen(1) #Esperar 1 conexion. Accion bloqueadora
        print 'Esperando conexion del cliente...\n\n'
        self.conex, addr = self.enchufe.accept()#Acepta la conexion
        print 'Conectado con: ', addr
        
    def clientConec(self,TCP_IP,TCP_PORT):#conecta al cliente
        self.conex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conex.connect((TCP_IP, TCP_PORT))
    
    def conectar(self,TCP_IP,TCP_PORT):#conecta dependiendo si se es cliente o servidor
        if self.tipo=='S':
            self.serverConec(TCP_IP,TCP_PORT)
        else:
            self.clientConec(TCP_IP,TCP_PORT)
        #while tipo not in ["S","C"]:
            #tipo=raw_input("Le gustaria ser (S)ervidor/(C)liente: ")

    def desconectar(self):
        self.conex.close()

    def imprimeMapas(self):
        print '   >>>>>>>> MAPA PRINCIPAL <<<<<<<<<<'
        self.mapaPrincipal.imprimeMapa()
        self.imprimeBarcos()
        print '   >>>>>>>> MAPA SECUNDARIO <<<<<<<<<'
        self.mapaSecundario.imprimeMapa()

    def pegarBarco(self,x,y):# Si hay barco en posicion (x,y) le pega y si es el ultimo tiro lo destruye 
        for i in range(len(self.listaBarcos)):
            if self.listaBarcos[i][0]<=x and x<=self.listaBarcos[i][0]+self.listaBarcos[i][3]-1 and self.listaBarcos[i][1]==y:
                print 'Barco en posicion ['+str(self.listaBarcos[i][0])+','+str(self.listaBarcos[i][1])+'] acaba de recibir un disparo\n'
                time.sleep(2)
                self.listaBarcos[i][2]-=1
                if self.listaBarcos[i][2]==0:
                    print 'Barco en posicion ['+str(self.listaBarcos[i][0])+','+str(self.listaBarcos[i][1])+'] acaba de ser destruido\n'
                    time.sleep(2)
                    self.Nbarcos-=1
    
    def procesa(self):
        if self.tiro!='000':            #si es la primera vez no procesa el tiro
            aux=self.tiro.split(',')
            tX=int(aux[0])
            tY=int(aux[1])
            objXY=self.mapaSecundario.buscaOxy(tX,tY)
            if self.res=='1' and objXY==-1: #ultimo tiro acerto
                print 'Su disparo acerto!'
                time.sleep(2)
                self.mapaSecundario.agregaObjetos(objeto(1,tX,tY))
            else:
                print 'Su disparo fallo!'                               #ultimo tiro fallo
                time.sleep(2)
                if objXY==-1:
                    self.mapaSecundario.agregaObjetos(objeto(2,tX,tY))
             
       #procesa contra tiro ct 
        aux=self.cTiro.split(',')
        ctX=int(aux[0])
        ctY=int(aux[1])
        iObj=self.mapaPrincipal.buscaOxy(ctX,ctY)  #busca objeto en el mapa
        if iObj!=-1: #encontro objeto
            simb=self.mapaPrincipal.objetos[iObj].getSimbolo()
            
            if simb=='0':# le dio a un barco
                self.pegarBarco(ctX,ctY)
                self.mapaPrincipal.objetos[iObj].setTipo(1)
                if self.Nbarcos==0: # Numero de barco ha acabado el juego termina
                    self.res=self.GAME_OVER
                else:
                    self.res='1'   #informa que el contra tiro ha pegado
        else:
            self.mapaPrincipal.agregaObjetos(objeto(2,ctX,ctY))
            self.res='0'
            
        
    
    def envia(self):#envia tiro de jugado como 'x,y'
        self.imprimeMapas()
        tiroX=tiroY=-1
        while (tiroX>self.tamX or tiroX<=0)and not self.BOT :
            tiro=raw_input('Ingrese la posicion X de su disparo(1-'+str(self.tamX)+') :')
            tiroX= int(tiro) if tiro.isdigit() else 0
        while (tiroY>self.tamX or tiroY<=0) and not self.BOT :
            tiro=raw_input('Ingrese la posicion Y de su disparo(1-'+str(self.tamX)+') :')
            tiroY= int(tiro) if tiro.isdigit() else 0
        self.tiro=str(tiroX)+','+str(tiroY)
        #Maneja el envio del BOT
        if self.BOT:
            self.tiraBot()
            tiroX=int(self.tiro.split(',')[0])
            tiroY=int(self.tiro.split(',')[1])
        self.conex.send(self.tiro)    
        #print 'Esperando respuesta.....\n'
        self.res=self.conex.recv(self.tamBuffer)
        if self.BOT and self.res =='1':
            self.utX=tiroX
            self.utY=tiroY
            if self.ntBot==0 and self.botD==-1:
                self.fijaX=tiroX
                self.fijaY=tiroY
            self.ut=1
        else:
            self.ut=-1
            if self.botD==1:
                self.ntBot=0
        '''if self.res=='1':
           # self.ntBot=0
            self.fijaX=tiroX
            self.fijaY=tiroY
            self.ut=0'''
        #return respuesta

    def recibe(self):
        self.imprimeMapas()
        print 'Esperando respuesta.....\n'
        self.cTiro=self.conex.recv(self.tamBuffer)
        self.procesa()
        
        self.conex.send(self.res)

    def comunica(self):
        if self.tipo=='S':#comunicacion para el servidor
            self.recibe()
            if self.res!=self.GAME_OVER:#el juego termino?
                self.envia()
                if self.res==self.GAME_OVER:#el juego termino?
                    self.imprimeMapas()
                    print 'Ha hundido todos los barcos de su contrincante. GANO el juego.'
                    time.sleep(3)
            else:
                self.imprimeMapas()
                print 'Todos sus barcos han sido hundidos. PERDIO el juego.'
                time.sleep(3)
        else:
            self.envia()#comunicacion para el cliente
            if self.res!=self.GAME_OVER:#el juego termino?
                self.recibe()
                if self.res==self.GAME_OVER:#el juego termino?
                    self.imprimeMapas()
                    print 'Todos sus barcos han sido hundidos. PERDIO el juego.'
                    time.sleep(3)
            else:
                tX=int(self.tiro.split(',')[0])
                tY=int(self.tiro.split(',')[1])
                self.mapaSecundario.agregaObjetos(objeto(1,tX,tY))
                self.imprimeMapas()
                print 'Ha hundido todos los barcos de su contrincante. GANO el juego.'
                time.sleep(3)
        
    def creaMapaPrincipal(self,tamX,tamY):     
        return mapa(tamX,tamY,[])
    
    def creaMapaSecundario(self,tamX,tamY):
        return mapa(tamX,tamY,[])

    def creaBarcos(self,nArchivo):#crea los objetos que conforman a los barcos y los agrega a mapaPrincipal
        try:
            archivo=open(nArchivo,'r')
        except IOError:
            print 'Debe crear un archivo llamado ExamenFinal.txt con la definicion de los barco'
            print 'Ejempo Definicion:\n3,4,5\nAqui se define un Barco en la posicion (x,y)=(3,4) de 5 unidades de largo'
        a=[]
        defBarcos=[]
        barcoX=barcoY=barcoTam=0
        posOcup=[]
        posObjetos=[]
        self.Nbarcos=Nobjetos=0
        for line in archivo:            #separa todas las lineas y las guarda
            
            a.append(line.split('\n')[0].split(','))    #quita las comas "," y los fines de linea "\n"

        archivo.close()    
        for i in range(len(a)):         #revisa todas las lineas del archivo
            posObjetos=[]
            bvalido=1 if len(a[i])==3 else 0
            for j in range(3):
                if not a[i][j].isdigit():   # son todos numero?/ quita cambio de linea
                   bvalido=0
                   print 'Definicion de Barco no valida en linea', i+1
                   time.sleep(1)
                   break
            if bvalido:
                barcoX=(int(a[i][0]))
                barcoY=(int(a[i][1]))
                barcoTam=(int(a[i][2]))
            if  bvalido and (barcoX<=self.tamX) and (barcoX+barcoTam-1<=self.tamX) and (barcoY<=self.tamY):  #restringe posicion y tamanho
                for k in range(barcoTam):#revisa si las posiciones de la definicion existen
                    pos=[barcoX+k,barcoY]
                    if not(pos in posOcup):
                        posObjetos.append(pos)
                    else:
                        bvalido=0
                        print 'Traslape del barco en la linea', i+1,' del archivo de barcos(ExamenFinal.Txt)' 
                        time.sleep(1)
                        break
            else:
                print 'Barco en la linea '+str(i+1)+' no cumple con las dimensiones'
                time.sleep(1)
                bvalido=0
            if bvalido:
                objetosBarco=[]                
                for l in range(len(posObjetos)):
                    obj=objeto(0,posObjetos[l][0],posObjetos[l][1])
                    self.mapaPrincipal.agregaObjetos(obj)
                    posOcup.append([posObjetos[l][0],posObjetos[l][1]])
                    Nobjetos+=1
                    if Nobjetos==self.maxPosi:
                     #   self.mapaPrincipal.agregaObjetos(objetosBarco)
                        break
                #self.mapaPrincipal.agregaObjetos(objetosBarco)
                self.listaBarcos.append([barcoX,barcoY,barcoTam,barcoTam])
                self.Nbarcos+=1    
            if self.Nbarcos==self.maxBarcos:
                break
              
                #self.listaBarcos.append([a[i][0],a[i][1],a[i][2]]
    """
    Aqui manejara la conexion LAN a traves de TCP, la creacion de mapas
    y los metodos del juego, en general.
    """

    def imprimeBarcos(self):#imprime que barcos tienen vida
        stringBarcos='Barcos Activos: '
        for i in range(len(self.listaBarcos)):
            if self.listaBarcos[i][2]!=0:
                stringBarcos=stringBarcos+'['+str(self.listaBarcos[i][0])+','+str(self.listaBarcos[i][1])+']'
        print stringBarcos+'\n'

    def tiraBot(self):# maneja los tiros que la computadora hace por su cuenta
        tiroBot='0'
        while tiroBot in self.tirosBot or tiroBot=='0': 
            if self.ut==-1 and (self.ntBot==0 or self.botD==1):
                tX=random.randint(1,self.tamX)
                tY=random.randint(1,self.tamY)
                self.ntBot=0
                self.botD=-1
            else:
                if self.ut==-1 and self.ntBot==1:
                    self.botD=1
                    self.utX=self.fijaX
                self.ntBot=1
                if self.botD+self.utX<1:
                    self.botD=1
                    self.ntBot=0
                    self.utX=self.fijaX
                tX=self.utX+self.botD
                tY=self.utY
                if tX>self.tamX:
                    tX=random.randint(1,self.tamX)
                    tY=random.randint(1,self.tamY)
            tiroBot=str(tX)+','+str(tY)
            if tiroBot in self.tirosBot:# and self.botD=-1:
                #self.ntBot=0
                #if self.botD==1:
                self.ut=-1
                #else:
                 #   self.botD=1
            
        self.tiro=tiroBot
        self.tirosBot.append(self.tiro)
        print 'Iiro a posicion ['+self.tiro+']'
        time.sleep(1)
        
    def ingresaBarcos(self):#ingreso de barcos en el archivo
        tamBarco=0
        X=0
        Y=0
        Sn=''
        n=0
        while n <=0 or n>self.maxBarcos:
            while not Sn.isdigit():
                Sn = raw_input('Con cuantas barcos desea su flota(max '+str(self.maxBarcos)+')?:')
            n=int(Sn)
            Sn=''
        f = open(self.archivo,'w')
        for i in range(n):
            tamBarco=0
            X=0
            Y=0
            print 'Barco # '+str(i+1)
            while X>self.tamX or X<=0:
                SX= raw_input('Ingrese posicion X:')
                X = int(SX) if SX.isdigit() else 0
            while Y>self.tamX or Y<=0:
                SY = raw_input('Ingrese posicion Y:')
                Y = int(SY) if SY.isdigit() else 0
            while (tamBarco+X-1>self.tamX) or (tamBarco<=0):
                StamBarco = raw_input('Ingrese longitud de su barco:')
                tamBarco = int(StamBarco) if StamBarco.isdigit() else 0
            barco=SX+','+SY+','+StamBarco+'\n'
           # barco=barco[:len(barco)-1]+'\n'
            f.write(barco)
        f.close()
        
        
        

class mapa(object):
    def __init__(self,tamX,tamY,objetos=[]):
        self.tamX = tamX #Tamanho inicial del mapa (columnas)
        self.tamY = tamY #Tamanho inicial del mapa (filas)
        self.objetos = objetos
        self.BORDE="+"
        self.espacio=" "
        
    def agregaObjetos(self,objetos): #Agregar mas objetos al mapa
        self.objetos.append(objetos)
   
    def posicionesY(self): #Devuelve posiciones Y de objetos
        pos=[]
        for i in range(len(self.objetos)):
            pos.append(self.objetos[i].getY())
        return pos


    def buscaOxy(self,x,y):#busca que haya un objeto en el mapa en la posicion (x,y) sin no existe devuelve -1
        encontrado=-1
        for i in range(len(self.objetos)):
            if self.objetos[i].getX()==x and self.objetos[i].getY()==y:
                encontrado=i
                break
        return encontrado
    
    def imprimeMapa(self):                      #Imprimir la abstraccion del mapa en pantalla
        posY=self.posicionesY()                 #posiciones Y de objetos
       # line=self.BORDE+(self.ESPACIO*(self.tamX-2))+self.BORDE #string a imprimir en pantalla
        for i in range(self.tamY+2):
            if (i==0)or(i==self.tamY+1):        # si se esta en los extremos se imprimen los delimitadores del juego
                print "   "+(self.BORDE+2*self.espacio)*(self.tamX+2)+"\n"
            else:
                line=" "+str(i)+" "+self.BORDE+(self.espacio*(3*(self.tamX+1)))#+self.BORDE#espacio#+self.BORDE
                line=line[:len(line)-1]+self.BORDE
                line=line if len(line)==(self.tamX+1)*3+4 else line[1:] 
                if i in posY:                   # si hay un objeto en la fila actual modifica line
                    for j in range(len(posY)):  # imprime todos los objetos existentes en la fila actual
                        ob=self.objetos[j]
                        if ob.getY() == i:
                            line=line[0:ob.getX()*3+3]+ob.getSimbolo()+line[ob.getX()*3+4:]#se concatena line con el simbolo del objeto y el resto de line         
                print line+'\n';# print "\n"
        line="      "                           #imprimir identificadores eje Y
        for i in range(self.tamX):
            line+=str(i+1)+(" "*(2/len(str(i+1))))#agrega 2 espacios si i<10 si no agrega 1 espacio
        print line,"\n"        
                
class objeto(object): #Un objeto puede ser el jugador, el tesoro u otra cosa
    def __init__(self,tipo,posX,posY):
        self.tipo = tipo #Tipo: Objeto, jugador, traza
        self.posX = posX #Posicion inicial en X
        self.posY = posY #Posicion inicial en Y
        self.tipo=tipo
        self.simbologia=["0","X","-"]
        self.simbolo=self.simbologia[tipo]
        
    def getX(self): #Devolver la posicion actual (X) del objeto
        return self.posX

    def getY(self): #Devolver la posicion actual (Y) del objeto
        return self.posY

    def setX(self,x): #Establecer posicion absoluta (X) del objeto
        self.posX=x

    def setY(self,y): #Establecer posicion absoluta (Y) del objeto
        self.posY=y

    def getTipo(self): #Que tipo de objeto soy (TESORO,JUGADOR,TRAZA)?
        return self.tipo

    def setTipo(self,tipo):#cambia el tipo
        self.tipo=tipo

    def getSimbolo(self):#devuelve el simbolo del objeto
        return self.simbologia[self.tipo]


def Instrucciones():
    print '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>INSTRUCCIONES<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n\n
    --Cuando ingresa las posiciones de los barcos tenga el cuidado de ponerlos en
    en correctas posiciones ya que estos se pueden traslapar, y tambien tener el cuidado
    de ingresar la longitud, ya que esta puede salir del area de juego.
        si ingresa alguna de las posiciones erroneamente al inicio del juego
        habra un mensaje informandole que barcos son invalidos.
    
    1.Escoger entre las opciones Humano y Computadora.
        Ud. tiene la opcion de escoger contra quién desea jugar, contra Computadora o
        Humano(algun compañero).
    2.Escoger entre servidor y cliente
        Si ud. escogio ser servidor su contricante debe de ser cliente o viceversa.
    3.Ingrese direccion IP
        Si la dirección IP no es valida, vuelva a ingresar IP correcta.
        Si desea salir ingrese X.
    A continuacion aparecera el tablero de juego, en el se muestra el mapa principal
    y el mapa secundario.
    El mapa principal contiene la posicion, tamaño de sus barcos, y los disparos
    recibidos.    
    El mapa secundario muestra los disparos hechos al contrincante.
    4.Empezar el juego
        Ingrese la posicion x,y de su disparo.
    5.Cuando uno de los dos jugadores haya ganado, el juego se lo mostrara.

    representaciones:
                    los barcos estan representados por 0.
                    los disparos acertados estan representados por x.
                    los disparos fallidos estan representados por -.'''
def menu():
    ja=juego('C',10,10,4,15,'ExamenFinal.txt',0)
    op=''
    while not op in ['4','X']:
        print '\n\n\n'+'>'*33+'  '+'<'*37
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BATTLESHIP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print '>'*33+'  '+'<'*37+'\n\n'
        print '1.Ingresar Barcos'
        print '2.Jugar'
        print '3.Ver Instrucciones'
        print '4.Salir\n'
        op=raw_input('OPCION :')
        if op=='2':
            jugar()
        if op=='1':
            ja.ingresaBarcos()
        if op=='3':
            Instrucciones()
                     
    
def jugar():
    global game
    tipo=''
    ip_valido=0
    dir_ip=''
    aux=''
    while not aux in ['1','0']:
        aux=raw_input('Desea jugar como Humano(0)/Computadora(1):')
    bot=int(aux)
    while not(tipo in ['S','C']):
        tipo=raw_input('Jugar como (S)ervidor/(C)liente? :')
    game=juego(tipo,10,10,4,15,'ExamenFinal.txt',bot)
    while not ip_valido  and dir_ip!='X':
        dir_ip=raw_input('Ingrese IP :')
        try:
            game.conectar(dir_ip,7408)
            ip_valido=1
        except socket.error:
            print 'IP no valido (ingrese X para salir)'
            ip_valido=0
    
    if dir_ip!='X':
        while not (game.res==game.GAME_OVER):
            game.comunica()
        game.desconectar()
 

menu()
