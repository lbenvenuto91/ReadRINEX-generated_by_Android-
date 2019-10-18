



import pandas as pd
from datetime import datetime, date, timedelta
import time
from progressbar import ProgressBar
from tqdm import tqdm
import sqlite3
import mmap


def get_num_lines(dir, file):
    lines = 0
    with open(dir + file) as handler:
    
        for i, line in  enumerate(handler):
                #Check for a Timestamp lable
                if '> ' in line:
                    lines+=1
   
    return lines


def readObs(dir, file, table_name):
    
    '''
    Function to read obs from a RINEX file (generated with GEO++ RINEX Logger app)
    returns a list of query which must be used to upload the data to a sqlite DB
    the list contains also the field code_minus_phase: this parameter is calculated within this function.

    '''
    lambda_l1= 0.1905 #lunghezza d'onda portante L1 [m]
    lambda_l5= 0.2548  #lunghezza d'onda portante L5 [m]
    #df = pd.DataFrame()
    #Grab header
    query=[]
    header = ''
    total_iter=get_num_lines(dir,file)
    with open(dir + file) as handler:
        for i,line in enumerate(handler):
            header += line
            total_iter+=1 #serve per barra di stato
            if 'END OF HEADER' in line:
                break
    
    #Grab Data
    print(total_iter)
    epoch=0
    #print('ciao sono qui')
    with open(dir + file) as handler:
        
        for i, line in  enumerate(tqdm(handler, total=total_iter)):
            #Check for a Timestamp lable
            if '> ' in line:
                epoch +=1 
                #Grab Timestamp
                links = line.split()
                #print(links)
                index = datetime.strptime(' '.join(links[1:7]), '%Y %m %d %H %M %S.%f0')
           
                #Identify number of satellites
                satNum = int(links[8])
                #print(satNum)
                #For every sat
                
                for j in range(satNum):
                    #just save the data as a string for now
                    satData = handler.readline()
                   
                    #print("satID",satData[0:3],index)
                    
                    if satData.startswith("E"):
                         #caso Galileo
                        
                        try:
                            try:
                                
                                C1 = float(satData[68:82])
                       #         print("C1", C1)
                            except:
                                C1 = 0.0
                        #        print("c1", C1)

                            try:
                                
                                L1=float(satData[83:98])
                         #       print("E1", L1)
                            except:
                                L1=0.0
                          #      print("E1", L1)
                            
                            try:
                                D1=float(satData[102:117])
                           #     print("d1", D1)
                            except:
                                D1=0.0
                            #    print("d1", D1)
                            
                            try:
                                C_N0_L1=float(satData[121:130])
                             #   print("c/n0_l1",C_N0_L1)
                            except:
                                C_N0_L1=0.0
                              #  print("c/n0_l1",C_N0_L1)
                            #print("\n")
                        except:
                            C1=0.0        
                        #    print("C1C",C1)
                            L1=0.0
                        #    print("E1", L1)
                            D1=0.0
                        #    print("D1", D1)
                            C_N0_L1=0.0
                         #   print("c/n0_E1",C_N0_L1)
                         #   print("\n")

                                      
                        
                        try:
                            
                            try:
                                C5=float(satData[132:146])
                          #      print("C5Q", C5)
                            except:
                                C5=0.0
                           #     print("C5Q",C5)

                            try:
                                L5= float(satData[148:164])
                            #    print("E5a", L5)
                            except:
                                L5=0.0
                             #   print("E5a", L5)
                            
                            try:
                                D5=float(satData[165:180])
                              #  print("D5", D5)
                            except:
                                D5=0.0
                               # print("D5", D5)
                            
                            try:
                                C_N0_L5=float(satData[186:194])
                                #print("c/n0_E5",C_N0_L5) 
                            except:
                                C_N0_L5=0.0
                                #print("c/n0_E5",C_N0_L5)
                            #print("\n")      
                        except:
                            C5=0.0
                            #print("C5Q",0.0)
                            L5=0.0
                            #print("E5a", 0.0)
                            D5=0.0
                            #print("D5", 0.0)
                            C_N0_L5=0.0
                            #print("c/n0_E5",0.0)
                        #    print("\n")
                   
                        
                    
                    #satelliti GPS GLONASS e BeiDou               
                    else:
                        
                        try:
                            C1=float(satData[5:17])
                  #          print("c1", C1)
                        except:
                            C1=0.0
                  #          print("c1", C1)
                        
                        try:
                            L1=float(satData[19:36])
                   #         print("L1", L1)
                        except:
                            L1=0.0
                    #        print("L1", L1)

                        try:
                            D1=float(satData[38:51])
                     #       print("d1", D1)
                        except:
                            D1=0.0
                      #      print("d1", D1)
                        
                        try:
                            C_N0_L1=float(satData[58:66])
                       #     print("c/n0_l1",C_N0_L1)
                        except:
                            C_N0_L1=0.0
                        #    print("c/n0_l1", C_N0_L1)
                        #print("\n")
                    
                        try:
                            
                            try:
                                C5=float(satData[68:82])
                         #       print("c5", C5)
                            except:
                                C5=0.0
                          #      print("c5", C5)
                            
                            try:
                                L5=float(satData[83:98])
                           #     print("l5", L5)
                            except:
                                L5=0.0
                            #    print("l5", 0.0)
                            
                            try:
                                D5=float(satData[102:117])
                             #   print("d5", float(satData[102:117]))
                            except:
                                D5=0.0
                              #  print("d5", D5)
                            
                            try:
                                C_N0_L5=float(satData[121:130])
                               # print("c/n0_l5", C_N0_L5)
                            except:
                                C_N0_L5=0.0
                                #print("c/n0_l5", C_N0_L5)
                            #print("\n")
                        except:
                            C5=0.0
                            #print("c5",C5)
                            L5=0.0
                            #print("l5", L5)
                            D5=0.0
                            #print("d5", D5)
                            C_N0_L5=0.0
                            #print("c/n0_l5",C_N0_L5)
                            #print("\n")

                    #code-phase

                    if C1 != 0.0 and L1!= 0.0:
                        cd_phs_l1=C1-L1*lambda_l1
                    else:
                        cd_phs_l1=0.0
                    
                    if C5 != 0.0 and L5!= 0.0:
                        cd_phs_l5=C5-L5*lambda_l5
                    else:
                        cd_phs_l5=0.0
                    
                    
                    
                    #Fix the names
                    
                    satdId = satData.replace("G ", "G0").split()[0]
                    
                    
                    #print(satdId)
                    #Make a dummy dataframe

                    c="INSERT INTO {} VALUES ({},'{}','{}',{},{},{},{},{},{},{},{},{},{})".format(table_name, epoch,index,satdId,C1,L1,D1,C_N0_L1,cd_phs_l1,C5,L5,D5,C_N0_L5,cd_phs_l5)
                    query.append(c)
                    #dff = pd.DataFrame([[index,epoch,satdId,C1,L1,D1,C_N0_L1,cd_phs_l1,C5,L5,D5,C_N0_L5,cd_phs_l5]], columns=['%_GPST','epoch','satID','C1','L1','D(L1)','C/N0(L1)','Code-Phase(L1)','C5','L5','D(L5)','C/N0(L5)','Code-Phase(L5)'])
                    #print(dff)
                    #Tack it on the end
                    #df = df.append(dff)
                   # print(df)
            else:
                continue

    return header, query




