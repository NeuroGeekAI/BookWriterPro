"""
Conversation Importer - Importe et analyse les conversations
"""
from pathlib import Path
from typing import List
from datetime import datetime
import re

class ConversationImporter:
    """Importe des conversations depuis fichiers texte"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "conversations"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def import_files(self, filepaths: List[str]) -> str:
        """Importe plusieurs fichiers de conversation"""
        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("📥 RAPPORT D'IMPORT CONVERSATIONS")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        all_content = []
        
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                filename = Path(filepath).name
                all_content.append(f"\n\n### FICHIER: {filename} ###\n\n{content}")
                
                # Analyser le contenu
                word_count = len(content.split())
                dates = self._extract_dates(content)
                themes = self._extract_themes(content)
                
                report_lines.append(f"✅ {filename}")
                report_lines.append(f"   • {word_count} mots")
                if dates:
                    report_lines.append(f"   • Dates trouvées: {len(dates)}")
                if themes:
                    report_lines.append(f"   • Thèmes: {', '.join(themes[:3])}")
                report_lines.append("")
                
            except Exception as e:
                report_lines.append(f"❌ Erreur {Path(filepath).name}: {e}")
                report_lines.append("")
        
        # Sauvegarder tout le contenu importé
        if all_content:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            import_file = self.data_dir / f"import_{timestamp}.txt"
            
            with open(import_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(all_content))
            
            report_lines.append(f"💾 Sauvegardé dans: {import_file.name}")
        
        report_lines.append("")
        report_lines.append("=" * 50)
        
        # Suggestions de chapitres
        all_text = "\n".join(all_content)
        themes = self._extract_themes(all_text)
        
        if themes:
            report_lines.append("")
            report_lines.append("💡 SUGGESTIONS DE CHAPITRES:")
            for theme in themes[:10]:
                report_lines.append(f"   • {theme}")
        
        return "\n".join(report_lines)
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extrait les dates du texte"""
        dates = []
        # Format DD/MM/YYYY ou DD-MM-YYYY
        pattern1 = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        dates.extend(re.findall(pattern1, text))
        
        # Années
        pattern2 = r'\b(19|20)\d{2}\b'
        dates.extend(re.findall(pattern2, text))
        
        return list(set(dates))
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extrait les thèmes principaux"""
        themes = []
        
        keywords = {
            "Enfance": [r'\benfance\b', r'\benfant\b', r'\bpetit\b', r'\bjeune\b'],
            "Adolescence": [r'\badolescence\b', r'\bado\b', r'\bcollège\b', r'\blycée\b'],
            "Travail - Pâtisserie": [r'\bpâtisserie\b', r'\bpâtissier\b', r'\bCAP\b', r'\bgâteau\b'],
            "Travail - Plongeur": [r'\bplongeur\b', r'\bCDI\b', r'\brestaurant\b', r'\bvaisselle\b'],
            "Travail - 9 ans": [r'\b9 ans\b', r'\bneuf ans\b'],
            "Burn-out": [r'\bburn.?out\b', r'\bépuisé\b', r'\bfatigué\b', r'\bépuisement\b'],
            "Diagnostic": [r'\bdiagnostic\b', r'\bschizophrénie\b', r'\bpsychiatre\b', r'\btrauma\b'],
            "Formation": [r'\bOpenClassrooms\b', r'\bformation\b', r'\bapprentissage\b'],
            "Entrepreneuriat": [r'\bentrepreneur\b', r'\bmicro.?entrepreneur\b', r'\bentreprise\b'],
            "Green SEO AI": [r'\bGreen SEO\b', r'\bSEO\b', r'\bIA\b', r'\bintelligence artificielle\b'],
            "Maire/SNCF": [r'\bmaire\b', r'\bSNCF\b', r'\bsurveillance\b', r'\bharcèlement\b'],
            "Combat juridique": [r'\bavocat\b', r'\bjustice\b', r'\bdroit\b', r'\bplainte\b']
        }
        
        for theme, patterns in keywords.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    themes.append(theme)
                    break
        
        return list(set(themes))

