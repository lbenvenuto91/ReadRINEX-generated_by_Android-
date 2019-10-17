



import pandas as pd
from datetime import datetime, date
import time

directory ="./Android_RINEX_data/"
rinex ="test_rinex_ridotto.19o" 



def readObs(dir, file):
    df = pd.DataFrame()
    #Grab header
    header = ''
    with open(dir + file) as handler:
        for i, line in enumerate(handler):
            header += line
            if 'END OF HEADER' in line:
                break
    #Grab Data
    
    #print('ciao sono qui')
    with open(dir + file) as handler:
        for i, line in enumerate(handler):
            #Check for a Timestamp lable
            if '> ' in line:
                #Grab Timestamp
                links = line.split()
                #print(links)
                index = datetime.strptime(' '.join(links[1:7]), '%Y %m %d %H %M %S.%f0')
                print(index)
                
                #Identify number of satellites
                satNum = int(links[8])
                print(satNum)
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



                    
                    
                    
                    
                    #Fix the names
                    
                    satdId = satData.replace("G ", "G0").split()[0]
                    
                    
                    #print(satdId)
                    #Make a dummy dataframe
                    dff = pd.DataFrame([[index,satdId,C1,L1,D1,C_N0_L1,C5,L5,D5,C_N0_L5]], columns=['%_GPST','satID','C1','L1','D(L1)','C/N0(L1)','C5','L5','D(L5)','C/N0(L5)'])
                    print(dff)
                    #Tack it on the end
                    df = df.append(dff)
                   # print(df)
                    
    return df, header



df, header = readObs (directory, rinex)    
df.set_index(['%_GPST', 'satID'])
