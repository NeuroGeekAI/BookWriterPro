"""
EPUB Exporter - Export en format ebook EPUB
"""
from ebooklib import epub
from pathlib import Path
from datetime import datetime
import html
import sys
import os

# Ajouter le chemin parent pour importer i18n
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.i18n import I18n

class EPUBExporter:
    """Exporte le livre en EPUB"""
    
    def export(self, book_manager, output_dir: Path, lang='fr') -> Path:
        """
        Exporte le livre en EPUB
        
        Args:
            book_manager: Le gestionnaire de livre
            output_dir: Répertoire de sortie
            lang: Code langue ('fr', 'en', 'es', etc.)
        
        Returns:
            Path: Chemin du fichier créé
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        lang_suffix = f"_{lang.upper()}" if lang != 'fr' else ""
        filename = f"{book_manager.title.replace(' ', '_')}{lang_suffix}_{timestamp}.epub"
        filepath = output_dir / filename
        
        # Créer le livre EPUB
        book = epub.EpubBook()
        
        # Métadonnées
        book.set_identifier(f'greenseoai{timestamp}')
        book.set_title(book_manager.title)
        book.set_language(lang)
        book.add_author(book_manager.author)
        
        # CSS
        style = '''
        @namespace epub "http://www.idpf.org/2007/ops";
        body {
            font-family: Georgia, serif;
            margin: 5%;
            text-align: justify;
        }
        h1 {
            text-align: center;
            color: #1a1a1a;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        h2 {
            color: #333;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        p {
            text-indent: 1.5em;
            margin: 0.5em 0;
        }
        '''
        
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)
        
        # Page de titre avec traductions
        intro_title = I18n.get('introduction', lang)
        by_text = I18n.get('by', lang)
        subtitle = I18n.get('subtitle', lang)
        
        intro = epub.EpubHtml(
            title=intro_title,
            file_name='intro.xhtml',
            lang=lang
        )
        intro_content = f'''
        <html>
        <head>
            <link rel="stylesheet" href="style/nav.css" type="text/css"/>
        </head>
        <body>
            <h1>{html.escape(book_manager.title)}</h1>
            <p style="text-align: center; font-style: italic;">{html.escape(by_text)} {html.escape(book_manager.author)}</p>
            <p style="text-align: center; margin-top: 2em;">
                {html.escape(subtitle)}
            </p>
        </body>
        </html>
        '''
        intro.content = intro_content
        book.add_item(intro)
        
        # Chapitres
        chapters_epub = [intro]
        
        for i, chapter in enumerate(book_manager.chapters):
            chapter_file = f'chapter_{i+1}.xhtml'
            c = epub.EpubHtml(
                title=chapter.title,
                file_name=chapter_file,
                lang=lang
            )
            
            # Contenu du chapitre selon la langue
            if lang == 'fr':
                content = chapter.content_fr
            else:
                content = chapter.get_translation(lang)
            
            # Texte "chapitre vide" traduit si besoin
            if not content or not content.strip():
                content = I18n.get('empty_chapter', lang)
            
            paragraphs = content.split('\n\n')
            paragraphs_html = ''.join(f'<p>{html.escape(p.strip())}</p>' for p in paragraphs if p.strip())
            
            # Titre du chapitre traduit
            chapter_num = I18n.get_chapter_number(i+1, lang)
            chapter_title = chapter.get_title_translation(lang)
            
            c.content = f'''
            <html>
            <head>
                <link rel="stylesheet" href="style/nav.css" type="text/css"/>
            </head>
            <body>
                <h2>{html.escape(chapter_num)}: {html.escape(chapter_title)}</h2>
                {paragraphs_html}
            </body>
            </html>
            '''
            
            book.add_item(c)
            chapters_epub.append(c)
        
        # Table des matières
        book.toc = tuple(chapters_epub)
        
        # Navigation
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Spine
        book.spine = ['nav'] + chapters_epub
        
        # Écrire le fichier
        epub.write_epub(str(filepath), book, {})
        
        return filepath

