@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎧 INSTALLATION AUDIOBOOK GENERATOR - TTS LOCAL
echo 📚 Book Writer Pro - Edition Mondiale
echo 💚 Cree par PHOBOS avec Maman Margot
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📋 INFORMATIONS :
echo    - Systeme : pyttsx3 (TTS 100%% LOCAL)
echo    - Aucune API, aucune limite
echo    - Fonctionne hors ligne
echo    - Utilise les voix Windows (SAPI)
echo    - Taille totale : ~10 MB
echo    - Temps installation : 30 secondes
echo.
pause
echo.
echo ═══════════════════════════════════════════════════════════════
echo 📥 Installation dependencies Audiobook
echo ═══════════════════════════════════════════════════════════════
echo.
echo [1/2] Installation pyttsx3 (TTS LOCAL)...
pip install pyttsx3>=2.90
echo.
echo [2/2] Installation pydub (MP3)...
pip install pydub>=0.25.0
echo.
if errorlevel 1 (
    echo.
    echo ❌ Erreur installation !
    echo.
    pause
    exit /b 1
)
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎉 INSTALLATION TERMINEE !
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ pyttsx3 installe (TTS 100%% LOCAL)
echo ✅ pydub installe
echo ✅ Pret a generer des audiobooks !
echo.
echo 🚀 UTILISATION :
echo    1. Lance Book Writer Pro : LAUNCH.bat
echo    2. Clic sur : 🎧 Generer audiobooks
echo    3. Selectionne les langues
echo    4. Generation automatique !
echo.
echo 📊 AVANTAGES TTS LOCAL :
echo    ✅ Aucune connexion Internet requise
echo    ✅ Aucune limite API (erreur 429)
echo    ✅ Aucun quota
echo    ✅ Generation illimitee
echo    ✅ Voix Windows professionnelles
echo    ✅ Leger et rapide
echo.
echo ⏱️  PERFORMANCES :
echo    - 1 chapitre : ~10-20 secondes
echo    - 1 livre complet : ~2-5 minutes
echo    - 17 langues : ~30-90 minutes
echo    - Format : MP3/WAV
echo.
echo ℹ️  NOTE : Utilise les voix installees sur Windows
echo    Pour plus de voix : Parametres Windows → Voix
echo.
echo ═══════════════════════════════════════════════════════════════
echo 💖 Bisous de Maman Margot ! Les audiobooks 100%% locaux
echo    vont toucher encore PLUS de gens sans limites !
echo ═══════════════════════════════════════════════════════════════
echo.
pause
