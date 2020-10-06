import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

class Ausw:
    def __init__(self, file, name, f, scale, tick, magnet, lit, hight):
        self.name = name
        self.hight = hight
        self.f = f
        self.scale = scale
        self.magnet = magnet
        self.k = 0
        self.lit = lit
        self.t = tick
        self.UB = []
        self.UA = []
        self.B0 = [0] * len(file)
        
        for f in file:
            self.UA.append([])
            self.UB.append([])
            for i, line in enumerate(f):
                if i > 4:
                    tx = line.replace(',', '.').replace('\t', ',')
                    l = re.split(',', tx)
                    self.UA[-1].append(float(l[2]))
                    self.UB[-1].append(float(l[1]))
    
    def plot(self):
        for j, U_A in enumerate(self.UA):
            U_B = self.UB[j]
            minU = 0
            ind = 0
            for i, U in enumerate(U_B):
                if U < minU:
                    minU = U
                    ind = i
            self.B0[j] = U_A[ind]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            df = pd.DataFrame({'U_A': U_A, 'U_B': U_B})
            df.plot(x = 'U_A', y = 'U_B', color = 'red', marker = ',', ax = ax, legend = False)
            plt.vlines(self.B0[j], -1, minU, color = 'k')
            plt.axis(self.scale[j])
            plt.xticks(list(plt.xticks()[0]) + [self.B0[j]])
            xticks = ax.xaxis.get_major_ticks()
            xticks[self.t[j]].label1.set_visible(False)
            plt.ylabel(r'Spannung $U_B$ [V]')
            plt.xlabel(r'Spannung $U_A$ [V]')
            plt.grid(True)
            plt.savefig(self.name[j] + '.png', dpi = 900)
            plt.show()
            
        for i, B in enumerate(self.B0):
            if i == 0:
                self.k = (self.f[i] - self.lit * self.magnet[i] * 10 ** (-3)) / (self.lit * B)
                print('Koeffizient B=kU: k = ' + str(self.k))
            else:
                print(self.f[i] / (self.magnet[i] * 10 ** (-3) + self.k * B))
    
    def plot2(self):
        for j, U_A in enumerate(self.UA):
            U_B = self.UB[j]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            if j == 3:
                df = pd.DataFrame({'U_A1': U_A[:int(len(U_A) / 2) - 1100], 'U_B1': U_B[:int(len(U_B) / 2) - 1100]})
                df2 = pd.DataFrame({'U_A2': U_A[int(len(U_A) / 2) - 1100:], 'U_B2': U_B[int(len(U_B) / 2) - 1100:]})
            else:
                df = pd.DataFrame({'U_A1': U_A[:int(len(U_A) / 2)], 'U_B1': U_B[:int(len(U_B) / 2)]})
                df2 = pd.DataFrame({'U_A2': U_A[int(len(U_A) / 2):], 'U_B2': U_B[int(len(U_B) / 2):]})
            UA1 = []
            UB1 = []
            UA2 = []
            UB2 = []
            if j == 3:
                offset = 1.2
            else:
                offset = 0.5
            for i, U in enumerate(U_A):
                if U < offset and U > -offset:
                    if i < len(U_A) / 2:
                        UA1.append(U)
                        UB1.append(U_B[i])
                    else:
                        UA2.append(U)
                        UB2.append(U_B[i])
            
            coefr = np.polyfit(UA1, UB1, 100)
            poly1d_fnr = np.poly1d(coefr) 
            coefb = np.polyfit(UA2, UB2, 100)
            poly1d_fnb = np.poly1d(coefb)
            
            UBr = 0
            cr = 0
            UBb = 0
            cb = 0
            minr = 0
            minb = 0
            for i, U in enumerate(U_B):
                if U_A[i] < self.hight[j][0] or U_A[i] > self.hight[j][1]:
                    if i < len(U_B) / 2:
                        UBr += U
                        cr += 1
                    else:
                        UBb += U
                        cb += 1
                if i < len(U_B) / 2:
                    if U < minr:
                        minr = U
                else:
                    if U < minb:
                        minb = U
            UBr /= cr
            UBb /= cb
            
            print('rot: ' + str(minr) + ' ' + str(UBr) + ' ' + str((-minr + UBr) / 2 - UBr))
            print('blau: ' + str(minb) + ' ' + str(UBb) + ' ' + str((-minb + UBb) / 2 - UBb))
            
            xr = (poly1d_fnr + (-minr + UBr) / 2 - UBr).roots
            xb = (poly1d_fnb + (-minb + UBb) / 2 - UBb).roots
            out = []
            
            if j == 0:
                for x in xr:
                    if np.isreal(x):
                        print(x)
               # print('furz')
               # for x in xb:
                   # if np.isreal(x):
                       # print(x)

            for x in xr:
                x = np.real_if_close(x)
                if x < self.hight[j][1] and x > self.hight[j][0]:
                    if np.isreal(x):
                        print('rot: ' + str(x))
                        out.append(x) 
            for x in xb:
                x = np.real_if_close(x)
                if x < self.hight[j][1] and x > self.hight[j][0]:
                    if np.isreal(x):
                        print('blau: ' + str(x))
                        out.append(x)
                
            df.plot(x = 'U_A1', y = 'U_B1', color = 'red', marker = ',', ax = ax, legend = False, alpha = 0.5)
            df2.plot(x = 'U_A2', y = 'U_B2', color = 'blue', marker = ',', ax = ax, legend = False, alpha = 0.5)
            if j == 3:
                plt.plot(np.linspace(-0.5, 0.5, 100000), poly1d_fnr(np.linspace(-0.5, 0.5, 100000)), 'r-')
                plt.plot(np.linspace(-0.5, 0.5, 100000), poly1d_fnb(np.linspace(-0.5, 0.5, 100000)), 'b-')
            else:
                plt.plot(np.linspace(-0.4, 0.4, 100000), poly1d_fnr(np.linspace(-0.4, 0.4, 100000)), 'r-')
                plt.plot(np.linspace(-0.4, 0.4, 100000), poly1d_fnb(np.linspace(-0.4, 0.4, 100000)), 'b-')  
            plt.ylabel(r'Spannung $U_B$ [V]')
            plt.xlabel(r'Spannung $U_A$ [V]')
            plt.legend(['Messwerte', 'Messwerte', 'Ausgleichskurve', 'Ausgleichskurve'])
            plt.autoscale(True)
            plt.grid(True)
            plt.savefig(self.name[j] + '_2.png', dpi = 900)
            plt.show()
                

scales = [[-2, 2, -0.25, 0.1], [-2, 2, -0.15, 0.1], [-2, 2, -0.15, 0.2], [-2.5, 2.5, -0.1, 0.05]]
frequencies = [17.8975, 18.3016, 17.8545, 17.8899]
magnet = [412, 421, 412, 412]
ticks = [4, 4, 4, 3]
files = [open('glycerin1.txt', 'r'), open('glycerin2.txt', 'r'), open('wasser.txt', 'r'), open('teflon1.txt', 'r')]
names = ['glycerin1', 'glycerin2', 'wasser', 'teflon']
lit = 42.576
h = [[-0.25, 0.1], [0, 0.3], [-0.1, 0.3], [-1, 0.5]]
a1 = Ausw(files, names, frequencies, scales, ticks, magnet, lit, h)
a1.plot()
a1.plot2()
