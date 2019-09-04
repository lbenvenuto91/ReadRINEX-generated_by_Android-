
from datetime import datetime, date
import matplotlib.pyplot as plt
import sys
import numpy as np

rinex_in_geopp = "/home/lorenzo/remote/progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/ANDROID/temp/3_settembre_19/2019-09-03,09_34_32_CEST/GTER246Htest.19o"
rinex_in_nsl = "/home/lorenzo/remote/progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/ANDROID/temp/3_settembre_19/data_20190903_093438/SMAR00GBR_R_20192460734test.19o"

header_nsl = 17
header_geopp= 34
record_nsl = [] #sat_id, pseudorange(L1), carrier phase(L1), doppler(L1), C/N0 (L1), pseudorange(L5), carrier phase(L5), doppler(L5), C/N0 (L5)
tempo_nsl = []
satelliti_nsl = []

#ATTENTION!!!!: the Geo++ RinexLogger app doesn't store the carrier phase value if it's = 0 (for the xiaomi mi9 AccumulatedDeltaRagne = 0.0)
record_geopp = [] #sat_id, pseudorange(L1), doppler(L1), C/N0 (L1), pseudorange(L5), doppler(L5), C/N0 (L5)
tempo_geopp = []
satelliti_geopp = []


############################## Reading data NSL (RinexOn App) ##############################

with open(rinex_in_nsl, 'r') as rnx_file:

    #skip header (RInex On app)
    for i in range(header_nsl):
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
            tempo_nsl.append(data)
        else:
            # storing all the satellite ID into an array
            if cleanLine[0] not in satelliti_nsl:
                satelliti_nsl.append(cleanLine[0])

#storing the raw data into a 2d array: for each row of the matrix I'm attaching the time corresponding time instant
with open(rinex_in_nsl, 'r') as rnx_file:
    
    #skip header (RInex On app)
    for i in range(header_nsl):
        next(rnx_file)    
    
    contatore = 0
    
    for line in rnx_file:
        
        cleanLine = line.split()
          
        if cleanLine[0] == '>': 
            contatore +=1
        else:
            cleanLine.append((tempo_nsl[contatore-1]))
            record_nsl.append(cleanLine)
            #print(cleanLine)


############################## Reading data Geo++ (Geo++ App) ############################## 
with open(rinex_in_geopp, 'r') as rnx_file:

    #skip header (RInex On app)
    for i in range(header_geopp):
        next(rnx_file)
    #storing time instant into an array
    for line in rnx_file:
        cleanLine = line.split()
        #print(cleanLine)
        if cleanLine[0]=='>':
            year=int(cleanLine[1])
            month = int(cleanLine[2])
            day = int(cleanLine[3])
            hour = int(cleanLine[4])
            minutes = int(cleanLine[5])
            seconds = float(cleanLine[6])
            data = datetime(year,month,day,hour,minutes,int(seconds))
            tempo_geopp.append(data)
        else:
            # storing all the satellite ID into an array
            if cleanLine[0] not in satelliti_geopp:
                satelliti_geopp.append(cleanLine[0])

#storing the raw data into a 2d array: for each row of the matrix I'm attaching the time corresponding time instant
with open(rinex_in_geopp, 'r') as rnx_file:
    
    #skip header (RInex On app)
    for i in range(header_geopp):
        next(rnx_file)    
    
    contatore = 0
    
    for line in rnx_file:
        
        cleanLine = line.split()
          
        if cleanLine[0] == '>': 
            contatore +=1
        else:
            cleanLine.append((tempo_geopp[contatore-1]))
            record_geopp.append(cleanLine)
            #print(cleanLine)


###################################### PLOTTING PART ######################################


#plot pseudorange 
sat = 'G10'

#pseudorange_nsl=[]
#cella_nsl=[]

pseudorange_to_plot_nsl_L1 = []
time_instant_nsl_L1 = []

pseudorange_to_plot_nsl_L5 = []
time_instant_nsl_L5 = []

for i in record_nsl:
    if i[0] == sat:
        #L1 freq
        pseudorange_to_plot_nsl_L1.append(i[1])
        time_instant_nsl_L1.append(i[-1])         
        #L5 freq
        if len(i) > 6:
            pseudorange_to_plot_nsl_L5.append(i[-5])
            time_instant_nsl_L5.append(i[-1])
        else:
            pseudorange_to_plot_nsl_L5.append(0.0)
            time_instant_nsl_L5.append(i[-1])    
        #cella_nsl.append(i[1])
        #cella_nsl.append(i[-1])
        #pseudorange_nsl.append(cella_nsl)

