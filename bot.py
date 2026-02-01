import os
import yfinance as yf
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configuration stable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def job():
    ticker = "BTC-USD" 
    print(f"\n🚀 --- ANALYSE EN DIRECT : {ticker} ---")
    
    try:
        # 1. Données boursières
        stock = yf.Ticker(ticker)
        prix = stock.history(period="1d")['Close'].iloc[-1]
        print(f"💰 PRIX ACTUEL : {prix} USD")

        # 2. Appel IA (Modèle 'gemini-pro' est le plus stable)
        print("🧠 Consultation de l'IA...")
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Le prix du {ticker} est de {prix}$. Donne un conseil court : ACHAT, VENTE ou ATTENTE ?"
        
        response = model.generate_content(prompt)
        conseil = response.text
        
        print("\n📢 --- CONSEIL DE L'IA ---")
        print(conseil)
        print("--------------------------\n")

    except Exception as e:
        print(f"💥 ERREUR : {e}")
        conseil = f"Erreur: {str(e)[:50]}"

    # 3. Mise à jour de la mémoire
    df = pd.DataFrame([[datetime.now(), ticker, prix, conseil]], columns=['date', 'ticker', 'prix', 'conseil'])
    df.to_csv('memoire.csv', mode='a', header=not os.path.exists('memoire.csv'), index=False)
    print("✅ Mémoire enregistrée sur GitHub.")

job()
