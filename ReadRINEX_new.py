
from datetime import datetime, date
import matplotlib.pyplot as plt
import sys
import numpy as np


rinex_in_geopp = "./Android_RINEX_data/geo++/merge_geopp_6sett.19o"
rinex_in_nsl = "./Android_RINEX_data/nsl/nsl_test_6sett.19o"
rinex_in_google = "./Android_RINEX_data/Google_GNSSLogger/rinex_from_gnssLogger_6_settembre.19o"

header_nsl = 17
header_geopp= 34
header_google = 19



def ReadRinexData(filename, header, app):
    #data = []
    
    print("\n\t Reading data from {0} app".format(app))
    
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
                cleanLine.append(tempo[contatore-1])
                record.append(cleanLine)
    
       
    print("\n\t\t**** Done! ****")
    return tempo,record,satelliti
          
def CommonStartingEndingTime(tempo_App1, tempo_App2,tempo_App3):
    common_starting_time= max(min(tempo_App1), min(tempo_App2), min(tempo_App3))
    common_ending_time=min(max(tempo_App1), max(tempo_App2), max(tempo_App3))
    return common_starting_time,common_ending_time


def Array2plot_PR (record, sat, freq, app):
    pseudorange_to_plot=[]
    time_instant=[]

    for i in record:
        if app == "NSL RinexOn" or app == "Google GNSSLogger":
            if i[0]==sat:
            
                if freq == "L1":
                    if float(i[1]) != 0.0:
                        pseudorange_to_plot.append(float(i[1]))
                        time_instant.append(i[-1])
                    else:
                        pseudorange_to_plot.append(np.nan)
                        time_instant.append(i[-1])                        
                elif freq == "L5":
                    if len(i)>6: 
                        if float(i[-5]) != 0.0:
                            pseudorange_to_plot.append(float(i[-5])) 
                            time_instant.append(i[-1])
                        else:
                            pseudorange_to_plot.append(np.nan)
                            time_instant.append(i[-1])                                                
                    else:
                        pseudorange_to_plot.append(np.nan)
                        time_instant.append(i[-1])
        elif app == "Geo++ RinexLogger":
            if i[0]==sat:
                if freq == "L1":
                    if float(i[1]) != 0.0:
                        pseudorange_to_plot.append(float(i[1]))
                        time_instant.append(i[-1])
                    else:
                        pseudorange_to_plot.append(np.nan)
                        time_instant.append(i[-1])
                elif freq == "L5":
                    if len(i)>6:
                        if float (i[-4])!=0.0:
                            pseudorange_to_plot.append(float(i[-4])) 
                            time_instant.append(i[-1])
                        else:
                            pseudorange_to_plot.append(np.nan)
                            time_instant.append(i[-1])
                    else:
                        pseudorange_to_plot.append(np.nan)
                        time_instant.append(i[-1])
        else:
            print("sei uno stronzo!")
    


    return (time_instant, pseudorange_to_plot)


def Array2plot_C_N0 (record, sat, freq, app):
    C_N0_to_plot=[]
    time_instant=[]

    for i in record:
        if app == "NSL RinexOn" or app == "Google GNSSLogger":
            if i[0]==sat:
            
                if freq == "L1":
                    if float(i[4]) != 0.0:
                        C_N0_to_plot.append(float(i[4]))
                        time_instant.append(i[-1])
                    else:
                        C_N0_to_plot.append(np.nan)
                        time_instant.append(i[-1])                        
                elif freq == "L5":
                    if len(i)>6: 
                        if float(i[-2]) != 0.0:
                            C_N0_to_plot.append(float(i[-2])) 
                            time_instant.append(i[-1])
                        else:
                            C_N0_to_plot.append(np.nan)
                            time_instant.append(i[-1])                                                
                    else:
                        C_N0_to_plot.append(np.nan)
                        time_instant.append(i[-1])
        elif app == "Geo++ RinexLogger":
            if i[0]==sat:
                if freq == "L1":
                    if float(i[3]) != 0.0:
                        C_N0_to_plot.append(float(i[3]))
                        time_instant.append(i[-1])
                    else:
                        C_N0_to_plot.append(np.nan)
                        time_instant.append(i[-1])
                elif freq == "L5":
                    if len(i)>6:
                        if float (i[-2])!=0.0:
                            C_N0_to_plot.append(float(i[-2])) 
                            time_instant.append(i[-1])
                        else:
                            C_N0_to_plot.append(np.nan)
                            time_instant.append(i[-1])
                    else:
                        C_N0_to_plot.append(np.nan)
                        time_instant.append(i[-1])
        else:
            print("sei uno stronzo!")
    


    return (time_instant, C_N0_to_plot)