def writeDataToDB(db_name, table_name,query):

    conn=sqlite3.connect(db_name)
    c=conn.cursor()

    dropTableStatement = "DROP TABLE IF EXISTS {}".format(table_name)

    c.execute(dropTableStatement)
    c.execute("CREATE TABLE {}(epoca INTEGER , gpst DATE, sat_id TEXT, pseudorange_l1 REAL, carrierphase_l1 REAL, doppler_l1 REAL, SNR_l1 REAL, carrier_minus_phase_l1 REAL, pseudorange_l5 REAL, carrierphase_l5 REAL, doppler_l5 REAL, SNR_l5 REAL, carrier_minus_phase_l5 REAL,  PRIMARY KEY (gpst, sat_id))".format(table_name))
    for i in query:
        #print(i)
        c.execute(i)

    c.close()
    conn.commit()
    conn.close()



def main():

    directory ="/home/lorenzo/remote/progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/lavoro_ION-PLANS/" #add your own path or if you want to test the script use ./Android_RINEX_data/
    rinex ="GEOP213I.19o" #put your own rinex file, or if you want to test the script put test_rinex_ridotto.19o
    database='/home/lorenzo/RINEX_OBS.db' #ATTENTION: DO NOT PUT THE DB IN A SAMBA FOLDER: otherwise it not gonna work
    tabella='GEOP213I'
    header, query = readObs (directory, rinex,tabella)    
    print(type(header))

    
    writeDataToDB(database, tabella, query)

if __name__=="__main__":
    main()