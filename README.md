# Schedule

## 1. 專案內容

Schedule 是一個自動化排程系統，透過整合 N8N、Python FastAPI 和 SQL Server，實現資料驅動的自動化通知服務。只需將資料寫入資料庫，系統即可自動執行多種通知方式，包括：

- **Email 發送**：自動寄送郵件通知
- **FTP 傳輸**：檔案自動上傳至 FTP 伺服器
- **HTTP 請求**：觸發 Webhook 或 API 呼叫

此系統適用於定期報表發送、系統通知、資料同步等自動化場景。

## 2. 專案架構

```
Schedule/
├── API/              # Python FastAPI 應用程式
│   └── ...          # API 服務相關程式碼
├── N8N/             # N8N 工作流程設定
│   └── ...          # 自動化流程配置檔案
└── Note/            # 專案文件與筆記
```

### 技術堆疊

- **N8N**：工作流程自動化引擎，負責監聽資料庫變更並觸發相應動作
- **Python FastAPI**：提供 RESTful API 服務，處理業務邏輯
- **SQL Server**：主要資料庫，儲存排程任務及相關資料

### 運作流程

1. 使用者/系統將排程任務資料寫入 SQL Server
2. N8N 監聽資料庫變更（透過輪詢或觸發器）
3. N8N 根據任務類型執行對應的工作流程
4. 透過 FastAPI 處理複雜的業務邏輯（如需要）
5. 執行最終動作（發送 Email/FTP 上傳/HTTP 請求等）

## 3. GitFlow 規範

### 分支策略

- **master**：主分支，包含穩定的生產環境程式碼
- **develop**：開發分支，整合所有功能開發
- **feature/**：功能分支，格式：`feature/功能名稱`（例如：`feature/email-notification`）
- **bugfix/**：Bug 修復分支，格式：`bugfix/問題描述`（例如：`bugfix/ftp-connection-error`）
- **hotfix/**：緊急修復分支，格式：`hotfix/問題描述`
- **release/**：發布分支，格式：`release/版本號`（例如：`release/v1.0.0`）

### 工作流程

1. 從 `develop` 分支建立 `feature/` 分支進行開發
2. 完成後發起 Pull Request 合併回 `develop`
3. 測試通過後，從 `develop` 建立 `release/` 分支
4. Release 分支測試完成後，合併至 `master` 並打上版本標籤
5. 同時將 `release/` 合併回 `develop`
6. 生產環境緊急問題從 `master` 建立 `hotfix/` 分支，修復後合併回 `master` 和 `develop`

### Commit 訊息規範

使用語意化的 commit 訊息：

```
<type>: <subject>

<body>
```

**Type 類型：**
- `feat`：新功能
- `fix`：Bug 修復
- `docs`：文件更新
- `style`：程式碼格式調整（不影響功能）
- `refactor`：程式碼重構
- `test`：測試相關
- `chore`：建置流程或輔助工具變更

**範例：**
```
feat: 新增 Email 發送功能

- 實作 SMTP 郵件發送服務
- 支援附件功能
- 新增郵件模板系統
```

## 4. 開發規範

### Python / FastAPI 規範

- **編碼風格**：遵循 PEP 8 規範
- **命名規則**：
  - 變數、函式：使用 `snake_case`
  - 類別：使用 `PascalCase`
  - 常數：使用 `UPPER_SNAKE_CASE`
- **文件字串**：所有函式和類別必須包含 docstring
- **型別提示**：使用 Python Type Hints 標註參數和回傳值
- **錯誤處理**：適當使用 try-except，記錄錯誤日誌

### N8N 工作流程規範

- **命名**：工作流程名稱清楚描述功能（例如：`發送每日報表郵件`）
- **註解**：複雜節點添加說明註記
- **錯誤處理**：設定錯誤處理節點，避免工作流程中斷
- **版本控制**：匯出工作流程 JSON 檔案至 `N8N/` 目錄

### 資料庫規範

- **命名**：
  - 資料表：使用 `PascalCase`（例如：`ScheduleTasks`）
  - 欄位：使用 `PascalCase`（例如：`TaskId`、`CreatedDate`）
- **索引**：為常用查詢欄位建立適當索引
- **文件**：維護資料庫 Schema 文件

### 程式碼審查

- 所有程式碼必須經過至少一位團隊成員審查
- Pull Request 需包含：
  - 功能說明
  - 測試結果
  - 相關截圖（如適用）

### 測試規範

- **單元測試**：核心業務邏輯需撰寫單元測試
- **整合測試**：API 端點需有整合測試
- **測試覆蓋率**：目標達到 80% 以上

### 環境設定

- 使用 `.env` 檔案管理環境變數
- `.env` 檔案不得提交至版本控制
- 提供 `.env.example` 作為範本

---

## 快速開始

（待補充：安裝步驟、設定說明、啟動指令等）

## 授權

（待補充：專案授權資訊）
