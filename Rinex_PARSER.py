



import pandas as pd
from datetime import datetime, date
import time

directory ="/home/lorenzo/remote/progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/lavoro_ION-PLANS/"
rinex ="testMDP.19o" 



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
    
    print('ciao')
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
                   
                    print("satID",satData[0:3],index)
                    
                    if satData.startswith("E"):
                         #caso Galileo
                        
                        try:
                            try:
                                print("c1", satData[68:82])
                            except:
                                print("c1", 0.0)

                            try:
                                print("E1", float(satData[83:98]))
                            except:
                                print("E1", 0.0)
                            
                            try:
                                print("d1", float(satData[102:117]))
                            except:
                                print("d1", 0.0)
                            
                            try:
                                print("c/n0_l1",float(satData[121:130]))
                            except:
                                print("c/n0_l1",0.0)
                            print("\n")
                        except:
                            print("C1C",0.0)
                            print("E1", 0.0)
                            print("D1", 0.0)
                            print("c/n0_E1",0.0)
                            print("\n")

                        
                      
                        
                        try:
                            
                            try:
                                print("C5Q", satData[132:146])
                            except:
                                print("C5Q", 0.0)

                            try:
                                print("E5a", float(satData[148:164]))
                            except:
                                print("E5a", 0.0)
                            
                            try:
                                print("D5", float(satData[165:180]))
                            except:
                                print("D5", 0.0)
                            
                            try:
                                print("c/n0_E5",float(satData[186:194])) 
                            except:
                                print("c/n0_E5",0.0)
                            print("\n")      
                        except:
                            print("C5Q",0.0)
                            print("E5a", 0.0)
                            print("D5", 0.0)
                            print("c/n0_E5",0.0)
                            print("\n")

                        
                        
                    
                        
                    else:
                        
                        try:
                            print("c1", float(satData[5:17]))
                        except:
                            print("c1", 0.0)
                        
                        try:
                            print("L1", float(satData[19:36]))
                        except:
                            print("L1", 0.0)

                        try:
                            print("d1", float(satData[38:51]))
                        except:
                            print("d1", 0.0)
                        
                        try:
                            print("c/n0_l1",float(satData[58:66]))
                        except:
                            print("c/n0_l1",0.0)
                        print("\n")
                    
                        try:
                            
                            try:
                                print("c5", float(satData[68:82]))
                            except:
                                print("c5", 0.0)
                            
                            try:
                                print("l5", float(satData[83:98]))
                            except:
                                print("l5", 0.0)
                            
                            try:
                                print("d5", float(satData[102:117]))
                            except:
                                print("d5", 0.0)
                            
                            try:
                                print("c/n0_l5", float(satData[121:130]))
                            except:
                                print("c/n0_l5", 0.0)
                            print("\n")
                        except:
                            print("c5",0.0)
                            print("l5", 0.0)
                            print("d5", 0.0)
                            print("c/n0_l5",0.0)
                            print("\n")



                    
                    
                    
                    
                    #Fix the names
                    
                    satdId = satData.replace("G ", "G0").split()[0]
                    
                    
                    #print(satdId)
                    #Make a dummy dataframe
                    dff = pd.DataFrame([[index,satdId,satData]], columns=['%_GPST','satID','satData'])
                    #Tack it on the end
                    df = df.append(dff)
                   # print(df)
                    
    return df, header



df, header = readObs (directory, rinex)    
df.set_index(['%_GPST', 'satID'])
