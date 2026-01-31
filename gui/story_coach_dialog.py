"""
Story Coach Dialog - Interface pour le coaching d'écriture
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Dict

class StoryCoachDialog:
    """Dialogue interactif avec le Story Coach"""
    
    def __init__(self, parent, chapter, story_coach, on_success_callback=None):
        self.parent = parent
        self.chapter = chapter
        self.story_coach = story_coach
        self.on_success_callback = on_success_callback
        self.questions = []
        self.answers = {}
        self.current_question_index = 0
        
        # Créer la fenêtre
        self.window = tk.Toplevel(parent)
        self.window.title(f"🤖 Story Coach - {chapter.title}")
        self.window.geometry("900x700")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Empêcher de fermer pendant le chargement
        self.loading = False
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._create_ui()
        
        # Générer les questions automatiquement
        self._generate_questions()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="🤖 Story Coach - Enrichis ton histoire !",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="L'IA va te poser des questions pour approfondir ton chapitre.\n"
                 "Réponds avec autant de détails que possible !",
            font=('Arial', 10),
            foreground='gray'
        )
        desc_label.pack(pady=(0, 20))
        
        # Zone de chargement / questions
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Loading label (visible au départ)
        self.loading_label = ttk.Label(
            self.content_frame,
            text="⏳ Analyse de ton chapitre en cours...\n\n"
                 "L'IA locale lit ton texte et prépare des questions\n"
                 "intelligentes pour t'aider à l'enrichir.\n\n"
                 "Cela peut prendre 10-30 secondes...",
            font=('Arial', 11),
            foreground='orange'
        )
        self.loading_label.pack(expand=True, pady=50)
        
        # Frame des questions (caché au départ)
        self.question_frame = ttk.Frame(self.content_frame)
        
        # Question actuelle
        question_header_frame = ttk.Frame(self.question_frame)
        question_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.question_number_label = ttk.Label(
            question_header_frame,
            text="Question 1/5",
            font=('Arial', 10, 'bold'),
            foreground='blue'
        )
        self.question_number_label.pack(side=tk.LEFT)
        
        self.question_label = ttk.Label(
            self.question_frame,
            text="",
            font=('Arial', 12),
            wraplength=850,
            justify=tk.LEFT
        )
        self.question_label.pack(fill=tk.X, pady=(0, 5))
        
        # Raison de la question
        self.reason_label = ttk.Label(
            self.question_frame,
            text="",
            font=('Arial', 9, 'italic'),
            foreground='gray',
            wraplength=850,
            justify=tk.LEFT
        )
        self.reason_label.pack(fill=tk.X, pady=(0, 15))
        
        # Zone de réponse
        response_label = ttk.Label(
            self.question_frame,
            text="Ta réponse :",
            font=('Arial', 10, 'bold')
        )
        response_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.answer_text = scrolledtext.ScrolledText(
            self.question_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            height=12
        )
        self.answer_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Boutons
        button_frame = ttk.Frame(self.question_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.prev_button = ttk.Button(
            button_frame,
            text="◀ Question précédente",
            command=self._prev_question,
            state='disabled'
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.skip_button = ttk.Button(
            button_frame,
            text="⏭ Passer",
            command=self._next_question
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Question suivante ▶",
            command=self._next_question
        )
        self.next_button.pack(side=tk.RIGHT, padx=5)
        
        self.finish_button = ttk.Button(
            button_frame,
            text="✅ Terminer et enrichir",
            command=self._finish_and_enrich
        )
        # finish_button sera affiché à la dernière question
        
        # Barre de progression
        self.progress = ttk.Progressbar(
            main_frame,
            mode='determinate',
            length=850
        )
        self.progress.pack(fill=tk.X, pady=(10, 0))
    
    def _generate_questions(self):
        """Génère les questions dans un thread"""
        self.loading = True
        threading.Thread(target=self._do_generate_questions, daemon=True).start()
    
    def _do_generate_questions(self):
        """Génère les questions (thread)"""
        try:
            # Générer les questions
            self.questions = self.story_coach.generate_questions(
                self.chapter.content_fr,
                self.chapter.title
            )
            
            # Mettre à jour l'UI dans le thread principal
            self.window.after(0, self._on_questions_generated)
            
        except Exception as e:
            self.window.after(0, lambda: self._on_error(str(e)))
    
    def _on_questions_generated(self):
        """Appelé quand les questions sont générées"""
        self.loading = False
        
        if not self.questions or len(self.questions) == 0:
            messagebox.showerror(
                "Erreur",
                "Impossible de générer des questions.\n\n"
                "Vérifie que le Story Coach est bien installé."
            )
            self.window.destroy()
            return
        
        # Cacher le loading, afficher les questions
        self.loading_label.pack_forget()
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        
        # Afficher la première question
        self._display_question(0)
    
    def _on_error(self, error_msg: str):
        """Appelé en cas d'erreur"""
        self.loading = False
        messagebox.showerror(
            "Erreur Story Coach",
            f"Une erreur s'est produite :\n\n{error_msg}\n\n"
            f"Le chapitre sera enrichi avec des questions génériques."
        )
        self.window.destroy()
    
    def _display_question(self, index: int):
        """Affiche une question"""
        if index < 0 or index >= len(self.questions):
            return
        
        self.current_question_index = index
        question_data = self.questions[index]
        
        # Mettre à jour les labels
        self.question_number_label.config(
            text=f"Question {index + 1}/{len(self.questions)}"
        )
        self.question_label.config(text=question_data['question'])
        self.reason_label.config(text=f"💡 {question_data['reason']}")
        
        # Charger la réponse si elle existe
        question_text = question_data['question']
        if question_text in self.answers:
            self.answer_text.delete('1.0', tk.END)
            self.answer_text.insert('1.0', self.answers[question_text])
        else:
            self.answer_text.delete('1.0', tk.END)
        
        # Mettre à jour les boutons
        self.prev_button.config(
            state='normal' if index > 0 else 'disabled'
        )
        
        # À la dernière question, afficher bouton Terminer
        if index == len(self.questions) - 1:
            self.next_button.pack_forget()
            self.finish_button.pack(side=tk.RIGHT, padx=5)
        else:
            self.finish_button.pack_forget()
            self.next_button.pack(side=tk.RIGHT, padx=5)
        
        # Mettre à jour la barre de progression
        self.progress['maximum'] = len(self.questions)
        self.progress['value'] = index + 1
    
    def _prev_question(self):
        """Question précédente"""
        # Sauvegarder la réponse actuelle
        self._save_current_answer()
        
        # Afficher la question précédente
        if self.current_question_index > 0:
            self._display_question(self.current_question_index - 1)
    
    def _next_question(self):
        """Question suivante"""
        # Sauvegarder la réponse actuelle
        self._save_current_answer()
        
        # Afficher la question suivante
        if self.current_question_index < len(self.questions) - 1:
            self._display_question(self.current_question_index + 1)
    
    def _save_current_answer(self):
        """Sauvegarde la réponse actuelle"""
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            answer = self.answer_text.get('1.0', tk.END).strip()
            
            if answer:
                self.answers[question_data['question']] = answer
    
    def _finish_and_enrich(self):
        """Termine et enrichit le chapitre"""
        # Sauvegarder la dernière réponse
        self._save_current_answer()
        
        # Vérifier qu'il y a au moins quelques réponses
        if len(self.answers) == 0:
            if not messagebox.askyesno(
                "Aucune réponse",
                "Tu n'as répondu à aucune question.\n\n"
                "Veux-tu quand même fermer le Story Coach ?"
            ):
                return
            self.window.destroy()
            return
        
        # Demander confirmation
        answered_count = len(self.answers)
        total_count = len(self.questions)
        
        if not messagebox.askyesno(
            "Enrichir le chapitre",
            f"Tu as répondu à {answered_count}/{total_count} questions.\n\n"
            f"Le Story Coach va maintenant enrichir ton chapitre\n"
            f"en intégrant tes réponses de manière fluide.\n\n"
            f"Continuer ?"
        ):
            return
        
        # Créer fenêtre de progression
        self._show_enrichment_progress()
    
    def _show_enrichment_progress(self):
        """Affiche la fenêtre de progression de l'enrichissement"""
        # Désactiver tous les boutons
        self.prev_button.config(state='disabled')
        self.skip_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.finish_button.config(state='disabled')
        self.answer_text.config(state='disabled')
        
        # Cacher le contenu actuel
        self.question_frame.pack_forget()
        
        # Afficher le loading
        self.loading_label.config(
            text="⏳ Enrichissement en cours...\n\n"
                 "L'IA intègre tes réponses dans le chapitre\n"
                 "pour créer un récit plus profond et touchant.\n\n"
                 "Cela peut prendre 30-60 secondes..."
        )
        self.loading_label.pack(expand=True, pady=50)
        
        # Lancer l'enrichissement dans un thread
        threading.Thread(target=self._do_enrich, daemon=True).start()
    
    def _do_enrich(self):
        """Effectue l'enrichissement (thread)"""
        try:
            # Enrichir avec le Story Coach
            enriched_content = self.story_coach.suggest_enrichment(
                self.chapter.content_fr,
                self.answers
            )
            
            # Mettre à jour le chapitre
            self.chapter.update_content(enriched_content)
            
            # Succès
            self.window.after(0, self._on_enrichment_success)
            
        except Exception as e:
            self.window.after(0, lambda: self._on_enrichment_error(str(e)))
    
    def _on_enrichment_success(self):
        """Appelé quand l'enrichissement réussit"""
        answered_count = len(self.answers)
        
        # Appeler le callback AVANT d'afficher le message
        if self.on_success_callback:
            self.on_success_callback()
        
        messagebox.showinfo(
            "✅ Enrichissement réussi !",
            f"Ton chapitre a été enrichi avec succès !\n\n"
            f"✅ {answered_count} réponses intégrées\n"
            f"✅ Texte plus profond et émotionnel\n"
            f"✅ Transitions fluides créées\n\n"
            f"💡 Relis le chapitre et ajuste si besoin !"
        )
        
        self.window.destroy()
    
    def _on_enrichment_error(self, error_msg: str):
        """Appelé en cas d'erreur d'enrichissement"""
        messagebox.showerror(
            "Erreur enrichissement",
            f"Une erreur s'est produite pendant l'enrichissement :\n\n"
            f"{error_msg}\n\n"
            f"Tes réponses ont été sauvegardées mais pas intégrées\n"
            f"au chapitre. Essaie de les copier-coller manuellement."
        )
        self.window.destroy()
    
    def _on_close(self):
        """Gère la fermeture de la fenêtre"""
        if self.loading:
            messagebox.showwarning(
                "Chargement en cours",
                "Attends que le Story Coach termine son analyse..."
            )
            return
        
        # Demander confirmation si des réponses ont été données
        if len(self.answers) > 0:
            if not messagebox.askyesno(
                "Fermer sans enrichir ?",
                f"Tu as répondu à {len(self.answers)} questions.\n\n"
                f"Si tu fermes maintenant, tes réponses seront perdues.\n\n"
                f"Fermer quand même ?"
            ):
                return
        
        self.window.destroy()
