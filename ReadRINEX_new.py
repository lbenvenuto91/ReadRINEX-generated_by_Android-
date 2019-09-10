
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
            if freq == "L1":
                if i[0] == sat:
                    pseudorange_to_plot.append(i[1])
                    time_instant.append(i[-1])
            elif freq == "L5":
                if len(i)>6:
                    pseudorange_to_plot.append(i[-5]) 
                    time_instant.append(i[-1])
                else:
                    pseudorange_to_plot.append(0.0)
                    time_instant.append(i[-1])
        elif app == "Geo++ RinexLogger":
            if freq == "L1":
                if i[0] == sat:
                    pseudorange_to_plot.append(i[1])
                    time_instant.append(i[-1])
            elif freq == "L5":
                if len(i)>6:
                    pseudorange_to_plot.append(i[-4]) 
                    time_instant.append(i[-1])
                else:
                    pseudorange_to_plot.append(0.0)
                    time_instant.append(i[-1])
        else:
            print("sei uno stronzo!")
    


    return (time_instant, pseudorange_to_plot)

def PoltPR(sat,freq):
    
    time2plot_nsl, PR2plot_nsl = Array2plot_PR (record_nsl, satellite, freq, "NSL RinexOn")
    time2plot_geopp, PR2plot_geopp = Array2plot_PR (record_geopp, satellite, "L1", "NSL RinexOn")
    time2plot_google, PR2plot_nsl_google = Array2plot_PR (record_google, satellite, "L1", "NSL RinexOn")
        
    start,end = CommonStartingEndingTime(time2plot_nsl,time2plot_geopp,time2plot_google)

    nsl_tmp=np.array(time2plot_nsl)
    nsl_start=list(nsl_tmp).index(start)
    nsl_end=list(nsl_tmp).index(end)
    geopp_tmp=np.array(time2plot_geopp)
    geopp_start=list(geopp_tmp).index(start)
    geopp_end=list(geopp_tmp).index(end)
    google_tmp=np.array(time2plot_google)
    google_start=list(google_tmp).index(start)
    google_end=list(google_tmp).index(end)

    plt.plot(time2plot_nsl[nsl_start:nsl_end], PR2plot_nsl[nsl_start:nsl_end])
    plt.ylabel('pseudoranges ({0}) [m]'.format('E1' if sat.startswith('E') else 'L1'))
    plt.xlabel('UTC time')
    plt.title('RinexON (NSL app) sat {0}'.format(sat))
    plt.show()




#POSSIBILE MAIN
tempo_nsl, record_nsl, satelliti_nsl = ReadRinexData(rinex_in_nsl, header_nsl, "NSL RinexOn")
tempo_geopp, record_geopp, satelliti_geopp = ReadRinexData(rinex_in_geopp, header_geopp, "Geo++ RinexLogger")
tempo_google, record_google, satelliti_google = ReadRinexData(rinex_in_google, header_google, "Google GNSSLogger")
print("\nRead data for the following satellites:\n{0}".format(satelliti_nsl))



start,end = CommonStartingEndingTime(tempo_nsl,tempo_geopp,tempo_google)
print("\ninizio = {0}".format(start))
print("\nfine = {0}".format(end))

satellite = input('\nInsert sat ID of the satellite to plot >> ')

PoltPR(satellite, "L1")
#tmp=np.array(time_instant)
#print(tmp)
#start_time=list(tmp).index(start) #restituisce l'indice dell'elemento corrispondente all'istante di inizio
#ending_time=list(tmp).index(end)



