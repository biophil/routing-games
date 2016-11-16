# -*- coding: utf-8 -*-

from operator import itemgetter
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import DataError, DatabaseError, InterfaceError
import general.Game as gm
import matplotlib.pyplot as plt
import farokhiHelpers as fh
import datetime
import time


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
    
TABLES['fsimsfixed'] = (
    "CREATE TABLE `fsimsfixed` ("
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
    "  `corrected_version_of` INT(11) NOT NULL,"
    "  PRIMARY KEY (`sim_no`),"
    "  KEY `poa1` (`poa1`),"
    "  FOREIGN KEY (net_no) REFERENCES fnets(net_no),"
    "  FOREIGN KEY (corrected_version_of) REFERENCES sims(sim_no)"
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
    
    
    
def getDBPoas(table,plotIt=True,config=MYSQL_CONFIG_LEARNING) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    query = "SELECT k1,k2,k3,k4,k5,k6,poa1,poa2,poa3,poa4,poa5,poa6,sim_no FROM "+table+" WHERE "
    query += "(poa1>=1) AND "
    query += "(poa2>=1 OR poa2 IS NULL) AND "
    query += "(poa3>=1 OR poa3 IS NULL) AND "
    query += "(poa4>=1 OR poa4 IS NULL) AND "
    query += "(poa5>=1 OR poa5 IS NULL) AND "
    query += "(poa6>=1 OR poa6 IS NULL) "
    cursor.execute(query)
    kk = []
    poas = []
    sim_nos = []
    for row in cursor :
        k = []
        poa = []
        for pair in zip(row[0:6],row[6:12]):
            if pair[0] is not None and pair[1] is not None :
                k.append(pair[0]) 
                poa.append(pair[1])
        kk.append(k)
        poas.append(poa)
        sim_nos.append(row[-1])
    if plotIt :
        for k,poa in zip(kk,poas) :
            plt.plot(k,poa)
    cursor.close()
    cnx.close()
    return kk,poas,sim_nos

def plotRes(res,plotMethod=plt.plot) :
    # res should be wher's returned by getDBPoas()
    for k,poa in zip(res[0],res[1]):
        plotMethod(k,poa)

def buildNetFromDB(net_no,rr,SS,netType,config=MYSQL_CONFIG_LEARNING) :
    # netType is either 'p' or 'f'
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    if netType == 'p' :
        query1 = "SELECT * FROM pnets WHERE net_no=%s"
    elif netType == 'f' :
        query1 = "SELECT * FROM fnets WHERE net_no=%s"
    else :
        print('invalid netType.')
        return None
    cursor.execute(query1,(net_no,))
    edge_nos = cursor.fetchone()[1:]
    # get used edge indices:
#    edgeList = [(i+1,e) for i,e in enumerate(edge_nos) if e is not None]
#    print(edge_nos)
    query2 = "SELECT edge_no,const,coeff,power FROM edges WHERE edge_no IN("
    query2 += ",".join(['%s']*len(edge_nos)) + ")"
    cursor.execute(query2,edge_nos)
    # now for each edge, build a latency function.
    # build a dict from the query result: edge_no:(latparams) kv pairs
    latparams = {}
    for edge_no,const,coeff,power in cursor :
        latparams[edge_no] = (const,coeff,power)
    edgeList = []
    latencies = []
    net = None
    for i,edge_no in enumerate(edge_nos) :
        if edge_no is not None :
            edgeList.append(i+1)
            latencies.append(buildMonomialLatF(latparams[edge_no]))
    if netType == 'p' :
        net = gm.SymmetricParallelNetwork(latencies,rr,SS)
    elif netType == 'f' :
        net = gm.FarokhiGame(edgeList,latencies,rr,SS)
    else :
        print('invalid netType')
        return None
    cursor.close()
    cnx.close()
    return net
    
def buildMonomialLatF(latparams) :
    # latparams is iterable of (const,coeff,power)
    return lambda x : latparams[0] + latparams[1]*(x**latparams[2])
    
        
def setNetworkPopulation(net,rr,SS) :
    net.setPopMasses(rr)
    net.setSensitivities(SS)
    return net
    
def getNetworkFromSim(sim_no,table,config=MYSQL_CONFIG_LEARNING) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    query1 = "SELECT net_no,r1,r2,r3,S1,S2,S3 FROM " + table + " WHERE sim_no=%s"
    cursor.execute(query1,(sim_no,))
    sim_res = cursor.fetchone()
    net_no = sim_res[0]
    rr = sim_res[1:4]
    SS = sim_res[4:]
    if table == 'sims' :
        return buildNetFromDB(net_no,rr,SS,netType='f')
    elif table == 'psims' :
        return buildNetFromDB(net_no,rr,SS,netType='p')
    else : 
        print("You didnt specify a table that I know. I don\'t honestly know how we even got here.")
        return None
    
def getLatencies(net_no,r1,r2,r3,netType,config=MYSQL_CONFIG_LEARNING) :
    # returns optimal and untolled latencies for net; pulls from db if they're there
    # output: Lopt, Luninf, optiter, uninfiter (a value of -1 indicates nonconvergence)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    table = 'fsimsfixed'
    if netType == 'p' :
        table = 'psimsfixed'
    query = "SELECT Lopt,Luninf,optiter,uninfiter FROM " + table + " WHERE "
    query += "net_no=%s AND r1=%s AND r2=%s AND r3=%s LIMIT 1"
    cursor.execute(query,(net_no,r1,r2,r3))
    row = cursor.fetchone()
    if row is None : # if we haven't done this yet, go ahead and compute
        return computeLatencies(net_no,r1,r2,r3,netType,config)
    else: 
        net = buildNetFromDB(net_no,[r1,r2,r3],[1,1,1],netType,config=config)
        return net,row[0],row[1],row[2],row[3]
    
def computeLatencies(net_no,r1,r2,r3,netType,config=MYSQL_CONFIG_LEARNING) :
    Lopt = -1
    Luninf = -1
    optiter = -1
    uninfiter = -1
    net = buildNetFromDB(net_no,[r1,r2,r3],[1,1,1],netType,config=config)
    net.setSensitivities([1,1,1])
    fh.updateNetworkTollsDPR(net,1,fh.buildSMCDPR) # get the opt flows
    net.totalMass = sum([r1,r2,r3])
    LL,code = fh.learnIt(net,rt=1e-7)
    if code == 1 :
        Lopt = LL[-1]
        optiter = len(LL)
    fh.updateNetworkTollsDPR(net,0,fh.buildUniversalTollDPR)
    LL,code = fh.learnIt(net,rt=1e-7) # now get the uninfluenced NF
    if code == 1 :
        Luninf = LL[-1]
        uninfiter = len(LL)
    return net,Lopt,Luninf,optiter,uninfiter
    
        
        
def checkSims(table,numToCheck=1,config=MYSQL_CONFIG_LEARNING,iterLim=10000) :
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    netType = ''
    KK = [0.5,1,2,5,10]
    if table == 'sims' :
        netType = 'f'
        updateTable = 'fsimsfixed'
    elif table == 'psims' :
        netType = 'p'
        updateTable = 'psimsfixed'
    else :
        print('bad table specification')
        return None
    for i in range(0,numToCheck) :
        query = "SELECT sim_no,net_no,r1,r2,r3,S1,S2,S3 from " + table + " WHERE "
        query += "uninfiter<" + str(iterLim) + " AND optiter<"+ str(iterLim)
        query += " AND verified=FALSE AND correct_version_of IS NULL LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            print('no more records!')
            return 1
#        print(result)
        sim_no = result[0]
        net_no = result[1]
        r1,r2,r3 = result[2:5]
        S1,S2,S3 = result[5:]
        print('Getting to work on simulation number ' + str(sim_no))
        # somewhere along the line, need a method to check if we've already tried computing
        # this net and failed; if that's the case, we should just abort.
        net,Lopt,Luninf,optiter,uninfiter = getLatencies(net_no,r1,r2,r3,netType)
        if optiter == -1 or uninfiter == -1 :
            # did not converge; flag this in original table and move on
            print('flagged net '+ str(net_no) +' from sim ' + str(sim_no))
            flagQuery = "UPDATE " + table + " SET correct_version_of=1 "
            flagQuery += "WHERE net_no=%s AND r1=%s AND r2=%s "
            flagQuery += "AND r3=%s"
            cursor.execute(flagQuery,(net_no,r1,r2,r3))
            cnx.commit()
        else :
            poas = [Luninf/Lopt]
            updateKK = [0]
            net.setSensitivities([S1,S2,S3])
            for k in KK :
                fh.updateNetworkTollsDPR(net,k,fh.buildUniversalTollDPR)
                LL,code = fh.learnIt(net,rt=1e-7)
                if code == 1 :
                    poas.append(LL[-1]/Lopt)
                    updateKK.append(k)
            insertQ = "INSERT INTO "
            insertQ += updateTable +" (net_no,r1,r2,r3,S1,S2,S3,"
            insertQ += "Lopt,Luninf,optiter,uninfiter,poa1,poa2,poa3,"
            insertQ += "poa4,poa5,poa6,k1,k2,k3,k4,k5,k6,corrected_version_of) "
            insertQ += "VALUES (" + ','.join(["%s"]*24) + ")"
            data = (net_no,r1,r2,r3,S1,S2,S3,)
            data += (Lopt,Luninf,optiter,uninfiter,)
            data += tuple(poas)
            data += (None,)*(6-len(poas))
            data += tuple(updateKK)
            data += (None,)*(6-len(updateKK))
            data += (sim_no,)
            try :
                cursor.execute(insertQ,data)
            except DataError :
                print('data error. bad query: ' + insertQ)
                print('bad data: ' + str(data))
            cnx.commit()
            # finally, mark this particular simulation as fixed
            print('simulation ' + str(sim_no) + " fixed.")
            fixedQ = "UPDATE " + table + " SET verified=TRUE WHERE "
            fixedQ += "sim_no=%s"
            cursor.execute(fixedQ,(sim_no,))
            cnx.commit()
    cursor.close()
    cnx.close()



def runAllNight() :
    timeToStop = datetime.datetime(2016,11,16,7,0,0)
    done = None
    try :
        while datetime.datetime.now()<timeToStop and done is None:
            print('strrrrrrectch.... ok back to work!')
            start = time.time()
            done = checkSims('sims')
            end = time.time()
            tosleep = round(end-start)
            toprint = "That took " + str(round(end-start)) + " seconds, "
            toprint += "so that\'s how long I\'ll sleep to cool down..."
            print(toprint)
            print()
            time.sleep(tosleep)
    except KeyboardInterrupt :
        print("And Done.")
    
    
    
    
    
    
    
    