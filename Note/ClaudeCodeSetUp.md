# Claude Code 安裝指南 (Windows)

## 📋 目錄
- [系統需求](#系統需求)
- [前置準備：安裝 Node.js](#前置準備安裝-nodejs)
- [安裝 Claude Code](#安裝-claude-code)
- [驗證安裝](#驗證安裝)
- [認證與啟動](#認證與啟動)
- [常見問題排除](#常見問題排除)

---

## 系統需求

- **作業系統**: Windows 10+ (建議使用 WSL 或 Git Bash)
- **Node.js**: 18.0 或更高版本
- **記憶體**: 建議 4GB RAM 以上
- **網路**: 需要穩定的網路連線

---

## 前置準備：安裝 Node.js

### 1. 檢查現有 Node.js 版本

開啟 **命令提示字元 (CMD)** 或 **PowerShell**，執行：

```bash
node --version
```

如果顯示 `v18.x.x` 或更高版本，可以跳過安裝步驟。

### 2. 下載並安裝 Node.js

如果沒有安裝或版本過舊：

1. 前往 [Node.js 官方網站](https://nodejs.org/)
2. 下載 **LTS 版本**（推薦 v20.x）
3. 執行安裝程式，一路點選「下一步」
4. **重新開啟終端機**（重要！）

### 3. 驗證安裝

```bash
node --version
npm --version
```

應該會看到類似：
```
v20.10.0
10.2.3
```

---

## 安裝 Claude Code

### 方法一：使用 npm（推薦）

在終端機執行以下指令：

```bash
npm install -g @anthropic-ai/claude-code
```

> ⚠️ **重要提醒**：
> - **不要使用** `sudo npm install -g`
> - 如果遇到權限錯誤，請參考[常見問題排除](#常見問題排除)

### 方法二：使用 Native Binary（進階）

**macOS/Linux:**
```bash
curl -fsSL https://download.claude.ai/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://download.claude.ai/install.ps1 | iex
```

---

## 驗證安裝

安裝完成後，執行以下指令確認：

```bash
claude --version
```

或使用診斷工具：

```bash
claude doctor
```

應該會顯示安裝類型、版本號和系統資訊。

---

## 認證與啟動

### 1. 進入專案目錄

```bash
cd C:\Git\Schedule
```

### 2. 啟動 Claude Code

```bash
claude
```

### 3. 選擇認證方式

首次啟動會提示選擇認證方式：

#### 選項 1: Anthropic Console（預設）
- 瀏覽器會自動開啟
- 完成 OAuth 登入流程
- 需要在 [console.anthropic.com](https://console.anthropic.com/) 設定計費

#### 選項 2: Claude Pro/Max 訂閱
- 如果你有 Claude Pro ($20/月) 或 Max ($100/月) 訂閱
- 使用現有帳號登入
- 性價比最高

#### 選項 3: 企業平台
- Amazon Bedrock
- Google Vertex AI
- 適合企業部署

### 4. 開始使用

認證完成後，你會看到互動式提示符：

```
Claude Code v2.0.5
Ready to help! What would you like to work on?
>
```

---

## 常見問題排除

### ❌ 問題 1: `claude` 指令找不到

**可能原因**: Node.js 全域套件路徑未加入 PATH

**解決方法**:

```bash
# 檢查全域套件安裝路徑
npm config get prefix

# 將該路徑加入系統 PATH
# Windows: 手動加入環境變數
# 路徑通常是: C:\Users\[你的使用者名稱]\AppData\Roaming\npm
```

### ❌ 問題 2: 權限錯誤 (Permission Denied)

**解決方法**: 配置 npm 使用使用者目錄

```bash
# 建立全域套件目錄
mkdir %USERPROFILE%\.npm-global

# 配置 npm
npm config set prefix %USERPROFILE%\.npm-global

# 將路徑加入 PATH（手動或使用以下指令）
setx PATH "%PATH%;%USERPROFILE%\.npm-global"

# 重新安裝
npm install -g @anthropic-ai/claude-code
```

### ❌ 問題 3: Windows 相容性問題

Claude Code 在 Windows 上建議使用以下環境：

**選項 A: WSL (Windows Subsystem for Linux)**

```bash
# 安裝 WSL
wsl --install

# 重啟電腦後，在 WSL 中安裝
npm install -g @anthropic-ai/claude-code
```

**選項 B: Git Bash**

1. 安裝 [Git for Windows](https://git-scm.com/download/win)
2. 使用 Git Bash 終端機
3. 設定環境變數（如果需要）：
   ```bash
   export CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
   ```

### ❌ 問題 4: 網路連線問題

如果你在企業環境或使用代理伺服器：

```bash
# 設定 npm 代理
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080
```

---

## 🎯 快速測試

安裝完成後，試試這些指令：

```bash
# 檢查版本
claude --version

# 系統診斷
claude doctor

# 在專案中啟動
cd C:\Git\Schedule
claude

# 詢問 Claude
> 解釋這個專案的結構
> 幫我建立一個 FastAPI 應用
> 查看所有 Python 檔案
```

---

## 📚 進階配置

### 配置檔案位置

Claude Code 的配置檔案位於：
- **Windows**: `%USERPROFILE%\.claude\`
- **macOS/Linux**: `~/.claude/`

### 常用設定

編輯 `~/.claude/settings.json`:

```json
{
  "autoUpdate": true,
  "theme": "dark",
  "editor": "code",
  "modelPreference": "claude-sonnet-4-5"
}
```

---

## 🔗 相關資源

- [Claude Code 官方文件](https://docs.claude.com/en/docs/claude-code/setup)
- [Anthropic Console](https://console.anthropic.com/)
- [GitHub Repository](https://github.com/anthropics/claude-code)
- [npm 套件頁面](https://www.npmjs.com/package/@anthropic-ai/claude-code)

---

## ✅ 安裝檢查清單

- [ ] Node.js 18+ 已安裝並驗證
- [ ] npm 全域套件路徑已加入 PATH
- [ ] Claude Code 已成功安裝
- [ ] `claude --version` 指令可執行
- [ ] `claude doctor` 診斷通過
- [ ] 已完成認證流程
- [ ] 可在專案目錄啟動 Claude

---

**最後更新**: 2025-10-03