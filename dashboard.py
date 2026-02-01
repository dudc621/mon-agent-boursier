import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Alpha-Trader Dashboard")

if st.sidebar.button('Rafraîchir les données'):
    df = pd.read_csv('memoire.csv')
    
    # Afficher le dernier conseil
    st.metric("Dernière Analyse", df['ticker'].iloc[-1], df['prix'].iloc[-1])
    
    # Graphique des prix suivis par l'IA
    fig = px.line(df, x='date', y='prix', color='ticker', title="Évolution des actifs suivis")
    st.plotly_chart(fig)
    
    # Tableau de la mémoire
    st.write("Mémoire de l'IA (Apprentissage) :", df)
