from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import brainRhythms as br

#This Example reads EEG data from Emotiv, then saves it as a .txt file

#Setting variables
fs = 128
dx = 1/250
time = 7 #seconds
channels = 14

EEG,headset = br.readEEG(fs,time,channels)
EEG_n = br.normalizeEEG(EEG)

filename = 'EEGdata'
br.saveEEGTxt(EEG,filename,Header)
