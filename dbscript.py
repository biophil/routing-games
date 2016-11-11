# -*- coding: utf-8 -*-

from operator import itemgetter
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import DataError, DatabaseError, InterfaceError
import general.Game as gm


MYSQL_CONFIG_LEARNING = {
  'user': 'bots',
  'password': 'thelcdpassword',
  'host': '127.0.0.1',
  'database': 'learning',
  'raise_on_warnings': True,
}
    
TABLES = {}
TABLES['fnets'] = (
    "CREATE TABLE `fnets` ("
    "  `net_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `edge01` int,"
    "  `edge02` int,"
    "  `edge03` int,"
    "  `edge04` int,"
    "  `edge05` int,"
    "  `edge06` int,"
    "  `edge07` int,"
    "  `edge08` int,"
    "  `edge09` int,"
    "  `edge10` int,"
    "  `edge11` int,"
    "  `edge12` int,"
    "  `edge13` int,"
    "  PRIMARY KEY (`net_no`),"
    "  FOREIGN KEY (edge01) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge02) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge03) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge04) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge05) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge06) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge07) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge08) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge09) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge10) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge11) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge12) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge13) REFERENCES edges(edge_no)"
    ") ENGINE=InnoDB")

TABLES['pnets'] = (
    "CREATE TABLE `pnets` ("
    "  `net_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `edge01` int,"
    "  `edge02` int,"
    "  `edge03` int,"
    "  `edge04` int,"
    "  `edge05` int,"
    "  `edge06` int,"
    "  `edge07` int,"
    "  PRIMARY KEY (`net_no`),"
    "  FOREIGN KEY (edge01) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge02) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge03) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge04) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge05) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge06) REFERENCES edges(edge_no),"
    "  FOREIGN KEY (edge07) REFERENCES edges(edge_no)"
    ") ENGINE=InnoDB")

TABLES['edges'] = (
    "CREATE TABLE `edges` ("
    "  `edge_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `const` DOUBLE NOT NULL,"
    "  `coeff` DOUBLE NOT NULL,"
    "  `power` int NOT NULL DEFAULT 4,"
    "  PRIMARY KEY (`edge_no`)"
    ") ENGINE=InnoDB")
    
TABLES['sims'] = (
    "CREATE TABLE `sims` ("
    "  `sim_no` int NOT NULL AUTO_INCREMENT,"
    "  `net_no` int(11) NOT NULL,"
    "  `r1` DOUBLE NOT NULL,"
    "  `r2` DOUBLE NOT NULL,"
    "  `r3` DOUBLE NOT NULL,"
    "  `S1` DOUBLE NOT NULL,"
    "  `S2` DOUBLE NOT NULL,"
    "  `S3` DOUBLE NOT NULL,"
    "  `Lopt` float DEFAULT NULL,"
    "  `Luninf` float DEFAULT NULL,"
    "  `optiter` int DEFAULT NULL,"
    "  `uninfiter` int DEFAULT NULL,"
    "  `poa1` float DEFAULT NULL,"
    "  `poa2` float DEFAULT NULL,"
    "  `poa3` float DEFAULT NULL,"
    "  `poa4` float DEFAULT NULL,"
    "  `poa5` float DEFAULT NULL,"
    "  `poa6` float DEFAULT NULL,"
    "  `k1` float DEFAULT NULL,"
    "  `k2` float DEFAULT NULL,"
    "  `k3` float DEFAULT NULL,"
    "  `k4` float DEFAULT NULL,"
    "  `k5` float DEFAULT NULL,"
    "  `k6` float DEFAULT NULL,"
    "  PRIMARY KEY (`sim_no`),"
    "  KEY `poa1` (`poa1`),"
    "  FOREIGN KEY (net_no) REFERENCES fnets(net_no)"
    ") ENGINE=InnoDB")

TABLES['psims'] = (
    "CREATE TABLE `psims` ("
    "  `sim_no` int NOT NULL AUTO_INCREMENT,"
    "  `net_no` int(11) NOT NULL,"
    "  `r1` DOUBLE NOT NULL,"
    "  `r2` DOUBLE NOT NULL,"
    "  `r3` DOUBLE NOT NULL,"
    "  `S1` DOUBLE NOT NULL,"
    "  `S2` DOUBLE NOT NULL,"
    "  `S3` DOUBLE NOT NULL,"
    "  `Lopt` float DEFAULT NULL,"
    "  `Luninf` float DEFAULT NULL,"
    "  `optiter` int DEFAULT NULL,"
    "  `uninfiter` int DEFAULT NULL,"
    "  `poa1` float DEFAULT NULL,"
    "  `poa2` float DEFAULT NULL,"
    "  `poa3` float DEFAULT NULL,"
    "  `poa4` float DEFAULT NULL,"
    "  `poa5` float DEFAULT NULL,"
    "  `poa6` float DEFAULT NULL,"
    "  `k1` float DEFAULT NULL,"
    "  `k2` float DEFAULT NULL,"
    "  `k3` float DEFAULT NULL,"
    "  `k4` float DEFAULT NULL,"
    "  `k5` float DEFAULT NULL,"
    "  `k6` float DEFAULT NULL,"
    "  PRIMARY KEY (`sim_no`),"
    "  KEY `poa1` (`poa1`),"
    "  FOREIGN KEY (net_no) REFERENCES pnets(net_no)"
    ") ENGINE=InnoDB")


    
