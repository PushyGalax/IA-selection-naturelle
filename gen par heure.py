import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('tempsia.csv')
    x = data['generation'].tolist()
    y2 = data['tempsmax'].tolist()

    cpt=0
    i=0
    heure=0
    novx=[]
    novy=[]

    plt.cla()

    for elem in y2:
        i+=1
        cpt+=elem
        if cpt >= 3600:
            heure+=1
            novx.append(heure)
            novy.append(i)
            cpt=elem
            i=0
    
    plt.plot(novx, novy, label='generation')
    
    plt.legend(loc='upper left')
    plt.tight_layout()


plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)

plt.show()
