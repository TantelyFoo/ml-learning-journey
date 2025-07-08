#!/usr/bin/env python3
"""
Machine Learning Environment Setup Script
Automates the installation and configuration of your ML environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors gracefully."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible!")
        print("   Please install Python 3.8 or higher.")
        return False

def main():
    print("🚀 Machine Learning Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Get the current directory
    ml_dir = Path.cwd()
    print(f"📁 Working directory: {ml_dir}")
    
    # Create virtual environment
    venv_path = ml_dir / "venv"
    if not venv_path.exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists!")
    
    # Activate virtual environment and install requirements
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    requirements_file = ml_dir / "requirements.txt"
    if requirements_file.exists():
        if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python packages"):
            return False
    else:
        print("⚠️  requirements.txt not found. Installing basic packages...")
        basic_packages = [
            "numpy", "pandas", "matplotlib", "seaborn", 
            "scikit-learn", "jupyter", "ipykernel"
        ]
        for package in basic_packages:
            if not run_command(f"{pip_cmd} install {package}", f"Installing {package}"):
                return False
    
    # Install Jupyter kernel
    if not run_command(f"{pip_cmd} install ipykernel", "Installing Jupyter kernel"):
        return False
    
    if not run_command(f"venv\\Scripts\\python -m ipykernel install --user --name=ml-env --display-name='ML Environment'", "Registering Jupyter kernel"):
        print("⚠️  Kernel registration failed, but this is often not critical.")
    
    # Create .gitignore if it doesn't exist
    gitignore_path = ml_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# Data files
*.csv
*.xlsx
*.json
data/
datasets/

# Models
*.pkl
*.joblib
*.h5
*.pt
*.pth

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
"""
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file!")
    
    print("\n🎉 Environment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate your environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Start Jupyter:")
    print("   jupyter notebook")
    print("3. Open the foundations notebook:")
    print("   01_foundations/ml_foundations_journey.ipynb")
    print("\n🚀 Happy learning!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
