#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install lasio
import lasio
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# read the las file and show the headers, or 'keys'
las = lasio.read(r"C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\OVBD_PSI.las")

las_OG_LS = lasio.read(r"C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\OG_LS_PPG.las")
las_OG_ML = lasio.read(r"C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\OG_ML_PPG.las")
las_OG_HS = lasio.read(r"C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\OG_HS_PPG.las")
print('the keys in the LAS file are: ' , las.keys())
print('the keys in the LAS file are: ' , las_OG_LS.keys())
print('the keys in the LAS file are: ' , las_OG_ML.keys())
print('the keys in the LAS file are: ' , las_OG_HS.keys())


# In[2]:


# look into the values
print("first value in the LAS array is: " , las['DEPTH'][0])
print("last value in the LAS array is: " , las['DEPTH'][-1])


# In[3]:


# check out the las data such as well name, company, date, etc..
las.well


# In[4]:


# store the las file in df variable as a pandas datafframe
df = las.df()

df_OG_LS = las_OG_LS.df()
df_OG_ML = las_OG_ML.df()
df_OG_HS = las_OG_HS.df()


print(df.head)
#print(df.shape)


# In[5]:


# check if any values are blank
df.isna().sum()

# drop rows where one or more of the subset logs has a null value
#  df_dropped = df.dropna(subset = ['GR', 'DT', 'SPOR'], axis = 0, how = 'any')


# In[6]:


# describe the data statistics
df.describe()


# In[7]:


# make a copy of the latest dataset
df1 = df.copy()
# add a column
#  df['Vsh'] = (df.GR.min()0 / (df.GR.max() - df.GR.min())


# In[8]:


# reindex
df1 = df.rename_axis('DEPTH').reset_index()

df_OG_LS = df_OG_LS.reset_index()
df_OG_ML = df_OG_ML.reset_index()
df_OG_HS = df_OG_HS.reset_index()

df_OG_LS.head()


# In[9]:


# graph objects
fig = go.Figure(data = go.Scatter(
    x = df1['DEPTH'],
    y = df1['OVBD_PSI']))

fig.update_layout(
    title = 'Depth vs Original Overburden Pressure (psi)',
    title_x = .5,
    xaxis_title = 'DEPTH',
    yaxis_title = 'OVBD_PSI')
fig.show()


# In[10]:


# plotly express
fig = px.line(
    df1,
    x = 'DEPTH',
    y = 'OVBD_PSI')
fig.show()
              


# In[11]:


# plotly express
fig = px.line(
    df1,
    x = 'DEPTH',
    y = 'OVBD_PSI',
    range_y = [0 , 15000],
    range_x = [0 , 15000]
)
# add a range slider
fig.update_xaxes(rangeslider_visible = True)
fig.show()
              


# In[12]:


fig = make_subplots(rows = 1, cols = 3, shared_yaxes = True)
fig.add_trace(go.Scatter(x = df1['OVBD_PSI'], y = df1['DEPTH']), row = 1, col = 1)
fig.add_trace(go.Scatter(x = df1['OVBD_PSI'], y = df1['DEPTH']), row = 1, col = 2)
fig.add_trace(go.Scatter(x = df1['OVBD_PSI'], y = df1['DEPTH']), row = 1, col = 3)

fig.update_xaxes(title_text = 'OVBD1', row = 1, col = 1)
fig.update_xaxes(title_text = 'OVBD2', row = 1, col = 2)
fig.update_xaxes(title_text = 'OVBD3', row = 1, col = 3)

fig.update_yaxes(title_text = 'Depth', row = 1, col = 1, autorange = 'reversed')


fig.update_layout(title_text = 'Log Plot', height = 600)
fig.show()


# In[13]:


# ***LOG MD SHIFT***

shift = 32

def main():
    if len(df1) == 0:
        print(f'Warning! The log is empty.')
        return

    else:
        df1['DEPTH'] = df1['DEPTH'] + shift
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)

# END LOG MD (KB) SHIFT
df1


# In[14]:


# *** CREATE COPY OF OVBD_PPG_MD_SHIFTED TO MAKE LOW SIDE PORE PRESSURE LOG AND EDIT ***
# WILL CONVERT TO PPG LATER
df_LS = df1.copy()
df_LS.rename(columns={'OVBD_PSI': 'LS_PPG'}, inplace=True)

df_ML = df1.copy()
df_ML.rename(columns={'OVBD_PSI': 'ML_PPG'}, inplace=True)

df_HS = df1.copy()
df_HS.rename(columns={'OVBD_PSI': 'HS_PPG'}, inplace=True)

# END COPY KB SHIFTED OVBD LOG
type(df_LS['DEPTH'])


# In[15]:


# bring in topset and remove last column
Topset1 = pd.read_csv(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\Topset1.txt', sep = "\t")
Topset1.drop('GeosteeringDip', axis = 1, inplace = True)
print(Topset1)


# In[26]:


# Standard Variables
Water_Table_Elev = 100.0
Seabed_Elev = 200.0
Base_Zone_1 = 14000
Base_Zone_2 = 14000
Base_Zone_3 = 15000
Base_Zone_4 = 16000
Base_Zone_5 = 17000

# Variables for Low Side Pore Pressure
LS_Sea_Water_Density = 0.45
LS_Formation_water_Density_1 = 0.45
LS_Formation_water_Density_2 = 0.45
LS_Formation_water_Density_3 = 0.45
LS_Formation_water_Density_4 = 0.45
LS_Formation_water_Density_5 = 0.45

# Variables for Most Likely Pore Pressure
ML_Sea_Water_Density = 0.47
ML_Formation_water_Density_1 = 0.47
ML_Formation_water_Density_2 = 0.47
ML_Formation_water_Density_3 = 0.47
ML_Formation_water_Density_4 = 0.47
ML_Formation_water_Density_5 = 0.47

# Variables for High Side Pore Pressure
HS_Sea_Water_Density = 0.49
HS_Formation_water_Density_1 = 0.49
HS_Formation_water_Density_2 = 0.49
HS_Formation_water_Density_3 = 0.49
HS_Formation_water_Density_4 = 0.49
HS_Formation_water_Density_5 = 0.49

# Variables for Low Side known pressure anomoly zones
#inyan_kara_swift = ""
LS_20_high_amsden = 2974
LS_300_low_rival = 200
LS_false_bakken_birdbear = 4662

# Variables for Most Likely known pressure anomoly zones
ML_inyan_kara = 2300
ML_swift = 2420
ML_20_high_amsden = 3370
ML_300_low_rival = 370
ML_false_bakken_birdbear = 5562

# Variables for High Side known pressure anomoly zones
HS_inyan_kara = 2600
HS_swift = 2420
HS_20_high_amsden = 3500
HS_300_low_rival = 3993
HS_false_bakken_birdbear = 6462

inyan_kara = Topset1[Topset1['TopName'] == 'Inyan Kara']['MD']
swift = Topset1[Topset1['TopName'] == 'Swift']['MD']
amsden = Topset1[Topset1['TopName'] == 'Amsden']['MD']
frobisher_alida = Topset1[Topset1['TopName'] == 'Frobisher-Alida Interval']['MD']
upper_bakken = Topset1[Topset1['TopName'] == 'Upper Bakken']['MD']
birdbear = Topset1[Topset1['TopName'] == 'Birdbear']['MD']


print((round((amsden)/10)*10 - 10))
print((round((amsden)/10)*10 + 10))
print(amsden)


# In[27]:


for i in range(len(df_LS)):
        if df_LS['DEPTH'][i] <= Water_Table_Elev + shift:
            df_LS['LS_PPG'][i] = 0
            
        elif df_LS['DEPTH'][i] <= Seabed_Elev + shift:
            df_LS['LS_PPG'][i] = (df_LS['DEPTH'][i] - Water_Table_Elev - shift) * LS_Sea_Water_Density
            
        elif df_LS['DEPTH'][i] <= Base_Zone_1 + shift:
             df_LS['LS_PPG'][i] = (LS_Formation_water_Density_1) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PPG'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_2 + shift:
             df_LS['LS_PPG'][i] = (LS_Formation_water_Density_2) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PPG'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_3 + shift:
             df_LS['LS_PPG'][i] = (LS_Formation_water_Density_3) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PPG'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_4 + shift:
             df_LS['LS_PPG'][i] = (LS_Formation_water_Density_4) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PPG'][i-1]
                
        else:
             df_LS['LS_PPG'][i] = (LS_Formation_water_Density_5) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PPG'][i-1]


                
for i in range(len(df_LS)): 
         if round(df_LS['DEPTH'][i]) in range(
             (round((amsden)/10))*10 - 10,
             (round((amsden)/10))*10 + 10):
                 df_LS['LS_PPG'][i] = LS_20_high_amsden

#     if round(df_LS['DEPTH'][i]) in range(
#         (round((frobisher_alida.MD)/10))*10 + 0,
#         (round((frobisher_alida.MD)/10))*10 + 130):
#             df_LS['LS_PPG'][i] = LS_300_low_rival

#     if round(df_LS['DEPTH'][i]) in range(
#         (round((upper_bakken.MD)/10))*10 + 0,
#         (round((birdbear.MD)/10))*10 - 280):
#             df_LS['LS_PPG'][i] = LS_false_bakken_birdbear
                
                
                
                
for i in range(len(df_ML)):
        if df_ML['DEPTH'][i] <= Water_Table_Elev + shift:
            df_ML['ML_PPG'][i] = 0
            
        elif df_ML['DEPTH'][i] <= Seabed_Elev + shift:
            df_ML['ML_PPG'][i] = (df_ML['DEPTH'][i] - Water_Table_Elev - shift) * ML_Sea_Water_Density
            
        elif df_ML['DEPTH'][i] <= Base_Zone_1 + shift:
             df_ML['ML_PPG'][i] = (ML_Formation_water_Density_1) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PPG'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_2 + shift:
             df_ML['ML_PPG'][i] = (ML_Formation_water_Density_2) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PPG'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_3 + shift:
             df_ML['ML_PPG'][i] = (ML_Formation_water_Density_3) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PPG'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_4 + shift:
             df_ML['ML_PPG'][i] = (ML_Formation_water_Density_4) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PPG'][i-1]
                
        else:
             df_ML['ML_PPG'][i] = (ML_Formation_water_Density_5) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PPG'][i-1]
                

                
                
for i in range(len(df_HS)):
        if df_HS['DEPTH'][i] <= Water_Table_Elev + shift:
            df_HS['HS_PPG'][i] = 0
            
        elif df_HS['DEPTH'][i] <= Seabed_Elev + shift:
            df_HS['HS_PPG'][i] = (df_HS['DEPTH'][i] - Water_Table_Elev - shift) * HS_Sea_Water_Density
            
        elif df_HS['DEPTH'][i] <= Base_Zone_1 + shift:
             df_HS['HS_PPG'][i] = (HS_Formation_water_Density_1) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PPG'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_2 + shift:
             df_HS['HS_PPG'][i] = (HS_Formation_water_Density_2) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PPG'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_3 + shift:
             df_HS['HS_PPG'][i] = (HS_Formation_water_Density_3) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PPG'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_4 + shift:
             df_HS['HS_PPG'][i] = (HS_Formation_water_Density_4) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PPG'][i-1]
                
        else:
             df_HS['HS_PPG'][i] = (HS_Formation_water_Density_5) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PPG'][i-1]
                
                
for i in range(len(df_LS)):
    if df_LS['DEPTH'][i] > 0:
        df_LS['LS_PPG'][i] = df_LS['LS_PPG'][i] / df_LS['DEPTH'][i] / 0.052
        
for i in range(len(df_ML)):
    if df_ML['DEPTH'][i] > 0:
        df_ML['ML_PPG'][i] = df_ML['ML_PPG'][i] / df_ML['DEPTH'][i] / 0.052   
        
for i in range(len(df_HS)):
    if df_HS['DEPTH'][i] > 0:
        df_HS['HS_PPG'][i] = df_HS['HS_PPG'][i] / df_HS['DEPTH'][i] / 0.052           


# In[ ]:


fig = make_subplots(rows = 1, cols = 5, shared_yaxes = True)
fig.add_trace(go.Scatter(x = df_LS['LS_PPG'], y = df_LS['DEPTH']), row = 1, col = 1)
fig.add_trace(go.Scatter(x = df_OG_LS['OG OF LS_PP_PPG'], y = df_OG_LS['DEPTH']), row = 1, col = 1)

fig.add_trace(go.Scatter(x = df_ML['ML_PPG'], y = df_ML['DEPTH']), row = 1, col = 2)
fig.add_trace(go.Scatter(x = df_OG_ML['OG OF ML_PP_PPG'], y = df_OG_ML['DEPTH']), row = 1, col = 2)

fig.add_trace(go.Scatter(x = df_HS['HS_PPG'], y = df_HS['DEPTH']), row = 1, col = 3)
fig.add_trace(go.Scatter(x = df_OG_HS['OG OF HS_PP_PPG'], y = df_OG_HS['DEPTH']), row = 1, col = 3)

fig.add_trace(go.Scatter(x = df_LS['LS_PPG'], y = df_LS['DEPTH']), row = 1, col = 4)
fig.add_trace(go.Scatter(x = df_ML['ML_PPG'], y = df_ML['DEPTH']), row = 1, col = 4)
fig.add_trace(go.Scatter(x = df_HS['HS_PPG'], y = df_HS['DEPTH']), row = 1, col = 4)

fig.add_trace(go.Scatter(x = df_OG_LS['OG OF LS_PP_PPG'], y = df_OG_LS['DEPTH']), row = 1, col = 5)
fig.add_trace(go.Scatter(x = df_OG_ML['OG OF ML_PP_PPG'], y = df_OG_ML['DEPTH']), row = 1, col = 5)
fig.add_trace(go.Scatter(x = df_OG_HS['OG OF HS_PP_PPG'], y = df_OG_HS['DEPTH']), row = 1, col = 5)



fig.update_yaxes(title_text = 'Depth', row = 1, col = 1, autorange = 'reversed')
fig.update_xaxes(range = [0,15])
fig.update_layout(title_text = 'Pore Pressure Log Plot', title_x = .5,  height = 700)

fig.update_xaxes(title_text = 'Low Side', row = 1, col = 1)
fig.update_xaxes(title_text = 'Most Likely', row = 1, col = 2)
fig.update_xaxes(title_text = 'High Side', row = 1, col = 3)
fig.update_xaxes(title_text = 'JRS Combined', row = 1, col = 4)
fig.update_xaxes(title_text = 'Standard Combined', row = 1, col = 5)

fig.show()


# In[ ]:


# for i in range(len(df_LS)):

# if OutputLog2.md[i] <= Water_Table_Elev + shift:
# OutputLog2.value[i] = OutputLog2.value[i]*0

# elif OutputLog2.md[i] <= Seabed_Elev + shift:
# OutputLog2.value[i] = (OutputLog2.md[i]- Water_Table_Elev - shift) * LS_Sea_Water_Density

# elif OutputLog2.md[i] <= Base_Zone_1 + shift:
# OutputLog2.value[i] = (LS_Formation_water_Density_1) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

# elif OutputLog2.md[i] <= Base_Zone_2 + shift:
# OutputLog2.value[i] = (LS_Formation_water_Density_2) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1] + shift
# elif OutputLog2.md[i] <= Base_Zone_3 + shift:
# OutputLog2.value[i] = (LS_Formation_water_Density_3) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

# elif OutputLog2.md[i] <= Base_Zone_4 + shift:
# OutputLog2.value[i] = (LS_Formation_water_Density_4) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

# else:
# OutputLog2.value[i] = (LS_Formation_water_Density_5) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]



# In[ ]:



# *** Caclulation to run Low Side Pore Pressure curve
for i in range(len(OutputLog2)):

if OutputLog2.md[i] <= Water_Table_Elev + shift:
OutputLog2.value[i] = OutputLog2.value[i]*0

elif OutputLog2.md[i] <= Seabed_Elev + shift:
OutputLog2.value[i] = (OutputLog2.md[i]- Water_Table_Elev - shift) * LS_Sea_Water_Density

elif OutputLog2.md[i] <= Base_Zone_1 + shift:
OutputLog2.value[i] = (LS_Formation_water_Density_1) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

elif OutputLog2.md[i] <= Base_Zone_2 + shift:
OutputLog2.value[i] = (LS_Formation_water_Density_2) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1] + shift
elif OutputLog2.md[i] <= Base_Zone_3 + shift:
OutputLog2.value[i] = (LS_Formation_water_Density_3) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