def PlotPR(sat,freq,sepPlot):
    
    App=["NSL RinexOn", "Geo++ RinexLogger", "Google GNSSLogger"]
    time2plot=[]
    PR2plot = []
    
    time2plot_nsl, PR2plot_nsl = Array2plot_PR (record_nsl, satellite, freq, "NSL RinexOn")
    time2plot.append(time2plot_nsl)
    PR2plot.append(PR2plot_nsl)
    
    time2plot_geopp, PR2plot_geopp = Array2plot_PR (record_geopp, satellite, freq, "Geo++ RinexLogger")
    time2plot.append(time2plot_geopp)
    PR2plot.append(PR2plot_geopp)
    
    time2plot_google, PR2plot_google = Array2plot_PR (record_google, satellite, freq, "Google GNSSLogger")
    time2plot.append(time2plot_google)
    PR2plot.append(PR2plot_google)
    
    start,end = CommonStartingEndingTime(time2plot_nsl,time2plot_geopp,time2plot_google)


    #Roba per grafici  
    if freq.endswith("1"):
        if sat.startswith("E"):
            frequenza = "E1"
        else:
            frequenza = "L1"
    elif freq.endswith("5"):
        if sat.startswith("E"):
            frequenza = "E5a"
        else:
            frequenza = "L5"
    
    if sepPlot == True:
      
        for i,j,k  in zip(App, time2plot, PR2plot):    
            
            tmp=np.array(j)
            time_start=list(tmp).index(start)
            time_end=list(tmp).index(end)
            
            
            plt.plot(j[time_start:time_end], k[time_start:time_end])
            plt.ylabel('pseudoranges ({0}) [m]'.format(frequenza))
            plt.xlabel('UTC time')
            plt.title('{0} sat {1}'.format(sat, i))
            
            plt.yticks(np.arange(min(k[time_start:time_end]), max(k[time_start:time_end])+1000, 20000))
            plt.figure()

        plt.show()

    elif sepPlot == False:
        print("sei stronzo!")
        
        
        nsl_tmp=np.array(time2plot_nsl)
        nsl_start=list(nsl_tmp).index(start)
        nsl_end=list(nsl_tmp).index(end)
    
        geopp_tmp=np.array(time2plot_geopp)
        geopp_start=list(geopp_tmp).index(start)
        geopp_end=list(geopp_tmp).index(end)
    
        google_tmp=np.array(time2plot_google)
        google_start=list(google_tmp).index(start)
        google_end=list(google_tmp).index(end)



        cfr_nsl_google=[]
        for n,g in zip(PR2plot_nsl[nsl_start:nsl_end],PR2plot_google[google_start:google_end]):
            if n != np.nan and g != np.nan:
                c = n-g
                cfr_nsl_google.append(c)
            else:
                cfr_nsl_google.append(np.nan)

   
        plt.plot(time2plot[0][nsl_start:nsl_end], PR2plot[0][nsl_start:nsl_end],label="{0}".format(App[0]))
        plt.plot(time2plot[1][geopp_start:geopp_end], PR2plot[1][geopp_start:geopp_end],label="{0}".format(App[1]))
        plt.plot(time2plot[2][google_start:google_end], PR2plot[2][google_start:google_end],label="{0}".format(App[2]))
        plt.ylabel('pseudoranges ({0}) [m]'.format(frequenza))
               
        plt.xlabel('UTC time')
        plt.title('Pseudoranges for sat {0}'.format(sat))
        plt.legend()

        plt.figure()

        plt.plot(time2plot_nsl[nsl_start:nsl_end], cfr_nsl_google[nsl_start:nsl_end])
        plt.ylabel('pseudorange difference ({0}) [m]'.format(frequenza))
        plt.xlabel('UTC time')
        plt.title('Difference between pseudorange from NSL app and Google app for sat {0}'.format(sat))



        plt.show()



