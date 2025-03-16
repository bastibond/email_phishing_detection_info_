phishing_detection.py
----------------
import openai
from decouple import config
import sys

# Lade den API-Schlüssel aus der Umgebungsdatei
api_key = config('OPENAI_API_KEY')

# Setze den API-Schlüssel für die OpenAI API
openai.api_key = api_key

def email_einschätzung_phishing(email_path):
    try:
        # E-Mail-Inhalt aus der Datei lesen
        with open(email_path, 'r', encoding='utf-8') as email_file:
            email_inhalt = email_file.read()

        # Prompt für die KI erstellen
        prompt = (
            "System: Du bist ein Sicherheitsexperte, spezialisiert auf das Erkennen von Phishing-E-Mails. "
            "Analysiere die folgende E-Mail auf typische Phishing-Merkmale wie verdächtige Links, Aufforderungen zu vertraulichen Informationen oder Drohungen. "
            "Bewerte das Risiko und erkläre kurz, warum. "
            "Antworte bitte auf Deutsch.\n\n"
            f"E-Mail:\n{email_inhalt}"
        )

        # Anfrage an OpenAI senden
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
                {"role": "user", "content": prompt}
            ]
        )

        # Antwort der API auslesen
        api_antwort = response.choices[0].message['content']

        # Prüfung auf Risikoeinschätzung
        if "Risiko" in api_antwort and ("Phishing" in api_antwort or "nicht Phishing" in api_antwort):
            print("\n✅ Analyse abgeschlossen:\n")
            print(api_antwort)
        else:
            print("⚠️ Die API-Antwort konnte nicht eindeutig interpretiert werden:\n")
            print(api_antwort)

    except Exception as e:
        print(f"❌ Fehler beim Überprüfen der E-Mail: {str(e)}")

if __name__ == "__main__":
    # Überprüfe die Befehlszeilenargumente
    if len(sys.argv) != 2:
        print("Verwendung: python phishing_detection.py <Pfad zur E-Mail-Datei>")
    else:
        email_path = sys.argv[1]
        email_einschätzung_phishing(email_path)