def createTables(config=MYSQL_CONFIG_LEARNING) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    times = 0
    while times < 1 :
        for table in TABLES:
            try:
                print("Creating table {}: ".format(table), end='')
                cursor.execute(TABLES[table])
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        times +=1
    cursor.close()
    cnx.close()

try :
    len(nets)  # general.Game : net_id key/val pairs
except NameError :
    nets = {}

def addEdgeToDB(edge,config=MYSQL_CONFIG_LEARNING) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
#    deg = 4
    const = edge.latency(0)
    coeff = edge.latency(1)-const
    insertQ = "INSERT INTO edges (const,coeff) VALUES(%s,%s)"
    cursor.execute(insertQ,(const,coeff))
    cnx.commit()
    lastid = cursor.lastrowid
    cursor.close()
    cnx.close()
    return lastid

    
    
def numstr(num) :
    if len(str(num)) < 2:
        return '0'+str(num)
    else :
        return str(num)
        
elistFarokhi = '('+','.join(['edge'+numstr(i) for i in range(1,14)])+')'
elistParallel = '('+','.join(['edge'+numstr(i) for i in range(1,8)])+')'

def addFNetToDB(net,config=MYSQL_CONFIG_LEARNING) :
    # adds a Farokhi network to the DB
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    possibleEdgeNames = ['e'+str(i) for i in range(1,14)]
    actualEdgeDict = {e.name:e for e in net.edges}
    edgesToAdd = []
    for ename in possibleEdgeNames :
        if ename in actualEdgeDict :
            edgesToAdd.append(addEdgeToDB(actualEdgeDict[ename]))
        else :
            edgesToAdd.append(None)
    insertQ = "INSERT INTO fnets "+elistFarokhi+" VALUES(" + ','.join(['%s']*13)+')'
    cursor.execute(insertQ,tuple(edgesToAdd))
    cnx.commit()
    netid = cursor.lastrowid
    cursor.close()
    cnx.close()
    return netid

def addPNetToDB(net,config=MYSQL_CONFIG_LEARNING) :
    # adds a symmetric parallel net to the DB
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    possibleEdgeNames = ['e'+str(i) for i in range(1,8)]
    actualEdgeDict = {e.name:e for e in net.edges}
    edgesToAdd = []
    for ename in possibleEdgeNames :
        if ename in actualEdgeDict :
            pass
            edgesToAdd.append(addEdgeToDB(actualEdgeDict[ename]))
        else :
            edgesToAdd.append(None)
    insertQ = "INSERT INTO pnets "+elistParallel+" VALUES(" + ','.join(['%s']*7)+')'
    cursor.execute(insertQ,tuple(edgesToAdd))
    cnx.commit()
    netid = cursor.lastrowid
    cursor.close()
    cnx.close()
    return netid
    
def countSims(record) :
    ct = 0
    for rec in record :
        if rec['opt converged'] and rec['uninf converged'] :
            ct += 1
            ct += len(rec['sensitivities'])
    return ct

def addRecordToDB(record,netType,config=MYSQL_CONFIG_LEARNING) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    simtabname = ''
    if netType == 'Farokhi' :
        simtabname = 'sims'
    elif netType == 'SymmParallel' :
        simtabname = 'psims'
    for rec in record :
        net = rec['net']
        net_id = -1
        if net in nets :
            net_id = nets[net]
        else :
            if netType == 'Farokhi' :
                net_id = addFNetToDB(net) # returns the net_id for db fk
            elif netType == 'SymmParallel' :
                net_id = addPNetToDB(net) # returns the net_id for db fk
            else :
                print('Not either kind of network we\'re ready for')
                break
            nets[net] = net_id
        if rec['opt converged'] and rec['uninf converged'] :
            Lopt = rec['Lopt']
            Luninf = rec['Luninf']
            try :
                optiter = rec['num iter to opt']
            except KeyError :
                optiter = 0
            try :
                uninfiter = rec['num iter to uninf']
            except KeyError :
                uninfiter = 0
            r1 = rec['popmass'][0]
            r2 = rec['popmass'][1]
            r3 = rec['popmass'][2]
            for sense in rec['sensitivities'] :
                ss = sense['pop']
                poas = sense['PoA']
                kk = sense['kk']
#                print(simtabname)
                insertQ = "INSERT INTO "
                insertQ += simtabname +" (net_no,r1,r2,r3,S1,S2,S3,"
                insertQ += "Lopt,Luninf,optiter,uninfiter,poa1,poa2,poa3,"
                insertQ += "poa4,poa5,poa6,k1,k2,k3,k4,k5,k6) "
                insertQ += "VALUES (" + ','.join(["%s"]*23) + ")"
                data = (net_id,r1,r2,r3,ss[0],ss[1],ss[2],)
                data += (Lopt,Luninf,optiter,uninfiter,)
                data += tuple(poas)
                data += (None,)*(6-len(poas))
                data += tuple(kk)
                data += (None,)*(6-len(kk))
                try :
                    cursor.execute(insertQ,data)
                except DataError :
                    print('data error. bad query: ' + insertQ)
                    print('bad data: ' + str(data))
                cnx.commit()
    
    
    








    
    
    
    
    
    
    
    
    