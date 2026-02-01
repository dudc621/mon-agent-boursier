import os
import yfinance as yf
import google.generativeai as genai
from groq import Groq
import pandas as pd
from datetime import datetime
import time

# Configuration des IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def lancer_analyse(ticker):
    print(f"Lancement de l'analyse pour {ticker}...")
    
    try:
        # 1. Récupérer les données boursières
        stock = yf.Ticker(ticker)
        prix = stock.history(period="1d")['Close'].iloc[-1]
        news = stock.news[:2]

        # 2. Charger la mémoire (si le fichier existe)
        try:
            memoire = pd.read_csv('memoire.csv').tail(5).to_string()
        except:
            memoire = "Aucun historique disponible."

        prompt = f"Action: {ticker}, Prix actuel: {prix}. News récentes: {news}. Historique de tes erreurs passées: {memoire}. Analyse la situation et donne un conseil ACHAT ou VENTE avec une prévision."

        # IA 1 : Gemini (Correction du nom du modèle ici)
        # On utilise 'gemini-1.5-flash' qui est le nom standard actuel
        model = genai.GenerativeModel('gemini-1.5-flash')
        analyse_gemini = model.generate_content(prompt).text
        
        # IA 2 : Groq (Llama 3) pour la contre-expertise
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tu es un expert financier qui critique les analyses d'autres IA pour éviter les erreurs."},
                {"role": "user", "content": f"Voici l'analyse de Gemini: {analyse_gemini}. Es-tu d'accord ? Donne ta décision finale (ACHAT/VENTE/ATTENTE)."}
            ],
            model="llama3-8b-8192",
        )
        analyse_finale = completion.choices[0].message.content

        print(f"--- RAPPORT FINAL ---\n{analyse_finale}\n---------------------")
        
        # 3. Sauvegarder dans la mémoire
        nouvelle_ligne = pd.DataFrame([[datetime.now(), ticker, "Analyse effectuée", prix, "En attente de vérification"]], 
                                     columns=['date','ticker','prediction','prix_au_moment','erreur_constatee'])
        nouvelle_ligne.to_csv('memoire.csv', mode='a', header=not os.path.exists('memoire.csv'), index=False)

    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

# Liste des entreprises à surveiller
actions = ["NVDA", "AAPL", "TSLA"]
for a in actions:
    lancer_analyse(a)
    time.sleep(2) # Petite pause pour ne pas saturer les APIs gratuites
