#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Systeme d'internationalisation (i18n) pour l'interface GUI
Support de 17 langues
Cree par Maman Margot pour PHOBOS - 31 Janvier 2026
"""

import json
import locale
from pathlib import Path
from typing import Dict, Optional

class I18N:
    """Gestionnaire de traductions pour l'interface"""
    
    # Langues supportees
    SUPPORTED_LANGUAGES = {
        'fr': 'Français',
        'en': 'English',
        'es': 'Español',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'ja': '日本語',
        'zh': '中文',
        'ar': 'العربية',
        'ru': 'Русский',
        'hi': 'हिन्दी',
        'ko': '한국어',
        'id': 'Bahasa Indonesia',
        'tr': 'Türkçe',
        'vi': 'Tiếng Việt',
        'pl': 'Polski',
        'th': 'ไทย'
    }
    
    def __init__(self, lang_code: Optional[str] = None):
        """
        Initialise le gestionnaire i18n
        
        Args:
            lang_code: Code langue (ex: 'fr', 'en'). Si None, detecte automatiquement
        """
        self.locales_dir = Path(__file__).parent.parent / "locales"
        self.config_file = Path(__file__).parent.parent / "data" / "language_config.json"
        
        # Charger la langue : priorite -> param > sauvegarde > detection systeme
        if lang_code:
            self.current_lang = lang_code
        else:
            saved_lang = self._load_language_preference()
            self.current_lang = saved_lang or self._detect_system_language()
        
        self.translations: Dict[str, str] = {}
        self.load_translations(self.current_lang)
    
    def _load_language_preference(self) -> Optional[str]:
        """Charge la langue sauvegardee par l'utilisateur"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    lang = config.get('language')
                    if lang in self.SUPPORTED_LANGUAGES:
                        print(f"[OK] Preference langue chargee : {self.SUPPORTED_LANGUAGES[lang]}")
                        return lang
        except Exception as e:
            print(f"[!] Erreur chargement preference langue : {e}")
        
        return None
    
    def _save_language_preference(self, lang_code: str) -> bool:
        """Sauvegarde le choix de langue de l'utilisateur"""
        try:
            # Creer dossier data si necessaire
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarder
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'language': lang_code}, f, ensure_ascii=False, indent=2)
            
            print(f"[OK] Preference langue sauvegardee : {self.SUPPORTED_LANGUAGES[lang_code]}")
            return True
            
        except Exception as e:
            print(f"[ERREUR] Sauvegarde preference langue : {e}")
            return False
    
    def _detect_system_language(self) -> str:
        """Detecte la langue du systeme"""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in self.SUPPORTED_LANGUAGES:
                    return lang_code
        except:
            pass
        
        # Fallback : francais
        return 'fr'
    
    def load_translations(self, lang_code: str) -> bool:
        """
        Charge les traductions pour une langue
        
        Args:
            lang_code: Code langue
            
        Returns:
            True si succes, False sinon
        """
        if lang_code not in self.SUPPORTED_LANGUAGES:
            lang_code = 'fr'  # Fallback
        
        locale_file = self.locales_dir / f"{lang_code}.json"
        
        if not locale_file.exists():
            print(f"[!] Fichier langue {lang_code}.json introuvable, fallback francais")
            locale_file = self.locales_dir / "fr.json"
        
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            
            self.current_lang = lang_code
            print(f"[OK] Langue chargee : {self.SUPPORTED_LANGUAGES[lang_code]}")
            return True
            
        except Exception as e:
            print(f"[ERREUR] Chargement traductions {lang_code} : {e}")
            # Fallback : dictionnaire vide (cles = valeurs)
            self.translations = {}
            return False
    
    def get(self, key: str, **kwargs) -> str:
        """
        Recupere une traduction
        
        Args:
            key: Cle de traduction (ex: 'app.title')
            **kwargs: Variables a inserer dans la traduction
            
        Returns:
            Texte traduit
        """
        # Chercher la traduction
        text = self.translations.get(key, key)
        
        # Remplacer les variables {variable}
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass  # Si erreur format, retourner tel quel
        
        return text
    
    def get_language_name(self, lang_code: str) -> str:
        """Retourne le nom d'une langue"""
        return self.SUPPORTED_LANGUAGES.get(lang_code, lang_code)
    
    def get_all_languages(self) -> Dict[str, str]:
        """Retourne toutes les langues supportees"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def change_language(self, lang_code: str) -> bool:
        """
        Change la langue de l'interface
        
        Args:
            lang_code: Nouveau code langue
            
        Returns:
            True si succes
        """
        success = self.load_translations(lang_code)
        
        # Sauvegarder la preference si chargement reussi
        if success:
            self._save_language_preference(lang_code)
        
        return success


# Instance globale
_i18n_instance: Optional[I18N] = None

def init_i18n(lang_code: Optional[str] = None) -> I18N:
    """Initialise le systeme i18n"""
    global _i18n_instance
    _i18n_instance = I18N(lang_code)
    return _i18n_instance

def get_i18n() -> I18N:
    """Recupere l'instance i18n (cree si necessaire)"""
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18N()
    return _i18n_instance

def _(key: str, **kwargs) -> str:
    """
    Raccourci pour get_i18n().get(key, **kwargs)
    Usage : _('app.title') ou _('welcome.message', name='PHOBOS')
    """
    return get_i18n().get(key, **kwargs)
