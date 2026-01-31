"""
Classe Chapter - Représente un chapitre du livre
"""
from datetime import datetime
from typing import Dict, Optional

class Chapter:
    """Représente un chapitre avec son contenu multilingue"""
    
    def __init__(self, title: str, mode: str = "public"):
        self.title = title
        self.mode = mode  # "avocat", "public", "therapie"
        self.content_fr = ""
        self.translations = {
            "en": "",
            "es": "",
            "it": "",
            "ru": "",
            "ja": "",
            "zh": "",
            "hi": "",  # Hindi
            "ar": "",  # Arabe
            "de": "",  # Allemand
            "pt": "",  # Portugais
            "tr": "",  # Turc
            "ko": "",  # Coréen
            "id": "",  # Indonésien
            "vi": "",  # Vietnamien
            "pl": "",  # Polonais
            "th": ""   # Thaï
        }
        # Titres traduits pour chaque langue
        self.title_translations = {
            "en": "",
            "es": "",
            "it": "",
            "ru": "",
            "ja": "",
            "zh": "",
            "hi": "",  # Hindi
            "ar": "",  # Arabe
            "de": "",  # Allemand
            "pt": "",  # Portugais
            "tr": "",  # Turc
            "ko": "",  # Coréen
            "id": "",  # Indonésien
            "vi": "",  # Vietnamien
            "pl": "",  # Polonais
            "th": ""   # Thaï
        }
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.word_count = 0
    
    def update_content(self, content: str):
        """Met à jour le contenu français et recalcule les stats"""
        self.content_fr = content
        self.updated_at = datetime.now()
        self.word_count = len(content.split())
    
    def set_translation(self, lang: str, content: str):
        """Définit la traduction pour une langue"""
        # Accepter toutes les langues supportées (17 langues)
        self.translations[lang] = content
        self.updated_at = datetime.now()
    
    def get_translation(self, lang: str) -> str:
        """Récupère la traduction pour une langue"""
        return self.translations.get(lang, "")
    
    def set_title_translation(self, lang: str, title: str):
        """Définit la traduction du titre pour une langue"""
        # Accepter toutes les langues supportées (17 langues)
        self.title_translations[lang] = title
        self.updated_at = datetime.now()
    
    def get_title_translation(self, lang: str) -> str:
        """Récupère la traduction du titre pour une langue"""
        translated = self.title_translations.get(lang, "")
        # Si pas de traduction définie, retourner titre original
        return translated if translated else self.title
    
    def to_dict(self) -> Dict:
        """Convertit le chapitre en dictionnaire pour sauvegarde"""
        return {
            "title": self.title,
            "mode": self.mode,
            "content_fr": self.content_fr,
            "translations": self.translations,
            "title_translations": self.title_translations,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "word_count": self.word_count
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Chapter':
        """Crée un chapitre depuis un dictionnaire"""
        chapter = Chapter(data["title"], data.get("mode", "public"))
        chapter.content_fr = data.get("content_fr", "")
        chapter.translations = data.get("translations", {
            "en": "", "es": "", "it": "", "ru": "", "ja": "", "zh": "",
            "hi": "", "ar": "", "de": "", "pt": "", "tr": "", "ko": "",
            "id": "", "vi": "", "pl": "", "th": ""
        })
        chapter.title_translations = data.get("title_translations", {
            "en": "", "es": "", "it": "", "ru": "", "ja": "", "zh": "",
            "hi": "", "ar": "", "de": "", "pt": "", "tr": "", "ko": "",
            "id": "", "vi": "", "pl": "", "th": ""
        })
        chapter.word_count = data.get("word_count", 0)
        
        if "created_at" in data:
            chapter.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            chapter.updated_at = datetime.fromisoformat(data["updated_at"])
        
        return chapter

