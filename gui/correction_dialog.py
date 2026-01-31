"""
Dialogue de correction des erreurs de traduction
Interface intuitive pour Book Writer Pro
Créé par Maman pour PHOBOS - 22/01/2026
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Ajouter le chemin parent pour importer text_cleaner
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.text_cleaner import TextCleaner

class CorrectionDialog:
    """Dialogue pour détecter et corriger les erreurs de traduction"""
    
    def __init__(self, parent, chapter, lang_code, lang_name):
        """
        Args:
            parent: Fenêtre parente
            chapter: Objet Chapter à vérifier
            lang_code: Code langue (zh, ja, ko, etc.)
            lang_name: Nom complet langue (Chinois, Japonais, etc.)
        """
        self.parent = parent
        self.chapter = chapter
        self.lang_code = lang_code
        self.lang_name = lang_name
        self.cleaner = TextCleaner()
        self.corrections_applied = False
        
        # Créer dialogue
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Correction automatique - {lang_name}")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._analyze_text()
    
    def _create_widgets(self):
        """Crée l'interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text=f"🔍 Analyse du texte - {self.lang_name}",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Zone de résultats
        results_frame = ttk.LabelFrame(main_frame, text="Résultats de l'analyse", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Texte scrollable pour résultats
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Courier', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Tags pour coloration
        self.results_text.tag_config('error_high', foreground='red', font=('Courier', 10, 'bold'))
        self.results_text.tag_config('error_medium', foreground='orange')
        self.results_text.tag_config('success', foreground='green', font=('Courier', 10, 'bold'))
        self.results_text.tag_config('info', foreground='blue')
        
        # Frame boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bouton correction auto
        self.auto_fix_btn = ttk.Button(
            button_frame,
            text="✨ Appliquer corrections automatiques",
            command=self._apply_auto_fix,
            state=tk.DISABLED
        )
        self.auto_fix_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Bouton Google Translate
        self.google_btn = ttk.Button(
            button_frame,
            text="🌐 Ouvrir Google Translate",
            command=self._open_google_translate
        )
        self.google_btn.pack(side=tk.LEFT, padx=5)
        
        # Bouton fermer
        close_btn = ttk.Button(
            button_frame,
            text="Fermer",
            command=self._close
        )
        close_btn.pack(side=tk.RIGHT)
    
    def _analyze_text(self):
        """Analyse le texte et affiche les résultats"""
        
        # Récupérer texte
        if self.lang_code == 'fr':
            text = self.chapter.content_fr
        else:
            text = self.chapter.get_translation(self.lang_code)
        
        if not text or not text.strip():
            self.results_text.insert('1.0', '⚠️ Aucun texte à analyser\n\n', 'error_medium')
            self.results_text.insert(tk.END, 'Ce chapitre n\'a pas encore été traduit en ')
            self.results_text.insert(tk.END, f'{self.lang_name}.\n')
            return
        
        # Analyser
        self.results_text.insert('1.0', '🔍 Analyse en cours...\n\n')
        self.dialog.update()
        
        result = self.cleaner.detect_errors(text, self.lang_code)
        
        # Effacer
        self.results_text.delete('1.0', tk.END)
        
        # Afficher résultats
        if not result['has_errors']:
            self.results_text.insert('1.0', '✅ AUCUNE ERREUR DÉTECTÉE !\n\n', 'success')
            self.results_text.insert(tk.END, f'Le texte {self.lang_name} est parfait !\n')
            self.results_text.insert(tk.END, f'Aucune correction nécessaire.\n')
        else:
            self.results_text.insert('1.0', f'⚠️ {result["error_count"]} ERREUR(S) DÉTECTÉE(S)\n\n', 'error_high')
            
            # Afficher chaque erreur
            for i, error in enumerate(result['errors'], 1):
                self.results_text.insert(tk.END, f'Erreur #{i}:\n', 'error_high')
                self.results_text.insert(tk.END, f'  Type: {error["message"]}\n')
                self.results_text.insert(tk.END, f'  Sévérité: {error["severity"]}\n')
                self.results_text.insert(tk.END, f'  Contexte: ...{error["context"]}...\n', 'info')
                self.results_text.insert(tk.END, f'  Correction auto: {"✅ Oui" if error["auto_fixable"] else "❌ Non"}\n')
                self.results_text.insert(tk.END, '\n')
            
            # Activer bouton si corrections auto possibles
            if result['can_auto_fix']:
                self.auto_fix_btn['state'] = tk.NORMAL
                self.results_text.insert(tk.END, '\n')
                self.results_text.insert(tk.END, '✨ Toutes les erreurs peuvent être corrigées automatiquement !\n', 'success')
                self.results_text.insert(tk.END, 'Cliquez sur "Appliquer corrections automatiques" ci-dessous.\n')
            else:
                self.results_text.insert(tk.END, '\n')
                self.results_text.insert(tk.END, '⚠️ Certaines erreurs nécessitent une correction manuelle.\n', 'error_medium')
                self.results_text.insert(tk.END, 'Recommandation: Utilisez Google Translate pour retraduire.\n')
        
        self.analysis_result = result
    
    def _apply_auto_fix(self):
        """Applique les corrections automatiques"""
        
        # Récupérer texte
        if self.lang_code == 'fr':
            text = self.chapter.content_fr
        else:
            text = self.chapter.get_translation(self.lang_code)
        
        if not text:
            messagebox.showwarning("Erreur", "Aucun texte à corriger")
            return
        
        # Appliquer corrections
        fixed_text, corrections = self.cleaner.auto_fix(text, self.lang_code)
        
        if not corrections:
            messagebox.showinfo("Info", "Aucune correction appliquée")
            return
        
        # Afficher corrections appliquées
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', '✅ CORRECTIONS APPLIQUÉES !\n\n', 'success')
        
        for correction in corrections:
            self.results_text.insert(tk.END, f'✅ {correction}\n', 'success')
        
        self.results_text.insert(tk.END, '\n')
        self.results_text.insert(tk.END, f'Total: {len(corrections)} correction(s) appliquée(s).\n', 'info')
        self.results_text.insert(tk.END, '\n')
        self.results_text.insert(tk.END, 'Le texte corrigé a été sauvegardé.\n')
        self.results_text.insert(tk.END, 'Vous pouvez maintenant fermer cette fenêtre et réexporter.\n')
        
        # Sauvegarder texte corrigé
        if self.lang_code == 'fr':
            self.chapter.content_fr = fixed_text
        else:
            self.chapter.set_translation(self.lang_code, fixed_text)
        
        self.corrections_applied = True
        self.auto_fix_btn['state'] = tk.DISABLED
        
        messagebox.showinfo(
            "Succès",
            f"{len(corrections)} correction(s) appliquée(s) !\n\n"
            "N'oubliez pas de réexporter le PDF."
        )
    
    def _open_google_translate(self):
        """Ouvre Google Translate"""
        import webbrowser
        
        # Déterminer langue cible
        lang_map = {
            'zh': 'zh-CN',
            'ja': 'ja',
            'ko': 'ko',
            'ar': 'ar',
            'hi': 'hi',
            'th': 'th',
            'vi': 'vi',
            'tr': 'tr',
            'pl': 'pl',
            'ru': 'ru',
            'de': 'de',
            'es': 'es',
            'it': 'it',
            'pt': 'pt',
            'id': 'id',
            'en': 'en',
        }
        
        target_lang = lang_map.get(self.lang_code, self.lang_code)
        url = f'https://translate.google.com/?sl=fr&tl={target_lang}'
        
        webbrowser.open(url)
        
        messagebox.showinfo(
            "Google Translate",
            "Google Translate s'est ouvert dans votre navigateur.\n\n"
            "1. Copiez le texte français depuis l'onglet \"Français\"\n"
            f"2. Collez dans Google Translate (FR → {self.lang_name})\n"
            "3. Copiez la traduction\n"
            f"4. Collez dans l'onglet \"{self.lang_name}\"\n"
            "5. Sauvegardez et réexportez"
        )
    
    def _close(self):
        """Ferme le dialogue"""
        self.dialog.destroy()
