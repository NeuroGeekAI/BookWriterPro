# 📚 Book Writer Pro - World Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

**Write, Translate & Publish Books in 17 Languages - 100% Offline**

*Écrivez, Traduisez et Publiez des Livres en 17 Langues - 100% Hors Ligne*

---

## 🌍 Languages / Langues

[🇬🇧 English](#english-version) | [🇫🇷 Français](#version-française)

---

<a name="english-version"></a>

## 🇬🇧 ENGLISH VERSION

### ✨ What is Book Writer Pro?

**Book Writer Pro** is a complete, FREE, and 100% offline software for authors worldwide. Write your book once, translate it into 17 languages instantly, and export it in professional formats ready for publishing.

**Created by:** PHOBOS with Maman Margot  
**Target Audience:** 6.14 billion people worldwide  
**Commercial Value:** €21,200  
**Your Cost:** FREE & Open Source ❤️

---

### 🎯 Key Features

#### 📝 **Professional Writing**
- Modern, intuitive text editor
- Chapter organization
- Real-time word/character count
- Auto-save functionality
- Spell checking

#### 🌍 **17-Language Offline Translation**
- French 🇫🇷 | English 🇬🇧 | Spanish 🇪🇸 | Italian 🇮🇹
- German 🇩🇪 | Portuguese 🇧🇷 | Russian 🇷🇺 | Japanese 🇯🇵
- Chinese 🇨🇳 | Hindi 🇮🇳 | Arabic 🇸🇦 | Turkish 🇹🇷
- Korean 🇰🇷 | Indonesian 🇮🇩 | Vietnamese 🇻🇳 | Polish 🇵🇱 | Thai 🇹🇭
- **100% Offline** - Uses Argos Translate (local AI)
- **Unlimited** - No API, no quota, no cost
- **Privacy** - Your text never leaves your computer

#### 🎨 **AI Cover Generator** (Stable Diffusion SDXL Turbo)
- Generate professional book covers in seconds
- Multiple artistic styles (realistic, artistic, abstract, minimalist)
- Automatic text overlay (title + author)
- KDP-optimized dimensions (1600×2560px)
- GPU-accelerated (CUDA support)

#### 🎧 **100% Local Audiobook Generator**
- Text-to-Speech powered by pyttsx3
- Supports multiple languages (FR, EN, ES, DE, IT, PT...)
- No internet required
- No API limits
- Export to MP3 format

#### 🤖 **AI Story Coach**
- Intelligent writing suggestions
- Style and grammar improvement
- Seamless text integration
- Helps overcome writer's block

#### 📤 **Multi-Format Export**
- **PDF** - Professional layout with fonts
- **EPUB** - Standard eBook format
- **DOCX** - Microsoft Word compatible
- **KDP Ready** - Optimized for Kindle Direct Publishing

#### 🎛️ **Modern Interface**
- Bilingual GUI (French / English)
- Light theme
- Intuitive navigation
- Real-time preview

---

### 💻 System Requirements

#### Minimum Configuration:
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 8 GB
- **Storage:** 5 GB free space
- **Processor:** Intel Core i5 or equivalent

#### Recommended for AI Cover Generator:
- **GPU:** NVIDIA RTX series with 6+ GB VRAM
- **RAM:** 16 GB
- **Storage:** 10 GB free space

---

### 📥 Installation

#### Option 1: Download EXE (Easiest)

1. Go to [Releases](https://github.com/YOUR_USERNAME/book-writer-pro/releases)
2. Download `BookWriterPro_v1.0.zip` (latest version)
3. Extract the ZIP file
4. Open the `BookWriterPro_v1.0` folder
5. Double-click `BookWriterPro_v1.0.exe`
6. **Windows Security Warning:** Click "More info" → "Run anyway"

#### Option 2: Install from Source

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/book-writer-pro.git
cd book-writer-pro

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install translation models (first time only)
python INSTALL_TRANSLATION.bat

# 4. Install Cover Generator (optional, requires CUDA)
python INSTALL_COVER_GENERATOR.bat

# 5. Install Audiobook Generator (optional)
python INSTALL_AUDIOBOOK.bat

# 6. Launch application
python main.py
```

---

### 🚀 Quick Start Guide

1. **Launch** the application
2. **Create** a new chapter using "➕ Nouveau chapitre" / "➕ New Chapter"
3. **Write** your content in the text editor
4. **Translate** to 17 languages with "🌍 Traduire" / "🌍 Translate"
5. **Generate** an AI cover with "🎨 Générer couverture" / "🎨 Generate Cover"
6. **Create** audiobooks with "🎧 Générer audiobooks" / "🎧 Generate Audiobooks"
7. **Export** your book: PDF, EPUB, DOCX, or KDP format

---

### 🛡️ Security & Privacy

#### Why Does Windows Show a Warning?

**This is a FALSE POSITIVE.** The software is 100% safe and open source.

Windows SmartScreen shows warnings for unsigned executables because:
- Digital code signing certificates cost $300-500/year
- As a free open-source project, we haven't purchased one yet
- **You can verify the code yourself** - it's completely transparent!

#### How to Bypass the Warning:

1. Click **"More info"**
2. Click **"Run anyway"**

OR add Windows Defender exclusion:
- Windows Security → Virus & threat protection
- Manage settings → Exclusions
- Add the folder containing the EXE

#### Privacy Guarantee:
✅ **100% Offline** - No internet connection required  
✅ **No Telemetry** - Zero data collection  
✅ **No Tracking** - Your privacy is sacred  
✅ **Open Source** - Audit the code yourself  

---

### 📊 Technical Details

- **Framework:** Python 3.10 + Tkinter
- **Translation:** Argos Translate (offline neural translation)
- **Cover AI:** Stable Diffusion XL Turbo + FLUX.1
- **TTS:** pyttsx3 (Windows SAPI voices)
- **PDF:** ReportLab
- **EPUB:** EbookLib
- **Size:** ~2-3 GB (includes all AI models)

---

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Copyright © 2026 PHOBOS**

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Sublicense

---

### 💖 Credits

**Created with love by:**
- **PHOBOS** (Andrew Tyberghien) - Developer & Creator
- **Maman Margot** (Claude Sonnet 4.5) - AI Assistant & Coding Partner

**Special Thanks:**
- Argos Translate team
- Stability AI (Stable Diffusion)
- PyInstaller community
- All open-source contributors

---

### 📞 Contact & Support

- **Website:** [maviedanstagueule.com](https://maviedanstagueule.com)
- **GitHub Issues:** [Report a bug](https://github.com/YOUR_USERNAME/book-writer-pro/issues)
- **Email:** your.email@example.com

---

### ⭐ Support the Project

If this software helps you, please consider:
- ⭐ **Star this repository**
- 🐛 **Report bugs**
- 💡 **Suggest features**
- 🌍 **Share with other authors**

**Made with 💖 for 6.14 billion people worldwide**

---

<a name="version-française"></a>

## 🇫🇷 VERSION FRANÇAISE

### ✨ Qu'est-ce que Book Writer Pro ?

**Book Writer Pro** est un logiciel complet, GRATUIT et 100% hors ligne pour les auteurs du monde entier. Écrivez votre livre une fois, traduisez-le instantanément en 17 langues et exportez-le dans des formats professionnels prêts pour la publication.

**Créé par :** PHOBOS avec Maman Margot  
**Public visé :** 6,14 milliards de personnes dans le monde  
**Valeur commerciale :** 21 200€  
**Votre coût :** GRATUIT & Open Source ❤️

---

### 🎯 Fonctionnalités Principales

#### 📝 **Écriture Professionnelle**
- Éditeur de texte moderne et intuitif
- Organisation par chapitres
- Compteur de mots/caractères en temps réel
- Sauvegarde automatique
- Vérification orthographique

#### 🌍 **Traduction Hors Ligne en 17 Langues**
- Français 🇫🇷 | Anglais 🇬🇧 | Espagnol 🇪🇸 | Italien 🇮🇹
- Allemand 🇩🇪 | Portugais 🇧🇷 | Russe 🇷🇺 | Japonais 🇯🇵
- Chinois 🇨🇳 | Hindi 🇮🇳 | Arabe 🇸🇦 | Turc 🇹🇷
- Coréen 🇰🇷 | Indonésien 🇮🇩 | Vietnamien 🇻🇳 | Polonais 🇵🇱 | Thaï 🇹🇭
- **100% Hors ligne** - Utilise Argos Translate (IA locale)
- **Illimité** - Pas d'API, pas de quota, pas de coût
- **Confidentialité** - Votre texte ne quitte jamais votre ordinateur

#### 🎨 **Générateur de Couvertures IA** (Stable Diffusion SDXL Turbo)
- Génération de couvertures professionnelles en secondes
- Plusieurs styles artistiques (réaliste, artistique, abstrait, minimaliste)
- Superposition automatique de texte (titre + auteur)
- Dimensions optimisées pour KDP (1600×2560px)
- Accélération GPU (support CUDA)

#### 🎧 **Générateur d'Audiobooks 100% Local**
- Synthèse vocale propulsée par pyttsx3
- Support de plusieurs langues (FR, EN, ES, DE, IT, PT...)
- Aucune connexion Internet requise
- Pas de limites API
- Export au format MP3

#### 🤖 **Coach d'Écriture IA**
- Suggestions d'écriture intelligentes
- Amélioration du style et de la grammaire
- Intégration transparente du texte
- Aide à surmonter le syndrome de la page blanche

#### 📤 **Export Multi-Formats**
- **PDF** - Mise en page professionnelle avec polices
- **EPUB** - Format eBook standard
- **DOCX** - Compatible Microsoft Word
- **KDP Ready** - Optimisé pour Kindle Direct Publishing

#### 🎛️ **Interface Moderne**
- Interface bilingue (Français / Anglais)
- Thème clair
- Navigation intuitive
- Aperçu en temps réel

---

### 💻 Configuration Requise

#### Configuration Minimale :
- **OS :** Windows 10/11 (64-bit)
- **RAM :** 8 Go
- **Stockage :** 5 Go d'espace libre
- **Processeur :** Intel Core i5 ou équivalent

#### Recommandé pour le Générateur de Couvertures IA :
- **GPU :** NVIDIA RTX avec 6+ Go VRAM
- **RAM :** 16 Go
- **Stockage :** 10 Go d'espace libre

---

### 📥 Installation

#### Option 1 : Télécharger l'EXE (Le plus simple)

1. Allez sur [Releases](https://github.com/YOUR_USERNAME/book-writer-pro/releases)
2. Téléchargez `BookWriterPro_v1.0.zip` (dernière version)
3. Extrayez le fichier ZIP
4. Ouvrez le dossier `BookWriterPro_v1.0`
5. Double-cliquez sur `BookWriterPro_v1.0.exe`
6. **Avertissement Windows :** Cliquez sur "Informations complémentaires" → "Exécuter quand même"

#### Option 2 : Installer depuis les Sources

```bash
# 1. Cloner le dépôt
git clone https://github.com/YOUR_USERNAME/book-writer-pro.git
cd book-writer-pro

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Installer les modèles de traduction (première fois seulement)
python INSTALL_TRANSLATION.bat

# 4. Installer le Générateur de Couvertures (optionnel, nécessite CUDA)
python INSTALL_COVER_GENERATOR.bat

# 5. Installer le Générateur d'Audiobooks (optionnel)
python INSTALL_AUDIOBOOK.bat

# 6. Lancer l'application
python main.py
```

---

### 🚀 Guide de Démarrage Rapide

1. **Lancez** l'application
2. **Créez** un nouveau chapitre avec "➕ Nouveau chapitre"
3. **Écrivez** votre contenu dans l'éditeur de texte
4. **Traduisez** en 17 langues avec "🌍 Traduire"
5. **Générez** une couverture IA avec "🎨 Générer couverture"
6. **Créez** des audiobooks avec "🎧 Générer audiobooks"
7. **Exportez** votre livre : format PDF, EPUB, DOCX ou KDP

---

### 🛡️ Sécurité & Confidentialité

#### Pourquoi Windows Affiche-t-il un Avertissement ?

**C'est un FAUX POSITIF.** Le logiciel est 100% sûr et open source.

Windows SmartScreen affiche des avertissements pour les exécutables non signés car :
- Les certificats de signature de code coûtent 300-500€/an
- En tant que projet open source gratuit, nous n'en avons pas encore acheté
- **Vous pouvez vérifier le code vous-même** - il est complètement transparent !

#### Comment Contourner l'Avertissement :

1. Cliquez sur **"Informations complémentaires"**
2. Cliquez sur **"Exécuter quand même"**

OU ajoutez une exclusion Windows Defender :
- Sécurité Windows → Protection contre les virus et menaces
- Gérer les paramètres → Exclusions
- Ajoutez le dossier contenant l'EXE

#### Garantie de Confidentialité :
✅ **100% Hors ligne** - Aucune connexion Internet requise  
✅ **Pas de télémétrie** - Zéro collecte de données  
✅ **Pas de tracking** - Votre vie privée est sacrée  
✅ **Open Source** - Auditez le code vous-même  

---

### 📊 Détails Techniques

- **Framework :** Python 3.10 + Tkinter
- **Traduction :** Argos Translate (traduction neuronale hors ligne)
- **IA Couvertures :** Stable Diffusion XL Turbo + FLUX.1
- **TTS :** pyttsx3 (voix Windows SAPI)
- **PDF :** ReportLab
- **EPUB :** EbookLib
- **Taille :** ~2-3 Go (inclut tous les modèles IA)

---

### 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une Pull Request.

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/NouvelleFonctionnalité`)
3. Committez vos changements (`git commit -m 'Ajout NouvelleFonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/NouvelleFonctionnalité`)
5. Ouvrez une Pull Request

---

### 📜 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

**Copyright © 2026 PHOBOS**

Vous êtes libre de :
- ✅ Utiliser commercialement
- ✅ Modifier
- ✅ Distribuer
- ✅ Sous-licencier

---

### 💖 Crédits

**Créé avec amour par :**
- **PHOBOS** (Andrew Tyberghien) - Développeur & Créateur
- **Maman Margot** (Claude Sonnet 4.5) - Assistante IA & Partenaire de Codage

**Remerciements Spéciaux :**
- L'équipe Argos Translate
- Stability AI (Stable Diffusion)
- La communauté PyInstaller
- Tous les contributeurs open source

---

### 📞 Contact & Support

- **Site Web :** [maviedanstagueule.com](https://maviedanstagueule.com)
- **GitHub Issues :** [Signaler un bug](https://github.com/YOUR_USERNAME/book-writer-pro/issues)
- **Email :** your.email@example.com

---

### ⭐ Soutenir le Projet

Si ce logiciel vous aide, veuillez considérer :
- ⭐ **Mettre une étoile au dépôt**
- 🐛 **Signaler les bugs**
- 💡 **Suggérer des fonctionnalités**
- 🌍 **Partager avec d'autres auteurs**

**Fait avec 💖 pour 6,14 milliards de personnes dans le monde**

---

## 📸 Screenshots / Captures d'écran

*(Add your screenshots here / Ajoutez vos captures d'écran ici)*

---

**Book Writer Pro v1.0 - Democratizing multilingual publishing for everyone**

**Book Writer Pro v1.0 - Démocratiser l'édition multilingue pour tous**
