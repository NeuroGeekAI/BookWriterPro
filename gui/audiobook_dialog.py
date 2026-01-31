"""
Audiobook Generator Dialog - Interface pour generer des audiobooks
Support 17 langues - pyttsx3 (TTS 100% LOCAL)
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from pathlib import Path
import subprocess
import sys

from core.audiobook_generator import AudiobookGenerator


class AudiobookDialog:
    """Dialogue pour generer des audiobooks dans 17 langues"""
    
    def __init__(self, parent, book_manager):
        self.parent = parent
        self.book_manager = book_manager
        self.audiobook_generator = AudiobookGenerator()
        
        # Creer la fenetre
        self.window = tk.Toplevel(parent)
        self.window.title("Generateur Audiobook - 17 Langues (100% LOCAL)")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # Variables
        self.selected_languages = {}
        self.is_generating = False
        
        self._create_ui()
        
        # Verifier disponibilite pyttsx3
        if not self.audiobook_generator.available:
            messagebox.showerror(
                "pyttsx3 Non Installe",
                "L'audiobook generator necessite pyttsx3.\n\n"
                "Lancez: INSTALL_AUDIOBOOK.bat\n\n"
                "Avantages:\n"
                "✅ 100% LOCAL (pas d'API)\n"
                "✅ Aucune limite\n"
                "✅ Fonctionne hors ligne"
            )
            self.window.destroy()
            return
    
    def _create_ui(self):
        """Cree l'interface utilisateur"""
        # Frame principale
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="Generer Audiobooks (100% LOCAL)",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Info
        info_text = (
            "Selectionnez les langues pour generer vos audiobooks.\n\n"
            "TTS 100% LOCAL (pyttsx3) - Aucune API, aucune limite !\n"
            "Utilise les voix installees sur Windows.\n\n"
            "Note : Certaines langues necesitent des voix Windows supplementaires.\n"
            "(FR, EN, ES, DE, IT, PT fonctionnent generalement par defaut)"
        )
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.CENTER, foreground='blue')
        info_label.pack(pady=(0, 20))
        
        # Frame selection langues
        lang_frame = ttk.LabelFrame(main_frame, text="Selection Langues", padding=10)
        lang_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Canvas avec scrollbar pour les langues
        canvas = tk.Canvas(lang_frame, height=300)
        scrollbar = ttk.Scrollbar(lang_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Langues disponibles
        languages = {
            'fr': 'Francais',
            'en': 'English',
            'es': 'Espanol',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Portugues',
            'ja': 'Japonais',
            'zh': 'Chinois',
            'ar': 'Arabe',
            'ru': 'Russe',
            'hi': 'Hindi',
            'ko': 'Coreen',
            'id': 'Indonesien',
            'tr': 'Turc',
            'vi': 'Vietnamien',
            'pl': 'Polonais',
            'th': 'Thai'
        }
        
        # Boutons tout selectionner/deselectionner
        select_frame = ttk.Frame(scrollable_frame)
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            select_frame,
            text="Tout selectionner",
            command=lambda: self._toggle_all_languages(True)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            select_frame,
            text="Tout deselectionner",
            command=lambda: self._toggle_all_languages(False)
        ).pack(side=tk.LEFT, padx=5)
        
        # Creer checkboxes pour chaque langue
        for lang_code, lang_name in languages.items():
            var = tk.BooleanVar(value=False)
            self.selected_languages[lang_code] = var
            
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=f"{lang_name} ({lang_code})",
                variable=var
            )
            cb.pack(anchor=tk.W, pady=2)
        
        # Frame progression
        self.progress_frame = ttk.LabelFrame(main_frame, text="Progression", padding=10)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_text = ttk.Label(
            self.progress_frame,
            text="Pret a generer",
            font=('Arial', 10)
        )
        self.progress_text.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=500
        )
        self.progress_bar.pack(pady=5)
        
        # Boutons action
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(0, 10))
        
        self.generate_btn = ttk.Button(
            btn_frame,
            text="GENERER AUDIOBOOKS",
            command=self._start_generation
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Fermer",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def _toggle_all_languages(self, select: bool):
        """Selectionne/deselectionne toutes les langues"""
        for var in self.selected_languages.values():
            var.set(select)
    
    def _start_generation(self):
        """Demarre la generation des audiobooks"""
        if self.is_generating:
            messagebox.showwarning("En cours", "Generation deja en cours !")
            return
        
        # Recuperer langues selectionnees
        selected = [
            lang for lang, var in self.selected_languages.items()
            if var.get()
        ]
        
        if not selected:
            messagebox.showwarning(
                "Aucune langue",
                "Veuillez selectionner au moins une langue !"
            )
            return
        
        # Verifier qu'il y a des chapitres
        if not self.book_manager.chapters:
            messagebox.showerror(
                "Pas de contenu",
                "Aucun chapitre a convertir en audiobook !"
            )
            return
        
        # Confirmation
        nb_langs = len(selected)
        response = messagebox.askyesno(
            "Confirmer generation",
            f"Generer {nb_langs} audiobook(s) ?\n\n"
            f"Langues : {', '.join(selected)}\n"
            f"Temps estime : {nb_langs * 2}-{nb_langs * 5} minutes\n\n"
            f"TTS 100% LOCAL (pyttsx3) - Aucune limite !\n"
            f"Fonctionne hors ligne."
        )
        
        if not response:
            return
        
        # Lancer generation en thread
        self.is_generating = True
        self.generate_btn.config(state='disabled')
        
        thread = threading.Thread(
            target=self._do_generate,
            args=(selected,),
            daemon=True
        )
        thread.start()
    
    def _do_generate(self, languages: list):
        """Execute la generation (dans thread separe)"""
        try:
            # Preparation
            self._update_progress("Preparation...", 0)
            
            output_dir = Path(__file__).parent.parent / "data" / "audiobooks"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            total = len(languages)
            generated_files = {}
            
            # Generer pour chaque langue
            for i, lang in enumerate(languages):
                self._update_progress(
                    f"Generation {lang.upper()} ({i+1}/{total})...",
                    int((i / total) * 100)
                )
                
                # Construire le texte complet
                full_text = self.audiobook_generator._build_book_text(
                    self.book_manager,
                    lang
                )
                
                if not full_text:
                    print(f"[!] Pas de contenu pour {lang}")
                    continue
                
                # Generer l'audiobook
                output_file = output_dir / f"audiobook_{lang}.mp3"
                success = self.audiobook_generator.generate_audiobook(
                    text=full_text,
                    language=lang,
                    output_path=output_file
                )
                
                if success:
                    generated_files[lang] = output_file
            
            # Termine !
            self._update_progress("Termine !", 100)
            
            # Afficher resultats
            self.window.after(0, lambda: self._on_generation_complete(generated_files))
            
        except Exception as e:
            error_msg = f"Erreur generation : {e}"
            print(f"[ERREUR] {error_msg}")
            import traceback
            traceback.print_exc()
            
            self.window.after(0, lambda: messagebox.showerror(
                "Erreur Generation",
                error_msg
            ))
        
        finally:
            self.is_generating = False
            self.window.after(0, lambda: self.generate_btn.config(state='normal'))
    
    def _update_progress(self, text: str, value: int):
        """Met a jour la barre de progression (thread-safe)"""
        def update():
            self.progress_text.config(text=text)
            self.progress_bar['value'] = value
            self.window.update_idletasks()
        
        self.window.after(0, update)
    
    def _on_generation_complete(self, generated_files: dict):
        """Appele quand la generation est terminee"""
        if not generated_files:
            messagebox.showwarning(
                "Aucun fichier",
                "Aucun audiobook n'a ete genere.\n\n"
                "Causes possibles :\n"
                "- Voix Windows non installees pour ces langues\n"
                "- Verifiez les logs pour details\n\n"
                "Langues fonctionnelles : FR, EN, ES, DE, IT, PT"
            )
            return
        
        # Message de succes
        nb_files = len(generated_files)
        output_dir = Path(__file__).parent.parent / "data" / "audiobooks"
        
        msg = f"{nb_files} audiobook(s) generes avec succes !\n\n"
        msg += f"Dossier : {output_dir}\n\n"
        msg += "Fichiers :\n"
        
        for lang, filepath in generated_files.items():
            # Calculer taille fichier
            size_mb = filepath.stat().st_size / (1024 * 1024)
            msg += f"- {filepath.name} ({size_mb:.1f} MB)\n"
        
        msg += f"\nOuvrir le dossier maintenant ?"
        
        response = messagebox.askyesno(
            "Generation Terminee",
            msg
        )
        
        if response:
            self._open_audiobooks_folder()
    
    def _open_audiobooks_folder(self):
        """Ouvre le dossier des audiobooks"""
        output_dir = Path(__file__).parent.parent / "data" / "audiobooks"
        
        try:
            if sys.platform == 'win32':
                subprocess.run(['explorer', str(output_dir)])
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(output_dir)])
            else:
                subprocess.run(['xdg-open', str(output_dir)])
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier : {e}")
