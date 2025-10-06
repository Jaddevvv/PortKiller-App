# Port Killer

Cross-platform utility for inspecting and terminating processes bound to a TCP port. The project ships with both a command-line interface and a standalone GUI executable that can be distributed to end users.

## Features
- **Standalone GUI executable** - Double-click to run, no Python installation required
- Modern, user-friendly graphical interface
- Inspect processes listening on a specific port before terminating them
- Kill every process bound to a port with confirmation
- Works on Windows, macOS, and Linux
- Built on `psutil` for reliable process management

## For End Users

### Download and Run (No Installation Required)
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

# Run the build script
python build_exe.py
```

The executable will be created in the `dist/` directory:
- **Windows:** `dist/PortKiller.exe`
- **macOS:** `dist/PortKiller.app`
- **Linux:** `dist/PortKiller`

You can then distribute this single file to end users. They can double-click it to run the application without any Python installation.

### What the Build Script Does
1. Installs PyInstaller if not already present
2. Bundles Python, dependencies, and your script into a single executable
3. Creates a GUI-only application with no console window
4. Outputs a distributable file ready for end users

## Usage

### Standalone GUI (Recommended for End Users)
Simply run the built executable:

**From File Explorer:**
- Double-click `PortKiller.exe` (Windows) or `PortKiller` (Linux/Mac)

**From Python (for development/testing):**
```bash
python port_killer_gui.py
```

The GUI provides two main actions:
- **Scan Port:** Check what processes are using a port without killing them
- **Kill Process:** Terminate all processes using the specified port (with confirmation)

### Command Line Interface (For Advanced Users)
The original CLI scripts are still available for command-line usage:

List processes without killing them:
```bash
python port_killer_gpt.py 8080 --action list
```

Kill every process bound to the port (with a confirmation prompt):
```bash
python port_killer_gpt.py 8080
```

Skip the confirmation prompt when you are certain:
```bash
python port_killer_gpt.py 8080 --yes
```

Launch the GUI from the CLI script:
```bash
python port_killer_gpt.py --gui
```

## Distribution

### Creating a GitHub Release with the Executable

1. **Build the executable:**
   ```bash
   python build_exe.py
   ```

2. **Create a new repository on GitHub** (e.g. `PortKiller`)

3. **Commit and push the source code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Port Killer"
   git remote add origin https://github.com/<your-github-username>/PortKiller.git
   git push -u origin main
   ```

4. **Create a GitHub Release:**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Create a new tag (e.g., `v1.0.0`)
   - Upload the executable from `dist/PortKiller.exe` (or your platform's equivalent)
   - Add release notes describing features
   - Publish the release

5. **Share the direct download link:**
   - Users can download from: `https://github.com/<your-github-username>/PortKiller/releases/latest`
   - They just download the executable and run it - no installation needed!

### Alternative Distribution Methods
- **Direct sharing:** Just send the executable file via email or file sharing
- **Network drive:** Place it on a shared network drive for your team
- **Installer (optional):** Use tools like Inno Setup (Windows) or create a .dmg (macOS) for a more polished installation experience

Replace `<your-github-username>` with your actual GitHub username.
