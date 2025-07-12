import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_file = "D:/School/IIT-PHD/FIeld Study/master_results.csv"

fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(6.5, 9))



df = pd.read_csv(data_file)


# AlbuquerqueNM
row = df[df['Climate'] == 'Boulder']

gr_24 = list(row['24 hr Ratio'])
gr_48 = list(row['48 hr Ratio'])
gr_168 = list(row['168 hr Ratio'])
set_hours = list(row['SET Hours'])

R = np.corrcoef(gr_24, set_hours)[0,1]
R_Squared_24 = R*R

axs[0,0].plot(gr_24, set_hours, 'o', color='blue')
m_24, b_24 = np.polyfit(gr_24, set_hours, 1)
axs[0,0].plot(gr_24, m_24*gr_24+b_24, color='blue', label=('24 hr R2=' + str(round(R_Squared_24,3))))

ratio_alb = round(((120 - b_24) / m_24), 3)

R = np.corrcoef(gr_48, set_hours)[0,1]
R_Squared_48 = R*R

axs[0,0].plot(gr_48, set_hours, 'o', color='orange')
m_48, b_48 = np.polyfit(gr_48, set_hours, 1)
axs[0,0].plot(gr_48, m_48*gr_48+b_48, color='orange', label=('48 hr R2=' + str(round(R_Squared_48,3))))

R = np.corrcoef(gr_168, set_hours)[0,1]
R_Squared_168 = R*R

axs[0,0].plot(gr_168, set_hours, 'o', color='green')
m_168, b_168 = np.polyfit(gr_168, set_hours, 1)
axs[0,0].plot(gr_168, m_168*gr_168+b_168, color='green', label=('168 hr R2=' + str(round(R_Squared_168,3))))

axs[0,0].axhline(y=120, color='r', linestyle='--')
axs[0,0].set_xlim(0, 1)
# axs[0,0].set_xlabel('Degree Hour Ratio [°F Hr]')
axs[0,0].set_ylabel('SET Hours [°F Hr]')
axs[0,0].legend(loc='best', fontsize=6)
axs[0,0].set_title('Albuquerque, NM\n Ratio = ' + str(ratio_alb), fontsize=8)

# ChicagoIL

row = df[df['Climate'] == 'Chicago']

gr_24 = row['24 hr Ratio']
gr_48 = row['48 hr Ratio']
gr_168 = row['168 hr Ratio']
set_hours = row['SET Hours']

R = np.corrcoef(gr_24, set_hours)[0,1]
R_Squared_24 = R*R

axs[0,1].plot(gr_24, set_hours, 'o', color='blue')
m_24, b_24 = np.polyfit(gr_24, set_hours, 1)
axs[0,1].plot(gr_24, m_24*gr_24+b_24, color='blue', label=('24 hr R2=' + str(round(R_Squared_24,3))))

ratio_chi = round(((120 - b_24) / m_24), 3)

R = np.corrcoef(gr_48, set_hours)[0,1]
R_Squared_48 = R*R

axs[0,1].plot(gr_48, set_hours, 'o', color='orange')
m_48, b_48 = np.polyfit(gr_48, set_hours, 1)
axs[0,1].plot(gr_48, m_48*gr_48+b_48, color='orange', label=('48 hr R2=' + str(round(R_Squared_48,3))))

R = np.corrcoef(gr_168, set_hours)[0,1]
R_Squared_168 = R*R

axs[0,1].plot(gr_168, set_hours, 'o', color='green')
m_168, b_168 = np.polyfit(gr_168, set_hours, 1)
axs[0,1].plot(gr_168, m_168*gr_168+b_168, color='green', label=('168 hr R2=' + str(round(R_Squared_168,3))))

axs[0,1].axhline(y=120, color='r', linestyle='--')
axs[0,1].set_xlim(0, 1)
# axs[0,1].set_xlabel('Degree Hour Ratio [°F Hr]')
# axs[0,1].set_ylabel('SET Hours [°F Hr]')
axs[0,1].legend(loc='best', fontsize=6)
axs[0,1].set_title('Chicago, IL\n Ratio = ' + str(ratio_chi), fontsize=8)

# ElPasoTX

row = df[df['Climate'] == 'Minneapolis']

gr_24 = row['24 hr Ratio']
gr_48 = row['48 hr Ratio']
gr_168 = row['168 hr Ratio']
set_hours = row['SET Hours']

R = np.corrcoef(gr_24, set_hours)[0,1]
R_Squared_24 = R*R

axs[1,0].plot(gr_24, set_hours, 'o', color='blue')
m_24, b_24 = np.polyfit(gr_24, set_hours, 1)
axs[1,0].plot(gr_24, m_24*gr_24+b_24, color='blue', label=('24 hr R2=' + str(round(R_Squared_24,3))))

ratio_ep = round(((120 - b_24) / m_24), 3)

R = np.corrcoef(gr_48, set_hours)[0,1]
R_Squared_48 = R*R

