@echo off
pyinstaller --noconfirm --onefile --windowed \
    --add-data "assets/cards;assets/cards" \
    --add-data "assets/backgrounds;assets/backgrounds" \
    --add-data "assets/ui;assets/ui" \
    --add-data "assets/effects;assets/effects" \
    --hidden-import pygame \
    main.py

echo Build completed!
pause
