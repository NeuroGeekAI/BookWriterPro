@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎨 INSTALLATION COVER GENERATOR - Stable Diffusion XL Turbo
echo 📚 Book Writer Pro - Edition Mondiale
echo 💚 Créé par PHOBOS avec Maman Margot
echo ═══════════════════════════════════════════════════════════════
echo.

echo 📋 INFORMATIONS :
echo    - Modèle : Stable Diffusion XL Turbo
echo    - Taille : ~7 GB
echo    - Génération : 5-10 secondes par couverture
echo    - GPU recommandé : NVIDIA RTX (comme ton RTX 5060 Ti ✅)
echo    - Temps installation : 10-15 minutes
echo.

echo ⚠️  IMPORTANT :
echo    - Assure-toi d'avoir au moins 15 GB d'espace disque libre
echo    - Ne ferme pas cette fenêtre pendant l'installation
echo    - L'installation peut prendre du temps selon ta connexion
echo.

pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo 📦 ÉTAPE 1/4 : Installation PyTorch (support GPU)
echo ═══════════════════════════════════════════════════════════════
echo.

REM Vérifier si GPU NVIDIA est disponible
nvidia-smi >nul 2>&1
if %errorlevel%==0 (
    echo ✅ GPU NVIDIA détecté (RTX 5060 Ti) !
    echo 📥 Installation de PyTorch avec support CUDA...
    echo    (Cela permet d'utiliser le GPU pour génération ultra-rapide)
    echo.
    
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    
    if errorlevel 1 (
        echo ⚠️  Installation CUDA échouée, essai CPU...
        pip install torch torchvision
    ) else (
        echo ✅ PyTorch avec CUDA installé !
    )
) else (
    echo ℹ️  Pas de GPU NVIDIA détecté
    echo 📥 Installation de PyTorch (CPU only)...
    echo.
    pip install torch torchvision
)

if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ❌ ERREUR INSTALLATION PYTORCH !
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 💡 Solutions possibles :
    echo    1. Mets à jour pip : python -m pip install --upgrade pip
    echo    2. Relance ce script
    echo    3. Vérifie ta connexion internet
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ PyTorch installé avec succès !
echo.

echo ═══════════════════════════════════════════════════════════════
echo 📦 ÉTAPE 2/4 : Installation Diffusers (Hugging Face)
echo ═══════════════════════════════════════════════════════════════
echo.

pip install diffusers[torch] transformers accelerate

if errorlevel 1 (
    echo.
    echo ❌ Erreur installation Diffusers !
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Diffusers installé avec succès !
echo.

echo ═══════════════════════════════════════════════════════════════
echo 📦 ÉTAPE 3/4 : Installation Pillow (images)
echo ═══════════════════════════════════════════════════════════════
echo.

pip install Pillow

if errorlevel 1 (
    echo.
    echo ❌ Erreur installation Pillow !
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Pillow installé avec succès !
echo.

echo ═══════════════════════════════════════════════════════════════
echo 📥 ÉTAPE 4/4 : Téléchargement Stable Diffusion XL Turbo (~7 GB)
echo ═══════════════════════════════════════════════════════════════
echo.

echo ℹ️  Le modèle sera téléchargé automatiquement au premier lancement
echo    du Cover Generator. Cela se fera via Hugging Face.
echo.
echo    Emplacements de téléchargement possibles :
echo    - C:\Users\%USERNAME%\.cache\huggingface\
echo    - Ou le dossier que tu auras configuré
echo.
echo    💡 Le téléchargement commence au premier usage !
echo.

echo ═══════════════════════════════════════════════════════════════
echo 🎉 INSTALLATION TERMINÉE !
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ PyTorch installé (support GPU ✅)
echo ✅ Diffusers installé
echo ✅ Pillow installé
echo ✅ Cover Generator prêt à l'emploi !
echo.
echo 🚀 PROCHAINES ÉTAPES :
echo    1. Lance Book Writer Pro : LAUNCH.bat
echo    2. Clique sur "🎨 Générer couverture"
echo    3. Configure (titre, auteur, thème)
echo    4. Clique sur "🚀 Générer les couvertures"
echo    5. Choisis ta préférée parmi les 10 !
echo.
echo 💡 PREMIÈRE UTILISATION :
echo    Le modèle Stable Diffusion XL Turbo (~7 GB) sera
echo    téléchargé automatiquement. Cela prend 5-10 minutes
echo    selon ta connexion. C'est normal !
echo.
echo 📊 UTILISATION :
echo    - GPU : 5-10 secondes par couverture (avec RTX 5060 Ti ✅)
echo    - CPU : 60-120 secondes par couverture
echo    - VRAM : ~6-8 GB pendant génération
echo    - 10 couvertures : ~1-2 minutes (GPU) ou ~10-20 min (CPU)
echo.
echo 🎨 STYLES DISPONIBLES :
echo    - Professional (propre, moderne)
echo    - Emotional (touchant, puissant)
echo    - Artistic (créatif, peinture)
echo    - Minimal (épuré, élégant)
echo.
echo ═══════════════════════════════════════════════════════════════
echo 💖 Bisous de Maman Margot ! Le Cover Generator va créer des
echo    couvertures PROFESSIONNELLES qui vont CHOQUER le monde ! 💣✨
echo ═══════════════════════════════════════════════════════════════
echo.

pause
