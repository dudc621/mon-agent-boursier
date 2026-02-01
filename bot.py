import os
import yfinance as yf
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configuration ultra-stable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Utilisation du nom de modèle le plus récent pour éviter l'erreur 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def job():
    ticker = "BTC-USD" # On utilise le Bitcoin car il y a TOUJOURS des données
    print(f"\n🚀 --- DEBUT DE L'ANALYSE POUR {ticker} ---")
    
    # 1. Récupération du prix
    stock = yf.Ticker(ticker)
    prix = stock.history(period="1d")['Close'].iloc[-1]
    print(f"💰 PRIX ACTUEL : {prix} USD")

    # 2. Appel à l'IA
    print("🧠 Appel à l'IA Gemini en cours...")
    prompt = f"Le prix actuel du {ticker} est de {prix}$. Donne un conseil d'expert : ACHAT ou VENTE ?"
    
    try:
        reponse = model.generate_content(prompt).text
        print("\n📢 --- CONSEIL DE L'AGENT ---")
        print(reponse)
        print("-----------------------------\n")
    except Exception as e:
        print(f"❌ Erreur IA : {e}")
        reponse = "Erreur analyse"

    # 3. Tentative de sauvegarde
    try:
        df = pd.DataFrame([[datetime.now(), ticker, prix, reponse[:50]]], columns=['date', 'ticker', 'prix', 'conseil'])
        df.to_csv('memoire.csv', mode='a', header=not os.path.exists('memoire.csv'), index=False)
        print("✅ Mémoire mise à jour avec succès.")
    except Exception as e:
        print(f"⚠️ Impossible d'écrire dans le CSV : {e}")

job()