elif OutputLog2.md[i] <= Base_Zone_4 + shift:
OutputLog2.value[i] = (LS_Formation_water_Density_4) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]

else:
OutputLog2.value[i] = (LS_Formation_water_Density_5) * (OutputLog2.md[i]- OutputLog2.md[i-1]) + OutputLog2.value[i-1]



## Define a function to calculate lithology interval??????????????

#def function(interval_1,interval_2):
#return range(interval_2 , interval_1)

#int_1 = (round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD +290))
#int_2 = (round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD +310))

#int_range = function(int_1, int_2)
#print(int_range)



for i in range(len(OutputLog2)): 
#if round(OutputLog2.md[i]) in range(
#(round(inyan_kara.MD + 0)),
#(round(swift.MD + 0))):
# OutputLog2.value[i] = LS_inyan_kara_swift

if round(OutputLog2.md[i]) in range(
(round((amsden.MD)/10))*10 -10,
(round((amsden.MD)/10))*10 +10):
OutputLog2.value[i] = LS_20_high_amsden

if round(OutputLog2.md[i]) in range(
(round((frobisher_alida.MD)/10))*10 + 0,
(round((frobisher_alida.MD)/10))*10 + 130):
OutputLog2.value[i] = LS_300_low_rival

if round(OutputLog2.md[i]) in range(
(round((upper_bakken.MD)/10))*10 + 0,
(round((birdbear.MD)/10))*10 - 280):
OutputLog2.value[i] = LS_false_bakken_birdbear


