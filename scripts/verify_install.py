#!/usr/bin/env python3
"""
Verify Cloud Splitter installation and dependencies
"""
import sys
import subprocess
import shutil
from pathlib import Path
import torch
import pkg_resources

def check_python_version():
    print("Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"✓ Python {sys.version.split()[0]} (compatible)")
    else:
        print(f"✗ Python {sys.version.split()[0]} (requires 3.8 or higher)")
        return False
    return True

def check_ffmpeg():
    print("\nChecking FFmpeg installation...")
    if shutil.which('ffmpeg'):
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                 capture_output=True, 
                                 text=True)
            version = result.stdout.split('version')[1].split()[0]
            print(f"✓ FFmpeg {version} found")
            return True
        except:
            print("✗ FFmpeg found but version check failed")
            return False
    else:
        print("✗ FFmpeg not found")
        return False

def check_gpu():
    print("\nChecking GPU support...")
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
        print(f"✓ CUDA available ({device_count} device(s))")
        print(f"  Device: {device_name}")
        return True
    else:
        try:
            if torch.backends.mps.is_available():
                print("✓ Apple Metal (MPS) available")
                return True
        except:
            pass
        
        if hasattr(torch, 'hipify') and torch.hipify.is_available():
            print("✓ ROCm (AMD GPU) available")
            return True
            
        print("ℹ No GPU support detected (will use CPU)")
        return True

def check_dependencies():
    print("\nChecking Python dependencies...")
    required = {
        'yt-dlp': '2023.3.4',
        'demucs': '4.0.0',
        'textual': '0.27.0',
        'torch': '2.0.0',
    }
    
    all_good = True
    for package, min_version in required.items():
        try:
            version = pkg_resources.get_distribution(package).version
            if pkg_resources.parse_version(version) >= pkg_resources.parse_version(min_version):
                print(f"✓ {package} {version}")
            else:
                print(f"✗ {package} {version} (requires >={min_version})")
                all_good = False
        except pkg_resources.DistributionNotFound:
            print(f"✗ {package} not found")
            all_good = False
    return all_good

def check_directories():
    print("\nChecking directories...")
    config_dir = Path.home() / ".config" / "cloud-splitter"
    config_file = config_dir / "config.toml"
    
    if not config_dir.exists():
        print(f"ℹ Creating config directory: {config_dir}")
        config_dir.mkdir(parents=True, exist_ok=True)
    
    if not config_file.exists():
        print(f"ℹ Default config file will be created on first run")
    else:
        print(f"✓ Configuration found: {config_file}")
    
    return True

def main():
    print("Cloud Splitter Installation Verification\n")
    
    checks = [
        check_python_version(),
        check_ffmpeg(),
        check_gpu(),
        check_dependencies(),
        check_directories()
    ]
    
    print("\nSummary:")
    if all(checks):
        print("✓ All checks passed! Cloud Splitter is ready to use.")
        print("\nTo get started, run:")
        print("  cloud-splitter")
        sys.exit(0)
    else:
        print("✗ Some checks failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
