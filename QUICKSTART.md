# Quick Start Guide - Building Port Killer Executable

## For First-Time Build

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable:**
   ```bash
   python build_exe.py
   ```

3. **Find your executable:**
   - Windows: `dist/PortKiller.exe`
   - macOS: `dist/PortKiller.app`
   - Linux: `dist/PortKiller`

4. **Test it:**
   - Double-click the executable
   - The GUI should open without any terminal window
   - Try scanning a port (e.g., 8080 or 3000)

## Distribute to End Users

### Option 1: Direct File Sharing
- Simply send them the executable file from the `dist/` folder
- They double-click to run - no installation needed!

### Option 2: GitHub Release
1. Create a release on GitHub
2. Upload the executable as a release asset
3. Share the release URL with users

## Troubleshooting

### "PyInstaller not found"
The build script will automatically install PyInstaller for you.

### Executable is too large
This is normal! PyInstaller bundles Python and all dependencies.
Typical size: 15-25 MB

### "Windows protected your PC" message
This is normal for unsigned executables on Windows.
Users can click "More info" → "Run anyway"

To avoid this, you'd need to code-sign the executable (requires a certificate).

### GUI doesn't open / Terminal appears
Make sure the build script uses `--windowed` and `--noconsole` flags.
Check that you're building from `port_killer_gui.py`, not the CLI script.

### Process killing fails
Some processes require Administrator/root privileges.
Users should right-click the executable and "Run as Administrator" (Windows).

## Development Testing

To test the GUI without building:
```bash
python port_killer_gui.py
```

This is faster during development than rebuilding the executable each time.


