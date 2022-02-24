from datetime import datetime

class ExamException(Exception):
  pass

class CSVTimeSeriesFile():
  def __init__(self, name):
    self.name= name
  #inizializzazione class
    if not isinstance(self.name,str):
      raise ExamException('Errore, l\'oggetto inserito non è un file')
  #controllo se nomefile inserito è una stringa
    try:
      open(self.name, 'r')
    except:
      raise ExamException('Errore, il file non è leggibile')
  #controllo apertura file
    

  def get_data(self):
  #metodo classe. creazione lista liste.
    time_s= []
  #dichirazione lista liste vuota
    my_file= open(self.name,'r')
  #apro file
   
    nw_line1=[]
  #lista controllo ordine
    nw_line2=[]
  #lista appoggio
    for line in my_file:
    #scorrimento file
      if len(line.strip())==0:
      #controllo linea vuota
        continue
      else:
        splitted_line= line.split(',')
      #divido linea file alla virgola 
        if splitted_line[0]!='date':
        #controllo parametro!=data
          l=splitted_line[0].split('-')
        #pulisco linea splittata per controllo

        #controllo valori==valori aspettati

          if l[0].isdigit()==False: 
          # primo elemento splittato != numero 
            splitted_line=['0']
          #sostituisco zero
            nw_line2.append(splitted_line)
          #aggiungo lista appoggio
            continue
          #passo iterazione successiva 
          else:
          #controllo 1949<valore anno<1960
            L=int(l[0])
            if (L<1949)==True or (L>1960)==True:  
              splitted_line=['0']
              nw_line2.append(splitted_line)
              continue
        
          if l[1].isdigit()==True:
          # secondo elemento splittato == numero 
            L1=int(l[1])
          #controllo 1<valore mese<12
            if (L1<1)==True or (L1>12)==True:
              splitted_line=['0']
              nw_line2.append(splitted_line)
              continue
            else:
              #elemento rispetta condizioni
              #appendo valore-->lista controllo & lista appoggio
              nw_line2.append(splitted_line)
              nw_line1.append(splitted_line)
          else:
          # secondo elemento splittato != numero 
            splitted_line=['0'] 
          #appendo zero a lista appoggio 
            nw_line2.append(splitted_line)
            continue
    
    #check lista controllo ==> ordine temporale

    nw_line_ord=[]
    #inizilizzazione lista da ordinare
    nw_line_ord=nw_line1[:]
    #creo copia lista controllo
    nw_line_ord.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m'))
    #ordino lista momentanea
  
    if not nw_line_ord==nw_line1:
    #controllo se lista ordinata == lista controllo
      raise ExamException('Errore, file non ordinato')
    
    
    n=[]
    #seconda lista appoggio
    for element in nw_line2:
    #scorrimento prima lista appoggio
      if element!=['0']:
      #pulizia valore passeggeri (new line)
        d=element[1].strip('\n')
      #split anno da mese 
        element=element[0].split('-')
      #aggiungo valore pulito 
        element.append(d)
      
        #controllo valore aspettato
        
        if (len(element[2])<3)==True:  
        #valore passengers>= ordine centinaia
          element=['0'] 
        #condizione non rispettata ==>inizializzazione a '0'
        else:
          if element[2].isdigit()==True:
          #controllo valore numerico
          #trasformazione intero
            element[2]=int(element[2])  
          else:
            element=['0']
          #condizione non rispettata ==>inizializzazione a '0'
          n.append(element)
      else:
      #presenza zero==>appendo elemento
        n.append(element)
    #assegno a time_s valore lista appoggio
    time_s=n[:]
  
    #controllo assenza duplicati
  
    for(i,element) in list(enumerate(time_s)):
    #scorrimento lista liste
      if element!=['0']:
      #check elemento diverso '0'
        l=str(element)
      #variabile appoggio==elemento
        I=[]
      #lista indici elementi
        for (j,element) in list(enumerate(time_s)):
        #scorro nuovamente lista liste
          l_s=str(element)
        #memorizzo valore corrente 
          if l==l_s:
          #se uguaglianza variabile precedente, appendo indice alla lista
            I.append(j)
        #terminato scorrimento lista liste
        for element in I:
        #controllo elementi lista indici 
        #check indice == indice aspettato
          if element!=i:
          #ugualianza non verificata ==> eccezione
            raise ExamException('Errore, file contiene duplicati')
      else:
      #salto iterazione successiva
        continue
    
    #creazione lista 12 liste --> 1 lista per anno
    
    y=[]
    #lista supporto-year
    nw_time_s=[]
    #lista_liste_2
    cont=-1
    #variabile contatore ==>posizione corrente
    Y=0 
    #anno corrente
    m=12 
    #mese corrente
    for (j,element) in list(enumerate(time_s)):
    #iterazione lista_liste principale
      if element!=['0']:
      #controllo elemento!=0
        if element[0]==Y:
        #check anno corrente == anno sottolista precedente
          if int(element[1])==m+1:
          #check continuità mesi
            nw_time_s[cont].append(element[2])
          #appendo elemento corrente 
          #lista indice cont in nw_time_s
            m+=1
          #incremento mese
          else:
          #caso assenza mesi
            while m!=(int(element[1])-1):
            #iterazione fino a mese precedente
              nw_time_s[cont].append(0)
            #aggiunta x '0' ==> x= mesi mancanti
              m+=1 
          #posizione mese corrente  
            m=int(element[1])
          #aggiunta valore
            nw_time_s[cont].append(element[2])        
        else:
        #caso anno corrente != anno sottolista precedente
          if m!=12:
          #check anno precedente --> 1 valore per mese
            while m!=12:
            #aggiunta x '0' ==> x= mesi mancanti
              nw_time_s[cont].append(0)
              m+=1

          if int(element[1])==1:
          #check mese == primo anno
            Y=element[0]
          #aggiorno anno corrente
            y.extend([element[0],element[2]])
          #appendo anno e valore a lista appoggio
            nw_time_s.append(y)
          #appendo lista year==> lista liste
            cont+=1
          #aggiorno contatore==>nuova posizione lista
            y=[]
          #inizializzaione lista vuota
            m=1
          #primo mese anno
          else: 
          #caso mese corrente != primo anno  
            Y=element[0]
            y.append(element[0])
            nw_time_s.append(y)
          #appendo lista year[anno corrente]-->lista liste
            cont+=1
            y=[]
            m=1
          #primo mese anno
            while m!=(int(element[1])):
            #aggiunta x '0' ==> x= mesi mancanti
              nw_time_s[cont].append(0)
              m+=1
            #aggiunta valore mese corrente
            nw_time_s[cont].append(element[2])       
      else:
      #caso elemento=='0'
      #'0' prima posizione 
        if j==0:
        #anno aspettato
          Y='1949'
        #creazione lista 
          y.extend([Y,int(element[0])])
          nw_time_s.append(y)
          cont+=1
          m=1
          y=[]
        #iterazione successiva
          continue
      #mesi anno non ancora terminati
        if m<12:
          nw_time_s[cont].append(int(element[0]))
        #appendo zero
          m+=1
        else:
        #mesi terminati
          if (int(Y)+1)<=1960:
          #caso anno corrente!= utlimo anno dataset  
            Y=str(int(Y)+1)
            #aggiornamento variabile anno corrente
            #creazione lista
            y.extend([Y,int(element[0])])
            nw_time_s.append(y)
            cont+=1
            m=1
            y=[]
    #inizializzo lista originale come vuota    
    time_s=[]
    #creazione copia lista appoggio ==>lista_liste_originale 
    time_s=nw_time_s[:]
    return (time_s)


