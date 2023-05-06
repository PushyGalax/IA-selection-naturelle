import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('type.csv')
    x = data['generation']
    y1 = data['type1']
    y2 = data['type2']
    y3 = data["type3"]

    plt.cla()

    plt.plot(x, y1, label='peureuse')
    plt.plot(x, y2, label='intello')
    plt.plot(x, y3, label='debile')

    plt.legend(loc='upper left')
    plt.tight_layout()


plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)

plt.show()