### CONVERT LOW SIDE FROM PSI TO PPG


for i in range(len(OutputLog2)):
if OutputLog2.md[i] > 0:
OutputLog2.value[i] = OutputLog2.value[i] / OutputLog2.md[i] / 0.052


####################################################################################################################
# *** CREATE ANOTHER COPY OF OVBD_PPG_MD_SHIFTED TO MAKE MOST LIKELY PORE PRESSURE LOG AND EDIT ***
# WILL CONVERT TO PPG LATER
OutputLog3 = Logs.create(InputWellName, OutputLogName3, OutputLog2)

# END COPY KB SHIFTED OVBD LOG





# *** Caclulation to run Most Likely Pore Pressure curve

for i in range(len(OutputLog3)):
#if OutputLog3.md[i] == 7220: #Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -20: 
#OutputLog3.value[i] = ML_20_high_amsden 
if OutputLog3.md[i] <= Water_Table_Elev + shift:
OutputLog3.value[i] = OutputLog3.value[i]*0

elif OutputLog3.md[i] <= Seabed_Elev + shift:
OutputLog3.value[i] = (OutputLog3.md[i]- Water_Table_Elev - shift) * ML_Sea_Water_Density

elif OutputLog3.md[i] <= Base_Zone_1 + shift:
OutputLog3.value[i] = (ML_Formation_water_Density_1) * (OutputLog3.md[i]- OutputLog3.md[i-1]) + OutputLog3.value[i-1]

