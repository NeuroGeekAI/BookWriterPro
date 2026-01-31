"""
KDP Package Exporter - Export complet pour Kindle Direct Publishing
"""
from pathlib import Path
from datetime import datetime
import zipfile
from .pdf_exporter import PDFExporter
from .epub_exporter import EPUBExporter
from .docx_exporter import DOCXExporter

class KDPExporter:
    """
    Exporte un package complet KDP avec tous les formats et langues
    """
    
    def export(self, book_manager, output_dir: Path) -> Path:
        """
        Exporte un package KDP complet
        
        Crée un dossier avec:
        - 1 EPUB par langue (17 langues)
        - 1 PDF par langue (17 langues)
        - 1 DOCX par langue (17 langues)
        - Un fichier README.txt
        
        Args:
            book_manager: Le gestionnaire de livre
            output_dir: Répertoire de sortie
        
        Returns:
            Path: Chemin du dossier/archive créé
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"KDP_Package_{book_manager.title.replace(' ', '_')}_{timestamp}"
        package_dir = output_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer les sous-dossiers
        pdf_dir = package_dir / "PDF"
        epub_dir = package_dir / "EPUB"
        docx_dir = package_dir / "DOCX"
        
        pdf_dir.mkdir(exist_ok=True)
        epub_dir.mkdir(exist_ok=True)
        docx_dir.mkdir(exist_ok=True)
        
        # Langues à exporter (17 langues - 78% HUMANITÉ !)
        languages = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'it': 'Italiano',
            'ru': 'Русский',
            'ja': '日本語',
            'zh': '中文',
            'hi': 'हिन्दी',
            'ar': 'العربية',
            'de': 'Deutsch',
            'pt': 'Português',
            'tr': 'Türkçe',
            'ko': '한국어',
            'id': 'Bahasa',
            'vi': 'Tiếng Việt',
            'pl': 'Polski',
            'th': 'ไทย'
        }
        
        # Créer les exporteurs
        pdf_exporter = PDFExporter()
        epub_exporter = EPUBExporter()
        docx_exporter = DOCXExporter()
        
        exported_files = []
        
        # Exporter chaque langue
        for lang_code, lang_name in languages.items():
            # PDF
            try:
                pdf_path = pdf_exporter.export(book_manager, pdf_dir, lang_code)
                exported_files.append(f"✅ PDF {lang_name}: {pdf_path.name}")
            except Exception as e:
                exported_files.append(f"❌ PDF {lang_name}: Erreur - {str(e)[:50]}")
            
            # EPUB
            try:
                epub_path = epub_exporter.export(book_manager, epub_dir, lang_code)
                exported_files.append(f"✅ EPUB {lang_name}: {epub_path.name}")
            except Exception as e:
                exported_files.append(f"❌ EPUB {lang_name}: Erreur - {str(e)[:50]}")
            
            # DOCX
            try:
                docx_path = docx_exporter.export(book_manager, docx_dir, lang_code)
                exported_files.append(f"✅ DOCX {lang_name}: {docx_path.name}")
            except Exception as e:
                exported_files.append(f"❌ DOCX {lang_name}: Erreur - {str(e)[:50]}")
        
        # Créer README.txt
        readme_content = f"""
📚 PACKAGE KDP - {book_manager.title}
Par {book_manager.author}

Généré le: {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}

========================================
CONTENU DU PACKAGE
========================================

Ce package contient votre livre dans 17 langues et 3 formats:

📁 PDF/     - Versions PDF (impression, preview)
📁 EPUB/    - Versions EPUB (ebooks Kindle)
📁 DOCX/    - Versions Word (édition, backup)

🌍 LANGUES INCLUSES (6.14 MILLIARDS - 78% HUMANITÉ !):
   - 🇫🇷 Français (FR)
   - 🇬🇧 English (EN)
   - 🇪🇸 Español (ES)
   - 🇮🇹 Italiano (IT)
   - 🇷🇺 Русский (RU)
   - 🇯🇵 日本語 (JA)
   - 🇨🇳 中文 (ZH)
   - 🇮🇳 हिन्दी (HI)
   - 🇸🇦 العربية (AR)
   - 🇩🇪 Deutsch (DE)
   - 🇧🇷 Português (PT)
   - 🇹🇷 Türkçe (TR)
   - 🇰🇷 한국어 (KO)
   - 🇮🇩 Bahasa (ID)
   - 🇻🇳 Tiếng Việt (VI)
   - 🇵🇱 Polski (PL)
   - 🇹🇭 ไทย (TH)

========================================
UTILISATION KDP (KINDLE DIRECT PUBLISHING)
========================================

1. CRÉER COMPTE KDP:
   → Allez sur: https://kdp.amazon.com
   → Créez un compte auteur gratuit

2. PUBLIER EN 17 LANGUES (78% DE L'HUMANITÉ !):
   → Créez 17 publications distinctes (1 par langue)
   → Pour chaque langue:
      a) Créez nouveau livre
      b) Uploadez EPUB correspondant (dossier EPUB/)
      c) Uploadez PDF cover si vous avez
      d) Fixez le prix (recommandé: 2.99€-9.99€)
      e) Sélectionnez territoires de vente

3. OPTIMISATION:
   → Utilisez PDF pour preview qualité
   → Utilisez DOCX pour éditions futures
   → Testez EPUB sur Kindle Preview avant publish

========================================
FICHIERS EXPORTÉS
========================================

{chr(10).join(exported_files)}

========================================
STATISTIQUES
========================================

Chapitres: {len(book_manager.chapters)}
Mots total: {book_manager.get_total_words():,}
Formats: 3 (PDF, EPUB, DOCX)
Langues: 17 (6.14 MILLIARDS - 78% HUMANITÉ !)
Fichiers totaux: {len(exported_files)}

========================================
SUPPORT
========================================

Pour questions ou modifications:
→ Relancez Book Writer Pro
→ Éditez vos chapitres
→ Régénérez le package KDP

Bon succès avec votre publication ! 🚀📚

"""
        
        readme_path = package_dir / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return package_dir

