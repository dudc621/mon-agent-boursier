import os
import yfinance as yf
import google.generativeai as genai
from groq import Groq
import pandas as pd
from datetime import datetime

print("--- DEMARRAGE DU DIAGNOSTIC ---")

# Vérification des clés
gemini_key = os.environ.get("GEMINI_API_KEY")
groq_key = os.environ.get("GROQ_API_KEY")

if not gemini_key or not groq_key:
    print("❌ ERREUR : Les clés API sont manquantes dans GitHub Secrets !")
else:
    print("✅ Clés API détectées.")

def lancer_analyse(ticker):
    print(f"\n🔍 Tentative sur : {ticker}")
    try:
        # 1. Test Bourse
        stock = yf.Ticker(ticker)
        prix = stock.history(period="1d")['Close'].iloc[-1]
        print(f"📈 Prix récupéré : {prix}$")

        # 2. Test News
        news = stock.news
        print(f"📰 Nombre de news trouvées : {len(news)}")
        
        # 3. Test IA
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("🧠 Envoi à Gemini...")
        response = model.generate_content(f"Analyse {ticker} à {prix}$").text
        print(f"🤖 Réponse IA : {response[:100]}...")

    except Exception as e:
        print(f"💥 LE SCRIPT A PLANTE ICI : {str(e)}")

lancer_analyse("BTC-USD") # On teste le Bitcoin car il bouge 24h/24
