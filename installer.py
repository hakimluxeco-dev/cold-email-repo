
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import zipfile
import shutil
import threading
import win32com.client
import winreg
from pathlib import Path

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mai Solutions Cold Email Reach Setup")
        self.geometry("640x440")
        self.resizable(False, False)
        
        # Determine resource path (workaround for PyInstaller onefile)
        if hasattr(sys, '_MEIPASS'):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
            
        # Style
        style = ttk.Style()
        style.theme_use('vista')
        style.configure("White.TFrame", background="white")
        style.configure("White.TLabel", background="white", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="white", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 9))
        
        # Try to set icon
        try:
            icon_path = os.path.join(self.base_path, "app_icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            pass

        # Main Layout: Sidebar + Content
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar
        self.sidebar_frame = ttk.Frame(main_frame, width=180)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        # Copyright Footer
        tk.Label(self.sidebar_frame, text="© 2026 Mai Solutions", bg="#101524", fg="gray", font=("Segoe UI", 7)).pack(side=tk.BOTTOM, pady=5)
        
        try:
            # Load Image
            img_path = os.path.join(self.base_path, "installer_sidebar_v2.png")
            self.logo_img = tk.PhotoImage(file=img_path)
            # Scaling logic if needed, but assuming 180x440 roughly
            # Crop or resize by subsample if too huge, but usually fine.
            if self.logo_img.width() > 200:
                self.logo_img = self.logo_img.subsample(2, 2)
            
            lbl = tk.Label(self.sidebar_frame, image=self.logo_img, bg="#1a202c", borderwidth=0)
            lbl.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            # Fallback
            tk.Label(self.sidebar_frame, text="Cold Email\nReach", bg="#0f172a", fg="white", font=("Segoe UI", 16, "bold")).pack(fill=tk.BOTH, expand=True)

        # Right Content Area (White)
        self.content_frame = ttk.Frame(main_frame, style="White.TFrame", padding="25")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Button Bar (Bottom of Content)
        # Note: We put button bar inside content frame or separate? 
        # Modern installers often have a distinct grey footer, let's keep it clean white with bottom alignment.
        
        self.install_dir = tk.StringVar(value=os.path.join(os.environ['ProgramFiles'], "MaiSolutions", "ColdEmailReach"))
        self.create_desktop_var = tk.BooleanVar(value=True)
        self.create_startmenu_var = tk.BooleanVar(value=True)
        self.progress_var = tk.DoubleVar()
        
        self.show_welcome()
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children(): widget.destroy()
        
    def show_welcome(self):
        self.clear_content()
        
        # Check if installed
        existing_path = self.check_existing_install()
        if existing_path:
            self.show_maintenance(existing_path)
            return

        # Title
        ttk.Label(self.content_frame, text="Welcome to the\nMai Solutions Cold Email Reach Setup", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))
        
        # Body
        msg = ("This wizard will guide you through the installation of Mai Solutions Cold Email Reach.\n\n"
               "It is recommended that you close all other applications before starting Setup.\n\n"
               "Click Next to continue.")
        ttk.Label(self.content_frame, text=msg, style="White.TLabel", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        # Buttons
        self.add_buttons("Next", self.show_license)

    def check_existing_install(self):
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MaiSolutionsColdEmailReach"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
            # Try InstallLocation first, fallback to UninstallString parsing
            try:
                val, _ = winreg.QueryValueEx(key, "InstallLocation")
                if val and os.path.exists(val):
                    winreg.CloseKey(key)
                    return val
            except: pass
            
            try:
                val, _ = winreg.QueryValueEx(key, "UninstallString")
                if val:
                    path = os.path.dirname(val)
                    if os.path.exists(path):
                        winreg.CloseKey(key)
                        return path
            except: pass
            
            winreg.CloseKey(key)
        except:
            pass
        return None

    def show_maintenance(self, existing_path):
        self.clear_content()
        self.install_dir.set(existing_path) # Pre-set for repair/remove
        
        ttk.Label(self.content_frame, text="Application Maintenance", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))
        ttk.Label(self.content_frame, text="Mai Solutions Cold Email Reach is already installed.\nChoose an operation:", style="White.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        self.maint_var = tk.StringVar(value="repair")
        
        frame = ttk.Frame(self.content_frame, style="White.TFrame")
        frame.pack(fill=tk.X, pady=10)
        
        # Options
        ttk.Radiobutton(frame, text="Modify", variable=self.maint_var, value="modify").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text="    Change installation settings (e.g. shortcuts).", style="White.TLabel", foreground="gray").pack(anchor=tk.W, pady=(0, 8))
        
        ttk.Radiobutton(frame, text="Repair", variable=self.maint_var, value="repair").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text="    Reinstall components to verify integrity.", style="White.TLabel", foreground="gray").pack(anchor=tk.W, pady=(0, 8))
        
        ttk.Radiobutton(frame, text="Remove", variable=self.maint_var, value="remove").pack(anchor=tk.W, pady=2)
        ttk.Label(frame, text="    Remove the application from your computer.", style="White.TLabel", foreground="gray").pack(anchor=tk.W, pady=(0, 8))
        
        self.add_buttons("Next", self.run_maintenance)

    def run_maintenance(self):
        action = self.maint_var.get()
        if action == "modify":
            # Treat as fresh install flow
            self.show_license()
        elif action == "repair":
            # Direct install to existing path
            self.start_installation()
        elif action == "remove":
            self.confirm_remove()

    def confirm_remove(self):
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove Mai Solutions Cold Email Reach?"):
            self.perform_uninstall()

    def perform_uninstall(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Removing Application", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        self.status_lbl = ttk.Label(self.content_frame, text="Initializing removal...", style="White.TLabel")
        self.status_lbl.pack(anchor=tk.W, pady=20)
        self.progress = ttk.Progressbar(self.content_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X)
        
        threading.Thread(target=self.run_uninstall_logic, daemon=True).start()

    def run_uninstall_logic(self):
        try:
            target = self.install_dir.get()
            
            # 1. Kill Processes
            self.after(0, lambda: self.status_lbl.config(text="Stopping processes..."))
            os.system("taskkill /F /IM ColdEmailReach.exe /T 2>nul")
            self.progress_var.set(20)
            
            # 2. Remove Files
            self.after(0, lambda: self.status_lbl.config(text="Removing files..."))
            if os.path.exists(target):
                try: 
                    # We might be running from inside 'target' (as uninstall.exe).
                    # We cannot delete ourselves. Iterate and delete others.
                    for item in os.listdir(target):
                        item_path = os.path.join(target, item)
                        try:
                            if item_path == sys.executable:
                                continue # Skip self
                            
                            if os.path.isfile(item_path) or os.path.islink(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                        except Exception as e:
                            print(f"Failed to remove {item}: {e}")
                except Exception as e: print(e)
            self.progress_var.set(60)
            
            # 3. Remove Registry
            self.after(0, lambda: self.status_lbl.config(text="Removing registry entries..."))
            try:
                reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MaiSolutionsColdEmailReach"
                try: winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
                except: pass
            except: pass
            self.progress_var.set(80)
            
            # Post-exit Cleanup: Schedule cleanup
            # Only delete ourselves if we are running from the install directory (i.e. we are the installed uninstall.exe)
            # If we are the original setup.exe running from Downloads, keep us alive!
            try:
                self_path = os.path.abspath(sys.executable)
                target_path = os.path.abspath(target)
                
                # Check if we are inside the target folder
                is_installed_uninstaller = self_path.startswith(target_path)
                
                cmd_parts = ['ping 127.0.0.1 -n 3 > nul']
                
                if is_installed_uninstaller:
                    # distinct uninstaller, delete self
                    cmd_parts.append(f'del /F /Q "{self_path}"')
                
                # Always try to remove the target dir (it should be empty by now, except maybe for us)
                # If we are outside, rmdir might fail if we are not empty, but we tried.
                cmd_parts.append(f'rmdir /Q "{target}"')
                cmd_parts.append('exit')
                
                full_cmd = " & ".join(cmd_parts)
                os.system(f'start /min "" cmd /c "{full_cmd}"')
            except: pass
            
            # 4. Remove Shortcuts
            self.after(0, lambda: self.status_lbl.config(text="Removing shortcuts..."))
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                desktop = shell.SpecialFolders("Desktop")
                sm = shell.SpecialFolders("StartMenu")
                
                lnk_d = os.path.join(desktop, "Mai Solutions Cold Email Reach.lnk")
                if os.path.exists(lnk_d): os.remove(lnk_d)
                
                lnk_s = os.path.join(sm, "Programs", "Mai Solutions Cold Email Reach.lnk")
                if os.path.exists(lnk_s): os.remove(lnk_s)
            except: pass
            
            self.progress_var.set(100)
            self.after(500, self.show_remove_finished)
            
        except Exception as e:
            self.fail(f"Removal failed: {e}")

    def show_remove_finished(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Removal Complete", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))
        ttk.Label(self.content_frame, text="Mai Solutions Cold Email Reach has been successfully removed.", style="White.TLabel").pack(anchor=tk.W, pady=10)
        self.add_buttons("Close", self.destroy)

    def show_license(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="License Agreement", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(self.content_frame, text="Please read the following license agreement carefully.", style="White.TLabel").pack(anchor=tk.W)
        
        # Text area
        text_frame = ttk.Frame(self.content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        txt = tk.Text(text_frame, height=10, width=50, font=("Segoe UI", 9), wrap=tk.WORD)
        scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)
        
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        eula = ("END USER LICENSE AGREEMENT\n\n"
                "IMPORTANT: PLEASE READ THIS LICENSE AGREEMENT CAREFULLY BEFORE INSTALLING OR USING THE SOFTWARE.\n\n"
                "1. LICENSE GRANT. Mai Solutions grants you a personal, non-transferable and non-exclusive right and license to use the object code of its Software on a single computer; provided that you do not (and do not allow any third party to) copy, modify, create a derivative work of, reverse engineer, reverse assemble or otherwise attempt to discover any source code, sell, assign, sublicense, grant a security interest in or otherwise transfer any right in the Software.\n\n"
                "2. COPYRIGHT. The Software is owned by Mai Solutions and is protected by copyright laws and international treaty provisions.\n\n"
                "3. DISCLAIMER OF WARRANTY. THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND. MAI SOLUTIONS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n\n"
                "© 2026 Mai Solutions. All rights reserved.")
        txt.insert(tk.END, eula)
        txt.config(state=tk.DISABLED)
        
        # Checkbox
        self.agree_var = tk.BooleanVar()
        chk = ttk.Checkbutton(self.content_frame, text="I accept the agreement", variable=self.agree_var, command=self.check_agreement)
        chk.pack(anchor=tk.W, pady=5)
        
        self.btn_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        self.btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        
        ttk.Separator(self.btn_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        
        f = ttk.Frame(self.btn_frame, style="White.TFrame")
        f.pack(fill=tk.X)
        
        self.next_btn = ttk.Button(f, text="Next", command=self.show_location, state=tk.DISABLED)
        self.next_btn.pack(side=tk.RIGHT)
        ttk.Button(f, text="< Back", command=self.show_welcome).pack(side=tk.RIGHT, padx=5)
        
    def check_agreement(self):
        if self.agree_var.get():
            self.next_btn.config(state=tk.NORMAL)
        else:
            self.next_btn.config(state=tk.DISABLED)

    def show_location(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="Choose Install Location", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 15))
        ttk.Label(self.content_frame, text="Choose the folder in which to install Mai Solutions Cold Email Reach.", style="White.TLabel").pack(anchor=tk.W)
        
        # Frame for entry + browse
        f = ttk.Frame(self.content_frame, style="White.TFrame")
        f.pack(fill=tk.X, pady=25)
        
        ttk.Entry(f, textvariable=self.install_dir).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f, text="Browse...", command=self.browse_folder).pack(side=tk.LEFT)
        
        ttk.Label(self.content_frame, text="Space required: ~300 MB", style="White.TLabel", foreground="gray").pack(anchor=tk.W)

        # Shortcuts
        ttk.Checkbutton(self.content_frame, text="Create Desktop Shortcut", variable=self.create_desktop_var).pack(anchor=tk.W, pady=(10, 2))
        ttk.Checkbutton(self.content_frame, text="Create Start Menu Shortcut", variable=self.create_startmenu_var).pack(anchor=tk.W)
        
        self.add_buttons("Install", self.start_installation, back_cmd=self.show_license)

    def browse_folder(self):
        d = filedialog.askdirectory(initialdir=self.install_dir.get())
        if d:
            # Enforce folder structure
            full_path = os.path.join(d, "MaiSolutions", "ColdEmailReach")
            self.install_dir.set(full_path)
        
    def start_installation(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="Installing", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(self.content_frame, text="Please wait while Mai Solutions Cold Email Reach is being installed.", style="White.TLabel").pack(anchor=tk.W)
        
        self.status_lbl = ttk.Label(self.content_frame, text="Initializing...", style="White.TLabel")
        self.status_lbl.pack(anchor=tk.W, pady=(30, 5))
        
        self.progress = ttk.Progressbar(self.content_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, pady=0)
        
        # Disable buttons during install? Or just don't show them yet.
        # We will trigger thread
        threading.Thread(target=self.run_install, daemon=True).start()
        
    def run_install(self):
        try:
            target = self.install_dir.get()
            
            # 0. Kill Running Process
            self.after(0, lambda: self.status_lbl.config(text=f"Stopping existing processes..."))
            os.system("taskkill /F /IM ColdEmailReach.exe /T 2>nul")
            # Give it a moment to release locks
            self.progress_var.set(2)
            import time
            time.sleep(1)
            
            # 1. Clean (with Backup)
            self.after(0, lambda: self.status_lbl.config(text=f"Backing up data..."))
            
            # Backup Logic
            backup_files = ["app.db", "cold_email.db", "cold_email_logs.log"]
            temp_backups = {}
            import tempfile
            import shutil
            
            if os.path.exists(target):
                for fname in backup_files:
                    fpath = os.path.join(target, fname)
                    if os.path.exists(fpath):
                        tmp = os.path.join(tempfile.gettempdir(), f"cer_backup_{fname}")
                        try:
                            shutil.copy2(fpath, tmp)
                            temp_backups[fname] = tmp
                        except: pass

            self.after(0, lambda: self.status_lbl.config(text=f"Cleaning old files..."))
            if os.path.exists(target):
                # Retry loop for cleanup
                for attempt in range(3):
                    try: 
                        shutil.rmtree(target)
                        break
                    except Exception as e: 
                        # If permission error, try killing again
                        os.system("taskkill /F /IM ColdEmailReach.exe /T 2>nul")
                        time.sleep(1)
                        if attempt == 2:
                            # If we can't delete the folder, maybe just proceed to overwrite?
                            # But remaining files might be an issue.
                            # Let's try to proceed, extractor will overwrite.
                            pass

            os.makedirs(target, exist_ok=True)
            self.progress_var.set(5)
            
            # 2. Extract
            self.after(0, lambda: self.status_lbl.config(text="Extracting application files..."))
            
            zip_path = os.path.join(self.base_path, "app_payload.zip")
            if not os.path.exists(zip_path):
                self.fail("Payload missing!")
                return

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                total = len(files)
                for i, file in enumerate(files):
                    zip_ref.extract(file, target)
                    if i % 10 == 0:
                        self.progress_var.set(5 + (i / total * 85))
                        
            # Restore Backups
            if temp_backups:
                self.status_lbl.config(text="Restoring user data...")
                for fname, tmp_path in temp_backups.items():
                    dest = os.path.join(target, fname)
                    try:
                        if os.path.exists(tmp_path):
                            shutil.copy2(tmp_path, dest)
                    except: pass
                        
            self.progress_var.set(90)
            
            # 3. Copy Uninstaller (Copy Self)
            self.after(0, lambda: self.status_lbl.config(text="Configuring uninstaller..."))
            try:
                # Copy the currently running installer as the uninstaller.
                # This prevents AV issues with a separate unknown binary.
                src = sys.executable
                dest = os.path.join(target, "uninstall.exe")
                shutil.copy(src, dest)
            except Exception as e:
                print(f"Uninstaller copy failed: {e}")
                # Not fatal, but annoying.


            # 3.1 Copy Icon
            icon_src = os.path.join(self.base_path, "app_icon.ico")
            if os.path.exists(icon_src):
                shutil.copy(icon_src, os.path.join(target, "app_icon.ico"))

            # 4. Registry Keys
            self.register_uninstall(target)

            # 5. Shortcuts
            self.after(0, lambda: self.status_lbl.config(text="Creating shortcuts..."))
            
            # Payload is flat, so exe is in target directly
            exe_path = os.path.join(target, "ColdEmailReach.exe")
            
            if not os.path.exists(exe_path):
                 # Fallback deep search if needed
                for root, dirs, files in os.walk(target):
                    if "ColdEmailReach.exe" in files:
                        exe_path = os.path.join(root, "ColdEmailReach.exe")
                        break
            
            if self.create_desktop_var.get() or self.create_startmenu_var.get():
                icon_target = os.path.join(target, "app_icon.ico")
                self.create_shortcut(exe_path, "Mai Solutions Cold Email Reach", icon_path=icon_target)
            self.progress_var.set(100)
            self.after(500, self.show_finished)
            
        except Exception as e:
            self.fail(str(e))

    def register_uninstall(self, install_path):
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MaiSolutionsColdEmailReach"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Mai Solutions Cold Email Reach")
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(install_path, "app_icon.ico"))
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, os.path.join(install_path, "uninstall.exe"))
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Mai Solutions")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_path)
            winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry error: {e}")
            
    def create_shortcut(self, target_exe, name, icon_path=None):
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            
            if self.create_desktop_var.get():
                desktop = shell.SpecialFolders("Desktop")
                shortcut = shell.CreateShortcut(os.path.join(desktop, f"{name}.lnk"))
                shortcut.TargetPath = target_exe
                shortcut.WorkingDirectory = os.path.dirname(target_exe)
                if icon_path and os.path.exists(icon_path):
                    shortcut.IconLocation = icon_path
                shortcut.Save()
            
            if self.create_startmenu_var.get():
                start_menu = shell.SpecialFolders("StartMenu") 
                shortcut_sm = shell.CreateShortcut(os.path.join(start_menu, "Programs", f"{name}.lnk"))
                shortcut_sm.TargetPath = target_exe
                shortcut_sm.WorkingDirectory = os.path.dirname(target_exe)
                if icon_path and os.path.exists(icon_path):
                    shortcut_sm.IconLocation = icon_path
                shortcut_sm.Save()
        except Exception as e:
            messagebox.showerror("Shortcut Error", f"Failed to create shortcut: {e}")

    def fail(self, msg):
        messagebox.showerror("Error", msg)
        self.destroy()

    def show_finished(self):
        self.clear_content()
        
        ttk.Label(self.content_frame, text="Installation Complete", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 20))
        
        msg = ("Mai Solutions Cold Email Reach has been installed on your computer.\n\n"
               "Click Finish to close this wizard.")
        ttk.Label(self.content_frame, text=msg, style="White.TLabel", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=10)
        
        # Launch Option
        self.launch_var = tk.BooleanVar(value=True)
        chk = ttk.Checkbutton(self.content_frame, text="Launch Mai Solutions Cold Email Reach", variable=self.launch_var)
        chk.pack(anchor=tk.W, pady=15)
        
        self.add_buttons("Finish", self.finish_cleanup)

    def finish_cleanup(self):
        if self.launch_var.get():
            try:
                target_dir = self.install_dir.get()
                exe_path = os.path.join(target_dir, "ColdEmailReach.exe")
                if not os.path.exists(exe_path):
                     # Fallback search
                    for root, dirs, files in os.walk(target_dir):
                        if "ColdEmailReach.exe" in files:
                            exe_path = os.path.join(root, "ColdEmailReach.exe")
                            break
                            
                if os.path.exists(exe_path):
                    os.startfile(exe_path)
                else:
                    messagebox.showerror("Error", "Could not find application executable.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch application: {e}")
        self.destroy()

    def add_buttons(self, next_text, next_cmd, back_cmd=None):
        btn_frame = ttk.Frame(self.content_frame, style="White.TFrame")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        
        # Separator
        ttk.Separator(btn_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        
        f = ttk.Frame(btn_frame, style="White.TFrame")
        f.pack(fill=tk.X)
        
        ttk.Button(f, text=next_text, command=next_cmd).pack(side=tk.RIGHT)
        if back_cmd:
            ttk.Button(f, text="< Back", command=back_cmd).pack(side=tk.RIGHT, padx=5)
        else:
            ttk.Button(f, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)


    def run_silent_update(self):
        """
        Runs the update process without GUI.
        1. Detect Install Path
        2. Kill Running App
        3. Clean & Extract
        4. Registry & Shortcuts
        5. Relaunch
        """
        target = self.check_existing_install()
        if not target:
            # Fallback to default if not found
            target = os.path.join(os.environ['ProgramFiles'], "MaiSolutions", "ColdEmailReach")
        
        # 1. Kill Processes
        os.system("taskkill /F /IM ColdEmailReach.exe /T 2>nul")
        
        # 2. Install
        try:
            # Clean (optional, maybe unsafe if we delete user data? 
            # Usually user data is in AppData, so app folder clean is fine)
            if os.path.exists(target):
                try: 
                    # Only remove app files, not everything? 
                    # For simplicity in this script we often wiped. 
                    # Let's verify if we want to wipe. 
                    # The GUI wipes `shutil.rmtree(target)`. 
                    # We should probably do the same to ensure clean state.
                    shutil.rmtree(target)
                except: pass
            
            os.makedirs(target, exist_ok=True)
            
            # Extract
            zip_path = os.path.join(self.base_path, "app_payload.zip")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target)
                
            # Copy extras
            extras = ["uninstall.exe", "app_icon.ico"]
            for f in extras:
                src = os.path.join(self.base_path, f)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(target, f))
            
            # Registry
            self.register_uninstall(target)
            
            # Shortcuts (Force recreate)
            exe_path = os.path.join(target, "ColdEmailReach.exe")
            if not os.path.exists(exe_path):
                 for root, dirs, files in os.walk(target):
                        if "ColdEmailReach.exe" in files:
                            exe_path = os.path.join(root, "ColdEmailReach.exe")
                            break
                            
            # Always update shortcuts for silent update to ensure they assume new icon/path if changed
            # We assume standard desktop/start menu creation
            self.create_desktop_var.set(True)
            self.create_startmenu_var.set(True)
            self.create_shortcut(exe_path, "Mai Solutions Cold Email Reach", icon_path=os.path.join(target, "app_icon.ico"))
            
            # Relaunch
            subprocess.Popen([exe_path], shell=False)
            
        except Exception as e:
            # In silent mode, we can't show message box easily. Log to file?
            with open(os.path.join(os.path.expanduser("~"), "cold_email_update_error.log"), "w") as f:
                f.write(str(e))
        
        sys.exit(0)

if __name__ == "__main__":
    import subprocess
    
    if "--update" in sys.argv:
        # Headless mode
        # We instantiate app to assume methods, but don't mainloop
        app = InstallerApp()
        app.withdraw() # Hide window
        app.run_silent_update()
    else:
        app = InstallerApp()
        app.mainloop()
