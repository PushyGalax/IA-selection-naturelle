import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('dataia.csv')
    x = data['generation']
    y1 = data['vitesse']
    y2 = data['taille']
    y3 = data["pv"]

    plt.cla()

    plt.plot(x, y1, label='vitesse')
    plt.plot(x, y2, label='taille')
    plt.plot(x, y3, label='pv')

    plt.legend(loc='upper left')
    plt.tight_layout()


plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)

plt.show()