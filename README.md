# Port Killer

Cross-platform utility for inspecting and terminating processes bound to a TCP port. 

## For End Users

### Fast Download (No Installation Required)
1. Download the `PortKiller.exe` (Windows) or `PortKiller` executable from the releases
2. Double-click the executable to launch the GUI
3. Enter a port number and click "Scan Port" to see what's using it, or "Kill Process" to terminate it
4. That's it! No Python, no terminal, no configuration needed

**Note:** On Windows, you may need to run as Administrator to kill certain system processes.

## For Developers

### Requirements
- Python 3.8 or newer
- [psutil](https://pypi.org/project/psutil/)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (for building executables)
- Tkinter (bundled with most desktop Python distributions)

Install all dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Building the Standalone Executable

To create a standalone executable that end users can run without Python:

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run the build script (creates the executable and helper shortcut)
python ./build_exe.py
```

The script drops the platform-specific executable in the `dist/` directory:
- **Windows:** `dist/PortKiller.exe` (plus a `PortKiller.lnk` shortcut you can move to your desktop)
- **macOS:** `dist/PortKiller.app`
- **Linux:** `dist/PortKiller`

You can then distribute this single file to end users. They can double-click it to run the application without any Python installation. On Windows, feel free to drag the generated shortcut to your desktop for quick access.

### What the Build Script Does
1. Installs PyInstaller if not already present
2. Bundles Python, dependencies, and your script into a single executable
3. Creates a GUI-only application with no console window
4. Outputs a distributable file ready for end users