axs[1,0].plot(gr_48, set_hours, 'o', color='orange')
m_48, b_48 = np.polyfit(gr_48, set_hours, 1)
axs[1,0].plot(gr_48, m_48*gr_48+b_48, color='orange', label=('48 hr R2=' + str(round(R_Squared_48,3))))

R = np.corrcoef(gr_168, set_hours)[0,1]
R_Squared_168 = R*R

axs[1,0].plot(gr_168, set_hours, 'o', color='green')
m_168, b_168 = np.polyfit(gr_168, set_hours, 1)
axs[1,0].plot(gr_168, m_168*gr_168+b_168, color='green', label=('168 hr R2=' + str(round(R_Squared_168,3))))

axs[1,0].axhline(y=120, color='r', linestyle='--')
axs[1,0].set_xlim(0, 1)
# axs[1,0].set_xlabel('Degree Hour Ratio [°F Hr]')
axs[1,0].set_ylabel('SET Hours [°F Hr]')
axs[1,0].legend(loc='best', fontsize=6)
axs[1,0].set_title('ElPaso, TX\n Ratio = ' + str('n/a'), fontsize=8)


# GreatFallsMT

row = df[df['Climate'] == 'Helena']

gr_24 = row['24 hr Ratio']
gr_48 = row['48 hr Ratio']
gr_168 = row['168 hr Ratio']
set_hours = row['SET Hours']

R = np.corrcoef(gr_24, set_hours)[0,1]
R_Squared_24 = R*R

axs[1,1].plot(gr_24, set_hours, 'o', color='blue')
m_24, b_24 = np.polyfit(gr_24, set_hours, 1)
axs[1,1].plot(gr_24, m_24*gr_24+b_24, color='blue', label=('24 hr R2=' + str(round(R_Squared_24,3))))

ratio_gf = round(((120 - b_24) / m_24), 3)

R = np.corrcoef(gr_48, set_hours)[0,1]
R_Squared_48 = R*R

axs[1,1].plot(gr_48, set_hours, 'o', color='orange')
m_48, b_48 = np.polyfit(gr_48, set_hours, 1)
axs[1,1].plot(gr_48, m_48*gr_48+b_48, color='orange', label=('48 hr R2=' + str(round(R_Squared_48,3))))

R = np.corrcoef(gr_168, set_hours)[0,1]
R_Squared_168 = R*R

axs[1,1].plot(gr_168, set_hours, 'o', color='green')
m_168, b_168 = np.polyfit(gr_168, set_hours, 1)
axs[1,1].plot(gr_168, m_168*gr_168+b_168, color='green', label=('168 hr R2=' + str(round(R_Squared_168,3))))

axs[1,1].axhline(y=120, color='r', linestyle='--')
axs[1,1].set_xlim(0, 1)
# axs[1,1].set_xlabel('Degree Hour Ratio [°F Hr]')
# axs[1,1].set_ylabel('SET Hours [°F Hr]')
axs[1,1].legend(loc='best', fontsize=6)
axs[1,1].set_title('Great Falls, MT\n Ratio = ' + str(ratio_gf), fontsize=8)

# InternationalFallsMN

row = df[df['Climate'] == 'Duluth']

gr_24 = row['24 hr Ratio']
gr_48 = row['48 hr Ratio']
gr_168 = row['168 hr Ratio']
set_hours = row['SET Hours']

R = np.corrcoef(gr_24, set_hours)[0,1]
R_Squared_24 = R*R

axs[2,0].plot(gr_24, set_hours, 'o', color='blue')
m_24, b_24 = np.polyfit(gr_24, set_hours, 1)
axs[2,0].plot(gr_24, m_24*gr_24+b_24, color='blue', label=('24 hr R2=' + str(round(R_Squared_24,3))))

ratio_if = round(((120 - b_24) / m_24), 3)

R = np.corrcoef(gr_48, set_hours)[0,1]
R_Squared_48 = R*R

axs[2,0].plot(gr_48, set_hours, 'o', color='orange')
m_48, b_48 = np.polyfit(gr_48, set_hours, 1)
axs[2,0].plot(gr_48, m_48*gr_48+b_48, color='orange', label=('48 hr R2=' + str(round(R_Squared_48,3))))

R = np.corrcoef(gr_168, set_hours)[0,1]
R_Squared_168 = R*R

axs[2,0].plot(gr_168, set_hours, 'o', color='green')
m_168, b_168 = np.polyfit(gr_168, set_hours, 1)
axs[2,0].plot(gr_168, m_168*gr_168+b_168, color='green', label=('168 hr R2=' + str(round(R_Squared_168,3))))

axs[2,0].axhline(y=120, color='r', linestyle='--')
axs[2,0].set_xlim(0, 1)
# axs[2,0].set_xlabel('Degree Hour Ratio [°F Hr]')
axs[2,0].set_ylabel('SET Hours [°F Hr]')
axs[2,0].legend(loc='best', fontsize=6)
axs[2,0].set_title('International Falls, MN\n Ratio = ' + str(ratio_if), fontsize=8)



fig.tight_layout(pad=3)
fig.suptitle('Correlation of Degree Hours and SET Hours')






plt.show()