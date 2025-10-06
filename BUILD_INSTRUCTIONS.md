# Build Instructions - IMPORTANT

## The Error You Saw

If you got a "Missing Dependency" error when running the .exe, it means **psutil wasn't installed when you built the executable**.

PyInstaller can only bundle dependencies that are **already installed** on your system at build time.

## How to Fix and Rebuild

### Option 1: Easy Way (Windows)
1. Double-click `install_dependencies.bat`
2. Wait for it to finish
3. Run `python build_exe.py`
4. Test the new .exe from `dist/PortKiller.exe`

### Option 2: Manual Way (All Platforms)
```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Verify psutil is installed
python -c "import psutil; print('psutil OK')"

# Step 3: Build the executable
python build_exe.py

# Step 4: Test it
# Navigate to dist/ folder and double-click PortKiller.exe
```

## What the Updated Build Script Does

The updated `build_exe.py` now:
1. ✅ Checks if psutil is installed BEFORE building
2. ✅ Uses `--hidden-import=psutil` to force PyInstaller to include it
3. ✅ Will tell you if dependencies are missing before wasting time building

## Verifying the Fix

After rebuilding, the .exe should:
- Open directly to the GUI (no error dialog)
- No terminal window
- Work on any Windows PC without Python installed

## Common Issues

### "psutil not found" during build
**Solution:** Run `pip install psutil` before building

### Old .exe still shows error
**Solution:** Make sure you're running the NEW .exe from `dist/` folder, not an old one

### "Permission denied" when building
**Solution:** Close any running instances of the old .exe, then rebuild

## Quick Test After Building

1. Open the `dist/` folder
2. Double-click `PortKiller.exe`
3. You should see the GUI open immediately (no error)
4. Try entering port `8080` and clicking "Scan Port"
5. If it works, you're ready to distribute!

