import os
import yfinance as yf
import google.generativeai as genai
from groq import Groq
import pandas as pd
from datetime import datetime

# Configuration
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def lancer_analyse(ticker):
    print(f"--- Analyse en cours pour {ticker} ---")
    stock = yf.Ticker(ticker)
    
    # 1. Récupérer le prix actuel
    data = stock.history(period="1d")
    if data.empty: return
    prix_actuel = data['Close'].iloc[-1]

    # 2. Charger la mémoire pour apprendre
    memoire_context = "Pas d'historique."
    if os.path.exists('memoire.csv'):
        df_mem = pd.read_csv('memoire.csv')
        memoire_context = df_mem.tail(10).to_string()

    # 3. Prompt pour l'IA
    prompt = f"""
    Action: {ticker} | Prix actuel: {prix_actuel}
    Historique récent et erreurs passées: {memoire_context}
    
    Tâche: Analyse les news et le prix. Donne un conseil (ACHAT/VENTE) 
    et explique pourquoi en te basant sur tes succès ou échecs passés.
    """

    # Appel Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    res_gemini = model.generate_content(prompt).text
    
    # Contre-expertise Groq
    res_finale = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": f"Analyse cette prédiction : {res_gemini}. Est-elle logique ? Réponds brièvement."}],
        model="llama3-8b-8192",
    ).choices[0].message.content

    print(f"Décision : {res_finale}")

    # 4. Sauvegarde dans la mémoire
    nouveau_log = pd.DataFrame([{
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'ticker': ticker,
        'prix': prix_actuel,
        'analyse': res_finale[:100] # On garde un résumé
    }])
    
    nouveau_log.to_csv('memoire.csv', mode='a', header=not os.path.exists('memoire.csv'), index=False)

# Test sur les leaders
for t in ["NVDA", "AAPL", "TSLA"]:
    lancer_analyse(t)
