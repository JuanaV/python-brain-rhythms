from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import brainRhythms as br


app = QtGui.QApplication([])

#Setting variables
fs = 128
dx = 1/250
time = 0.4
channels = 14
win_size = 5
color = [(255,102,102),(255,178,102),(255, 255, 102),(178, 255, 102),(102, 255, 102),(102, 255, 178),(102,255,255),(102,178,255)]
#Deg = [90., 45., 330., 300., 240., 210., 150., 120.]
Deg = [90., 45., 0. ,315., 270. , 225., 180., 135.]
f_min = 0.8
w = (1/f_min)*fs

EEG,headset = br.readEEG(fs,time,channels)
EEG_n = br.normalizeEEG(EEG)

y = EEG_n.transpose()
x = np.linspace(0,time,fs*time)

ri = br.rhythmsAllWaves(fs,dx,EEG)
#ri = br.rhythmsBasicWaves(fs,dx,EEG)
r =  br.normalizeRhythms(ri)

xr,yr = br.wavesDiagram(r,Deg)

#Main Window
win = pg.GraphicsWindow(title="EEG Data System")
win.resize(1000,600)

win.setWindowTitle('EEG Data System')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

#--------------------------------------------------------
#Rhythms Bar Graphic
plt1 = win.addPlot(title="Brain Rhythms", row=0, col=0,colspan=2)
#plt1.setWindowTitle('Brain Rhythms')
plt1.getAxis('bottom').setTicks([[(0, 'Delta'), (1, 'Theta'), (2, 'Low\nAlpha'), (3, 'High\nAlpha'), (4, 'Low\nBeta'), (5, 'High\nBeta'), (6, 'Low\nGamma'), (7, 'High\nGamma')]])
plt1.setLabel('left', 'Energy', units='%')
#plt1.resize(350, 500)
plt1.setYRange(0, 105)
plt1.setGeometry(0,100, 100,60 ) 

c= color

graph = dict()
for i in range(len(r)):
    graph[str(i)] = pg.BarGraphItem(x=[i], height=[r[i]], width=0.5, brush=c[i])
    plt1.addItem(graph["%s" %(str(i))]) 

#--------------------------------------------------------
#Waves Diagram
plt2 = win.addPlot(title="Waves Diagram",row=0, col=2,colspan=1)
plt2.hideAxis('bottom')
plt2.hideAxis('left')
plt2.setYRange(-150, 150)
plt2.setXRange(-150, 150)
#plt2.resize(100, 100)

#x_p = [0,70,86,50,-50,-86,-86,-50]
#y_p = [100,70,-50,-86,-86,-50,50,86]

x_p = [0,70,100,70,0,-70,-100,-70]
y_p = [100,70,0,-70,-100,-70,0,70]

waves_name = ['Delta','Theta', 'Low\nAlpha', 'High\nAlpha', 'Low\nBeta', 'High\nBeta', 'Low\nGamma', 'High\nGamma']

for l in range(len(x_p)):
    if l < len(x_p)/2:
        text = pg.TextItem(waves_name[l])
        text.setPos(x_p[l]+10, y_p[l]+15)
        plt2.addItem(text)
    else: 
        text = pg.TextItem(waves_name[l])
        text.setPos(x_p[l]-40, y_p[l]+15)
        plt2.addItem(text)



waves = []
wavesx = []
wavesy = []
waves.append(plt2.plot(x_p, y_p, pen=None, symbol='o', symbolPen=(255,178,102), symbolBrush=(153,255,204,230)))
waves.append(plt2.plot(xr, yr, pen=(255,255,102), fillLevel=0, fillBrush=(102,255,102,40)))
wavesx.append(xr)
wavesy.append(yr)

#plt2.plot(xr, yr, pen=(255,255,102), fillLevel=0, fillBrush=(102,255,102,40))
#plt2.plot(x_p, y_p, pen=None, symbol='o', symbolPen=(51,153,255), symbolBrush=(153,255,204))
#--------------------------------------------------------

win.nextRow()
#--------------------------------------------------------
#EEG Plot
plt3 = win.addPlot(title="EEG",row=1, col=0, colspan=3)
plt3.setWindowTitle('EEG Signal')
plt3.setLabel('bottom', 'Time', units='sec')
plt3.getAxis('left').setTicks([[(100, 'F3'), (200, 'F4'), (300, 'P7'), (400, 'FC6'), (500, 'F7'), (600, 'F8'), (700, 'T7'), (800, 'P8'), (900, 'FC5'), (1000, 'AF4'), (1100, 'T8'), (1200, 'O2'), (1300, 'O1'), (1400, 'AF3')]])
plt3.setYRange(0, (channels*100)+20)
plt3.setXRange(0, win_size)
#plt3.resize(1000, 300)

curve = []
for i in range(channels):
    c = plt3.plot(x, y[i], pen=(i,14))  ## setting pen=(i,3) automaticaly creates three different-colored pe
    c.setPos(0,i)
    curve.append(c)
counter = time

x = np.linspace(0,win_size,fs*win_size)
xT = np.linspace(0,win_size,fs*win_size)

instant = 1

def update():
    global curve, waves, wavesx, wavesy, y, x, xT, ri, r, EEG_n, counter,instant, headset, time,fs, win_size

    EEG_new = br.readEEG2(fs,time,channels,headset)
    EEG_n_new = br.normalizeEEG(EEG_new )
    y2 = EEG_n_new.transpose()

    
    #--------------------------------------------------------
    #Rhythms Bar Graphic
    if EEG_n.shape[0] < w-1:
        EEG_n = np.r_[EEG_n,EEG_n_new]
    else:
        EEG_n = np.r_[EEG_n,EEG_n_new]
        EEG_n = EEG_n[-w:,:]

    ri = br.rhythmsAllWaves(fs,dx,EEG_n)
    #ri = br.rhythmsBasicWaves(fs,dx,EEG_n)
    r =  br.normalizeRhythms(ri)

    for i in range(len(r)):
        graph["%s" %(str(i))].setOpts(x=[i], height=[r[i]])

    #--------------------------------------------------------
    #Waves Diagram
    xr_new,yr_new = br.wavesDiagram(r,Deg)

    if instant < 3:
        waves.append(plt2.plot(xr_new, yr_new, pen=(255,255,102), fillLevel=0, fillBrush=(102,255,102,40)))
        #plt2.plot(x_p, y_p, pen=None, symbol='o', symbolPen=(51,153,255), symbolBrush=(153,255,204))
        wavesx.append(xr_new)
        wavesy.append(yr_new)
        instant += 1
    else:
        wavesx.append(xr_new)
        wavesy.append(yr_new)
        for k in range(1,len(waves)):
            waves[k].setData(wavesx[k],wavesy[k])
        wavesx = wavesx[-len(waves):]
        wavesy = wavesy[-len(waves):]
              
    #--------------------------------------------------------
    #EEG Plot
    
    if np.ceil(counter) < win_size:
        y = np.c_[y,y2]
        x = xT[:y.shape[1]]
    else:
        y = np.c_[y,y2]
        y = y[:,int(time*fs):]

    for i in range(channels):
        curve[i].setData(x,y[i])
    counter = counter + time



timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()