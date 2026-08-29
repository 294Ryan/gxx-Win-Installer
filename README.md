# ***G++ Windows 自動安裝器***

## **目錄**
- [專案概述](#專案概述)
- [重點特色](#重點特色)
- [使用說明](#使用說明)
- [開發須知](#開發須知)
- [使用技術](#使用技術)
- [專案結構](#專案結構)
- [備註](#備註)

---

## **專案概述**
在 Windows 上自動安裝 g++（UCRT64）並將其寫入系統 PATH，讓 VSCode 可直接使用，省去手動配置 MSYS2 環境的繁瑣流程。

---

## **重點特色**
- 自動偵測 g++ 是否已存在，避免重複安裝
- 透過 **winget** 安裝 MSYS2，無需手動下載
- 安裝完成後自動將 `C:\msys64\ucrt64\bin` 寫入系統 PATH
- 寫入後即時廣播環境變數更新，重開 VSCode 即可使用
- 每個步驟皆有彩色狀態提示，錯誤時暫停等待確認後再退出

---

## **使用說明**
請至 [Release](https://github.com/294Ryan/gxx-Win-Installer/releases) 下載並解壓縮。

- **啟動：**
  - 直接執行執行檔：
    以**系統管理員身份**執行 `.exe`，如 `gxx-Win-Installer_vX.X.X.exe`
  - 由程式碼啟動：
    ```
    python main.py
    ```
    > 注意：由程式碼啟動同樣需要以**系統管理員身份**開啟終端機。

- **執行流程：**
1. **檢查 g++：** 偵測系統是否已安裝 g++，若已存在則跳過安裝步驟。
2. **安裝 MSYS2：** 透過 winget 自動下載並安裝 MSYS2。
3. **安裝 g++：** 透過 MSYS2 的 pacman 安裝 `mingw-w64-ucrt-x86_64-gcc`。
4. **寫入 PATH：** 將 `C:\msys64\ucrt64\bin` 加入系統環境變數並即時廣播更新。

---

## **開發須知**
1. 請先閱讀以下開發須知並遵守所用條款。
2. 請運行以下指令複製此倉庫至您的本地電腦：
```
git clone https://github.com/294Ryan/gxx-Win-Installer.git
```
3. 使用語言：
   - Python 3.x
4. 安裝必要工具：
   - Python 模組：請運行以下指令
     ```
     pip install -r requirements.txt
     ```
5. 使用技術：請參見 [使用技術](#使用技術)
6. 專案結構：請參見 [專案結構](#專案結構)

---

## **使用技術**
- **winget**：Windows 內建套件管理器，用於自動下載並安裝 MSYS2
- **MSYS2 / pacman**：透過 pacman 安裝 `mingw-w64-ucrt-x86_64-gcc`，採用 UCRT64 runtime 以確保與現代 Windows 環境的相容性
- **winreg**：直接讀寫 Windows 登錄檔，將路徑永久寫入系統 PATH
- **SendMessageTimeoutW**：廣播 `WM_SETTINGCHANGE`，通知系統環境變數已更新，無需重新登入
- **colorama**：跨平台終端機彩色輸出，提供狀態提示

---

## **專案結構**
```
gxx-Win-Installer/
├── .gitignore          # 指定 Git 忽略上傳的檔案
├── icon.ico            # 執行檔圖示
├── LICENSE             # MIT License
├── main.py             # 主程式
├── main.spec           # PyInstaller 打包設定
├── README.md           # 專案說明文件
└── requirements.txt    # Python 相依套件清單
```

---

## **備註**
- 維護者：294Ryan - [Github](https://github.com/294Ryan)
- 使用條款：`MIT License`
- <!> 敬請在本專案所用條款之允許範圍內進行使用。且任何因操作疏失或不當使用造成的後果請自負。

---

# ***G++ Windows Auto Installer***

## **Table of Contents**
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Instructions for Use](#instructions-for-use)
- [Development Guidelines](#development-guidelines)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Notes](#notes)

---

## **Project Overview**
Automatically installs g++ (UCRT64) on Windows and writes it to the system PATH, enabling direct use in VSCode without manually configuring the MSYS2 environment.

---

## **Key Features**
- Detects existing g++ installation to avoid redundant setup
- Installs MSYS2 via **winget** — no manual download required
- Automatically adds `C:\msys64\ucrt64\bin` to the system PATH
- Broadcasts environment variable updates immediately after writing — just restart VSCode
- Color-coded status output at every step; pauses on error before exiting

---

## **Instructions for Use**
Download and extract the package from [Release](https://github.com/294Ryan/gxx-Win-Installer/releases).

- **Launch:**
  - Execute the executable file directly:
    Run the `.exe` file **as Administrator**, e.g. `gxx-Win-Installer_vX.X.X.exe`
  - Launch from code:
    ```
    python main.py
    ```
    > Note: Running from code also requires opening the terminal **as Administrator**.

- **Execution Flow:**
1. **Check g++:** Detects whether g++ is already installed. If found, skips the installation steps.
2. **Install MSYS2:** Automatically downloads and installs MSYS2 via winget.
3. **Install g++:** Installs `mingw-w64-ucrt-x86_64-gcc` via MSYS2's pacman.
4. **Write PATH:** Adds `C:\msys64\ucrt64\bin` to the system environment variables and broadcasts the update immediately.

---

## **Development Guidelines**
1. Please read the following development guidelines and comply with all applicable terms.
2. Run the following command to clone this repository to your local machine:
```
git clone https://github.com/294Ryan/gxx-Win-Installer.git
```
3. Programming Languages:
   - Python 3.x
4. Required Tool Installation:
   - Python Modules: Please run the following command
     ```
     pip install -r requirements.txt
     ```
5. Technologies Used: Please refer to [Technologies Used](#technologies-used)
6. Project Structure: Please refer to [Project Structure](#project-structure)

---

## **Technologies Used**
- **winget**: Windows built-in package manager, used to automatically download and install MSYS2
- **MSYS2 / pacman**: Installs `mingw-w64-ucrt-x86_64-gcc` via pacman, using the UCRT64 runtime for compatibility with modern Windows environments
- **winreg**: Reads and writes the Windows registry directly to permanently add the path to the system PATH
- **SendMessageTimeoutW**: Broadcasts `WM_SETTINGCHANGE` to notify the system of environment variable updates without requiring a re-login
- **colorama**: Cross-platform terminal color output for status indication

---

## **Project Structure**
```
gxx-Win-Installer/
├── .gitignore          # Specifies files for Git to ignore
├── icon.ico            # Executable icon
├── LICENSE             # MIT License
├── main.py             # Main script
├── main.spec           # PyInstaller build configuration
├── README.md           # Project documentation
└── requirements.txt    # Python dependency list
```

---

## **Notes**
- Maintainer: 294Ryan - [Github](https://github.com/294Ryan)
- Terms of Use: `MIT License`
- <!> Please use this product only within the scope permitted by the terms and conditions of this project. You are solely responsible for any consequences arising from operational errors or improper use.
