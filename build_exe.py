"""Build script for creating standalone Port Killer executable.

This script uses PyInstaller to create a single executable file
that can be distributed to end users without requiring Python installation.

Usage:
    python build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller."""
    print("PyInstaller not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("PyInstaller installed successfully.")


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("Checking dependencies...")
    
    missing = []
    try:
        import psutil
        print("  ✓ psutil found")
    except ImportError:
        missing.append("psutil")
        print("  ✗ psutil not found")
    
    if missing:
        print(f"\n❌ Missing required dependencies: {', '.join(missing)}")
        print("Please install them with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("All dependencies found!\n")
    return True


def build_executable():
    """Build the executable using PyInstaller."""
    print("\n" + "="*60)
    print("Building Port Killer Executable")
    print("="*60 + "\n")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (Windows/Mac)
        "--noconsole",                  # Alternative flag for no console
        "--name=PortKiller",            # Executable name
        "--clean",                      # Clean PyInstaller cache
        "--noconfirm",                  # Replace output directory without asking
        "--hidden-import=psutil",       # Explicitly include psutil
        "port_killer_gui.py"           # Entry point script
    ]
    
    # Add icon if available (you can create one later)
    icon_path = Path("icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    print("Running PyInstaller with the following options:")
    print(" ".join(cmd))
    print()
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build completed successfully!")
        print("="*60)
        
        # Show output location
        dist_dir = Path("dist")
        if sys.platform == "win32":
            exe_path = dist_dir / "PortKiller.exe"
        elif sys.platform == "darwin":
            exe_path = dist_dir / "PortKiller.app"
        else:
            exe_path = dist_dir / "PortKiller"
        
        if exe_path.exists():
            print(f"\nExecutable location: {exe_path.absolute()}")
            print(f"File size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
            print("\nYou can now distribute this file to end users.")
            print("They can double-click it to run Port Killer without installing Python.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        return False
    
    return True


def cleanup_build_files():
    """Clean up temporary build files."""
    print("\nCleaning up temporary build files...")
    
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["PortKiller.spec"]
    
    for dir_name in dirs_to_remove:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  Removed: {dir_name}/")
    
    for file_name in files_to_remove:
        if Path(file_name).exists():
            Path(file_name).unlink()
            print(f"  Removed: {file_name}")
    
    print("Cleanup complete.")


def main():
    """Main build process."""
    # Check for PyInstaller
    if not check_pyinstaller():
        install_pyinstaller()
    
    # Check if source file exists
    if not Path("port_killer_gui.py").exists():
        print("❌ Error: port_killer_gui.py not found!")
        print("Make sure you're running this script from the project directory.")
        sys.exit(1)
    
    # Check dependencies before building
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    
    # Build the executable
    success = build_executable()
    
    if success:
        # Ask about cleanup
        cleanup_build_files()
        print("\n✅ All done! Your executable is ready for distribution.")
    else:
        print("\n❌ Build process failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()


