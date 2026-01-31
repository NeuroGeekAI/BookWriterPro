# Book Writer Pro - Compilation en EXE
# PowerShell script (plus fiable que .bat pour Unicode)

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📦 BOOK WRITER PRO - Compilation en EXE" -ForegroundColor Green
Write-Host "🌍 Edition Mondiale - 17 langues" -ForegroundColor Yellow
Write-Host "💚 Créé par PHOBOS avec Maman Margot" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Vérifier PyInstaller
Write-Host "⏳ Vérification de PyInstaller..." -ForegroundColor Yellow
$pyinstaller = pip show pyinstaller 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ PyInstaller n'est pas installé." -ForegroundColor Red
    Write-Host "📥 Installation de PyInstaller en cours..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur installation PyInstaller !" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ PyInstaller installé avec succès !" -ForegroundColor Green
} else {
    Write-Host "✅ PyInstaller déjà installé." -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔨 COMPILATION EN COURS..." -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Options de compilation :" -ForegroundColor Yellow
Write-Host "   - Mode : --onefile (un seul fichier EXE)" -ForegroundColor Gray
Write-Host "   - Interface : --windowed (pas de console)" -ForegroundColor Gray
Write-Host "   - Nom : BookWriterPro_v1.0.exe" -ForegroundColor Gray
Write-Host "   - Inclut : data/, fonts/, core/, gui/, exporters/, locales/" -ForegroundColor Gray
Write-Host ""
Write-Host "⏳ Compilation... (peut prendre 15-20 minutes)" -ForegroundColor Yellow
Write-Host ""

# Compilation avec PyInstaller
$result = pyinstaller --noconfirm `
    --onefile `
    --windowed `
    --name "BookWriterPro_v1.0" `
    --add-data "data;data" `
    --add-data "fonts;fonts" `
    --add-data "core;core" `
    --add-data "gui;gui" `
    --add-data "exporters;exporters" `
    --add-data "importers;importers" `
    --add-data "locales;locales" `
    --hidden-import tkinter `
    --hidden-import argostranslate `
    --hidden-import reportlab `
    --hidden-import ebooklib `
    --hidden-import docx `
    --hidden-import PIL `
    --hidden-import pyttsx3 `
    --hidden-import pydub `
    --hidden-import torch `
    --hidden-import diffusers `
    --hidden-import transformers `
    main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host "❌ ERREUR DE COMPILATION !" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Solutions possibles :" -ForegroundColor Yellow
    Write-Host "   1. Vérifiez que tous les modules sont installés" -ForegroundColor Gray
    Write-Host "   2. Relancez ce script" -ForegroundColor Gray
    Write-Host "   3. Consultez le fichier build\BookWriterPro_v1.0\warn.txt" -ForegroundColor Gray
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ COMPILATION RÉUSSIE !" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# Vérifier taille fichier
if (Test-Path "dist\BookWriterPro_v1.0.exe") {
    $fileSize = (Get-Item "dist\BookWriterPro_v1.0.exe").Length / 1MB
    Write-Host "📦 Fichier EXE créé : dist\BookWriterPro_v1.0.exe" -ForegroundColor Green
    Write-Host "📊 Taille : $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Fichier EXE introuvable dans dist\" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 PROCHAINES ÉTAPES :" -ForegroundColor Yellow
Write-Host "   1. Testez l'EXE : dist\BookWriterPro_v1.0.exe" -ForegroundColor Gray
Write-Host "   2. Si ça fonctionne, uploadez sur GitHub Releases" -ForegroundColor Gray
Write-Host "   3. Partagez au monde entier ! 🌍" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 STRUCTURE CRÉÉE :" -ForegroundColor Yellow
Write-Host "   ├─ build\              (fichiers temporaires)" -ForegroundColor Gray
Write-Host "   ├─ dist\               (📦 VOTRE EXE EST ICI !)" -ForegroundColor Green
Write-Host "   │  └─ BookWriterPro_v1.0.exe" -ForegroundColor Cyan
Write-Host "   └─ BookWriterPro_v1.0.spec (config PyInstaller)" -ForegroundColor Gray
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "🎉 SUCCÈS !" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "💖 Bisous de Maman Margot ! Tu es un champion !" -ForegroundColor Magenta
Write-Host ""

pause
