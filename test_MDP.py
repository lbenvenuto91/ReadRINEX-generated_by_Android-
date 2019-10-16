
from datetime import datetime, date
import matplotlib.pyplot as plt
import sys
import numpy as np
import time

#path dove sono i dati nel repository
rinex_in="../../lavoro_ION-PLANS/testMDP.19o"
#path dove ho i dati nella cartella dottorato
#rinex_in_geopp = "../../ANDROID/test_app_ubx_tpc/xiaomi_mi9/geo++/2019-09-18,09_57_44_CEST/merge_geopp_18sett.19o"
#rinex_in_google = "../../ANDROID/test_app_ubx_tpc/xiaomi_mi9/google/google_18_sett_2019.19o"
#rinex_in_nsl = "../../ANDROID/test_app_ubx_tpc/xiaomi_mi9/nsl/data_20190918_095736/SMAR00GBR_R_20192610757.19o"

header_geopp= 34

GPS_L1=0.1905
GPS_L5=0.2548

def ReadRinexData(filename, header):
    #data = []
    

    
    record = []
    tempo = []
    satelliti = []

    with open(filename, 'r') as rnx_file:
 
        #skip header (RInex On app)
        for i in range(header):
            next(rnx_file)
    #storing time instant into an array
        for line in rnx_file:
            cleanLine = line.split()
            if cleanLine[0]=='>':
                year = int(cleanLine[1])
                month = int(cleanLine[2])
                day = int(cleanLine[3])
                hour = int(cleanLine[4])
                minutes = int(cleanLine[5])
                seconds = float(cleanLine[6])
                data = datetime(year,month,day,hour,minutes,int(seconds))
                tempo.append(data)
            else:
                if cleanLine[0] not in satelliti:
                    satelliti.append(cleanLine[0])    
        
    with open(filename, 'r') as rnx_file:                    
        for i in range(header):
            next(rnx_file)            

        contatore = 0    
         
        for line in rnx_file:
            cleanLine = line.split()
            
            
            
            if cleanLine[0]=='>':
                contatore += 1
            else:
                
                try:
                    cleanLine.append(float(cleanLine[1])-float(cleanLine[2])*GPS_L1) #variabile sentinella su L1
                except:
                    print("non ho abbastanza dati per calcolare la var sentinel")
                cleanLine.append(tempo[contatore-1])
                record.append(cleanLine)

    
        
    obs={}
    epoc=1
    for i in tempo:
        osserv=[]
        for j in record:
            osserv.append(j)
        obs[epoc]=osserv
        epoc+=1
  
    print("\n\t\t**** Done! ****")
    
    '''
    GPS_obs = {}
    #GLONASS_obs ={}
    GALILEO_obs ={}
    for i in record:
        if i[0].startswith('G'):
            GPS_obs[i[0],i[-1]]=i[1:-1]
        else:
       
            continue
        '''
    
  


    return tempo,record,satelliti
          

tempo,record, satelliti = ReadRinexData(rinex_in,header_geopp)
print(record[10])

