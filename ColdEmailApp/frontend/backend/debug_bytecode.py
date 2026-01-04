import pkgutil
import dis
import os
import sys

def check_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            if filepath.endswith('.pyc'):
                f.seek(16) 
                pass
            else:
                source = f.read()
                try:
                    code = compile(source, filepath, 'exec')
                    for _ in dis.get_instructions(code):
                        pass
                except SyntaxError:
                    pass 
                except ImportError:
                    pass
    except IndexError:
        print(f"CRASH: {filepath}")
        return False
    except Exception as e:
        pass
    return True

def main():
    site_packages = next(p for p in sys.path if 'site-packages' in p)
    print(f"Scanning {site_packages}...")
    
    count = 0
    for root, dirs, files in os.walk(site_packages):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                if not check_file(path):
                    print(f"Found culprit: {path}")
                    # return
                count += 1
                if count % 1000 == 0:
                    print(f"Scanned {count} files...")

main()
