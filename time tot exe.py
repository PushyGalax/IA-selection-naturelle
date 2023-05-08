import pandas as pd

data = pd.read_csv('tempsia.csv')
y2 = data['tempsmax'].tolist()

cpt=0

for elem in y2:
    cpt+=elem

print(f"{cpt} s \n{cpt/60} m \n{(cpt/60)/60} h")