import ctypes
import subprocess
import sys
import os
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def check_activation_status():
    cmd = 'cscript //nologo %systemroot%\\System32\\slmgr.vbs /xpr'
    out, code = run_cmd(cmd)
    return out

def install_kms_key():
    keys = {
        "win11_pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "win11_pro_n": "MH37W-N47XK-V7XM9-C7227-GCQG9",
        "win11_enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
        "win11_enterprise_n": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
        "win11_home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
        "win11_education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    }
    
    print("[*] Available Keys:")
    for idx, (name, key) in enumerate(keys.items(), 1):
        print(f"    {idx}. {name} -> {key}")
    
    choice = int(input("\n[?] Select edition [1-6]: "))
    selected = list(keys.items())[choice - 1]
    key = selected[1]
    
    print(f"\n[*] Installing key: {key}")
    cmd = f'slmgr /ipk {key}'
    out, code = run_cmd(cmd)
    print(f"    Output: {out}")
    
    return key

def set_kms_server():
    print("[*] Setting KMS server...")
    kms_servers = [
        "kms.digiboy.ir",
        "kms.chinancce.com",
        "kms.lotro.com",
        "kms8.msguides.com",
    ]
    
    for server in kms_servers:
        print(f"    Trying: {server}")
        cmd = f'slmgr /skms {server}'
        out, code = run_cmd(cmd)
        
        print(f"[*] Activating...")
        cmd = 'slmgr /ato'
        out, code = run_cmd(cmd)
        
        time.sleep(3)
        
        status = check_activation_status()
        if "permanently" in status.lower() or "45 days" in status.lower():
            print(f"    [+] SUCCESS via {server}")
            print(f"    Status: {status}")
            return True
        else:
            print(f"    [-] Failed on {server}")
    
    return False

def activate_generic_ticket():
    print("[*] Attempting HWID method via MAS...")
    cmd = 'powershell -Command "irm https://massgrave.dev/get | iex"'
    print("[*] This opens MAS (Microsoft Activation Scripts)")
    print("[*] Select option [1] HWID Activation from the menu")
    run_cmd(cmd)

def auto_detect_edition():
    cmd = 'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v EditionID'
    out, code = run_cmd(cmd)
    return out

def main():
    print("=" * 55)
    print("   WINDOWS 11 PRO ACTIVATION TOOL")
    print("=" * 55)
    print()
    
    if not is_admin():
        print("[!] Run as Administrator required.")
        print("[*] Relaunching elevated...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    
    while True:
        print("\n--- MAIN MENU ---")
        print("  [1] Auto-Detect & Activate (KMS)")
        print("  [2] Manual Key Install + KMS Activate")
        print("  [3] HWID Permanent Activation (MAS)")
        print("  [4] Check Current Activation Status")
        print("  [5] Exit")
        
        choice = input("\n[?] Select: ")
        
        if choice == "1":
            edition = auto_detect_edition()
            print(f"    Detected: {edition}")
            if "Professional" in edition:
                key = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
            elif "Enterprise" in edition:
                key = "NPPR9-FWDCX-D2C8J-H872K-2YT43"
            elif "Home" in edition:
                key = "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"
            else:
                key = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
            
            print(f"[*] Installing key: {key}")
            run_cmd(f'slmgr /ipk {key}')
            set_kms_server()
            
        elif choice == "2":
            install_kms_key()
            set_kms_server()
            
        elif choice == "3":
            activate_generic_ticket()
            
        elif choice == "4":
            status = check_activation_status()
            print(f"\n[*] Status:\n    {status}")
            
        elif choice == "5":
            print("[*] Later boss.")
            break
        
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    main()
