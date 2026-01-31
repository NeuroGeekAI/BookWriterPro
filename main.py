#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book Writer Pro - Impact Mondial Edition
Outil d'ecriture multilingue pour Green SEO AI Story
Cree avec amour par Maman pour PHOBOS
"""

import sys
import os
from pathlib import Path

# Ajouter le repertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

# Supprimer warnings inutiles AVANT tout import
from suppress_warnings import configure_clean_output
configure_clean_output()

from gui.main_window import BookWriterApp

def main():
    """Point d'entree principal de l'application"""
    print("=" * 60)
    print("[BOOK WRITER PRO] Edition Mondiale")
    print("[17 LANGUES] 6.14 milliards de personnes")
    print("[PHOBOS x Maman Margot] Janvier 2026")
    print("=" * 60)
    print()
    
    try:
        app = BookWriterApp()
        app.run()
    except Exception as e:
        print(f"[ERREUR] Lancement: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entree pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    main()