elif OutputLog3.md[i] <= Base_Zone_2 + shift:
OutputLog3.value[i] = (ML_Formation_water_Density_2) * (OutputLog3.md[i]- OutputLog3.md[i-1]) + OutputLog3.value[i-1] + shift
elif OutputLog3.md[i] <= Base_Zone_3 + shift:
OutputLog3.value[i] = (ML_Formation_water_Density_3) * (OutputLog3.md[i]- OutputLog3.md[i-1]) + OutputLog3.value[i-1]

elif OutputLog3.md[i] <= Base_Zone_4 + shift:
OutputLog3.value[i] = (ML_Formation_water_Density_4) * (OutputLog3.md[i]- OutputLog3.md[i-1]) + OutputLog3.value[i-1]


else:
OutputLog3.value[i] = (ML_Formation_water_Density_5) * (OutputLog3.md[i]- OutputLog3.md[i-1]) + OutputLog3.value[i-1]




# try except block
# try:
# block of code
# except Exception as e:
# print(e)

print((round((inyan_kara.MD)/10))*10)

for i in range(len(OutputLog3)): 

# continue function removes the calculation starting at the inyan kara +20 to swift -10 interval
# without this continue function- its the steeper gradient to the bottom value. 
# with thecontinue function - the original gradient is placed in making a much higher angle vertical line

