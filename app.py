import os
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime


lista_citta=["citta"+str(i+1) for i in range(5)]
lista_citta.insert(0,"id")

# --- SCARICO IL NUMERO CASUALE DALL'API ---
url_api = "https://www.random.org/integers/?num=5&min=0&max=30&col=1&base=10&format=plain&rnd=new"

try:
    response = requests.get(url_api)
    response.raise_for_status()
    numeri_correnti=response.text.split("\n")[:-1]
    numeri_correnti = [int(numeri_correnti[i]) for i in range(len(numeri_correnti))]

except Exception as e:
    print(f"Errore API: {e}")
    numeri_correnti = [546,547,548,549,550]

data_attuale=datetime.now().strftime("%Y-%m-%d")
ora_attuale=datetime.now().strftime("%H:%M:%S")

### 

numeri_correnti.insert(0,1)

nuova_riga=pd.DataFrame([{"id":1, "data":data_attuale, "ora":ora_attuale}]).join(pd.DataFrame([dict(zip(lista_citta,numeri_correnti))]).set_index("id"),on="id").drop(columns="id")

cartella_dati = "data"
file_csv = os.path.join(cartella_dati, "history.csv")
os.makedirs(cartella_dati, exist_ok=True)

### 

if os.path.exists(file_csv):
    df_storico = pd.read_csv(file_csv)
    df_storico = pd.concat([df_storico, nuova_riga], ignore_index=True)
else:
    df_storico = nuova_riga

df_storico.to_csv(file_csv, index=False)

# --- GENERO IL GRAFICO PLOTLY IN HTML ---
fig = px.line(
    df_storico,
    x="ora",
    y="citta1",
    title="📈 Cruscotto Numeri Casuali - Storico in Tempo Reale",
    markers=True
)
fig.update_layout(template="plotly_white", title_x=0.5)

# Salviamo la pagina HTML
fig.write_html("index.html")
print("Processo completato con successo!")
