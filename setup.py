import subprocess
import sys
import os

def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'convert_images.py')
    if not os.path.isfile(main_script):
        print(f"Error: Main script '{main_script}' not found.")
        return
    subprocess.run([sys.executable, main_script])

if __name__ == '__main__':
    install_packages()
    main()