# Schedule 專案待辦事項

## 🔴 高優先級（核心功能）

### 1. 資料庫初始化
- [ ] **建立 `Database/01_create_tables.sql`**
  - [ ] tblScheduleHttp 資料表建立語句
  - [ ] tblScheduleMail 資料表建立語句
  - [ ] tblScheduleFTP 資料表建立語句
  - [ ] tblScheduleException 資料表建立語句
  - [ ] tblScheduleExecutionHistory 資料表建立語句
  - [ ] 所有索引建立
  - [ ] 欄位註解說明
- [ ] 測試資料庫初始化流程
  - [ ] 啟動 PostgreSQL 容器
  - [ ] 驗證資料表自動建立
  - [ ] 檢查索引是否正確

### 2. Python FastAPI 服務開發
- [ ] **建立 API 專案結構**
  - [ ] 建立 `API/` 目錄
  - [ ] 設定專案結構（main.py, routers, models, schemas, services）
  - [ ] 建立 `requirements.txt`
  - [ ] 設定 FastAPI 基本配置
- [ ] **資料庫連線模組**
  - [ ] 設定 SQLAlchemy ORM
  - [ ] 建立資料庫連線池
  - [ ] 建立 Models（對應 5 個資料表）
- [ ] **API 端點開發**
  - [ ] HTTP 排程 CRUD API
  - [ ] Email 排程 CRUD API
  - [ ] FTP 排程 CRUD API
  - [ ] 執行歷史查詢 API
  - [ ] 例外記錄查詢 API
- [ ] **核心功能實作**
  - [ ] HTTP 請求執行服務
  - [ ] Email 發送服務（SMTP）
  - [ ] FTP 檔案傳輸服務
  - [ ] 重試機制
  - [ ] 錯誤處理與日誌
- [ ] **API 文件**
  - [ ] Swagger/OpenAPI 自動文件
  - [ ] API 使用範例

### 3. N8N 工作流程設計
- [ ] **建立 N8N 容器**
  - [ ] 在 `docker-compose.yml` 新增 N8N 服務
  - [ ] 設定 N8N 環境變數
  - [ ] 配置 N8N 與 PostgreSQL 連線
- [ ] **工作流程開發**
  - [ ] HTTP 排程監聽與執行流程
  - [ ] Email 排程監聽與執行流程
  - [ ] FTP 排程監聽與執行流程
  - [ ] 錯誤處理與重試流程
  - [ ] 執行結果記錄流程
- [ ] **匯出工作流程**
  - [ ] 建立 `N8N/workflows/` 目錄
  - [ ] 匯出所有工作流程為 JSON
  - [ ] 撰寫工作流程說明文件

## 🟡 中優先級（完善功能）

### 4. 測試
- [ ] **單元測試**
  - [ ] API 端點測試
  - [ ] 服務邏輯測試
  - [ ] 資料庫操作測試
- [ ] **整合測試**
  - [ ] 端到端流程測試
  - [ ] N8N 工作流程測試
- [ ] **測試覆蓋率**
  - [ ] 設定 pytest-cov
  - [ ] 達到 80% 覆蓋率目標

### 5. 部署與 CI/CD
- [ ] **Docker 完整化**
  - [ ] 建立 FastAPI Dockerfile
  - [ ] 更新 docker-compose.yml（整合 API + N8N + PostgreSQL）
  - [ ] 多階段建置優化
- [ ] **CI/CD 流程**
  - [ ] 設定 GitHub Actions
  - [ ] 自動化測試流程
  - [ ] 自動化部署流程

### 6. 監控與日誌
- [ ] **日誌系統**
  - [ ] 整合 Python logging
  - [ ] 結構化日誌輸出
  - [ ] 日誌等級設定
- [ ] **監控告警**
  - [ ] 例外數量監控
  - [ ] 執行失敗率告警
  - [ ] 系統效能監控

## 🟢 低優先級（優化項目）

### 7. 文件完善
- [ ] **快速開始指南**
  - [ ] 完成 README.md「快速開始」章節
  - [ ] 安裝步驟說明
  - [ ] 設定檔案範例
  - [ ] 啟動指令說明
- [ ] **開發文件**
  - [ ] API 開發規範
  - [ ] N8N 工作流程開發規範
  - [ ] 常見問題 FAQ
- [ ] **範例與教學**
  - [ ] 使用範例程式碼
  - [ ] 常見場景實作教學

### 8. 安全性強化
- [ ] **密碼加密**
  - [ ] SmtpPassword 加密儲存
  - [ ] FtpPassword 加密儲存
  - [ ] 密鑰管理機制
- [ ] **API 安全**
  - [ ] JWT 認證
  - [ ] API Rate Limiting
  - [ ] CORS 設定

### 9. 效能優化
- [ ] **資料庫優化**
  - [ ] 定期清理歷史記錄機制
  - [ ] 資料表分割（如需要）
  - [ ] 索引效能分析
- [ ] **快取機制**
  - [ ] Redis 整合
  - [ ] 查詢結果快取

### 10. 功能擴展
- [ ] **排程增強**
  - [ ] Cron 表達式驗證
  - [ ] 視覺化排程設定介面
  - [ ] 排程衝突檢測
- [ ] **通知方式擴展**
  - [ ] Slack 通知
  - [ ] Webhook 通知
  - [ ] SMS 簡訊通知
- [ ] **前端管理介面**
  - [ ] 排程任務管理頁面
  - [ ] 執行歷史查詢介面
  - [ ] Dashboard 儀表板

## 📋 立即要做的 3 件事

1. **建立 `Database/01_create_tables.sql`** - 完成資料庫初始化
2. **建立 API 專案結構** - 建立 `API/` 目錄並設定 FastAPI
3. **整合 N8N 到 Docker Compose** - 讓系統可以完整啟動

---

## 🏷️ 標籤說明
- 🔴 高優先級：核心功能，必須完成
- 🟡 中優先級：重要功能，應盡快完成
- 🟢 低優先級：優化項目，可後續規劃

## 📅 更新日期
最後更新：2025-10-05
