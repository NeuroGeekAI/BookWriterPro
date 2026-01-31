"""
Translator - Moteur de traduction locale avec Argos Translate
"""
import os
import sys
import re
from typing import Optional

class Translator:
    """Gère les traductions locales via Argos Translate"""
    
    def __init__(self):
        self.available = False
        self.installed_languages = set()
        self._init_argos()
    
    def _init_argos(self):
        """Initialise Argos Translate"""
        try:
            import argostranslate.package
            import argostranslate.translate
            
            self.argos_package = argostranslate.package
            self.argos_translate = argostranslate.translate
            
            # Charger les packages déjà installés
            installed = self.argos_package.get_installed_packages()
            
            if len(installed) == 0:
                print("Aucun pack de traduction installe.")
                print("Lancez: python install_translation_packs.py")
                self.available = False
                return
            
            # Debug: afficher packs trouvés
            print(f"DEBUG: {len(installed)} packs trouves")
            for p in installed:
                print(f"  {p.from_code} -> {p.to_code}")
            
            # Vérifier quelles langues sont disponibles
            # Langues cibles (via EN) - 17 LANGUES TOTAL !
            target_langs = ['en', 'es', 'it', 'ru', 'ja', 'zh', 'hi', 'ar', 'de', 'pt', 'tr', 'ko', 'id', 'vi', 'pl', 'th']
            
            # Vérifier FR -> EN (requis)
            has_fr_en = any(p.from_code == 'fr' and p.to_code == 'en' for p in installed)
            
            if has_fr_en:
                self.installed_languages.add('en')
                print("  -> EN disponible (direct)")
                
                # Vérifier EN -> autres langues
                for target in ['es', 'it', 'ru', 'ja', 'zh', 'hi', 'ar', 'de', 'pt', 'tr', 'ko', 'id', 'vi', 'pl', 'th']:
                    has_en_target = any(p.from_code == 'en' and p.to_code == target for p in installed)
                    if has_en_target:
                        self.installed_languages.add(target)
                        print(f"  -> {target.upper()} disponible (via EN)")
                    else:
                        print(f"  -> {target.upper()} NON disponible")
            
            print(f"Langues activees: {self.installed_languages}")
            self.available = len(self.installed_languages) > 0
            
        except ImportError:
            print("⚠️ argostranslate non installé. Traductions désactivées.")
            print("   Lancez INSTALL.bat pour installer les dépendances.")
            self.available = False
        except Exception as e:
            print(f"⚠️ Erreur initialisation traducteur: {e}")
            self.available = False
    
    def _clean_repetitions(self, text: str, lang: str) -> str:
        """Nettoie les répétitions excessives (bug Argos chinois)"""
        if lang not in ['zh', 'ja']:
            return text
        
        # Pour chinois : supprimer répétitions de caractères
        # Exemple : 相相相相相 → 相
        cleaned = re.sub(r'(.)\1{4,}', r'\1', text)  # 5+ répétitions → 1 seul
        
        # Pour phrases répétées
        cleaned = re.sub(r'(\S+\s+\S+)\s+\1{2,}', r'\1', cleaned)  # Phrases dupliquées
        
        return cleaned
    
    def translate(self, text: str, target_lang: str) -> str:
        """Traduit un texte du français vers la langue cible"""
        if not self.available:
            return f"[Traduction {target_lang.upper()} non disponible - Installez argostranslate]"
        
        if not text or not text.strip():
            return ""
        
        if target_lang not in self.installed_languages:
            return f"[Langue {target_lang.upper()} non installee]"
        
        try:
            # Traduction directe pour EN
            if target_lang == 'en':
                translated = self.argos_translate.translate(text, 'fr', 'en')
                return translated
            
            # Traduction en chaîne pour autres langues (FR -> EN -> target)
            else:
                # Étape 1: FR -> EN
                text_en = self.argos_translate.translate(text, 'fr', 'en')
                # Étape 2: EN -> target
                translated = self.argos_translate.translate(text_en, 'en', target_lang)
                
                # Étape 3: Nettoyage répétitions (chinois/japonais)
                translated = self._clean_repetitions(translated, target_lang)
                
                return translated
                
        except Exception as e:
            return f"[Erreur traduction {target_lang.upper()}: {str(e)[:50]}]"
    
    def get_language_name(self, code: str) -> str:
        """Retourne le nom complet de la langue"""
        names = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'it': 'Italiano',
            'ru': 'Русский',
            'ja': '日本語',
            'zh': '中文',
            'hi': 'हिन्दी',  # Hindi
            'ar': 'العربية',  # Arabe
            'de': 'Deutsch',  # Allemand
            'pt': 'Português', # Portugais
            'tr': 'Türkçe',   # Turc
            'ko': '한국어',    # Coréen
            'id': 'Bahasa',   # Indonésien
            'vi': 'Tiếng Việt', # Vietnamien
            'pl': 'Polski',   # Polonais
            'th': 'ไทย'       # Thaï
        }
        return names.get(code, code.upper())
    
    def get_flag_emoji(self, code: str) -> str:
        """Retourne l'emoji drapeau de la langue"""
        flags = {
            'fr': '🇫🇷',
            'en': '🇬🇧',
            'es': '🇪🇸',
            'it': '🇮🇹',
            'ru': '🇷🇺',
            'ja': '🇯🇵',
            'zh': '🇨🇳',
            'hi': '🇮🇳',  # Inde
            'ar': '🇸🇦',  # Arabie Saoudite
            'de': '🇩🇪',  # Allemagne
            'pt': '🇧🇷',  # Brésil
            'tr': '🇹🇷',  # Turquie
            'ko': '🇰🇷',  # Corée du Sud
            'id': '🇮🇩',  # Indonésie
            'vi': '🇻🇳',  # Vietnam
            'pl': '🇵🇱',  # Pologne
            'th': '🇹🇭'   # Thaïlande
        }
        return flags.get(code, '🌍')