# if round(OutputLog3.md[i]) in range(
# (round((inyan_kara.MD)/10))*10 + 20,
# (round((swift.MD)/10))*10 - 10):
# continue
# define value at the top of the Inyan Kara
if round(OutputLog3.md[i]) in range(
(round((inyan_kara.MD)/10))*10,
(round((swift.MD)/10))*10 - 0):
OutputLog3.value[i] = ML_inyan_kara

# define value at the top of the Swift
if round(OutputLog3.md[i]) in range(
(round((swift.MD)/10))*10 + 0,
(round((swift.MD)/10))*10 +20):
OutputLog3.value[i] = ML_swift

if round(OutputLog3.md[i]) in range(
(round((amsden.MD)/10))*10 -10,
(round((amsden.MD)/10))*10 + 10):
OutputLog3.value[i] = ML_20_high_amsden

if round(OutputLog3.md[i]) in range(
(round((frobisher_alida.MD)/10))*10 + 0,
(round((frobisher_alida.MD)/10))*10 + 130):
OutputLog3.value[i] = ML_300_low_rival

if round(OutputLog3.md[i]) in range(
(round((upper_bakken.MD)/10))*10 + 0,
(round((birdbear.MD)/10))*10 - 280):
OutputLog3.value[i] = ML_false_bakken_birdbear


### CONVERT MOST LIKELY FROM PSI TO PPG


for i in range(len(OutputLog3)):
if OutputLog3.md[i] > 0:
OutputLog3.value[i] = OutputLog3.value[i] / OutputLog3.md[i] / 0.052






#############################################################################################################################################
# *** CREATE ANOTHER COPY OF OVBD_PPG_MD_SHIFTED TO MAKE MOST LIKELY PORE PRESSURE LOG AND EDIT ***
# WILL CONVERT TO PPG LATER
OutputLog4 = Logs.create(InputWellName, OutputLogName4, OutputLog3)

# END COPY KB SHIFTED OVBD LOG


# *** Caclulation to run High Side Pore Pressure curve

for i in range(len(OutputLog4)):
#if OutputLog4.md[i] == 7220: #Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -20: 
#OutputLog4.value[i] = HS_20_high_amsden 

if OutputLog4.md[i] <= Water_Table_Elev + shift:
OutputLog4.value[i] = OutputLog4.value[i]*0

elif OutputLog4.md[i] <= Seabed_Elev + shift:
OutputLog4.value[i] = (OutputLog4.md[i]- Water_Table_Elev - shift) * HS_Sea_Water_Density

elif OutputLog4.md[i] <= Base_Zone_1 + shift:
OutputLog4.value[i] = (HS_Formation_water_Density_1) * (OutputLog4.md[i]- OutputLog4.md[i-1]) + OutputLog4.value[i-1]

