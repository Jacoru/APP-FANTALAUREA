import streamlit as st
import os
import sys
import pandas as pd
import io
from Funzioni import download_to_s3, upload_to_s3, carica_stile
import ast

carica_stile()

file_path = "persone.csv"
# Setup path per importare moduli locali
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

content = download_to_s3()
df = pd.read_csv(io.StringIO(content))

#df = pd.read_csv("persone.csv")


 # Interfaccia Streamlit
st.title("FANTALAUREA - Il gioco più bello per una festa di Laurea")

st.write("Benvenuti a FANTALAUREA, il gioco più divertente per ogni festa di laurea!")
with st.expander("📘 User Guide", expanded=True):
    st.markdown("""
    - Fate punti, giocate e in palio si possono vincere favolosi premi.
    - In base ai bonus e malus potrete ottenere punti, attenzione a non barare. Avrò occhi ovunque quindi le penalità saranno severe.
    - Il gioco è semplice, basta seguire le istruzioni e mettersi in gioco. Attenti ai MALUS!
    - I punteggi sono calcolati automaticante, accedete inserendo il vostro Nickname e il vostro punteggio sarà aggiornato in tempo reale.
    - Selezionate il bonus o il malus che avete ottenuto e schiacciate il pulsante "Aggiorna Punteggio" per vedere il vostro punteggio aggiornato.
    - Per chi non aggiornerà il proprio punteggio, la penalità è di 15 pt per ogni dimenticanza certificata.
    """)

# Input utente
st.write("Inserire Nome e Cognome solo per la registrazione, per accedere basterà inserire il Nickname.")
nome = st.text_input("Insert your name", key="name")
cognome = st.text_input("Insert your surname", key="surname")
nick = st.text_input("Insert your nickname *", key="email")