def detect_similar_monthly_variations(time_s, years):
  #controllo elementi years ==> due numeri
  
  cont=0
  for element in years:
    cont+=1
    if str(element).isdigit()==True:
      continue
    else:
      raise ExamException('Errore, valori years non validi')
  
  #controllo numeri valori
  
  if cont!=2:
    raise ExamException('Errore, valori years non validi')
  
  #controllo consecutività valori
  
  if int(years[1])!=int(years[0]+1):
    raise ExamException('Errore, valori years non validi')

  #ricerca indici valori years

  s=-1
  e=-1
  #variabili appoggio indici
  for(i,element) in (enumerate(time_s)):
    if element[0]==str(years[0]):
      s=i
      continue
    if element[0]==str(years[1]):
      e=i
      continue
  #lista indici
  l_ind=[]
  #aggiunta indici valori
  l_ind.extend([s,e])

  Prec=[]
  Succ=[]
  #liste anno analizzato
  cont=0
  #contatore elemento
  for element in l_ind:
    V=[]
  #lista appoggio
    J=element
  #indice primo valore
    i=1
    cont+=1
    while i!=12:
    #creazione lista variazioni
      if time_s[J][i]!=0 and time_s[J][i+1]!=0:
        if time_s[J][i]<time_s[J][i+1]:
          var=time_s[J][i+1]-time_s[J][i]
        else:
          var= time_s[J][i]-time_s[J][i+1]
        V.append(var)
      #aggiungo variazione mese (x+1)-(x), (se x+1>x)
      else:
      #caso elemento==0 --> variazione non calcolabile
        V.append('F')
      #iterazione per intero anno
      i+=1
    if cont==1:
    #primo valore years
      Prec=V[:]
    else:
    #valore successivo
      Succ=V[:]

  #creazione lista check variazioni simili ==> True or False

  TF=[]
  i=0
  while i!=11:
  #iterazione su 11 variazioni
    if Prec[i]!='F' and Succ[i]!='F':
    #check possibilità paragone
      v=1
    #valore tolleranza somiglianza variazioni
      flag=1
    #variabile True or False
      while v!=3:
      #caso valori uguali
        if Prec[i]==Succ[i]:
          flag=0
          break
        else:
        #caso precedente maggiore successivo
          if Prec[i]>Succ[i]:
            if (Prec[i]-v)==Succ[i]:
            #check uguali a meno della var tolleranza
              flag=0
              break
          else:
          #caso precedente minore successivo
            if (Prec[i]+v)==Succ[i]:
            #check uguali con aggiunta della var tolleranza
              flag=0
              break
        v+=1  
      #controllo variabile falg
      if flag==0:
        TF.append('True')
      else:
        TF.append('False')
    else:
    #caso impossibilità variazione
      TF.append('False')
    i+=1
  return TF