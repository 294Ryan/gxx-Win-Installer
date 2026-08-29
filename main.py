import subprocess
import sys
import os
import ctypes
import winreg
from colorama import Fore, init

init(autoreset=True)
WINGET_PACKAGE_ID = "MSYS2.MSYS2"
MSYS2_DEFAULT_PATH = r"C:\msys64"


### Theme ###
class TextTheme:
    ERROR   = Fore.LIGHTRED_EX
    INFO    = Fore.CYAN
    SUCCESS = Fore.GREEN
    NONE    = Fore.RESET
    TITLE   = Fore.BLUE


### Messager ###
def showInfo(content):
    print(TextTheme.INFO + f"[*] {content}")

def showSuccess(content):
    print(TextTheme.SUCCESS + f"[+] {content}")

def showError(content):
    print(TextTheme.ERROR + f"[!] {content}")

def waitEnter(msg="Press [Enter] to continue..."):
    input(TextTheme.INFO + f"[>] {msg}" + Fore.RESET)


### Helpers ###
def run(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


### Check ###
def checkGpp():
    return run("where g++").returncode == 0

def checkWinget():
    return run("winget --version").returncode == 0

def getSystemPath():
    regPath = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regPath, access=winreg.KEY_READ) as key:
        value, _ = winreg.QueryValueEx(key, "Path")
    return value

def setSystemPath(newPath):
    regPath = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regPath, access=winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, newPath)
    # 廣播 WM_SETTINGCHANGE 通知系統環境變數已更新
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 2, 5000, None
    )


### Install ###
def installViaMsys2():
    showInfo("Installing MSYS2 via winget...")    # 透過 winget 安裝 MSYS2
    result = subprocess.run(
        f'winget install --id {WINGET_PACKAGE_ID} --silent --accept-package-agreements --accept-source-agreements',
        shell=True
    )
    WINGET_ALREADY_INSTALLED = 0x8A150049
    if result.returncode not in (0, WINGET_ALREADY_INSTALLED):
        showError("Failed to install MSYS2 via winget. Please download manually at https://www.msys2.org")    # winget 安裝 MSYS2 失敗 請手動下載
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)

    showInfo("Installing mingw-w64 g++ via MSYS2...")    # 透過 MSYS2 安裝 mingw-w64 g++
    msys2Bash = os.path.join(MSYS2_DEFAULT_PATH, "usr", "bin", "bash.exe")
    if not os.path.exists(msys2Bash):
        showError(f"MSYS2 bash not found: {msys2Bash}. Please verify the installation path.")    # 找不到 MSYS2 bash 請確認安裝路徑
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)

    pacmanCmd = f'"{msys2Bash}" -lc "pacman -S --noconfirm mingw-w64-ucrt-x86_64-gcc"'
    result = subprocess.run(pacmanCmd, shell=True)
    if result.returncode != 0:
        showError("Failed to install g++ via pacman. Please run manually in MSYS2 terminal: pacman -S mingw-w64-ucrt-x86_64-gcc")    # pacman 安裝 g++ 失敗 請手動在 MSYS2 終端執行
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)


### PATH ###
def ensurePath(binPath):
    showInfo(f"Checking if PATH contains {binPath}...")    # 檢查 PATH 是否包含指定路徑
    try:
        currentPath = getSystemPath()
    except OSError as e:
        showError(f"Failed to read system PATH: {e}")    # 讀取系統 PATH 失敗
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)

    # 分段比對 避免子字串誤判（如 bin 誤判成 bin2）
    segments = [s.strip() for s in currentPath.split(";")]
    if any(s.lower() == binPath.lower() for s in segments):
        showSuccess("PATH already contains the target. No changes needed.")    # PATH 已包含 無需修改
        return

    newPath = currentPath.rstrip(";") + ";" + binPath
    try:
        setSystemPath(newPath)
    except OSError as e:
        showError(f"Failed to write system PATH: {e}")    # 寫入系統 PATH 失敗
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)
    showSuccess(f"Successfully added {binPath} to system PATH.")    # 已將路徑加入系統 PATH


### Main ###
def main():
    print(TextTheme.TITLE + r"""
  __ _   _     _                                              
 / _` |_| |_ _| |_                                            
| (_| |_   _|_   _|                                           
 \__, | |_|   |_|       (For Windows 10 1709 Build 16299+)
 |___/        _          ___           _        _ _           
   / \  _   _| |_ ___   |_ _|_ __  ___| |_ __ _| | | ___ _ __ 
  / _ \| | | | __/ _ \   | || '_ \/ __| __/ _` | | |/ _ \ '__|
 / ___ \ |_| | || (_) |  | || | | \__ \ || (_| | | |  __/ |   
/_/   \_\__,_|\__\___/  |___|_| |_|___/\__\__,_|_|_|\___|_|   

""")
    waitEnter("Press [Enter] to start installing...")
    showInfo("Start installing.")

    # 需要管理員權限才能寫入系統 PATH
    if not ctypes.windll.shell32.IsUserAnAdmin():
        showError("Please run this script as Administrator (Right-click -> Run as administrator).")    # 請以系統管理員身份執行
        waitEnter("Press [Enter] to exit...")
        sys.exit(1)

    ### Step 1: 檢查 g++ ###
    showInfo("Checking if g++ is already installed...")    # 檢查 g++ 是否已安裝
    if checkGpp():
        showSuccess("g++ already exists. Skipping installation.")    # g++ 已存在 跳過安裝
    else:
        ### Step 2: 確認 winget 可用 ###
        showInfo("Checking if winget is available...")    # 檢查 winget 是否可用
        if not checkWinget():
            showError("winget not found. Please ensure Windows version >= 1709 or install App Installer manually.")    # 找不到 winget 請確認 Windows 版本或手動安裝
            waitEnter("Press [Enter] to exit...")
            sys.exit(1)
        showSuccess("winget is available.")    # winget 可用

        ### Step 3: 安裝 ###
        installViaMsys2()

    ### Step 4: 確保 PATH 正確 ###
    mingwBin = os.path.join(MSYS2_DEFAULT_PATH, "ucrt64", "bin")
    ensurePath(mingwBin)

    print(TextTheme.NONE + "\n=== Done ===")    # 完成
    print("Please restart VSCode or your terminal to apply the new PATH.")    # 請重新開啟 VSCode 或終端機以套用新的 PATH
    print("Verify with: g++ --version")    # 驗證指令

    waitEnter("Press [Enter] to exit...")


if __name__ == "__main__":
    main()