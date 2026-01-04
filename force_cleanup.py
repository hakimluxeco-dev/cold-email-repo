import os
import shutil
import winreg
import time

def force_cleanup():
    print("Starting Force Cleanup...")
    
    # 1. Kill processes
    print("Killing running processes...")
    os.system("taskkill /F /IM ColdEmailReach.exe /T 2>nul")
    os.system("taskkill /F /IM ColdEmailReachSetup.exe /T 2>nul")
    time.sleep(1)

    # 2. Remove Installation Directory
    install_path = os.path.join(os.environ['LOCALAPPDATA'], "MaiSolutions", "ColdEmailReach")
    if os.path.exists(install_path):
        print(f"Removing installation directory: {install_path}")
        try:
            shutil.rmtree(install_path)
            print("Directory removed.")
        except Exception as e:
            print(f"Failed to remove directory: {e}")
    else:
        print("Installation directory not found.")

    # 3. Remove Registry Key
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MaiSolutionsColdEmailReach"
    print(f"Removing registry key: {reg_path}")
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
        print("Registry key removed.")
    except FileNotFoundError:
        print("Registry key not found.")
    except Exception as e:
        print(f"Failed to remove registry key: {e}")

    # 4. Remove Shortcuts
    print("Removing shortcuts...")
    desktop = os.path.join(os.environ['USERPROFILE'], "Desktop", "Mai Solutions Cold Email Reach.lnk")
    if os.path.exists(desktop):
        os.remove(desktop)
        print("Desktop shortcut removed.")
        
    start_menu = os.path.join(os.environ['APPDATA'], "Microsoft", "Windows", "Start Menu", "Programs", "Mai Solutions Cold Email Reach.lnk")
    if os.path.exists(start_menu):
        os.remove(start_menu)
        print("Start Menu shortcut removed.")

    print("\nCleanup Complete. You can now try to install again.")
    print("Press Enter to close.")
    input()

if __name__ == "__main__":
    force_cleanup()
