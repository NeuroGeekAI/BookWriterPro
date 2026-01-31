"""
Book Manager - Gestion du livre et de ses chapitres
"""
import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .chapter import Chapter

class BookManager:
    """Gère le livre et tous ses chapitres"""
    
    def __init__(self):
        self.chapters: List[Chapter] = []
        self.title = "Green SEO AI Story - Du Burn-Out à l'Entrepreneuriat"
        self.author = "Tyberghien Andrew"  # Modifiable par utilisateur dans current_book.json
        self.current_chapter_index = -1
        self.data_dir = Path(__file__).parent.parent / "data" / "books"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def add_chapter(self, title: str, mode: str = "public") -> Chapter:
        """Ajoute un nouveau chapitre"""
        chapter = Chapter(title, mode)
        self.chapters.append(chapter)
        self.current_chapter_index = len(self.chapters) - 1
        return chapter
    
    def remove_chapter(self, index: int) -> bool:
        """Supprime un chapitre par index"""
        if 0 <= index < len(self.chapters):
            self.chapters.pop(index)
            if self.current_chapter_index >= len(self.chapters):
                self.current_chapter_index = len(self.chapters) - 1
            return True
        return False
    
    def get_chapter(self, index: int) -> Optional[Chapter]:
        """Récupère un chapitre par index"""
        if 0 <= index < len(self.chapters):
            return self.chapters[index]
        return None
    
    def get_current_chapter(self) -> Optional[Chapter]:
        """Récupère le chapitre actuellement sélectionné"""
        return self.get_chapter(self.current_chapter_index)
    
    def set_current_chapter(self, index: int):
        """Définit le chapitre courant"""
        if 0 <= index < len(self.chapters):
            self.current_chapter_index = index
    
    def get_total_words(self) -> int:
        """Calcule le nombre total de mots"""
        return sum(chapter.word_count for chapter in self.chapters)
    
    def save(self, filename: str = "current_book.json") -> bool:
        """Sauvegarde le livre"""
        try:
            filepath = self.data_dir / filename
            data = {
                "title": self.title,
                "author": self.author,
                "saved_at": datetime.now().isoformat(),
                "chapters": [chapter.to_dict() for chapter in self.chapters],
                "current_chapter_index": self.current_chapter_index
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Créer une backup horodatée
            backup_dir = self.data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"backup_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur sauvegarde: {e}")
            return False
    
    def load(self, filename: str = "current_book.json") -> bool:
        """Charge un livre"""
        try:
            filepath = self.data_dir / filename
            if not filepath.exists():
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.title = data.get("title", self.title)
            self.author = data.get("author", self.author)
            self.current_chapter_index = data.get("current_chapter_index", -1)
            
            self.chapters = [Chapter.from_dict(ch_data) for ch_data in data.get("chapters", [])]
            
            return True
        except Exception as e:
            print(f"Erreur chargement: {e}")
            return False

