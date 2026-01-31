"""
Main Window - Interface graphique principale
Support multilingue 17 langues
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from pathlib import Path
import json

from core.book_manager import BookManager
from core.translator import Translator
from core.security_checker import SecurityChecker, SecurityAlert
from core.autosave import AutoSave
from core.story_coach import StoryCoach
from core.cover_generator import CoverGenerator
from core.audiobook_generator import AudiobookGenerator
from core.i18n_gui import get_i18n, init_i18n, _
from importers.conversation_importer import ConversationImporter
from gui.story_coach_dialog import StoryCoachDialog
from gui.cover_generator_dialog import CoverGeneratorDialog
from gui.audiobook_dialog import AudiobookDialog
from exporters.pdf_exporter import PDFExporter
from exporters.epub_exporter import EPUBExporter
from exporters.docx_exporter import DOCXExporter
from exporters.kdp_exporter import KDPExporter
from gui.correction_dialog import CorrectionDialog

class BookWriterApp:
    """Application principale Book Writer Pro"""
    
    def __init__(self):
        # Initialiser i18n AVANT tout le reste
        init_i18n()
        
        self.root = tk.Tk()
        self.root.title(_('app.title'))
        self.root.geometry("1400x900")
        
        # Managers
        self.book_manager = BookManager()
        self.translator = Translator()
        self.security_checker = SecurityChecker()
        self.story_coach = StoryCoach()
        self.cover_generator = CoverGenerator()
        self.audiobook_generator = AudiobookGenerator()
        self.conversation_importer = ConversationImporter()
        
        # État
        self.current_mode = "public"  # Mode fixe pour grand public
        self.current_lang = "fr"
        self.translating = False
        
        # Auto-save
        self.autosave = AutoSave(self._do_autosave, interval=30)
        
        # Charger livre existant
        self.book_manager.load()
        
        # Créer l'interface
        self._create_ui()
        
        # Démarrer auto-save
        self.autosave.start()
        
        # Mettre à jour l'interface
        self._update_chapter_tree()
        self._update_stats()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_('menu.file'), menu=file_menu)
        file_menu.add_command(label=_('menu.settings'), command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label=_('menu.quit'), command=self._on_close)
        
        # Menu Langue
        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_('menu.language'), menu=lang_menu)
        
        i18n = get_i18n()
        for lang_code, lang_name in i18n.get_all_languages().items():
            lang_menu.add_command(
                label=lang_name,
                command=lambda lc=lang_code: self._change_gui_language(lc)
            )
        
        # Barre supérieure - Langue uniquement (mode public par défaut)
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(top_frame, text="🌍 LANGUE:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.lang_combo = ttk.Combobox(top_frame, width=15, state='readonly')
        self.lang_combo['values'] = [
            '🇫🇷 Français',
            '🇬🇧 English',
            '🇪🇸 Español',
            '🇮🇹 Italiano',
            '🇷🇺 Русский',
            '🇯🇵 日本語',
            '🇨🇳 中文',
            '🇮🇳 हिन्दी',
            '🇸🇦 العربية',
            '🇩🇪 Deutsch',
            '🇧🇷 Português',
            '🇹🇷 Türkçe',
            '🇰🇷 한국어',
            '🇮🇩 Bahasa',
            '🇻🇳 Tiếng Việt',
            '🇵🇱 Polski',
            '🇹🇭 ไทย'
        ]
        self.lang_combo.current(0)
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        
        # Frame principal - 3 panneaux
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panneau gauche - Chapitres
        left_frame = ttk.Frame(main_frame, width=250)
        main_frame.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text=_('panel.structure'), font=('Arial', 11, 'bold')).pack(pady=5)
        
        self.chapter_tree = ttk.Treeview(left_frame, selectmode='browse', height=25)
        self.chapter_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chapter_tree.bind('<<TreeviewSelect>>', self._on_chapter_select)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text=_('button.new_chapter'), command=self._add_chapter).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text=_('button.delete'), command=self._remove_chapter).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text=_('button.import'), command=self._import_conversations).pack(side=tk.LEFT, padx=2)
        
        btn_frame2 = ttk.Frame(left_frame)
        btn_frame2.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(btn_frame2, text=_('button.translate_title'), command=self._translate_chapter_title).pack(fill=tk.X, padx=2)
        
        # Panneau central - Éditeur
        center_frame = ttk.Frame(main_frame)
        main_frame.add(center_frame, weight=3)
        
        self.chapter_title_label = ttk.Label(center_frame, text=_('panel.editor'), 
                                            font=('Arial', 12, 'bold'))
        self.chapter_title_label.pack(pady=5)
        
        self.editor = scrolledtext.ScrolledText(center_frame, wrap=tk.WORD, 
                                               font=('Arial', 11), 
                                               undo=True)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.editor.bind('<KeyRelease>', self._on_text_change)
        
        # Alerte frame (caché en version simplifiée)
        # Version grand public : pas d'alertes affichées
        
        # Boutons éditeur
        editor_btn_frame = ttk.Frame(center_frame)
        editor_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(editor_btn_frame, text=_('button.save'), 
                  command=self._manual_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(editor_btn_frame, text=_('button.story_coach'), 
                  command=self._open_story_coach).pack(side=tk.LEFT, padx=5)
        ttk.Button(editor_btn_frame, text=_('button.translate_all'), 
                  command=self._translate_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(editor_btn_frame, text=_('button.translate_selection'), 
                  command=self._translate_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(editor_btn_frame, text=_('button.check_quality'), 
                  command=self._check_translation_quality).pack(side=tk.LEFT, padx=5)
        
        self.autosave_label = ttk.Label(editor_btn_frame, text=_('stats.autosave_never'))
        self.autosave_label.pack(side=tk.RIGHT, padx=5)
        
        # Panneau droit - Traductions
        right_frame = ttk.Frame(main_frame, width=350)
        main_frame.add(right_frame, weight=2)
        
        ttk.Label(right_frame, text=_('panel.translations'), font=('Arial', 11, 'bold')).pack(pady=5)
        
        self.translation_notebook = ttk.Notebook(right_frame)
        self.translation_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Créer les onglets de traduction (16 langues - toutes sauf français)
        self.translation_texts = {}
        for lang_code, lang_name in [('en', 'English'), ('es', 'Español'), 
                                     ('it', 'Italiano'), ('ru', 'Русский'),
                                     ('ja', '日本語'), ('zh', '中文'),
                                     ('hi', 'हिन्दी'), ('ar', 'العربية'), 
                                     ('de', 'Deutsch'), ('pt', 'Português'),
                                     ('tr', 'Türkçe'), ('ko', '한국어'),
                                     ('id', 'Bahasa'), ('vi', 'Tiếng Việt'),
                                     ('pl', 'Polski'), ('th', 'ไทย')]:
            frame = ttk.Frame(self.translation_notebook)
            self.translation_notebook.add(frame, text=f"{self.translator.get_flag_emoji(lang_code)} {lang_name}")
            
            text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                                   font=('Arial', 10),
                                                   state='disabled')
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.translation_texts[lang_code] = text_widget
        
        # Barre inférieure - Statistiques et exports
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(bottom_frame, text=_('stats.label', words=0, chapters=0),
                                     font=('Arial', 10))
        self.stats_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Separator(bottom_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(bottom_frame, text=_('export.label'), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text=_('export.pdf'), command=lambda: self._export("pdf")).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text=_('export.epub'), command=lambda: self._export("epub")).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text=_('export.docx'), command=lambda: self._export("docx")).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(bottom_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(bottom_frame, text=_('button.generate_cover'), command=self._open_cover_generator).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text=_('button.audiobook'), command=self._open_audiobook_generator).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text=_('button.all_languages'), command=self._export_all_languages).pack(side=tk.LEFT, padx=2)
        ttk.Button(bottom_frame, text=_('button.kdp_package'), command=lambda: self._export("kdp")).pack(side=tk.LEFT, padx=2)
    
    def _on_mode_change(self):
        """Appelé quand le mode change (désactivé en version simplifiée)"""
        pass
    
    def _on_text_change(self, event=None):
        """Appelé quand le texte change"""
        chapter = self.book_manager.get_current_chapter()
        if chapter:
            content = self.editor.get('1.0', tk.END).strip()
            chapter.update_content(content)
            self._update_stats()
    
    def _check_security(self):
        """Vérifie le contenu pour alertes de sécurité (désactivé en version simplifiée)"""
        # Version grand public : pas d'alertes de sécurité
        pass
    
    def _update_chapter_tree(self):
        """Met à jour l'arborescence des chapitres"""
        self.chapter_tree.delete(*self.chapter_tree.get_children())
        
        for i, chapter in enumerate(self.book_manager.chapters):
            # Version simplifiée : icône unique 📚
            self.chapter_tree.insert('', 'end', iid=str(i), 
                                    text=f"📚 Ch{i+1}: {chapter.title}",
                                    values=(chapter.word_count,))
    
    def _on_chapter_select(self, event):
        """Appelé quand un chapitre est sélectionné"""
        selection = self.chapter_tree.selection()
        if selection:
            index = int(selection[0])
            self.book_manager.set_current_chapter(index)
            self._load_chapter_content()
    
    def _load_chapter_content(self):
        """Charge le contenu du chapitre courant"""
        chapter = self.book_manager.get_current_chapter()
        if chapter:
            self.editor.delete('1.0', tk.END)
            self.editor.insert('1.0', chapter.content_fr)
            
            self.chapter_title_label.config(text=f"📝 {chapter.title}")
            
            # Charger les traductions
            for lang, text_widget in self.translation_texts.items():
                text_widget.config(state='normal')
                text_widget.delete('1.0', tk.END)
                translation = chapter.get_translation(lang)
                if translation:
                    text_widget.insert('1.0', translation)
                text_widget.config(state='disabled')
    
    def _add_chapter(self):
        """Ajoute un nouveau chapitre"""
        title = tk.simpledialog.askstring(_('chapter.new_title'), 
                                         _('chapter.new_prompt'),
                                         parent=self.root)
        if title:
            self.book_manager.add_chapter(title, self.current_mode)
            self._update_chapter_tree()
            self._update_stats()
            self.book_manager.save()
    
    def _remove_chapter(self):
        """Supprime le chapitre sélectionné"""
        selection = self.chapter_tree.selection()
        if selection:
            if messagebox.askyesno(_('confirmation'), _('chapter.delete_confirm')):
                index = int(selection[0])
                self.book_manager.remove_chapter(index)
                self._update_chapter_tree()
                self._update_stats()
                self.book_manager.save()
    
    def _translate_all(self):
        """Traduit tous les chapitres"""
        if self.translating:
            messagebox.showinfo(_('translation.in_progress'), _('translation.already_running'))
            return
        
        if not self.translator.available:
            messagebox.showerror(_('error'), _('translation.not_available'))
            return
        
        self.translating = True
        threading.Thread(target=self._do_translate_all, daemon=True).start()
    
    def _do_translate_all(self):
        """Effectue la traduction (dans un thread)"""
        try:
            total = len(self.book_manager.chapters)
            for i, chapter in enumerate(self.book_manager.chapters):
                if not chapter.content_fr.strip():
                    continue
                
                self.root.after(0, lambda i=i, t=total: self.stats_label.config(
                    text=_('translation.translating', current=i+1, total=t)))
                
                for lang in ['en', 'es', 'it', 'ru', 'ja', 'zh', 'hi', 'ar', 'de', 'pt', 'tr', 'ko', 'id', 'vi', 'pl', 'th']:
                    translation = self.translator.translate(chapter.content_fr, lang)
                    chapter.set_translation(lang, translation)
            
            self.root.after(0, lambda: messagebox.showinfo(_('success'), 
                                                           _('translation.success', total=total)))
            self.root.after(0, self._load_chapter_content)
            self.root.after(0, self._update_stats)
            self.book_manager.save()
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(_('error'), _('translation.error', error=str(e))))
        finally:
            self.translating = False
    
    def _translate_selection(self):
        """Traduit le chapitre courant vers des langues sélectionnées"""
        chapter = self.book_manager.get_current_chapter()
        if not chapter:
            messagebox.showwarning(_('attention'), _('translation.no_chapter'))
            return
        
        if not chapter.content_fr.strip():
            messagebox.showwarning(_('attention'), _('translation.empty_chapter'))
            return
        
        if self.translating:
            messagebox.showinfo(_('translation.in_progress'), _('translation.already_running'))
            return
        
        if not self.translator.available:
            messagebox.showerror(_('error'), _('translation.not_available'))
            return
        
        # Fenêtre de sélection des langues (AGRANDIE pour meilleure visibilité)
        selection_window = tk.Toplevel(self.root)
        selection_window.title(_('translation.select_languages'))
        selection_window.geometry("600x750")  # Plus grand pour voir toutes les langues
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        main_frame = ttk.Frame(selection_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=_('translation.select_prompt'),
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text=_('translation.select_hint'),
                 font=('Arial', 9), foreground='gray').pack(pady=5)
        
        # Frame avec scrollbar pour la liste des langues (AMÉLIORÉE)
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        canvas = tk.Canvas(list_frame, height=500)  # Plus haut pour voir toutes les langues
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Liste des langues avec checkboxes
        languages = [
            ('🇬🇧 English', 'en'),
            ('🇪🇸 Español', 'es'),
            ('🇮🇹 Italiano', 'it'),
            ('🇷🇺 Русский', 'ru'),
            ('🇯🇵 日本語', 'ja'),
            ('🇨🇳 中文', 'zh'),
            ('🇮🇳 हिन्दी', 'hi'),
            ('🇸🇦 العربية', 'ar'),
            ('🇩🇪 Deutsch', 'de'),
            ('🇧🇷 Português', 'pt'),
            ('🇹🇷 Türkçe', 'tr'),
            ('🇰🇷 한국어', 'ko'),
            ('🇮🇩 Bahasa Indonesia', 'id'),
            ('🇻🇳 Tiếng Việt', 'vi'),
            ('🇵🇱 Polski', 'pl'),
            ('🇹🇭 ไทย', 'th')
        ]
        
        checkboxes = {}
        for lang_name, lang_code in languages:
            var = tk.BooleanVar()
            # Cocher par défaut si déjà traduit
            if chapter.get_translation(lang_code):
                var.set(True)
            
            cb = ttk.Checkbutton(scrollable_frame, text=lang_name, variable=var,
                                style='TCheckbutton')
            cb.pack(anchor='w', pady=3, padx=10)
            checkboxes[lang_code] = var
        
        # Boutons de sélection rapide
        quick_frame = ttk.Frame(main_frame)
        quick_frame.pack(fill=tk.X, pady=10)
        
        def select_all():
            for var in checkboxes.values():
                var.set(True)
        
        def select_none():
            for var in checkboxes.values():
                var.set(False)
        
        ttk.Button(quick_frame, text=_('translation.select_all'), 
                  command=select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text=_('translation.select_none'), 
                  command=select_none).pack(side=tk.LEFT, padx=5)
        
        # Boutons de validation
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        def start_translation():
            selected_langs = [code for code, var in checkboxes.items() if var.get()]
            
            if not selected_langs:
                messagebox.showwarning(_('attention'), _('translation.at_least_one'))
                return
            
            selection_window.destroy()
            self.translating = True
            threading.Thread(target=self._do_translate_selection, 
                           args=(chapter, selected_langs), 
                           daemon=True).start()
        
        ttk.Button(btn_frame, text=_('translation.start'), 
                  command=start_translation).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text=_('button.cancel'), 
                  command=selection_window.destroy).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def _do_translate_selection(self, chapter, selected_langs):
        """Effectue la traduction sélective (dans un thread)"""
        # Créer la fenêtre de progression
        progress_window = None
        progress_bar = None
        progress_label = None
        
        def create_progress_window():
            nonlocal progress_window, progress_bar, progress_label
            progress_window = tk.Toplevel(self.root)
            progress_window.title(_('translation.in_progress_title'))
            progress_window.geometry("500x200")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            frame = ttk.Frame(progress_window, padding=30)
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text=_('translation.in_progress_message'), 
                     font=('Arial', 12, 'bold')).pack(pady=10)
            
            progress_label = ttk.Label(frame, text=_('translation.starting'), 
                                      font=('Arial', 10))
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(frame, length=400, mode='determinate')
            progress_bar.pack(pady=20)
            progress_bar['maximum'] = 100
            progress_bar['value'] = 0
            
            ttk.Label(frame, text=_('translation.do_not_close'), 
                     font=('Arial', 9), foreground='orange').pack(pady=5)
        
        self.root.after(0, create_progress_window)
        
        try:
            total = len(selected_langs)
            
            # Message de démarrage
            self.root.after(0, lambda: progress_label.config(
                text=_('translation.of_languages', total=total)))
            
            for i, lang in enumerate(selected_langs):
                # Mise à jour de la barre de progression
                progress_percent = int((i / total) * 100)
                self.root.after(0, lambda p=progress_percent: progress_bar.config(value=p))
                
                # Mise à jour du label
                lang_name = _('language.name.' + lang)
                
                self.root.after(0, lambda i=i, t=total, ln=lang_name: progress_label.config(
                    text=_('translation.current', current=i+1, total=t, language=ln)))
                
                # Mise à jour du label de stats en bas aussi
                self.root.after(0, lambda i=i, t=total, l=lang: self.stats_label.config(
                    text=_('translation.current_short', current=i+1, total=t, code=l.upper())))
                
                # TRADUCTION (seulement cette langue !)
                translation = self.translator.translate(chapter.content_fr, lang)
                chapter.set_translation(lang, translation)
            
            # Finaliser la barre à 100%
            self.root.after(0, lambda: progress_bar.config(value=100))
            self.root.after(0, lambda: progress_label.config(
                text=_('translation.completed', total=total)))
            
            # Sauvegarder AVANT de fermer la fenêtre
            self.book_manager.save()
            
            # Attendre un peu pour que l'utilisateur voie le 100%
            import time
            time.sleep(0.5)
            
            # Fermer la fenêtre de progression
            if progress_window:
                self.root.after(0, progress_window.destroy)
            
            # FORCER le rechargement des onglets de traduction
            def refresh_translations():
                chapter_current = self.book_manager.get_current_chapter()
                if chapter_current:
                    for lang, text_widget in self.translation_texts.items():
                        text_widget.config(state='normal')
                        text_widget.delete('1.0', tk.END)
                        translation = chapter_current.get_translation(lang)
                        if translation:
                            text_widget.insert('1.0', translation)
                        text_widget.config(state='disabled')
            
            # Recharger le contenu complet
            self.root.after(100, self._load_chapter_content)
            self.root.after(200, refresh_translations)
            self.root.after(300, self._update_stats)
            
            # Message de succès
            langs_text = ', '.join([l.upper() for l in selected_langs])
            self.root.after(400, lambda: messagebox.showinfo(_('success'), 
                                                           _('translation.success_message', total=total, languages=langs_text)))
            
        except Exception as e:
            if progress_window:
                self.root.after(0, progress_window.destroy)
            self.root.after(0, lambda: messagebox.showerror(_('error'), _('translation.error', error=str(e))))
        finally:
            self.translating = False
    
    def _open_story_coach(self):
        """Ouvre le Story Coach pour enrichir le chapitre"""
        chapter = self.book_manager.get_current_chapter()
        if not chapter:
            messagebox.showwarning(_('attention'), _('story_coach.no_chapter'))
            return
        
        if not chapter.content_fr.strip():
            messagebox.showwarning(
                _('story_coach.empty_chapter'),
                _('story_coach.empty_message')
            )
            return
        
        # Ouvrir le dialogue Story Coach avec callback pour rafraîchir l'affichage
        StoryCoachDialog(self.root, chapter, self.story_coach, 
                        on_success_callback=self._load_chapter_content)
    
    def _open_cover_generator(self):
        """Ouvre le Cover Generator"""
        # Ouvrir le dialogue Cover Generator (PyTorch deja installe !)
        CoverGeneratorDialog(self.root, self.book_manager, self.cover_generator)
    
    def _open_audiobook_generator(self):
        """Ouvre l'Audiobook Generator"""
        # Ouvrir le dialogue Audiobook Generator (gTTS)
        AudiobookDialog(self.root, self.book_manager)
    
    def _check_translation_quality(self):
        """Ouvre le dialogue de vérification qualité"""
        chapter = self.book_manager.get_current_chapter()
        if not chapter:
            messagebox.showwarning(_('attention'), _('quality.no_chapter'))
            return
        
        # Déterminer la langue de l'onglet de traduction actif
        current_tab_index = self.translation_notebook.index(self.translation_notebook.select())
        
        # Map des index aux codes langues (dans le même ordre que la création des onglets)
        lang_map = [
            ('en', _('language.name.en')),
            ('es', _('language.name.es')),
            ('it', _('language.name.it')),
            ('ru', _('language.name.ru')),
            ('ja', _('language.name.ja')),
            ('zh', _('language.name.zh')),
            ('hi', _('language.name.hi')),
            ('ar', _('language.name.ar')),
            ('de', _('language.name.de')),
            ('pt', _('language.name.pt')),
            ('tr', _('language.name.tr')),
            ('ko', _('language.name.ko')),
            ('id', _('language.name.id')),
            ('vi', _('language.name.vi')),
            ('pl', _('language.name.pl')),
            ('th', _('language.name.th'))
        ]
        
        if current_tab_index >= len(lang_map):
            messagebox.showwarning(_('attention'), _('quality.cannot_determine'))
            return
        
        lang_code, lang_name = lang_map[current_tab_index]
        
        # Vérifier si la traduction existe
        translation = chapter.get_translation(lang_code)
        if not translation or not translation.strip():
            messagebox.showwarning(
                _('attention'), 
                _('quality.no_translation', language=lang_name)
            )
            return
        
        # Ouvrir le dialogue de correction
        CorrectionDialog(self.root, chapter, lang_code, lang_name)
    
    def _import_conversations(self):
        """Importe des conversations"""
        files = filedialog.askopenfilenames(
            title=_('import.title'),
            filetypes=[("Fichiers texte", "*.txt"), ("Markdown", "*.md"), ("Tous", "*.*")]
        )
        
        if files:
            report = self.conversation_importer.import_files(list(files))
            messagebox.showinfo(_('success'), 
                              _('import.success', count=len(files), report=report[:200]+"..."))
    
    def _export(self, format_type):
        """Exporte le livre (langue française uniquement)"""
        if not self.book_manager.chapters:
            messagebox.showwarning(_('attention'), _('export.no_chapters'))
            return
        
        export_dir = Path(__file__).parent.parent / "data" / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type == "pdf":
                exporter = PDFExporter()
                filepath = exporter.export(self.book_manager, export_dir, lang='fr')
                messagebox.showinfo(_('success'), _('export.success_pdf', filename=filepath.name))
            
            elif format_type == "epub":
                exporter = EPUBExporter()
                filepath = exporter.export(self.book_manager, export_dir, lang='fr')
                messagebox.showinfo(_('success'), _('export.success_epub', filename=filepath.name))
            
            elif format_type == "docx":
                exporter = DOCXExporter()
                filepath = exporter.export(self.book_manager, export_dir, lang='fr')
                messagebox.showinfo(_('success'), _('export.success_docx', filename=filepath.name))
            
            elif format_type == "kdp":
                # Export complet KDP (17 langues, 3 formats)
                if messagebox.askyesno(_('button.kdp_package'), _('export.kdp_confirm')):
                    self._export_kdp_package()
            
        except Exception as e:
            messagebox.showerror(_('error'), _('export.error', error=str(e)))
    
    def _export_all_languages(self):
        """Exporte le livre dans toutes les langues traduites"""
        if not self.book_manager.chapters:
            messagebox.showwarning(_('attention'), _('export.no_chapters'))
            return
        
        # Demander le format
        format_choice = messagebox.askquestion(_('export.formats'),
                                              _('export.all_format'),
                                              icon='question',
                                              type=messagebox.YESNOCANCEL)
        
        if format_choice is None:
            return
        
        format_map = {
            'yes': ('pdf', PDFExporter),
            'no': ('epub', EPUBExporter),
            'cancel': ('docx', DOCXExporter)
        }
        
        format_type, exporter_class = format_map.get(str(format_choice).lower(), ('pdf', PDFExporter))
        
        export_dir = Path(__file__).parent.parent / "data" / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        languages = {
            'fr': _('language.french'),
            'en': _('language.english'),
            'es': _('language.spanish'),
            'it': _('language.italian'),
            'ru': _('language.russian'),
            'ja': _('language.japanese'),
            'zh': _('language.chinese'),
            'hi': _('language.hindi'),
            'ar': _('language.arabic'),
            'de': _('language.german'),
            'pt': _('language.portuguese'),
            'tr': _('language.turkish'),
            'ko': _('language.korean'),
            'id': _('language.indonesian'),
            'vi': _('language.vietnamese'),
            'pl': _('language.polish'),
            'th': _('language.thai')
        }
        
        try:
            exporter = exporter_class()
            exported_files = []
            
            for lang_code, lang_name in languages.items():
                try:
                    filepath = exporter.export(self.book_manager, export_dir, lang_code)
                    exported_files.append(f"✅ {lang_name}: {filepath.name}")
                except Exception as e:
                    exported_files.append(f"❌ {lang_name}: Erreur - {str(e)[:30]}")
            
            messagebox.showinfo(_('success'),
                              _('export.all_complete', format=format_type.upper(), files="\n".join(exported_files)))
        
        except Exception as e:
            messagebox.showerror(_('error'), _('export.all_error', error=str(e)))
    
    def _export_kdp_package(self):
        """Exporte le package KDP complet"""
        export_dir = Path(__file__).parent.parent / "data" / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Message de progression
        progress_window = tk.Toplevel(self.root)
        progress_window.title(_('export.kdp_in_progress'))
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        progress_label = ttk.Label(progress_window, 
                                   text=_('export.kdp_generating'),
                                   font=('Arial', 10))
        progress_label.pack(expand=True, pady=20)
        
        def do_export():
            try:
                exporter = KDPExporter()
                package_dir = exporter.export(self.book_manager, export_dir)
                
                self.root.after(0, lambda: progress_window.destroy())
                self.root.after(0, lambda: messagebox.showinfo(_('success'),
                                                               _('export.kdp_success', folder=package_dir.name)))
            except Exception as e:
                self.root.after(0, lambda: progress_window.destroy())
                self.root.after(0, lambda: messagebox.showerror(_('error'), 
                                                                _('export.kdp_error', error=str(e))))
        
        # Lancer l'export dans un thread
        threading.Thread(target=do_export, daemon=True).start()
    
    def _update_stats(self):
        """Met à jour les statistiques"""
        total_words = self.book_manager.get_total_words()
        total_chapters = len(self.book_manager.chapters)
        
        self.stats_label.config(
            text=_('stats.label', words=f"{total_words:,}", chapters=total_chapters)
        )
        
        # Mettre à jour auto-save
        elapsed = self.autosave.get_last_save_elapsed()
        if elapsed == 0:
            self.autosave_label.config(text=_('stats.autosave_never'))
        else:
            self.autosave_label.config(text=_('stats.autosave_ago', seconds=elapsed))
    
    def _manual_save(self):
        """Sauvegarde manuelle"""
        if self.book_manager.save():
            messagebox.showinfo(_('success'), _('save.manual_success'))
            self.autosave.last_save_time = 0
            self._update_stats()
    
    def _do_autosave(self):
        """Effectue la sauvegarde automatique"""
        self.book_manager.save()
        self.root.after(0, self._update_stats)
    
    def run(self):
        """Lance l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
    
    def _translate_chapter_title(self):
        """Ouvre la fenêtre de traduction du titre du chapitre"""
        chapter = self.book_manager.get_current_chapter()
        if not chapter:
            messagebox.showwarning(_('attention'), _('translation.no_chapter'))
            return
        
        # Fenêtre de traduction (agrandie pour 16 langues + scrollbar)
        translate_window = tk.Toplevel(self.root)
        translate_window.title(_('translate_title.window_title', title=chapter.title))
        translate_window.geometry("700x750")  # Plus grand pour 16 langues
        translate_window.transient(self.root)
        translate_window.grab_set()
        
        # Frame principal avec scroll
        main_frame = ttk.Frame(translate_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre original (français)
        ttk.Label(main_frame, text=_('translate_title.original'), 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        
        fr_label = ttk.Label(main_frame, text=chapter.title, 
                            font=('Arial', 11), foreground='blue')
        fr_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Séparateur
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, 
                                                             sticky="ew", pady=10)
        
        # Info
        info_label = ttk.Label(main_frame, 
                              text=_('translate_title.info'),
                              font=('Arial', 9), foreground='gray')
        info_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Champs de traduction (16 langues - toutes sauf français)
        languages = [
            ('🇬🇧 English', 'en'),
            ('🇪🇸 Español', 'es'),
            ('🇮🇹 Italiano', 'it'),
            ('🇷🇺 Русский', 'ru'),
            ('🇯🇵 日本語', 'ja'),
            ('🇨🇳 中文', 'zh'),
            ('🇮🇳 हिन्दी', 'hi'),
            ('🇸🇦 العربية', 'ar'),
            ('🇩🇪 Deutsch', 'de'),
            ('🇧🇷 Português', 'pt'),
            ('🇹🇷 Türkçe', 'tr'),
            ('🇰🇷 한국어', 'ko'),
            ('🇮🇩 Bahasa', 'id'),
            ('🇻🇳 Tiếng Việt', 'vi'),
            ('🇵🇱 Polski', 'pl'),
            ('🇹🇭 ไทย', 'th')
        ]
        
        entries = {}
        row = 3
        
        for lang_name, lang_code in languages:
            ttk.Label(main_frame, text=f"{lang_name}:", 
                     font=('Arial', 10)).grid(row=row, column=0, sticky="w", pady=5)
            
            entry = ttk.Entry(main_frame, width=40, font=('Arial', 10))
            entry.insert(0, chapter.get_title_translation(lang_code))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            
            entries[lang_code] = entry
            row += 1
        
        # Configurer le redimensionnement
        main_frame.columnconfigure(1, weight=1)
        
        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=15)
        
        def save_translations():
            for lang_code, entry in entries.items():
                translation = entry.get().strip()
                chapter.set_title_translation(lang_code, translation)
            
            self.book_manager.save()
            messagebox.showinfo(_('success'), 
                              _('translate_title.save_success', title=chapter.title))
            translate_window.destroy()
        
        def clear_all():
            if messagebox.askyesno(_('confirmation'), 
                                  _('translate_title.clear_all')):
                for entry in entries.values():
                    entry.delete(0, tk.END)
        
        ttk.Button(btn_frame, text=_('button.save'), 
                  command=save_translations).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_('button.delete'), 
                  command=clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_('button.cancel'), 
                  command=translate_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _open_settings(self):
        """Ouvre la fenêtre de paramètres"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(_('settings.title'))
        settings_window.geometry("500x200")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre du livre
        ttk.Label(main_frame, text=_('settings.book_title'), font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        title_entry = ttk.Entry(main_frame, width=50)
        title_entry.insert(0, self.book_manager.title)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Auteur
        ttk.Label(main_frame, text=_('settings.author'), font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        author_entry = ttk.Entry(main_frame, width=50)
        author_entry.insert(0, self.book_manager.author)
        author_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Info
        info_label = ttk.Label(main_frame, 
                              text=_('settings.info'),
                              font=('Arial', 9), foreground='gray')
        info_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        def save_settings():
            self.book_manager.title = title_entry.get().strip()
            self.book_manager.author = author_entry.get().strip()
            self.book_manager.save()
            messagebox.showinfo(_('success'), _('settings.save_success'))
            settings_window.destroy()
        
        ttk.Button(btn_frame, text=_('button.save'), command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=_('button.cancel'), command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _change_gui_language(self, lang_code: str):
        """Change la langue de l'interface GUI"""
        i18n = get_i18n()
        if i18n.change_language(lang_code):
            lang_name = i18n.get_language_name(lang_code)
            messagebox.showinfo(
                "Language Changed",
                _('language.changed', language=lang_name)
            )
    
    def _on_close(self):
        """Appele a la fermeture"""
        self.autosave.stop()
        self.book_manager.save()
        self.root.destroy()


# Import pour dialog
import tkinter.simpledialog