if nick in df["Nickname"].values:
    st.success(f"Benvenuto {nick}! Il tuo punteggio attuale è: {df.loc[df['Nickname'] == nick, 'Punteggio'].values[0]} punti")
    # Recupera i dati dell'utente
    dati_utente = df[df["Nickname"] == nick].iloc[0]
    
    punteggio = dati_utente["Punteggio"]
    
    Lista_bonus = ast.literal_eval(dati_utente["Lista Bonus"])
    Lista_malus = ast.literal_eval(dati_utente["Lista Malus"])  

    # Selezione bonus/malus
    bonus_options = {"Bevuto un drink": 5,
                    "Fai gli auguri per la Laurea a Jaco": 1,
                    "Giocare a \"Paolo Ruffini o Non Paolo Ruffini\" e fare almeno 6/10": 10,
                    "Inciampare/cadere": 5,
                    "Bere analcolici": 1,
                    "Fare foto alla festa (punti per ogni foto)": 0.5,
                    "Essere vestito di colori strani (viola, rosa, verde acqua)": 10,
                    "Essere in camicia": 5,
                    "Giocare a NPC o non NPC e fare almeno 6/10": 10,
                    "Portare a Jacopo il suo drink preferito": 15,
                    "Risolvere il cubo di Rubik senza aiuti entro 5 minuti": 15,
                    "Essere colui che guida e quindi non può bere": 10,
                    "Fermare/ andare da gente e fare un video di auguri per la mia Laurea": 15,
                    "Fare le rampe di scale 2 volte a salire e scendere": 15,
                    "Cantare uno spezzone \"Pasta a mezzogiorno\"": 20,
                    "Cantare uno spezzone \"Libri di pongo\"": 20,
                    "Cantare uno spezzone \"Giovanni Furla\"": 20,
                    "Cantare uno spezzone \"Dammi un pugno dove non fa male\"": 20,
                    "Cantare uno spezzone \"Se ci sei tu ci sono io\"": 20,
                    "Cantare una canzone di Lucio Corsi (No volevo essere un duro)": 10}

    malus_options = {"persone arrivano in ritardo": -5,
                    "Lasciare bicchieri per terra o mezzi pieni": -5,
                    "Chiedere il voto di laurea": -2,
                    "Lamentarsi": -5,
                    "Arriva la polizia": -10,
                    "Atteggiamenti scontrosi (NON SI FA!!!)": -5,
                    "Buttare roba nella fontana": -10,
                    "Parlare con meno di 6 persone": -10,
                    "Non trovare il posto": -10,
                    "Inciampare o cadere": -5,
                    "perdere ai Giochi Paolo Ruffini o NPC": -10,
                    "Non ricordarsi il nome di una persona": -5,
                    "Non sapere l'argomento della tesi di Jacopo": -5,
                    "Chi è più alto di Jacopo": -2,
                    "Non trovare il posto e quindi chiamare Jaco": -10
                    }

    bonus = ["Bevuto un drink", "Fai gli auguri per la Laurea a Jaco", "Giocare a \"Paolo Ruffini o Non Paolo Ruffini\" e fare almeno 6/10",
            "Bere analcolici", "Fare foto alla festa (punti per ogni foto)", "Essere vestito di colori strani (viola, rosa, verde acqua)", "Essere in camicia", 
            "Giocare a NPC o non NPC e fare almeno 6/10", "Portare a Jacopo il suo drink preferito", "Risolvere il cubo di Rubik senza aiuti entro 5 minuti", 
            "Essere colui che guida e quindi non può bere", "Fermare/ andare da gente e fare un video di auguri per la mia Laurea", "Fare le rampe di scale 2 volte a salire e scendere", 
            "Cantare uno spezzone \"Pasta a mezzogiorno\"","Cantare uno spezzone \"Libri di pongo\"", "Cantare uno spezzone \"Giovanni Furla\"", "Cantare uno spezzone \"Dammi un pugno dove non fa male\"", "Cantare uno spezzone \"Se ci sei tu ci sono io\""
            , "Cantare una canzone di Lucio Corsi (No volevo essere un duro)"]


    Bonus = st.pills("Bonus", bonus, selection_mode="multi")

    malus = ["persone arrivano in ritardo", "Lasciare bicchieri per terra o mezzi pieni", "Chiedere il voto di laurea", 
            "Lamentarsi", "Arriva la polizia", "Atteggiamenti scontrosi (NON SI FA!!!)", "Buttare roba nella fontana", 
            "Parlare con meno di 6 persone", "Non trovare il posto e quindi chiamare Jaco", "Inciampare o cadere",
            "perdere ai Giochi Paolo Ruffini o NPC", "Non ricordarsi il nome di una persona", "Non sapere l'argomento della tesi di Jacopo", 
            "Chi è più alto di Jacopo"]

    Malus = st.pills("Malus", malus, selection_mode="multi")

    Punteggio_bonus = 0
    if Bonus == []:
            Punteggio_bonus = 0
    else:
            subj=[]
            for bonus in Bonus:
                    Punteggio_bonus += bonus_options[bonus]

    Punteggio_malus = 0
    if Malus == []:
            Punteggio_malus = 0 
    else:
            for malus in Malus:
                    Punteggio_malus += malus_options[malus]

                                
    if st.button("Aggiorna Punteggio"):
        st.write(f"Bonus: {Punteggio_bonus} punti")
        st.write(f"Malus: {Punteggio_malus} punti")

    Punteggio = Punteggio_bonus + Punteggio_malus
    
    # Aggiorna il punteggio nel DataFrame
    punteggio += Punteggio
    for bonus in Bonus:
        Lista_bonus.append(bonus)
    for malus in Malus:
        Lista_malus.append(malus)

    new_row = {
                                "Nome": nome,
                                "Cognome": cognome,
                                "Nickname": nick, 
                                "Punteggio": punteggio,
                                "Lista Bonus": Lista_bonus,
                                "Lista Malus": Lista_malus
                                }
    index = df[df["Nickname"] == nick].index
    for col, val in new_row.items():
                                df.loc[index, col] = str(val)
    if st.button("Salva"):
        if nick in df["Nickname"].values:
            # UPDATE
            index = df[df["Nickname"] == nick].index
            for col, val in new_row.items():
                df.loc[index, col] = str(val)
        else:
            # INSERT
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        upload_to_s3(df)
        st.success("Punteggio aggiornato e salvato con successo!")


