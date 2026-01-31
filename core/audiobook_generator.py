"""
Audiobook Generator - Génère des audiobooks dans 17 langues
Utilise pyttsx3 (TTS 100% LOCAL) - Aucune API, aucune limite !
"""
import os
from pathlib import Path
from typing import List, Optional, Dict
import pyttsx3

class AudiobookGenerator:
    """Génère des audiobooks avec pyttsx3 (TTS 100% local)"""
    
    def __init__(self):
        self.available = False
        self.engine = None
        self._check_availability()
        
        # Mapping langues vers identifiants voix (multi-plateforme)
        self.voice_models = {
            'fr': 'fr',
            'en': 'en',
            'es': 'es',
            'it': 'it',
            'de': 'de',
            'ru': 'ru',
            'ja': 'ja',
            'zh': 'zh',
            'hi': 'hi',
            'ar': 'ar',
            'pt': 'pt',
            'tr': 'tr',
            'ko': 'ko',
            'id': 'id',
            'vi': 'vi',
            'pl': 'pl',
            'th': 'th'
        }
    
    def _check_availability(self):
        """Vérifie si pyttsx3 est disponible"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
            print("[OK] Audiobook Generator disponible ! (pyttsx3 - 100% LOCAL)")
            print("[OK] Aucune API, aucune limite, fonctionne hors ligne !")
        except ImportError:
            print("[!] pyttsx3 non installe")
            print("[INFO] Lance: pip install pyttsx3")
            self.available = False
        except Exception as e:
            print(f"[!] Erreur initialisation pyttsx3 : {e}")
            self.available = False
    
    def generate_audiobook(
        self,
        text: str,
        language: str,
        output_path: Path,
        speed: float = 1.0
    ) -> bool:
        """
        Génère un audiobook pour une langue
        
        Args:
            text: Texte à convertir en audio
            language: Code langue (fr, en, etc.)
            output_path: Chemin de sortie (.mp3)
            speed: Vitesse de lecture (0.5-2.0, défaut 1.0)
            
        Returns:
            True si succès, False sinon
        """
        if not self.available or not self.engine:
            print("[ERREUR] pyttsx3 non disponible")
            return False
        
        # Vérifier que la langue est supportée
        if language not in self.voice_models:
            print(f"[ERREUR] Langue non supportee : {language}")
            return False
        
        try:
            # Créer dossier de sortie
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Configurer vitesse
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', int(rate * speed))
            
            # Sélectionner voix appropriée si disponible
            voices = self.engine.getProperty('voices')
            
            # Essayer de trouver une voix correspondant à la langue
            lang_code = self.voice_models[language]
            voice_found = False
            
            for voice in voices:
                # Vérifier si la voix correspond à la langue
                if lang_code.lower() in voice.id.lower() or lang_code.lower() in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    voice_found = True
                    print(f"[TTS] Voix trouvée pour {language}: {voice.name}")
                    break
            
            if not voice_found:
                # Utiliser voix par défaut
                print(f"[TTS] Utilisation voix par défaut pour {language}")
            
            # Générer l'audio
            print(f"[TTS] Generation audio en {language}...")
            print(f"[TTS] Texte : {len(text)} caracteres")
            
            # Sauvegarder en MP3 (ou WAV selon disponibilité)
            output_str = str(output_path)
            
            # Essayer MP3 d'abord, sinon WAV
            if output_str.endswith('.mp3'):
                # Certaines versions de pyttsx3 ne supportent pas MP3 directement
                # On sauvegarde en WAV puis convertit (optionnel)
                wav_path = output_path.with_suffix('.wav')
                self.engine.save_to_file(text, str(wav_path))
                self.engine.runAndWait()
                
                # Si WAV créé avec succès, on le garde (ou convertit en MP3 si pydub disponible)
                if wav_path.exists():
                    try:
                        from pydub import AudioSegment
                        audio = AudioSegment.from_wav(str(wav_path))
                        audio.export(str(output_path), format="mp3")
                        wav_path.unlink()  # Supprimer WAV temporaire
                        print(f"[OK] Audio genere (MP3) : {output_path}")
                    except:
                        # Si conversion échoue, renommer WAV en MP3
                        wav_path.rename(output_path.with_suffix('.wav'))
                        print(f"[OK] Audio genere (WAV) : {output_path.with_suffix('.wav')}")
                else:
                    print(f"[ERREUR] Echec generation audio")
                    return False
            else:
                # Format WAV direct
                self.engine.save_to_file(text, output_str)
                self.engine.runAndWait()
                print(f"[OK] Audio genere : {output_path}")
            
            return True
                
        except Exception as e:
            print(f"[ERREUR] Generation audio : {e}")
            return False
    
    def generate_all_audiobooks(
        self,
        book_manager,
        output_dir: Optional[Path] = None,
        languages: Optional[List[str]] = None
    ) -> Dict[str, Path]:
        """
        Génère des audiobooks pour toutes les langues
        
        Args:
            book_manager: BookManager avec les chapitres
            output_dir: Dossier de sortie (défaut: data/audiobooks/)
            languages: Liste de langues (défaut: toutes)
            
        Returns:
            Dictionnaire {langue: chemin_fichier}
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "data" / "audiobooks"
        
        if languages is None:
            languages = list(self.voice_models.keys())
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        
        for lang in languages:
            print(f"\n[AUDIOBOOK] Generation {lang.upper()}...")
            
            # Construire le texte complet du livre
            full_text = self._build_book_text(book_manager, lang)
            
            if not full_text:
                print(f"[!] Pas de contenu pour {lang}, ignore")
                continue
            
            # Générer l'audio
            output_file = output_dir / f"audiobook_{lang}.mp3"
            
            success = self.generate_audiobook(
                text=full_text,
                language=lang,
                output_path=output_file
            )
            
            if success:
                generated_files[lang] = output_file
        
        return generated_files
    
    def _build_book_text(self, book_manager, language: str) -> str:
        """Construit le texte complet du livre dans une langue"""
        parts = []
        
        # Ajouter le titre
        parts.append(f"{book_manager.title}\n")
        parts.append(f"Par {book_manager.author}\n\n")
        
        # Ajouter chaque chapitre
        for i, chapter in enumerate(book_manager.chapters):
            # Titre du chapitre
            chapter_title = chapter.get_title_translation(language)
            if not chapter_title:
                chapter_title = chapter.title
            
            parts.append(f"Chapitre {i+1}: {chapter_title}\n\n")
            
            # Contenu du chapitre
            if language == 'fr':
                content = chapter.content_fr
            else:
                content = chapter.get_translation(language)
            
            if content:
                parts.append(content)
                parts.append("\n\n")
        
        return "".join(parts)
    
    def get_audio_duration(self, audio_file: Path) -> Optional[float]:
        """Retourne la durée de l'audio en secondes"""
        try:
            from pydub import AudioSegment
            
            # Détecter format
            if audio_file.suffix == '.mp3':
                audio = AudioSegment.from_mp3(str(audio_file))
            elif audio_file.suffix == '.wav':
                audio = AudioSegment.from_wav(str(audio_file))
            else:
                return None
            
            duration = len(audio) / 1000.0  # Convertir ms en secondes
            return duration
            
        except Exception as e:
            print(f"[!] Impossible de lire la duree : {e}")
            return None