def PlotC_N0(sat,freq, sepPlot):
    
    App=["NSL RinexOn", "Geo++ RinexLogger", "Google GNSSLogger"]
    time2plot=[]
    C_N02plot = []

    time2plot_nsl, C_N02plot_nsl = Array2plot_C_N0 (record_nsl, satellite, freq, "NSL RinexOn")
    time2plot.append(time2plot_nsl)
    C_N02plot.append(C_N02plot_nsl)
    
    time2plot_geopp, C_N02plot_geopp = Array2plot_C_N0 (record_geopp, satellite, freq, "Geo++ RinexLogger")
    time2plot.append(time2plot_geopp)
    C_N02plot.append(C_N02plot_geopp)
    
    time2plot_google, C_N02plot_google = Array2plot_C_N0 (record_google, satellite, freq, "Google GNSSLogger")
    time2plot.append(time2plot_google)
    C_N02plot.append(C_N02plot_google)
    
    start,end = CommonStartingEndingTime(time2plot_nsl,time2plot_geopp,time2plot_google)

    #Roba per grafici  
    if freq.endswith("1"):
        if sat.startswith("E"):
            frequenza = "E1"
        else:
            frequenza = "L1"
    elif freq.endswith("5"):
        if sat.startswith("E"):
            frequenza = "E5a"
        else:
            frequenza = "L5"
    if sepPlot == True:
        for i,j,k  in zip(App, time2plot, C_N02plot):    
                
            tmp=np.array(j)
            time_start=list(tmp).index(start)
            time_end=list(tmp).index(end)
            
            
            plt.plot(j[time_start:time_end], k[time_start:time_end])
            plt.ylabel('C/N0 ({0}) [dB-Hz]'.format(frequenza))
            plt.xlabel('UTC time')
            plt.title('{0} sat {1}'.format(sat, i))
            
            #plt.yticks(np.arange(min(k[time_start:time_end]), max(k[time_start:time_end])+1000, 20000))
            plt.figure()

        plt.show()
    elif sepPlot == False:
        print("sei stronzo!")    
        nsl_tmp=np.array(time2plot_nsl)
        nsl_start=list(nsl_tmp).index(start)
        nsl_end=list(nsl_tmp).index(end)
    
        geopp_tmp=np.array(time2plot_geopp)
        geopp_start=list(geopp_tmp).index(start)
        geopp_end=list(geopp_tmp).index(end)
    
        google_tmp=np.array(time2plot_google)
        google_start=list(google_tmp).index(start)
        google_end=list(google_tmp).index(end)


        plt.plot(time2plot[0][nsl_start:nsl_end], C_N02plot[0][nsl_start:nsl_end],label="{0}".format(App[0]))
        plt.plot(time2plot[1][geopp_start:geopp_end], C_N02plot[1][geopp_start:geopp_end],label="{0}".format(App[1]))
        plt.plot(time2plot[2][google_start:google_end], C_N02plot[2][google_start:google_end],label="{0}".format(App[2]))
        plt.ylabel('C/N0 ({0}) [dB-Hz]'.format(frequenza))
               
        plt.xlabel('UTC time')
        plt.title('C/N0 for sat {0}'.format(sat))
        plt.legend()

        plt.show()




#POSSIBILE MAIN
tempo_nsl, record_nsl, satelliti_nsl = ReadRinexData(rinex_in_nsl, header_nsl, "NSL RinexOn")
tempo_geopp, record_geopp, satelliti_geopp = ReadRinexData(rinex_in_geopp, header_geopp, "Geo++ RinexLogger")
tempo_google, record_google, satelliti_google = ReadRinexData(rinex_in_google, header_google, "Google GNSSLogger")
print("\nRead data for the following satellites:\n{0}".format(satelliti_nsl))

satellite = input('\nInsert sat ID of the satellite to plot >> ')

carrierFreq = input('\n Choose between L1 or L5: ')
assert(carrierFreq == "L1" or carrierFreq == "L5"), "the only possible answers are L1 or L5"
figSeparate = input("\nDo you want separate plot for the different apps? ")
assert(figSeparate == "yes" or figSeparate == "no"), "the only possible answers are yes or no"
if figSeparate == "yes":
    sepPlot = True
elif figSeparate == "no":
    sepPlot =False


#PlotPR(satellite, carrierFreq, sepPlot)

PlotC_N0(satellite, carrierFreq, sepPlot)