else:
    st.success(f"Benvenuto {nick}!")

    # Selezione bonus/malus
    bonus_options = {"Bevuto un drink": 5,
                    "Fai gli auguri per la Laurea a Jaco (reiterabile)": 1,
                    "Giocare a \"Paolo Ruffini o Non Paolo Ruffini\" e fare almeno 6/10": 10,
                    "Inciampare/cadere": 5,
                    "Bere analcolici": 1,
                    "Fare foto alla festa (punti per ogni foto)": 0.5,
                    "Essere vestito di colori strani (viola, rosa, verde acqua)": 10,
                    "Essere in camicia": 5,
                    "Giocare a NPC o non NPC e fare almeno 6/10": 10,
                    "Portare a Jacopo il suo drink preferito": 15,
                    "Risolvere il cubo di Rubik senza aiuti entro 5 minuti": 15,
                    "Essere colui che guida e quindi non può bere": 10,
                    "Fermare/ andare da gente e fare un video di auguri per la mia Laurea": 15,
                    "Fare le rampe di scale 2 volte a salire e scendere": 15,
                    "Cantare uno spezzone \"Pasta a mezzogiorno\"": 20,
                    "Cantare uno spezzone \"Libri di pongo\"": 20,
                    "Cantare uno spezzone \"Giovanni Furla\"": 20,
                    "Cantare uno spezzone \"Dammi un pugno dove non fa male\"": 20,
                    "Cantare uno spezzone \"Se ci sei tu ci sono io\"": 20,
                    "Cantare una canzone di Lucio Corsi (No volevo essere un duro)": 10, "Momento Lontra, guarda un video di Hana e Kotaro": 40}

    malus_options = {"persone arrivano in ritardo": -5,
                    "Lasciare bicchieri per terra o mezzi pieni": -5,
                    "Chiedere il voto di laurea": -2,
                    "Lamentarsi": -5,
                    "Arriva la polizia": -10,
                    "Atteggiamenti scontrosi (NON SI FA!!!)": -5,
                    "Buttare roba nella fontana": -10,
                    "Parlare con meno di 6 persone": -10,
                    "Inciampare o cadere": -5,
                    "perdere ai Giochi Paolo Ruffini o NPC": -10,
                    "Non ricordarsi il nome di una persona": -5,
                    "Non sapere l'argomento della tesi di Jacopo": -5,
                    "Chi è più alto di Jacopo": -2,
                    "Non trovare il posto e quindi chiamare Jaco": -10, 
                    "non vedere tutto il video delle lontre": -50
                    }

    bonus = ["Bevuto un drink", "Fai gli auguri per la Laurea a Jaco (reiterabile)", "Giocare a \"Paolo Ruffini o Non Paolo Ruffini\" e fare almeno 6/10",
            "Bere analcolici", "Fare foto alla festa (punti per ogni foto)", "Essere vestito di colori strani (viola, rosa, verde acqua)", "Essere in camicia", 
            "Giocare a NPC o non NPC e fare almeno 6/10", "Portare a Jacopo il suo drink preferito", "Risolvere il cubo di Rubik senza aiuti entro 5 minuti", 
            "Essere colui che guida e quindi non può bere", "Fermare/ andare da gente e fare un video di auguri per la mia Laurea", "Fare le rampe di scale 2 volte a salire e scendere", 
            "Cantare uno spezzone \"Pasta a mezzogiorno\"","Cantare uno spezzone \"Libri di pongo\"", "Cantare uno spezzone \"Giovanni Furla\"", "Cantare uno spezzone \"Dammi un pugno dove non fa male\"", "Cantare uno spezzone \"Se ci sei tu ci sono io\""
            , "Cantare una canzone di Lucio Corsi (No volevo essere un duro)", "Momento Lontra, guarda un video di Hana e Kotaro"]


    Bonus = st.pills("Malus", bonus, selection_mode="multi")

    malus = ["persone arrivano in ritardo", "Lasciare bicchieri per terra o mezzi pieni", "Chiedere il voto di laurea", 
            "Lamentarsi", "Arriva la polizia", "Atteggiamenti scontrosi (NON SI FA!!!)", "Buttare roba nella fontana", 
            "Parlare con meno di 6 persone", "Non trovare il posto e quindi chiamare Jaco", "Inciampare o cadere",
            "perdere ai Giochi Paolo Ruffini o NPC", "Non ricordarsi il nome di una persona", "Non sapere l'argomento della tesi di Jacopo", 
            "Chi è più alto di Jacopo", "non vedere tutto il video delle lontre"]

    Malus = st.pills("Malus", malus, selection_mode="multi")

    Punteggio_bonus = 0
    if Bonus == []:
            Punteggio_bonus = 0
    else:
            subj=[]
            for bonus in Bonus:
                    Punteggio_bonus += bonus_options[bonus]

    Punteggio_malus = 0
    if Malus == []:
            Punteggio_malus = 0 
    else:
            for malus in Malus:
                    Punteggio_malus += malus_options[malus]

                                
    if st.button("Aggiorna Punteggio"):
        st.write(f"Bonus: {Punteggio_bonus} punti")
        st.write(f"Malus: {Punteggio_malus} punti")

    Punteggio = Punteggio_bonus + Punteggio_malus
    Lista_bonus = Bonus
    Lista_malus = Malus

    new_row = {
                                "Nome": nome,
                                "Cognome": cognome,
                                "Nickname": nick, 
                                "Punteggio": Punteggio,
                                "Lista Bonus": Lista_bonus,
                                "Lista Malus": Lista_malus
                                }
    index = df[df["Nickname"] == nick].index

    if st.button("Salva"):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])
        upload_to_s3(df)
        st.success("Punteggio aggiornato e salvato con successo!")