#pseudorange_to_plot_nsl = [i[0] for i in pseudorange_nsl]
#time_instant_nsl = [i[1] for i in pseudorange_nsl]

#pseudorange_geopp=[]
#cella_geopp=[]
pseudorange_to_plot_geopp_L1 = []
time_instant_geopp_L1 = []

pseudorange_to_plot_geopp_L5 = []
time_instant_geopp_L5 = []

for i in record_geopp:
    if i[0] == sat:
        #L1 freq
        pseudorange_to_plot_geopp_L1.append(i[1])
        time_instant_geopp_L1.append(i[-1])    
        #L5 freq
        if len(i) > 6:
            pseudorange_to_plot_geopp_L5.append(i[-4])
            time_instant_geopp_L5.append(i[-1])
        else:
            pseudorange_to_plot_geopp_L5.append(0.0)
            time_instant_geopp_L5.append(i[-1])
        
#        cella_geopp.append(i[1])
#        cella_geopp.append(i[-1])
#        pseudorange_geopp.append(cella_nsl)

#pseudorange_to_plot_geopp = [i[0] for i in pseudorange_geopp]
#time_instant_geopp = [i[1] for i in pseudorange_geopp]



############# cfr app ####################

cfr_pseudorange_L1 = []

#check: same temporal instant
common_starting_time= max(min(time_instant_nsl_L1), min(time_instant_geopp_L1))
#print(common_starting_time)

nsl_tmp=np.array(time_instant_nsl_L1)
nsl_start=list(nsl_tmp).index(common_starting_time)

geopp_tmp=np.array(time_instant_geopp_L1)
geopp_start=list(geopp_tmp).index(common_starting_time)
print(nsl_start)
print(geopp_start)

common_ending_time= min(max(time_instant_nsl_L1), max(time_instant_geopp_L1))
#print(common_starting_time)

nsl_end=list(nsl_tmp).index(common_ending_time)
geopp_end=list(geopp_tmp).index(common_ending_time)
print("\n")
print(nsl_end)
print(geopp_end)


print("\n")
print(pseudorange_to_plot_nsl_L1[nsl_start:nsl_end])
print(time_instant_nsl_L1[nsl_start:nsl_end])
print("\n")
print(pseudorange_to_plot_geopp_L1[geopp_start:geopp_end])
print(time_instant_geopp_L1[geopp_start:geopp_end])
sys.exit()
if time_instant_nsl_L1[0] != time_instant_geopp_L1[0]:
    raise ValueError ("the starting temporal instant must be the same")
    
else:
    
    #check same lenght for the 2 arrays
    for a,b in zip(pseudorange_to_plot_nsl_L1, pseudorange_to_plot_geopp_L1):
        c = (float(a)-float(b))
        cfr_pseudorange_L1.append(c)
        




############# plot ###########################
plt.plot(time_instant_nsl_L1, pseudorange_to_plot_nsl_L1)
plt.ylabel('pseudoranges ({0}) [m]'.format('E1' if sat.startswith('E') else 'L1'))
plt.xlabel('UTC time')
plt.title('RinexON (NSL app) sat {0}'.format(sat))

plt.figure()

plt.plot(time_instant_geopp_L1, pseudorange_to_plot_geopp_L1)
plt.ylabel('pseudoranges ({0}) [m]'.format('E1' if sat.startswith('E') else 'L1'))
plt.xlabel('UTC time')
plt.title('Rinex Logger  (GEO++ app) sat {0}'.format(sat))

plt.figure()

plt.plot(time_instant_nsl_L5, pseudorange_to_plot_nsl_L5)
plt.ylabel('pseudoranges ({0}) [m]'.format('E5a' if sat.startswith('E') else 'L5'))
plt.xlabel('UTC time')
plt.title('RinexON (NSL app) sat {0}'.format(sat))

plt.figure()

plt.plot(time_instant_geopp_L5, pseudorange_to_plot_geopp_L5)
plt.ylabel('pseudoranges ({0}) [m]'.format('E5a' if sat.startswith('E') else 'L5'))
plt.xlabel('UTC time')
plt.title('Rinex Logger  (GEO++ app) sat {0}'.format(sat))

plt.figure()

plt.plot(time_instant_geopp_L1, cfr_pseudorange_L1)
plt.ylabel('pseudorange difference ({0}) [m]'.format('E1' if sat.startswith('E') else 'L1'))
plt.xlabel('UTC time')
plt.title('Difference between pseudorange from Geo++ app and NSL app sat {0}'.format(sat))


plt.show()









