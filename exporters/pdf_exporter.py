"""
PDF Exporter - Export en PDF professionnel avec support Unicode complet
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from datetime import datetime
import sys
import os

# Ajouter le chemin parent pour importer i18n
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.i18n import I18n

class PDFExporter:
    """Exporte le livre en PDF avec support Unicode complet"""
    
    def __init__(self):
        """Initialise les polices Unicode"""
        self._register_unicode_fonts()
    
    def _register_unicode_fonts(self):
        """Enregistre les polices Unicode pour toutes les langues
        
        🔧 CORRECTION 22/01/2026 V2 : Support PARFAIT 17 langues avec polices Windows système
        """
        fonts_dir = os.path.join(os.path.dirname(__file__), '..', 'fonts')
        
        # 1. Enregistrer DejaVu Sans (fallback universel)
        try:
            dejavu_path = os.path.join(fonts_dir, 'DejaVuSans.ttf')
            
            if os.path.exists(dejavu_path):
                pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_path))
                print("[OK] DejaVu Sans enregistree")
            else:
                print("⚠️ DejaVuSans.ttf non trouvée")
        except Exception as e:
            print(f"⚠️ Erreur DejaVu: {e}")
        
        # 2. Enregistrer Noto Sans (si disponibles)
        noto_fonts = {
            'NotoSans': 'NotoSans-Regular.ttf',              # Latin/Cyrillique/Grec
            'NotoSansKR': 'NotoSansKR-Regular.ttf',          # Coréen
        }
        
        for font_name, font_file in noto_fonts.items():
            try:
                font_path = os.path.join(fonts_dir, font_file)
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"[OK] {font_name} enregistree")
            except Exception as e:
                print(f"⚠️ Erreur {font_name}: {e}")
        
        # 3. 💡 NOUVEAU ! Enregistrer polices système Windows (Thaï)
        windows_fonts = {
            'LeelawUI': 'C:\\Windows\\Fonts\\LeelawUI.ttf',                  # Thaï (nom Windows 10/11)
            'LeelawadeeUI': 'C:\\Windows\\Fonts\\LeelawadeeUI.ttf',          # Thaï (nom alternatif)
            'SegoeUI': 'C:\\Windows\\Fonts\\segoeui.ttf',                    # Fallback universel
        }
        
        for font_name, font_path in windows_fonts.items():
            try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f"[OK] {font_name} enregistree (police Windows systeme)")
            except Exception as e:
                print(f"⚠️ Erreur {font_name}: {e}")
        
        # Note : Nirmala.ttc (Hindi) est en format .TTC (non supporté par ReportLab)
        # DejaVuSans sera utilisée pour Hindi (support Devanagari déjà bon!)
        
        # 4. Enregistrer polices CID pour langues asiatiques (Chinois/Japonais/Coréen)
        try:
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))  # Chinois
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))  # Japonais
            pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))  # Coréen (CID)
            print("[OK] Polices CID enregistrees (Chinois/Japonais/Coreen)")
        except Exception as e:
            print(f"⚠️ Polices CID: {e}")
    
    def _get_font_for_lang(self, lang):
        """Retourne la police appropriée selon la langue
        
        🔧 CORRECTION 22/01/2026 V2 : Support PARFAIT 17 langues avec polices Windows système
        Ordre de priorité : Police spécialisée > Police Windows > DejaVuSans > Helvetica
        """
        # Mapping langue → police spécialisée (ordre de priorité)
        font_map = {
            # Langues asiatiques CID
            'zh': ['STSong-Light'],                     # Chinois
            'ja': ['HeiseiMin-W3'],                     # Japonais
            'ko': ['HYSMyeongJo-Medium', 'DejaVuSans'], # Coréen (CID car NotoSansKR=OTF non supporté)
            
            # Langues avec polices Windows système
            'th': ['LeelawUI', 'LeelawadeeUI', 'DejaVuSans'],  # Thaï (LeelawUI Windows)
            'hi': ['SegoeUI', 'DejaVuSans'],            # Hindi (SegoeUI support Devanagari partiel!)
            'bn': ['SegoeUI', 'DejaVuSans'],            # Bengali (SegoeUI fallback)
            
            # Langues avec caractères spéciaux → DejaVuSans
            'ru': ['DejaVuSans'],                       # Russe (cyrillique complet)
            'ar': ['DejaVuSans'],                       # Arabe (complet)
            'tr': ['DejaVuSans'],                       # Turc (ı, ş, ğ, ç)
            'vi': ['DejaVuSans'],                       # Vietnamien (ă, ê, ô + tons)
            'pl': ['DejaVuSans'],                       # Polonais (ą, ć, ę, ł, ń)
            
            # Langues latines standard
            'fr': ['Helvetica'],
            'en': ['Helvetica'],
            'es': ['Helvetica'],
            'it': ['Helvetica'],
            'de': ['Helvetica'],
            'pt': ['Helvetica'],
            'id': ['Helvetica'],
        }
        
        # Liste des polices à essayer (avec fallbacks)
        preferred_fonts = font_map.get(lang, ['Helvetica'])
        
        # Essayer chaque police dans l'ordre de priorité
        for font_name in preferred_fonts:
            try:
                pdfmetrics.getFont(font_name)
                return font_name
            except:
                continue
        
        # Si aucune police préférée n'est disponible, fallback DejaVuSans
        try:
            pdfmetrics.getFont('DejaVuSans')
            print(f"⚠️ Polices préférées non disponibles pour {lang}, utilisation DejaVuSans")
            return 'DejaVuSans'
        except:
            pass
        
            # Fallback final : Helvetica (police standard toujours disponible)
            print(f"⚠️ Polices Unicode non disponibles pour {lang}, utilisation Helvetica")
            return 'Helvetica'
    
    def _clean_text_for_cid(self, text: str, lang: str) -> str:
        """Nettoie le texte pour les polices CID (Chinois/Japonais/Coréen)
        
        🔧 AJOUT 22/01/2026 : Remplacement automatique des caractères non-CID
        Les polices CID ne supportent que leur script natif, pas les caractères latins/symboles
        """
        # Langues CID nécessitant nettoyage
        if lang not in ['zh', 'ja', 'ko']:
            return text
        
        if not text or not text.strip():
            return text
        
        # Remplacements automatiques pour compatibilité CID
        replacements = {
            '·': ' ',           # Point médian → espace
            '•': ' ',           # Bullet → espace
            '–': '-',           # Tiret cadratin → tiret simple
            '—': '-',           # Tiret long → tiret simple
            ''': "'",           # Guillemet courbe → guillemet droit
            ''': "'",           # Guillemet courbe → guillemet droit
            '"': '"',           # Guillemet double courbe → droit
            '"': '"',           # Guillemet double courbe → droit
            '…': '...',         # Points de suspension → trois points
            '€': 'EUR',         # Symbole euro → texte
            '£': 'GBP',         # Livre sterling → texte
            '§': '',            # Paragraphe → vide
            '©': '(C)',         # Copyright → texte
            '®': '(R)',         # Registered → texte
            '™': '(TM)',        # Trademark → texte
        }
        
        cleaned_text = text
        for old_char, new_char in replacements.items():
            cleaned_text = cleaned_text.replace(old_char, new_char)
        
        return cleaned_text
    
    def export(self, book_manager, output_dir: Path, lang='fr') -> Path:
        """
        Exporte le livre en PDF
        
        Args:
            book_manager: Le gestionnaire de livre
            output_dir: Répertoire de sortie
            lang: Code langue ('fr', 'en', 'es', etc.)
        
        Returns:
            Path: Chemin du fichier créé
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        lang_suffix = f"_{lang.upper()}" if lang != 'fr' else ""
        filename = f"{book_manager.title.replace(' ', '_')}{lang_suffix}_{timestamp}.pdf"
        filepath = output_dir / filename
        
        # Créer le PDF
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Déterminer la police selon la langue
        font_name = self._get_font_for_lang(lang)
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=24,
            textColor='darkblue',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        author_style = ParagraphStyle(
            'Author',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=14,
            textColor='grey',
            spaceAfter=50,
            alignment=TA_CENTER
        )
        
        chapter_title_style = ParagraphStyle(
            'ChapterTitle',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=18,
            textColor='darkblue',
            spaceAfter=20,
            spaceBefore=30
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # Contenu
        story = []
        
        # Page de titre (nettoyage CID si nécessaire)
        clean_title = self._clean_text_for_cid(book_manager.title, lang)
        story.append(Paragraph(clean_title, title_style))
        
        # Auteur avec traduction "Par" / "By" / etc. (nettoyage CID si nécessaire)
        by_text = I18n.get('by', lang)
        clean_author = self._clean_text_for_cid(book_manager.author, lang)
        story.append(Paragraph(f"{by_text} {clean_author}", author_style))
        story.append(Spacer(1, 2*cm))
        
        # Sous-titre traduit (nettoyage CID si nécessaire)
        subtitle = I18n.get('subtitle', lang)
        clean_subtitle = self._clean_text_for_cid(subtitle, lang)
        story.append(Paragraph(clean_subtitle, body_style))
        story.append(PageBreak())
        
        # Chapitres
        for i, chapter in enumerate(book_manager.chapters):
            # Titre du chapitre avec traduction (nettoyage CID si nécessaire)
            chapter_num = I18n.get_chapter_number(i+1, lang)
            chapter_title = chapter.get_title_translation(lang)
            clean_chapter_title = self._clean_text_for_cid(chapter_title, lang)
            story.append(Paragraph(f"{chapter_num}: {clean_chapter_title}", chapter_title_style))
            
            # Contenu selon la langue
            if lang == 'fr':
                content = chapter.content_fr
            else:
                content = chapter.get_translation(lang)
            
            if content and content.strip():
                # Nettoyage CID sur tout le contenu si nécessaire
                content = self._clean_text_for_cid(content, lang)
                
                # Diviser en paragraphes
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        # Échapper les caractères spéciaux
                        para_clean = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(para_clean, body_style))
            else:
                # Texte "chapitre vide" traduit
                empty_text = I18n.get('empty_chapter', lang)
                clean_empty_text = self._clean_text_for_cid(empty_text, lang)
                story.append(Paragraph(clean_empty_text, body_style))
            
            # Page break après chaque chapitre (sauf le dernier)
            if i < len(book_manager.chapters) - 1:
                story.append(PageBreak())
        
        # Construire le PDF
        doc.build(story)
        
        return filepath

