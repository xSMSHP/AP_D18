import re
import matplotlib.pyplot as plt
import pandas as pd

class Ausw:
    def __init__(self, file, name, f, scale, tick, magnet, lit):
        self.name = name
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
                

scales = [[-2, 2, -0.25, 0.1], [-2, 2, -0.15, 0.1], [-2, 2, -0.15, 0.2], [-2.5, 2.5, -0.1, 0.05]]
frequencies = [17.8975, 18.3016, 17.8545, 17.8899]
magnet = [412, 421, 412, 412]
ticks = [4, 4, 4, 3]
files = [open('glycerin1.txt', 'r'), open('glycerin2.txt', 'r'), open('wasser.txt', 'r'), open('teflon1.txt', 'r')]
names = ['glycerin1', 'glycerin2', 'wasser', 'teflon']
lit = 42.576
a1 = Ausw(files, names, frequencies, scales, ticks, magnet, lit)
a1.plot()
