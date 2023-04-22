import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('tempsia.csv')
    x = data['generation']
    y1 = data['tempsmin']
    y2 = data['tempsmax']
    y3 = data["tempsmoy"]

    plt.cla()

    plt.plot(x, y1, label='mini')
    plt.plot(x, y2, label='maxi')
    plt.plot(x, y3, label='moyenne')

    plt.legend(loc='upper left')
    plt.tight_layout()


plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)

plt.show()