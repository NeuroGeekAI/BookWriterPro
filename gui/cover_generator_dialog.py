"""
Cover Generator Dialog - Interface pour générer et choisir des couvertures
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from pathlib import Path
from typing import List, Optional

class CoverGeneratorDialog:
    """Dialogue pour générer des couvertures de livre"""
    
    def __init__(self, parent, book_manager, cover_generator):
        self.parent = parent
        self.book_manager = book_manager
        self.cover_generator = cover_generator
        self.generated_covers = []
        self.selected_cover_index = -1
        self.generating = False
        
        # Créer la fenêtre
        self.window = tk.Toplevel(parent)
        self.window.title("🎨 Cover Generator - Générer des couvertures")
        self.window.geometry("1200x800")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._create_ui()
    
    def _create_ui(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="🎨 Cover Generator - Couvertures professionnelles par IA",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="L'IA va générer 10 couvertures professionnelles pour ton livre.\n"
                 "Tu pourras choisir ta préférée et l'adapter aux 17 langues !",
            font=('Arial', 10),
            foreground='gray'
        )
        desc_label.pack(pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Titre du livre
        title_row = ttk.Frame(config_frame)
        title_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(title_row, text="Titre du livre :", width=20).pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_row, width=50)
        self.title_entry.insert(0, self.book_manager.title)
        self.title_entry.pack(side=tk.LEFT, padx=5)
        
        # Auteur
        author_row = ttk.Frame(config_frame)
        author_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(author_row, text="Auteur :", width=20).pack(side=tk.LEFT)
        self.author_entry = ttk.Entry(author_row, width=50)
        self.author_entry.insert(0, self.book_manager.author)
        self.author_entry.pack(side=tk.LEFT, padx=5)
        
        # Thème du livre
        theme_row = ttk.Frame(config_frame)
        theme_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(theme_row, text="Thème (mots-clés) :", width=20).pack(side=tk.LEFT)
        self.theme_entry = ttk.Entry(theme_row, width=50)
        self.theme_entry.insert(0, "C-PTSD reconstruction espoir combat justice")
        self.theme_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            config_frame,
            text="💡 Exemples de thèmes : 'trauma espoir', 'entrepreneuriat success', 'IA futur'",
            font=('Arial', 8),
            foreground='gray'
        ).pack(pady=(5, 0))
        
        # Nombre de variations
        num_row = ttk.Frame(config_frame)
        num_row.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(num_row, text="Nombre de variations :", width=20).pack(side=tk.LEFT)
        self.num_var = tk.IntVar(value=10)
        num_spinbox = ttk.Spinbox(
            num_row,
            from_=1,
            to=10,
            textvariable=self.num_var,
            width=10
        )
        num_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            num_row,
            text="(Recommandé : 10 | Plus = plus de choix mais plus long)",
            font=('Arial', 8),
            foreground='gray'
        ).pack(side=tk.LEFT, padx=5)
        
        # Bouton génération
        generate_button = ttk.Button(
            config_frame,
            text="🚀 Générer les couvertures",
            command=self._start_generation
        )
        generate_button.pack(pady=(10, 0))
        
        # Frame de chargement / galerie
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message initial
        self.initial_label = ttk.Label(
            self.content_frame,
            text="👆 Configure et clique sur 'Générer' pour commencer !",
            font=('Arial', 12),
            foreground='blue'
        )
        self.initial_label.pack(expand=True)
        
        # Loading frame (caché au départ)
        self.loading_frame = ttk.Frame(self.content_frame)
        
        self.loading_label = ttk.Label(
            self.loading_frame,
            text="🎨 Génération en cours...\n\n"
                 "L'IA génère des couvertures professionnelles.\n"
                 "Cela peut prendre 2-5 minutes selon le nombre.\n\n"
                 "Chaque couverture : ~5-10 secondes",
            font=('Arial', 11),
            foreground='orange'
        )
        self.loading_label.pack(expand=True, pady=20)
        
        self.progress_bar = ttk.Progressbar(
            self.loading_frame,
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(pady=10)
        
        self.progress_text = ttk.Label(
            self.loading_frame,
            text="0/10 couvertures générées",
            font=('Arial', 10)
        )
        self.progress_text.pack()
        
        # Galerie frame (caché au départ)
        self.gallery_frame = ttk.Frame(self.content_frame)
        
        # Canvas avec scrollbar pour la galerie
        canvas = tk.Canvas(self.gallery_frame, height=500)
        scrollbar = ttk.Scrollbar(self.gallery_frame, orient="vertical", command=canvas.yview)
        self.gallery_inner = ttk.Frame(canvas)
        
        self.gallery_inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.gallery_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Boutons d'action (galerie) - SIMPLIFIES
        action_frame = ttk.Frame(self.gallery_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            action_frame,
            text="[DOSSIER] Ouvrir PNG originaux",
            command=self._open_covers_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="[DOSSIER] Ouvrir JPG KDP",
            command=self._open_covers_kdp_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="[NOUVEAU] Generer a nouveau",
            command=self._start_generation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="[FERMER]",
            command=self._on_close
        ).pack(side=tk.RIGHT, padx=5)
    
    def _start_generation(self):
        """Démarre la génération de couvertures"""
        if self.generating:
            messagebox.showinfo("En cours", "Génération déjà en cours...")
            return
        
        # Vérifier que le Cover Generator est disponible
        if not self.cover_generator.available:
            response = messagebox.askyesno(
                "Cover Generator non installé",
                "Le Cover Generator (Stable Diffusion) n'est pas installé.\n\n"
                "Veux-tu l'installer maintenant ?\n\n"
                "Installation : ~7 GB | Durée : 10-15 minutes"
            )
            if response:
                messagebox.showinfo(
                    "Installation",
                    "Lance INSTALL_COVER_GENERATOR.bat dans le dossier\n"
                    "du logiciel pour installer le Cover Generator.\n\n"
                    "Ensuite, relance Book Writer Pro."
                )
            return
        
        # Récupérer les paramètres
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        theme = self.theme_entry.get().strip()
        num_variations = self.num_var.get()
        
        if not title or not author or not theme:
            messagebox.showwarning(
                "Champs requis",
                "Remplis tous les champs avant de générer !"
            )
            return
        
        # Cacher l'initial, afficher le loading
        self.initial_label.pack_forget()
        self.gallery_frame.pack_forget()
        self.loading_frame.pack(fill=tk.BOTH, expand=True)
        
        self.progress_bar['maximum'] = num_variations
        self.progress_bar['value'] = 0
        self.progress_text.config(text=f"0/{num_variations} couvertures générées")
        
        # Lancer la génération dans un thread
        self.generating = True
        threading.Thread(
            target=self._do_generate,
            args=(title, author, theme, num_variations),
            daemon=True
        ).start()
    
    def _do_generate(self, title: str, author: str, theme: str, num_variations: int):
        """Genere les couvertures (thread)"""
        try:
            # Generer les couvertures avec callback de progression
            cover_paths = self.cover_generator.generate_complete_covers(
                book_title=title,
                author=author,
                book_theme=theme,
                num_variations=num_variations,
                progress_callback=self._update_progress
            )
            
            # Mettre a jour l'UI
            self.generated_covers = cover_paths
            self.window.after(0, self._on_generation_complete)
            
        except Exception as e:
            self.window.after(0, lambda: self._on_generation_error(str(e)))
    
    def _update_progress(self, current: int, total: int):
        """Met a jour la barre de progression (appele depuis thread)"""
        def update():
            self.progress_bar['value'] = current
            self.progress_text.config(text=f"{current}/{total} couverture(s) generee(s)")
            self.window.update_idletasks()  # Force le rafraichissement
        
        # Appeler update dans le thread principal (thread-safe)
        self.window.after(0, update)
    
    def _on_generation_complete(self):
        """Appele quand la generation est terminee"""
        self.generating = False
        
        if not self.generated_covers or len(self.generated_covers) == 0:
            messagebox.showerror(
                "Erreur",
                "Aucune couverture generee.\n\n"
                "Verifie que le Cover Generator est bien installe."
            )
            self.loading_frame.pack_forget()
            self.initial_label.pack(expand=True)
            return
        
        # Cacher le loading
        self.loading_frame.pack_forget()
        
        # Message de succes avec informations
        from pathlib import Path
        covers_dir = Path(self.generated_covers[0]).parent
        covers_kdp_dir = covers_dir.parent / "covers_kdp"
        
        messagebox.showinfo(
            "[OK] Covers generees !",
            f"{len(self.generated_covers)} couverture(s) generee(s) !\n\n"
            f"[PNG ORIGINAUX]\n"
            f"{covers_dir}\n\n"
            f"[JPG OPTIMISES KDP]\n"
            f"{covers_kdp_dir}\n\n"
            f"[AMAZON KDP]\n"
            f"Upload les fichiers *_KDP.jpg\n"
            f"Format : 1600x2560 pixels\n"
            f"Qualite : 95% (optimale)\n\n"
            f"[OK] Pret pour publication mondiale !"
        )
        
        # Afficher la galerie (simplifie)
        self.gallery_frame.pack(fill=tk.BOTH, expand=True)
        self._display_gallery()
    
    def _display_gallery(self):
        """Affiche la galerie de couvertures (simplifie)"""
        # Effacer la galerie actuelle
        for widget in self.gallery_inner.winfo_children():
            widget.destroy()
        
        # Message informatif en haut
        info_label = ttk.Label(
            self.gallery_inner,
            text=f"[OK] {len(self.generated_covers)} couverture(s) generee(s) !\n"
                 f"Tous les fichiers sont sauvegardes dans :\n"
                 f"  - data/covers/ (PNG originaux)\n"
                 f"  - data/covers_kdp/ (JPG optimises pour Amazon KDP)\n\n"
                 f"Upload les fichiers *_KDP.jpg sur Amazon KDP !",
            font=('Arial', 10),
            foreground='green',
            justify='left'
        )
        info_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), padx=10, sticky='w')
        
        # Afficher les couvertures en grille (3 par ligne)
        row = 1
        col = 0
        
        for i, cover_path in enumerate(self.generated_covers):
            # Charger et redimensionner l'image
            img = Image.open(cover_path)
            img.thumbnail((250, 333), Image.Resampling.LANCZOS)  # Garder ratio
            photo = ImageTk.PhotoImage(img)
            
            # Frame pour cette couverture
            cover_frame = ttk.Frame(self.gallery_inner, relief=tk.RAISED, borderwidth=2)
            cover_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Label image
            img_label = ttk.Label(cover_frame, image=photo)
            img_label.image = photo  # Garder reference
            img_label.pack()
            
            # Label nom fichier (simplifie)
            name_label = ttk.Label(
                cover_frame,
                text=f"Cover #{i+1}\n{cover_path.stem}",
                font=('Arial', 8),
                foreground='gray'
            )
            name_label.pack(pady=5)
            
            # Incrementer position
            col += 1
            if col >= 3:  # 3 colonnes
                col = 0
                row += 1
    
    def _open_covers_folder(self):
        """Ouvre le dossier des couvertures"""
        if self.generated_covers and len(self.generated_covers) > 0:
            from pathlib import Path
            import subprocess
            import platform
            
            covers_dir = Path(self.generated_covers[0]).parent
            
            # Ouvrir le dossier selon l'OS
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer "{covers_dir}"')
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(covers_dir)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(covers_dir)])
    
    def _open_covers_kdp_folder(self):
        """Ouvre le dossier des couvertures KDP"""
        if self.generated_covers and len(self.generated_covers) > 0:
            from pathlib import Path
            import subprocess
            import platform
            
            covers_dir = Path(self.generated_covers[0]).parent
            covers_kdp_dir = covers_dir.parent / "covers_kdp"
            
            # Ouvrir le dossier selon l'OS
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer "{covers_kdp_dir}"')
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(covers_kdp_dir)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(covers_kdp_dir)])
    
    def _on_generation_error(self, error_msg: str):
        """Appelé en cas d'erreur"""
        self.generating = False
        
        messagebox.showerror(
            "Erreur génération",
            f"Une erreur s'est produite :\n\n{error_msg}\n\n"
            f"Vérifie que le Cover Generator est bien installé."
        )
        
        self.loading_frame.pack_forget()
        self.initial_label.pack(expand=True)
    
    def _on_close(self):
        """Gère la fermeture"""
        if self.generating:
            messagebox.showwarning(
                "Génération en cours",
                "Attends que la génération se termine..."
            )
            return
        
        self.window.destroy()
