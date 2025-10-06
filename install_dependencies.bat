@echo off
echo ================================================
echo Installing Port Killer Dependencies
echo ================================================
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ================================================
echo Dependencies installed successfully!
echo ================================================
echo.
echo You can now build the executable with:
echo   python build_exe.py
echo.
pause

