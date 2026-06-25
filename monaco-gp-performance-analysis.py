import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
lap=pd.read_csv('lap_times.csv')
race=pd.read_csv('races.csv')
driver=pd.read_csv('drivers.csv')
pit=pd.read_csv('pit_stops.csv',usecols=['raceId','driverId','stop','lap'])
race=race.drop(columns=['url'])
driver=driver.drop(columns=['url'])
ma=race.merge(lap,on='raceId')
merge=ma.merge(driver,on='driverId')
merge=merge[(merge['year']==2023) & (merge['name']=="Monaco Grand Prix")]
merge['milliseconds']=merge['milliseconds']/1000
merge['min']=merge['milliseconds']/60
try_merge=merge.merge(pit,on=['raceId','driverId','lap'])
try_merge_h=try_merge[try_merge['surname']=='Hamilton']
pit_1=try_merge_h['lap'].iloc[0]
pit_2=try_merge_h['lap'].iloc[1]
print(pit)
ham=merge[merge['surname']=='Hamilton']
fuel=110000
tyre=100

for i in range(len(ham['lap'])):
    ham['fuel']=fuel-(ham['lap']*1350)

ham.loc[ham['lap']<pit_1,'tyre_age']=tyre-(ham['lap']*2.5)
ham.loc[(ham['lap']>=pit_1) & (ham['lap']<pit_2),'tyre_age']=tyre-((ham['lap']-pit_1)*2.5)
ham.loc[ham['lap']>=pit_2,'tyre_age']=tyre-((ham['lap']-pit_2)*2.5)

ham['temp']=400+(1.5*ham['lap']+(25*(np.sin(ham['lap']))))

try_merge_v=try_merge[try_merge['surname']=='Verstappen']

pit_1_v=try_merge_v['lap'].iloc[0]


ver=merge[merge['surname']=='Verstappen']
for i in range(len(ver['lap'])):
    ver['fuel']=fuel-(ver['lap']*1350)

ver.loc[ver['lap']<pit_1_v,'tyre_age']=tyre-(ver['lap']*2.5)
ver.loc[ver['lap']>=pit_1_v,'tyre_age']=tyre-((ver['lap']-pit_1_v)*2.5)
ver['tyre_age']=ver['tyre_age'].clip(lower=10)
ver['temp']=400+(1.5*ver['lap']+(25*(np.sin(ver['lap']))))

f,a=plt.subplots(2,2,figsize=(10,7))
a[0,0].plot(ham['lap'],ham['min'],color='#00D7B6')

a[0,1].plot(ham['lap'],ham['fuel'],color="#00FFD9",linewidth='3')

a[1,0].plot(ham['lap'],ham['tyre_age'],color='#00D7B6')

a[1,1].plot(ham['lap'],ham['temp'],color="#00FFD9",linewidth='3')


a[0,0].plot(ver['lap'],ver['min'],color="#001E4BFF")
a[0,0].set_ylabel("Lap Time (Minutes)")
a[0,0].set_xlabel("Lap Number")
a[0,0].set_title("Lap Time")

a[0,1].plot(ver['lap'],ver['fuel'],color="#001E4BFF",linestyle='dashed')
a[0,1].set_ylabel("Fuel Level (in gram's)")
a[0,1].set_xlabel("Lap Number")
a[0,1].set_title("Fuel Consumption")

a[1,0].plot(ver['lap'],ver ['tyre_age'],color='#001E4BFF')
a[1,0].set_ylabel("Tyre degradation (%)")
a[1,0].set_xlabel("Lap Number")
a[1,0].set_title("Tyre degradation")

a[1,1].plot(ver['lap'],ver['temp'],color='#001E4BFF',linestyle='dashed')
a[1,1].set_ylabel("Temperature")
a[1,1].set_xlabel("Lap Number")
a[1,1].set_title("Temperature Variation")

f.suptitle("Comprehensive Performance Analysis| Monaco Grand Prix 2023\nLewis Hamilton & Max Verstappen", fontsize=14, fontweight='bold')

a[0, 0].legend(["Verstappen", "Hamilton"], loc="upper left")
a[0, 1].legend(["Verstappen", "Hamilton"], loc="upper right")
a[1, 0].legend(["Verstappen", "Hamilton"], loc="lower left")
a[1, 1].legend(["Verstappen", "Hamilton"], loc="upper left")
plt.tight_layout()
plt.show()