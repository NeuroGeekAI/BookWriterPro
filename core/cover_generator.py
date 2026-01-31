"""
Cover Generator - Génère des couvertures de livre professionnelles avec IA
Utilise Stable Diffusion XL Turbo en local
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import io

class CoverGenerator:
    """Génère des couvertures de livre avec Stable Diffusion"""
    
    def __init__(self):
        self.pipeline = None
        self.available = False
        self._check_availability()
        
    def _check_availability(self):
        """Vérifie si Stable Diffusion est disponible"""
        try:
            import torch
            import diffusers
            
            self.available = True
            print("[OK] Cover Generator disponible !")
            
        except ImportError as e:
            print("⚠️ Cover Generator non installé")
            print("📥 Lancez INSTALL_COVER_GENERATOR.bat pour installer")
            self.available = False
    
    def load_model(self):
        """Charge le modèle Stable Diffusion XL Turbo"""
        if not self.available:
            return False
        
        if self.pipeline is not None:
            return True  # Déjà chargé
        
        try:
            import torch
            from diffusers import AutoPipelineForText2Image
            
            print("⏳ Chargement de Stable Diffusion XL Turbo...")
            print("   (Peut prendre 1-2 minutes la première fois)")
            
            # Charger le pipeline
            self.pipeline = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                torch_dtype=torch.float16,
                variant="fp16"
            )
            
            # Utiliser le GPU si disponible
            if torch.cuda.is_available():
                self.pipeline.to("cuda")
                print("[GPU] Utilisation du GPU (CUDA)")
            else:
                print("ℹ️  Utilisation du CPU (plus lent)")
            
            print("[OK] Stable Diffusion XL Turbo charge !")
            return True
            
        except Exception as e:
            print(f"[ERREUR] Chargement modele : {e}")
            self.pipeline = None
            return False
    
    def generate_cover(
        self,
        book_title: str,
        book_theme: str,
        style: str = "professional",
        num_images: int = 1
    ) -> List[Image.Image]:
        """
        Génère des couvertures de livre
        
        Args:
            book_title: Titre du livre
            book_theme: Thème (ex: "C-PTSD reconstruction espoir")
            style: Style ("professional", "artistic", "minimal", "emotional")
            num_images: Nombre de variations à générer (1-10)
            
        Returns:
            Liste d'images PIL
        """
        if not self.available or not self.load_model():
            return []
        
        # Créer le prompt
        prompt = self._create_cover_prompt(book_title, book_theme, style)
        
        images = []
        
        try:
            import torch
            
            print(f"[COVER] Generation de {num_images} couverture(s)...")
            print(f"   Thème : {book_theme}")
            print(f"   Style : {style}")
            
            for i in range(num_images):
                print(f"   Generation {i+1}/{num_images}...")
                
                # Generer l'image
                result = self.pipeline(
                    prompt=prompt,
                    num_inference_steps=1,  # SDXL Turbo = 1 step only
                    guidance_scale=0.0,  # SDXL Turbo n'utilise pas CFG
                    height=1024,
                    width=768  # Format livre standard
                )
                
                images.append(result.images[0])
                print(f"   [OK] Image {i+1} generee !")
                
                # IMPORTANT : Vider le cache GPU apres chaque generation
                # Evite saturation memoire au-dela de 5 images
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    torch.cuda.synchronize()
            
            return images
            
        except Exception as e:
            print(f"[ERREUR] Generation : {e}")
            return []
    
    def _create_cover_prompt(self, title: str, theme: str, style: str) -> str:
        """Crée le prompt pour Stable Diffusion"""
        
        style_prompts = {
            "professional": "professional book cover design, modern typography, clean layout, high quality, photorealistic",
            "artistic": "artistic book cover, painting style, expressive, creative, beautiful colors",
            "minimal": "minimalist book cover, simple, elegant, clean design, subtle colors",
            "emotional": "emotional book cover, touching, powerful imagery, deep feelings, inspiring"
        }
        
        style_text = style_prompts.get(style, style_prompts["professional"])
        
        # Analyser le thème pour extraire des concepts visuels
        visual_concepts = self._extract_visual_concepts(theme)
        
        prompt = f"{visual_concepts}, {style_text}, book cover, centered composition, professional quality, detailed, 8k"
        
        # Negative prompt (ce qu'on ne veut PAS)
        negative_prompt = "text, words, letters, title, ugly, blurry, low quality, watermark, signature, frame, border"
        
        return prompt
    
    def _extract_visual_concepts(self, theme: str) -> str:
        """
        Extrait des concepts visuels du theme
        AMELIORE : Garde les mots originaux + enrichit avec dictionnaire
        """
        
        # Dictionnaire de mots-cles → concepts visuels SUPPLEMENTAIRES
        theme_to_visual_enrichment = {
            "c-ptsd": "broken chains, light breaking through darkness",
            "trauma": "stormy sky with sun rays, transformation",
            "reconstruction": "phoenix rising from ashes, rebirth",
            "espoir": "sunrise, horizon, hope",
            "hope": "sunrise, bright light, optimism",
            "abandon": "lone figure, misty landscape",
            "justice": "balanced scales, law, courthouse",
            "combat": "warrior, strength, determination",
            "fight": "power, courage, battle",
            "ia": "artificial intelligence, neural network, circuits",
            "ai": "technology, digital, futuristic",
            "burnout": "exhausted, darkness, recovery",
            "entrepreneuriat": "business, success, growth",
            "entrepreneurship": "innovation, leadership, vision",
            "dragon": "majestic dragon, mythical creature, fantasy",
            "green": "nature, emerald, forest green color",
            "phoenix": "phoenix bird, fire, rebirth",
            "ocean": "sea, waves, water",
            "mountain": "mountain peak, summit, landscape",
            "star": "stars, celestial, night sky",
            "light": "radiant light, illumination, brightness",
            "dark": "darkness, shadows, mystery"
        }
        
        theme_lower = theme.lower()
        
        # 1. TOUJOURS garder le theme original comme base
        visual_concepts = [theme]
        
        # 2. Enrichir avec elements du dictionnaire (max 2)
        enrichments = []
        for keyword, enrichment in theme_to_visual_enrichment.items():
            if keyword in theme_lower:
                enrichments.append(enrichment)
                if len(enrichments) >= 2:  # Max 2 enrichissements
                    break
        
        # 3. Construire le prompt final
        if enrichments:
            # Theme original + enrichissements
            return f"{theme}, {', '.join(enrichments)}, epic, detailed, vibrant colors"
        else:
            # Theme original seul + descripteurs generiques
            return f"{theme}, epic, inspirational, powerful, detailed, vibrant colors"
    
    def add_text_overlay(
        self,
        image: Image.Image,
        title: str,
        author: str,
        title_color: tuple = (255, 255, 255),
        author_color: tuple = (200, 200, 200)
    ) -> Image.Image:
        """
        Ajoute le titre et l'auteur sur la couverture
        AMELIORE : Taille adaptative + multiligne + meilleur positionnement
        
        Args:
            image: Image PIL de base
            title: Titre du livre
            author: Nom de l'auteur
            title_color: Couleur du titre (R, G, B)
            author_color: Couleur de l'auteur (R, G, B)
            
        Returns:
            Image PIL avec texte
        """
        # Copier l'image pour ne pas modifier l'original
        img = image.copy()
        draw = ImageDraw.Draw(img)
        
        width, height = img.size
        
        # === TITRE ADAPTATIF ===
        # Determiner la taille de police optimale en fonction de la longueur
        title_len = len(title)
        
        if title_len <= 20:
            title_size = 70  # Titre court : grosse police
        elif title_len <= 35:
            title_size = 55  # Titre moyen
        elif title_len <= 50:
            title_size = 45  # Titre long
        else:
            title_size = 35  # Titre tres long
        
        try:
            # Essayer d'utiliser Arial Bold pour le titre
            title_font = ImageFont.truetype("arialbd.ttf", title_size)
        except:
            try:
                title_font = ImageFont.truetype("arial.ttf", title_size)
            except:
                # Fallback
                title_font = ImageFont.load_default()
        
        # Decouper le titre en plusieurs lignes si trop long
        max_title_width = width - 80  # Marges de 40px de chaque cote
        title_lines = self._wrap_text(title, title_font, max_title_width, draw)
        
        # Calculer la hauteur totale du titre multiligne
        title_total_height = 0
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            title_total_height += (bbox[3] - bbox[1]) + 10  # +10 pour l'espacement
        
        # Position de depart (haut, centre, avec marge)
        title_y = height // 8
        
        # Dessiner chaque ligne du titre
        for line in title_lines:
            # Centrer cette ligne
            bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = bbox[2] - bbox[0]
            line_x = (width - line_width) // 2
            
            # Contour noir epais pour lisibilite
            for offset in [(-3, -3), (-3, 3), (3, -3), (3, 3), (-2, 0), (2, 0), (0, -2), (0, 2)]:
                draw.text(
                    (line_x + offset[0], title_y + offset[1]),
                    line,
                    font=title_font,
                    fill=(0, 0, 0)
                )
            
            # Dessiner la ligne du titre
            draw.text((line_x, title_y), line, font=title_font, fill=title_color)
            
            # Avancer pour la prochaine ligne
            title_y += (bbox[3] - bbox[1]) + 10
        
        # === AUTEUR ===
        # Taille adaptative pour l'auteur aussi
        author_len = len(author)
        
        if author_len <= 20:
            author_size = 35
        else:
            author_size = 28
        
        try:
            author_font = ImageFont.truetype("arial.ttf", author_size)
        except:
            author_font = ImageFont.load_default()
        
        # Calculer la position de l'auteur (bas, centre)
        author_bbox = draw.textbbox((0, 0), author, font=author_font)
        author_width = author_bbox[2] - author_bbox[0]
        author_height = author_bbox[3] - author_bbox[1]
        author_x = (width - author_width) // 2
        author_y = height - height // 7
        
        # Contour noir
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text(
                (author_x + offset[0], author_y + offset[1]),
                author,
                font=author_font,
                fill=(0, 0, 0)
            )
        
        # Dessiner l'auteur
        draw.text((author_x, author_y), author, font=author_font, fill=author_color)
        
        return img
    
    def _wrap_text(self, text: str, font, max_width: int, draw) -> list:
        """
        Decoupe le texte en plusieurs lignes pour respecter la largeur max
        
        Args:
            text: Texte a decouper
            font: Police utilisee
            max_width: Largeur maximale en pixels
            draw: Objet ImageDraw pour mesurer le texte
            
        Returns:
            Liste de lignes de texte
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Tester si on peut ajouter ce mot a la ligne actuelle
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                # Le mot rentre : l'ajouter
                current_line.append(word)
            else:
                # Le mot ne rentre pas : nouvelle ligne
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Cas special : un seul mot trop long
                    lines.append(word)
        
        # Ajouter la derniere ligne
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
    
    def generate_complete_covers(
        self,
        book_title: str,
        author: str,
        book_theme: str,
        num_variations: int = 10,
        output_dir: Optional[Path] = None,
        progress_callback = None
    ) -> List[Path]:
        """
        Génère des couvertures complètes (image + texte) et les sauvegarde
        
        Args:
            book_title: Titre du livre
            author: Nom de l'auteur
            book_theme: Thème du livre
            num_variations: Nombre de variations (max 10)
            output_dir: Dossier de sortie (défaut: data/covers/)
            
        Returns:
            Liste des chemins vers les fichiers générés
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "data" / "covers"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generer les images de base (sans texte)
        # CORRECTION : Distribution intelligente entre styles
        styles = ["professional", "emotional", "artistic", "minimal"]
        
        # Calculer combien d'images par style (minimum 1 si demande)
        if num_variations >= len(styles):
            # Cas normal : distribuer equitablement
            images_per_style = num_variations // len(styles)
            remaining = num_variations % len(styles)
        else:
            # Cas < 4 images : 1 image par style jusqu'a epuisement
            images_per_style = 0
            remaining = num_variations
        
        saved_files = []
        saved_files_kdp = []
        cover_index = 1
        
        # Dossier KDP
        output_dir_kdp = output_dir.parent / "covers_kdp"
        output_dir_kdp.mkdir(parents=True, exist_ok=True)
        
        for style_idx, style in enumerate(styles):
            # Determiner combien d'images pour ce style
            if images_per_style > 0:
                num_for_this_style = images_per_style
                # Distribuer le reste sur les premiers styles
                if style_idx < remaining:
                    num_for_this_style += 1
            else:
                # Cas < 4 images : 1 image par style jusqu'a epuisement
                if style_idx < remaining:
                    num_for_this_style = 1
                else:
                    num_for_this_style = 0
            
            if num_for_this_style == 0:
                continue  # Passer ce style
            
            print(f"\n[GENERATION] Style '{style}' - {num_for_this_style} image(s)")
            
            base_images = self.generate_cover(
                book_title=book_title,
                book_theme=book_theme,
                style=style,
                num_images=num_for_this_style
            )
            
            # Ajouter le texte sur chaque image
            for base_img in base_images:
                # Creer la couverture finale avec texte
                final_cover = self.add_text_overlay(
                    base_img,
                    book_title,
                    author
                )
                
                # Sauvegarder PNG original (768x1024)
                filename = f"cover_{cover_index:02d}_{style}.png"
                filepath = output_dir / filename
                final_cover.save(filepath, "PNG", dpi=(300, 300))
                saved_files.append(filepath)
                print(f"   [OK] Original PNG : {filename}")
                
                # OPTIMISATION AUTOMATIQUE KDP (1600x2560 JPG)
                try:
                    # Redimensionner a 1600x2560 (format KDP optimal)
                    cover_kdp = final_cover.resize(
                        (1600, 2560),
                        Image.Resampling.LANCZOS
                    )
                    
                    # Convertir en RGB (necessaire pour JPG)
                    if cover_kdp.mode == 'RGBA':
                        background = Image.new('RGB', cover_kdp.size, (255, 255, 255))
                        background.paste(cover_kdp, mask=cover_kdp.split()[3])
                        cover_kdp = background
                    elif cover_kdp.mode != 'RGB':
                        cover_kdp = cover_kdp.convert('RGB')
                    
                    # Sauvegarder JPG optimise KDP
                    filename_kdp = f"cover_{cover_index:02d}_{style}_KDP.jpg"
                    filepath_kdp = output_dir_kdp / filename_kdp
                    cover_kdp.save(
                        filepath_kdp,
                        "JPEG",
                        quality=95,
                        optimize=True,
                        dpi=(300, 300)
                    )
                    saved_files_kdp.append(filepath_kdp)
                    print(f"   [OK] KDP JPG : {filename_kdp} (1600x2560)")
                    
                except Exception as e:
                    print(f"   [!] Erreur optimisation KDP : {e}")
                
                # Notifier la progression (callback GUI)
                if progress_callback:
                    progress_callback(cover_index, num_variations)
                
                cover_index += 1
        
        print(f"\n[TERMINE] {len(saved_files)} cover(s) generee(s) !")
        print(f"[KDP] {len(saved_files_kdp)} cover(s) optimisee(s) pour Amazon KDP !")
        print(f"\n[DOSSIERS]")
        print(f"   PNG originaux : {output_dir}")
        print(f"   JPG KDP (1600x2560) : {output_dir_kdp}")
        
        return saved_files
    
    def unload_model(self):
        """Décharge le modèle de la mémoire (libère VRAM)"""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
            
            # Libérer la VRAM
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except:
                pass
            
            print("💾 Stable Diffusion déchargé de la mémoire")
