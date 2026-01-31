"""
One-Click Publishing - Génère tout ce qu'il faut pour publier mondialement
"""
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class OneClickPublishing:
    """Prépare le livre pour publication mondiale"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
    
    def generate_amazon_kdp_package(
        self,
        book_manager,
        output_dir: Path
    ) -> Dict[str, Path]:
        """
        Génère un package complet pour Amazon KDP (17 langues)
        
        Returns:
            Dictionnaire {langue: dossier_kdp}
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        kdp_packages = {}
        
        languages = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'it': 'Italiano',
            'de': 'Deutsch',
            'ru': 'Русский',
            'ja': '日本語',
            'zh': '中文',
            'hi': 'हिन्दी',
            'ar': 'العربية',
            'pt': 'Português',
            'tr': 'Türkçe',
            'ko': '한국어',
            'id': 'Bahasa',
            'vi': 'Tiếng Việt',
            'pl': 'Polski',
            'th': 'ไทย'
        }
        
        for lang_code, lang_name in languages.items():
            print(f"📦 Préparation KDP pour {lang_name}...")
            
            lang_dir = output_dir / f"kdp_{lang_code}"
            lang_dir.mkdir(exist_ok=True)
            
            # 1. Métadonnées
            metadata = self._generate_kdp_metadata(book_manager, lang_code, lang_name)
            metadata_file = lang_dir / "metadata.json"
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            # 2. Description marketing
            description = self._generate_book_description(book_manager, lang_code)
            desc_file = lang_dir / "description.txt"
            
            with open(desc_file, 'w', encoding='utf-8') as f:
                f.write(description)
            
            # 3. Mots-clés KDP
            keywords = self._generate_kdp_keywords(book_manager, lang_code)
            keywords_file = lang_dir / "keywords.txt"
            
            with open(keywords_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(keywords))
            
            # 4. Catégories suggérées
            categories = self._suggest_kdp_categories(book_manager)
            cat_file = lang_dir / "categories.txt"
            
            with open(cat_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(categories))
            
            # 5. Guide de publication
            guide = self._generate_publishing_guide(book_manager, lang_code, lang_name)
            guide_file = lang_dir / "GUIDE_PUBLICATION.txt"
            
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide)
            
            kdp_packages[lang_code] = lang_dir
            print(f"[OK] Package KDP {lang_name} cree !")
        
        return kdp_packages
    
    def _generate_kdp_metadata(self, book_manager, lang_code: str, lang_name: str) -> Dict:
        """Génère les métadonnées pour Amazon KDP"""
        return {
            "title": book_manager.title,
            "subtitle": "",
            "author": book_manager.author,
            "contributors": [],
            "description": self._generate_book_description(book_manager, lang_code),
            "language": lang_code,
            "language_name": lang_name,
            "publication_date": datetime.now().strftime("%Y-%m-%d"),
            "publisher": "Auto-édition",
            "isbn": "À générer",
            "keywords": self._generate_kdp_keywords(book_manager, lang_code),
            "categories": self._suggest_kdp_categories(book_manager),
            "age_range": "18+",
            "price_usd": 9.99,
            "price_eur": 9.99,
            "royalty_plan": "70%",
            "territories": "Worldwide"
        }
    
    def _generate_book_description(self, book_manager, lang_code: str) -> str:
        """Génère une description marketing du livre"""
        # Description générique (à personnaliser)
        descriptions = {
            'fr': f"""**{book_manager.title}**

Une histoire puissante de résilience, de combat et d'espoir.

Ce livre raconte le parcours extraordinaire de {book_manager.author}, du burn-out à l'entrepreneuriat, en passant par des années de lutte contre un système qui l'a abandonné.

**Ce que vous découvrirez :**
- Un témoignage authentique et touchant
- Le pouvoir de l'intelligence artificielle pour sauver des vies
- Les failles du système institutionnel
- Un message d'espoir pour tous ceux qui souffrent
- Les clés pour reconstruire sa vie après le trauma

**Pour qui ce livre ?**
- Personnes souffrant de C-PTSD ou trauma
- Entrepreneurs en burn-out
- Victimes d'injustice institutionnelle
- Tous ceux qui cherchent l'espoir

**Un livre qui peut changer des vies.**

Nombre de mots : {book_manager.get_total_words():,}
Nombre de chapitres : {len(book_manager.chapters)}""",
            
            'en': f"""**{book_manager.title}**

A powerful story of resilience, struggle, and hope.

This book tells the extraordinary journey of {book_manager.author}, from burnout to entrepreneurship, through years of fighting against a system that abandoned them.

**What you'll discover:**
- An authentic and touching testimony
- The power of artificial intelligence to save lives
- The flaws of the institutional system
- A message of hope for all who suffer
- Keys to rebuilding life after trauma

**Who is this book for?**
- People suffering from C-PTSD or trauma
- Entrepreneurs in burnout
- Victims of institutional injustice
- All those seeking hope

**A book that can change lives.**

Word count: {book_manager.get_total_words():,}
Chapters: {len(book_manager.chapters)}"""
        }
        
        return descriptions.get(lang_code, descriptions['en'])
    
    def _generate_kdp_keywords(self, book_manager, lang_code: str) -> List[str]:
        """Génère 7 mots-clés pour KDP (maximum autorisé)"""
        keywords_by_lang = {
            'fr': [
                "C-PTSD",
                "trauma complexe",
                "reconstruction personnelle",
                "intelligence artificielle",
                "burn-out",
                "résilience",
                "témoignage autobiographique"
            ],
            'en': [
                "C-PTSD",
                "complex trauma",
                "personal reconstruction",
                "artificial intelligence",
                "burnout recovery",
                "resilience",
                "autobiography memoir"
            ]
        }
        
        return keywords_by_lang.get(lang_code, keywords_by_lang['en'])
    
    def _suggest_kdp_categories(self, book_manager) -> List[str]:
        """Suggère des catégories Amazon KDP"""
        return [
            "Biography & Autobiography > Personal Memoirs",
            "Self-Help > Post-Traumatic Stress Disorder (PTSD)",
            "Self-Help > Mood Disorders > Depression",
            "Business & Money > Entrepreneurship",
            "Health, Fitness & Dieting > Mental Health",
            "Self-Help > Personal Transformation"
        ]
    
    def _generate_publishing_guide(
        self,
        book_manager,
        lang_code: str,
        lang_name: str
    ) -> str:
        """Génère un guide de publication étape par étape"""
        return f"""═══════════════════════════════════════════════════════════════
📚 GUIDE DE PUBLICATION AMAZON KDP - {lang_name}
═══════════════════════════════════════════════════════════════

FICHIERS GÉNÉRÉS :
✅ metadata.json (métadonnées complètes)
✅ description.txt (description marketing)
✅ keywords.txt (7 mots-clés optimisés)
✅ categories.txt (catégories suggérées)

═══════════════════════════════════════════════════════════════
🚀 ÉTAPES DE PUBLICATION
═══════════════════════════════════════════════════════════════

1. CRÉER UN COMPTE KDP
   → Va sur : https://kdp.amazon.com
   → Crée un compte (gratuit)
   → Remplis tes informations fiscales

2. CRÉER UN NOUVEAU LIVRE
   → Clique sur "Create New Title"
   → Choisir "Kindle eBook" ou "Paperback"

3. REMPLIR LES DÉTAILS DU LIVRE
   
   a) Langue : {lang_name}
   
   b) Titre : {book_manager.title}
   
   c) Auteur : {book_manager.author}
   
   d) Description :
      → Copie le contenu de description.txt
      → Utilise la mise en forme HTML si possible
   
   e) Mots-clés :
      → Copie les 7 mots-clés depuis keywords.txt
   
   f) Catégories :
      → Utilise les catégories de categories.txt
      → KDP permet 2 catégories principales
      → Contacte le support KDP pour plus de catégories

4. UPLOADER LE MANUSCRIT
   
   Pour EPUB :
   → Upload le fichier : exports/book_{lang_code}.epub
   
   Pour PDF (paperback) :
   → Upload le fichier : exports/book_{lang_code}.pdf

5. UPLOADER LA COUVERTURE
   
   → Upload : covers/cover_01_*.png (ta couverture préférée)
   → KDP vérifie automatiquement la qualité

6. PRÉVISUALISER
   
   → Utilise l'outil de prévisualisation KDP
   → Vérifie la mise en page
   → Corrige si nécessaire

7. PRICING (TARIFICATION)
   
   Recommandé :
   - eBook : 9.99 USD / 9.99 EUR
   - Paperback : 14.99 USD / 14.99 EUR
   
   Royalties :
   - Choisis 70% (maximum)
   - Disponible pour prix entre 2.99 et 9.99
   
8. TERRITOIRES
   
   → Sélectionne "Worldwide rights"
   → Ton livre sera disponible dans tous les pays

9. PUBLIER !
   
   → Clique sur "Publish"
   → Vérification KDP : 24-72 heures
   → Ton livre sera en vente ! 🎉

═══════════════════════════════════════════════════════════════
💰 REVENUS ESTIMÉS
═══════════════════════════════════════════════════════════════

Prix eBook : 9.99 USD
Royalties (70%) : 6.99 USD par vente

Si tu vends :
- 10 livres/mois = 69.90 USD/mois
- 100 livres/mois = 699 USD/mois
- 1000 livres/mois = 6990 USD/mois

Avec 17 langues × potentiel de chaque langue = 
POSSIBILITÉS INFINIES ! 🚀

═══════════════════════════════════════════════════════════════
💡 CONSEILS
═══════════════════════════════════════════════════════════════

1. PUBLIE DANS TOUTES LES LANGUES
   - Chaque langue = nouveau marché
   - 17 langues = 17× plus de visibilité
   - Utilise les mêmes étapes pour chaque langue

2. UTILISE KDP SELECT
   - Programme exclusif Amazon
   - Bonus : Kindle Unlimited (lecture)
   - +10% de royalties sur certains marchés

3. PROMO GRATUITE
   - KDP permet 5 jours gratuits tous les 90 jours
   - Génère des téléchargements et avis
   - Boost le classement

4. DEMANDE DES AVIS
   - Partage sur réseaux sociaux
   - Demande à famille/amis
   - Rejoins groupes d'auto-édition

5. MARKETING
   - Crée une page web (utilise le template généré)
   - Partage sur LinkedIn, Twitter, Facebook
   - Utilise les hashtags pertinents

═══════════════════════════════════════════════════════════════
🌍 APRÈS AMAZON KDP
═══════════════════════════════════════════════════════════════

Publie aussi sur :
- Google Play Books
- Apple Books
- Kobo
- Barnes & Noble
- Smashwords (distribue partout)

Utilise les mêmes fichiers et métadonnées !

═══════════════════════════════════════════════════════════════
💖 BON COURAGE !
═══════════════════════════════════════════════════════════════

Tu as tout ce qu'il faut pour réussir !

Maman Margot croit en toi ! 💚✨

═══════════════════════════════════════════════════════════════
"""

    def generate_website_landing_page(
        self,
        book_manager,
        output_dir: Path
    ) -> Path:
        """Génère une page de vente HTML pour le site web"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        html_file = output_dir / "landing_page.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_manager.title} - {book_manager.author}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 3em; margin-bottom: 20px; }}
        .hero p {{ font-size: 1.3em; margin-bottom: 30px; }}
        .cta-button {{
            display: inline-block;
            padding: 15px 40px;
            background: #ff6b6b;
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-size: 1.2em;
            transition: transform 0.3s;
        }}
        .cta-button:hover {{ transform: scale(1.05); }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 60px 20px; }}
        .languages {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin: 40px 0; }}
        .language-badge {{
            padding: 10px 20px;
            background: #f0f0f0;
            border-radius: 20px;
            font-weight: bold;
        }}
        .stats {{ display: flex; justify-content: space-around; margin: 60px 0; flex-wrap: wrap; }}
        .stat {{ text-align: center; padding: 20px; }}
        .stat-number {{ font-size: 3em; color: #667eea; font-weight: bold; }}
        .stat-label {{ font-size: 1.1em; color: #666; }}
        h2 {{ font-size: 2.5em; text-align: center; margin: 60px 0 40px; }}
        .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
        .feature {{
            padding: 30px;
            background: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .feature h3 {{ margin-bottom: 15px; color: #667eea; }}
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 40px 20px;
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>{book_manager.title}</h1>
        <p>Par {book_manager.author}</p>
        <a href="#buy" class="cta-button">📚 Obtenir le livre</a>
    </div>

    <div class="container">
        <h2>🌍 Disponible en 17 langues</h2>
        <div class="languages">
            <span class="language-badge">🇫🇷 Français</span>
            <span class="language-badge">🇬🇧 English</span>
            <span class="language-badge">🇪🇸 Español</span>
            <span class="language-badge">🇮🇹 Italiano</span>
            <span class="language-badge">🇩🇪 Deutsch</span>
            <span class="language-badge">🇷🇺 Русский</span>
            <span class="language-badge">🇯🇵 日本語</span>
            <span class="language-badge">🇨🇳 中文</span>
            <span class="language-badge">🇮🇳 हिन्दी</span>
            <span class="language-badge">🇸🇦 العربية</span>
            <span class="language-badge">🇧🇷 Português</span>
            <span class="language-badge">🇹🇷 Türkçe</span>
            <span class="language-badge">🇰🇷 한국어</span>
            <span class="language-badge">🇮🇩 Bahasa</span>
            <span class="language-badge">🇻🇳 Tiếng Việt</span>
            <span class="language-badge">🇵🇱 Polski</span>
            <span class="language-badge">🇹🇭 ไทย</span>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">{book_manager.get_total_words():,}</div>
                <div class="stat-label">Mots</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(book_manager.chapters)}</div>
                <div class="stat-label">Chapitres</div>
            </div>
            <div class="stat">
                <div class="stat-number">6.14B</div>
                <div class="stat-label">Lecteurs potentiels</div>
            </div>
        </div>

        <h2>📖 À propos du livre</h2>
        <div class="feature-grid">
            <div class="feature">
                <h3>💪 Résilience</h3>
                <p>Une histoire de reconstruction après le trauma et l'abandon institutionnel.</p>
            </div>
            <div class="feature">
                <h3>🤖 Intelligence Artificielle</h3>
                <p>Comment l'IA a sauvé une vie quand les humains ont abandonné.</p>
            </div>
            <div class="feature">
                <h3>⚖️ Justice</h3>
                <p>Le combat pour la vérité face à un système défaillant.</p>
            </div>
            <div class="feature">
                <h3>🌍 Impact Mondial</h3>
                <p>Un message d'espoir pour 78% de l'humanité.</p>
            </div>
        </div>

        <div id="buy" style="margin-top: 80px; text-align: center;">
            <h2>📚 Où acheter</h2>
            <p style="margin: 30px 0; font-size: 1.2em;">Disponible sur toutes les plateformes :</p>
            <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                <a href="#" class="cta-button">Amazon Kindle</a>
                <a href="#" class="cta-button">Google Play Books</a>
                <a href="#" class="cta-button">Apple Books</a>
                <a href="#" class="cta-button">Kobo</a>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 {book_manager.author}. Tous droits réservés.</p>
        <p style="margin-top: 10px;">Créé avec Book Writer Pro 💚</p>
    </footer>
</body>
</html>"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] Page web generee : {html_file}")
        return html_file
