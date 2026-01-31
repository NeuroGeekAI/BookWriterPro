@echo off
echo ============================================================
echo  BOOK WRITER PRO - Impact Mondial Edition
echo  Lancement de l'application...
echo ============================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERREUR au lancement !
    echo Si les dependances ne sont pas installees, lancez INSTALL.bat
    echo.
    pause
)

