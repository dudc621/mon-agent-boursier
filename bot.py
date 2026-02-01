import os
import yfinance as yf
import google.generativeai as genai
from groq import Groq
import pandas as pd
from datetime import datetime

# Configuration des IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def lancer_analyse(ticker):
    # 1. Récupérer données
    stock = yf.Ticker(ticker)
    prix = stock.history(period="1d")['Close'].iloc[-1]
    news = stock.news[:2]

    # 2. Lire la mémoire pour apprendre des erreurs passées
    memoire = pd.read_csv('memoire.csv').tail(5).to_string()

    prompt = f"Action: {ticker}, Prix: {prix}. News: {news}. Historique erreurs: {memoire}. Analyse et dis: ACHAT ou VENTE avec une prévision de prix."

    # IA 1 : Gemini
    analyse_gemini = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text
    
    # IA 2 : Groq (Llama 3)
    analyse_groq = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": f"Voici l'analyse de Gemini: {analyse_gemini}. Es-tu d'accord ? Corrige si besoin."}],
        model="llama3-8b-8192",
    ).choices[0].message.content

    print(f"RAPPORT POUR {ticker}:\n{analyse_groq}")
    
    # 3. Sauvegarder en mémoire pour le prochain tour
    nouvelle_ligne = pd.DataFrame([[datetime.now(), ticker, "Analyse faite", prix, "En attente"]], columns=['date','ticker','prediction','prix_au_moment','erreur_constatee'])
    nouvelle_ligne.to_csv('memoire.csv', mode='a', header=False, index=False)

lancer_analyse("NVDA") # Tu peux ajouter d'autres tickers ici