elif OutputLog4.md[i] <= Base_Zone_2 + shift:
OutputLog4.value[i] = (HS_Formation_water_Density_2) * (OutputLog4.md[i]- OutputLog4.md[i-1]) + OutputLog4.value[i-1] + shift
elif OutputLog4.md[i] <= Base_Zone_3 + shift:
OutputLog4.value[i] = (HS_Formation_water_Density_3) * (OutputLog4.md[i]- OutputLog4.md[i-1]) + OutputLog4.value[i-1]

elif OutputLog4.md[i] <= Base_Zone_4 + shift:
OutputLog4.value[i] = (HS_Formation_water_Density_4) * (OutputLog4.md[i]- OutputLog4.md[i-1]) + OutputLog4.value[i-1]


else:
OutputLog4.value[i] = (HS_Formation_water_Density_5) * (OutputLog4.md[i]- OutputLog4.md[i-1]) + OutputLog4.value[i-1]




for i in range(len(OutputLog4)): 
if round(OutputLog4.md[i]) in range(
(round((inyan_kara.MD)/10))*10 + 0,
(round((swift.MD)/10))*10 + 0):
OutputLog4.value[i] = HS_inyan_kara

if round(OutputLog4.md[i]) in range(
(round((amsden.MD)/10))*10 -10,
(round((amsden.MD)/10))*10 +10):
OutputLog4.value[i] = HS_20_high_amsden

if round(OutputLog4.md[i]) in range(
(round((frobisher_alida.MD)/10))*10 + 0,
(round((frobisher_alida.MD)/10))*10 + 120):
OutputLog4.value[i] = HS_300_low_rival

if round(OutputLog4.md[i]) in range(
(round((upper_bakken.MD)/10))*10 + 0,
(round((birdbear.MD)/10))*10 - 280):
OutputLog4.value[i] = HS_false_bakken_birdbear

### CONVERT MOST LIKELY FROM PSI TO PPG


for i in range(len(OutputLog4)):
if OutputLog4.md[i] > 0:
OutputLog4.value[i] = OutputLog4.value[i] / OutputLog4.md[i] / 0.052







### Add Lithology to predefined intervals using a PPG insert

# Define a range in multiples of 10 to match step-rate of log MD values of original log: OVBD_PPG
# High Side Amsden that works!!
#for output in range(
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -30)),
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -10)),1):
#print(output)

# Check if value is in list and append the PPG data to the log
#for i in range(len(OutputLog4)):
# if round(OutputLog4.md[i]) in range(
# (round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -30)),
# (round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -10))):
# print("yes, "+'HS_20_high_amsden'+" found in list:", range),
# OutputLog4.value[i] = HS_20_high_amsden


#print(round(HS_20_high_amsden))

#print("20' high from Amsden is: " + str(round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -23,-1)) + "'")
###################################################


# Define a range in multiples of 10 to match step-rate of log MD values of original log: OVBD_PPG
# Low Side Frobisher Alida test

## below is unneccecsary but helpful to see the values sometimes
#for output in range(
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD -30)),
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD -10)),1):
#print(output)




#### Below code works, just grayed out to test PSI insert before conversion to PPG

# Check if value is in list and append the PPG data to the log
#for i in range(len(OutputLog2)):
#if round(OutputLog2.md[i]) in range(
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD +190)),
#(round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD +210))):
#print("yes, "+'LS_300_low_rival'+" found in list:", range),
#OutputLog2.value[i] = LS_300_low_rival


#print(round(LS_300_low_rival,2))
#amsden_depth = round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -10)
#i = OutputLog4.indexByMD[round(Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -30)]
#OutputLog4.value[i] = HS_20_high_amsden

#for i in range(len(OutputLog4)):
#if OutputLog4.md[i] == '7220': #Wells[InputWellName].TopSets["Topset1"].Tops["AMSDEN"].MD -20: 
#OutputLog4.value[i] = HS_20_high_amsden


#print("300' low from Frobisher Alida is: " + str(round(Wells[InputWellName].TopSets["Topset1"].Tops["FROBISHER-ALIDA_INTERVAL"].MD +300,-1)) + "'")






if __name__ == "__main__":
try:
main()
except Exception as ex:
print(ex)



# In[ ]:




