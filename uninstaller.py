
import os
import shutil
import win32com.client
import winreg
import sys
import ctypes
import time
from tkinter import messagebox, Tk

APP_NAME = "Mai Solutions Cold Email Reach"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MaiSolutionsColdEmailReach"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def remove_shortcuts():
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = shell.SpecialFolders("Desktop")
        start_menu = shell.SpecialFolders("StartMenu")
        
        shortcut_d = os.path.join(desktop, f"{APP_NAME}.lnk")
        if os.path.exists(shortcut_d):
            os.remove(shortcut_d)
            
        shortcut_sm = os.path.join(start_menu, "Programs", f"{APP_NAME}.lnk")
        if os.path.exists(shortcut_sm):
            os.remove(shortcut_sm)
    except Exception as e:
        print(f"Error removing shortcuts: {e}")

def remove_registry():
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    except Exception as e:
        print(f"Registry key not found or error: {e}")

def main():
    # Hide root window
    root = Tk()
    root.withdraw()
    
    confirm = messagebox.askyesno(APP_NAME, f"Are you sure you want to uninstall {APP_NAME}?")
    if not confirm:
        sys.exit()

    # Self-delete workaround is tricky in PyInstaller onefile.
    # Usually we leave the uninstaller or schedule it for deletion on reboot.
    # For now, we will delete EVERYTHING else in the folder.
    
    install_dir = os.path.dirname(os.path.abspath(sys.executable))
    
    # 1. Remove Shortcuts
    remove_shortcuts()
    
    # 2. Remove Registry Key
    remove_registry()
    
    # 3. Remove Files
    # We cannot delete the running exe, so we schedule it or ignore it.
    try:
        for item in os.listdir(install_dir):
            item_path = os.path.join(install_dir, item)
            if item_path == sys.executable:
                continue # Skip self
            
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # Try to schedule self deletion (simple batch approach)
        batch_script = f"""
@echo off
:loop
del "{sys.executable}"
if exist "{sys.executable}" goto loop
del "%~f0"
"""
        with open(os.path.join(install_dir, "cleanup.bat"), "w") as f:
            f.write(batch_script)
            
        # Execute batch content in separate process? 
        # Actually sending the command directly is easier
        cmd = f'start /min cmd /c "ping 127.0.0.1 -n 3 > nul & del "{sys.executable}" & rmdir "{install_dir}" & exit"'
        os.system(cmd)
        
    except Exception as e:
        messagebox.showerror("Error", f"Uninstall failed: {str(e)}")
        sys.exit(1)

    messagebox.showinfo(APP_NAME, f"{APP_NAME} has been uninstalled.")
    sys.exit()

if __name__ == "__main__":
    main()
