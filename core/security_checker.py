"""
Security Checker - Système "Alerte Maman" pour détecter les contenus à risque
"""
import re
from typing import List, Tuple, Dict

class SecurityAlert:
    """Représente une alerte de sécurité"""
    
    def __init__(self, alert_type: str, text: str, suggestion: str, position: int):
        self.type = alert_type  # "name", "date", "risky"
        self.text = text
        self.suggestion = suggestion
        self.position = position

class SecurityChecker:
    """Vérifie le contenu et génère des alertes selon le mode"""
    
    def __init__(self):
        # Mots à risque (diffamation, violence, etc.)
        self.risky_words = [
            r'\bmenace\b', r'\bmenacer\b', r'\bmenacé\b',
            r'\btuer\b', r'\btuera\b', r'\btuerai\b',
            r'\bviolence\b', r'\bviolent\b',
            r'\battaquer\b', r'\battaque\b',
            r'\bdétruire\b', r'\bdétruira\b',
            r'\bcriminel\b', r'\bcrime\b',
            r'\bsuicide\b', r'\bsuicider\b',
        ]
        
        self.risky_pattern = re.compile('|'.join(self.risky_words), re.IGNORECASE)
    
    def check_content(self, text: str, mode: str) -> List[SecurityAlert]:
        """Vérifie le contenu et retourne les alertes"""
        alerts = []
        
        if mode == "avocat":
            # Mode avocat : aucune alerte (tout est autorisé)
            return alerts
        
        # Détection dates précises (mode public uniquement)
        if mode == "public":
            # Années complètes (ex: 2022, 1999)
            for match in re.finditer(r'\b(19|20)\d{2}\b', text):
                year = match.group()
                decade = year[:3] + "0"
                suggestion = f"Début années {decade}"
                alerts.append(SecurityAlert(
                    "date",
                    year,
                    suggestion,
                    match.start()
                ))
            
            # Dates complètes (ex: 21/10/2025)
            for match in re.finditer(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text):
                date = match.group()
                suggestion = "Courant 2020" if "20" in date else "Une date"
                alerts.append(SecurityAlert(
                    "date",
                    date,
                    suggestion,
                    match.start()
                ))
        
        # Détection noms propres (mode public uniquement)
        if mode == "public":
            # Mots en majuscules (potentiellement des noms)
            for match in re.finditer(r'\b[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜ][a-zàâäéèêëïîôùûüç]+\b', text):
                word = match.group()
                # Ignorer les mots en début de phrase et les mots courants
                if match.start() == 0 or text[match.start()-1] in '.!?':
                    continue
                if word.lower() in ['je', 'le', 'la', 'les', 'un', 'une', 'phobos', 'green', 'seo']:
                    continue
                
                suggestion = f"Monsieur/Madame X" if len(word) > 3 else word
                alerts.append(SecurityAlert(
                    "name",
                    word,
                    suggestion,
                    match.start()
                ))
        
        # Détection mots à risque (tous modes sauf avocat)
        if mode != "avocat":
            for match in self.risky_pattern.finditer(text):
                word = match.group()
                alerts.append(SecurityAlert(
                    "risky",
                    word,
                    "⚠️ Attention : mot potentiellement risqué",
                    match.start()
                ))
        
        return alerts
    
    def get_alert_message(self, alert: SecurityAlert) -> str:
        """Génère le message d'alerte formaté"""
        if alert.type == "date":
            return f"🛡️ ALERTE DATE: '{alert.text}' → Suggérer '{alert.suggestion}' ?"
        elif alert.type == "name":
            return f"🛡️ ALERTE NOM: '{alert.text}' → Anonymiser en '{alert.suggestion}' ?"
        elif alert.type == "risky":
            return f"⚠️ MOT RISQUÉ: '{alert.text}' → {alert.suggestion}"
        return ""

