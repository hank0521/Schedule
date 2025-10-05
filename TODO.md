# Schedule 專案待辦事項

## 📋 開發任務清單

### 階段一：FastAPI 基礎架構
- [ ] 建立 FastAPI 專案基礎架構
  - [ ] 安裝依賴套件 (FastAPI, SQLAlchemy, asyncpg, pydantic 等)
  - [ ] 設定專案目錄結構
  - [ ] 建立資料庫連線配置
  - [ ] 設定環境變數管理
  - [ ] 建立基礎 models, schemas, routers 架構

### 階段二：排程任務管理 API (CRUD)
- [ ] 實作 HTTP 排程任務的 CRUD API
  - [ ] POST `/api/schedule/http` - 建立任務
  - [ ] GET `/api/schedule/http` - 查詢列表
  - [ ] GET `/api/schedule/http/{id}` - 查詢單一任務
  - [ ] PUT `/api/schedule/http/{id}` - 更新任務
  - [ ] DELETE `/api/schedule/http/{id}` - 刪除任務
  - [ ] PATCH `/api/schedule/http/{id}/status` - 啟用/停用任務

- [ ] 實作 Mail 排程任務的 CRUD API
  - [ ] POST `/api/schedule/mail` - 建立任務
  - [ ] GET `/api/schedule/mail` - 查詢列表
  - [ ] GET `/api/schedule/mail/{id}` - 查詢單一任務
  - [ ] PUT `/api/schedule/mail/{id}` - 更新任務
  - [ ] DELETE `/api/schedule/mail/{id}` - 刪除任務
  - [ ] PATCH `/api/schedule/mail/{id}/status` - 啟用/停用任務

- [ ] 實作 FTP 排程任務的 CRUD API
  - [ ] POST `/api/schedule/ftp` - 建立任務
  - [ ] GET `/api/schedule/ftp` - 查詢列表
  - [ ] GET `/api/schedule/ftp/{id}` - 查詢單一任務
  - [ ] PUT `/api/schedule/ftp/{id}` - 更新任務
  - [ ] DELETE `/api/schedule/ftp/{id}` - 刪除任務
  - [ ] PATCH `/api/schedule/ftp/{id}/status` - 啟用/停用任務

### 階段三：執行服務實作 (供 N8N 呼叫)
- [ ] 實作 HTTP 請求執行服務
  - [ ] POST `/api/execute/http/{id}` - 執行 HTTP 任務
  - [ ] 實作重試機制
  - [ ] 實作執行狀態更新
  - [ ] 實作結果記錄

- [ ] 實作 Email 發送服務
  - [ ] POST `/api/execute/mail/{id}` - 執行 Mail 任務
  - [ ] 實作 SMTP 連線
  - [ ] 實作附件處理
  - [ ] 實作多收件者處理

- [ ] 實作 FTP 傳輸服務
  - [ ] POST `/api/execute/ftp/{id}` - 執行 FTP 任務
  - [ ] 支援 FTP/FTPS/SFTP 協定
  - [ ] 實作萬用字元檔案選取
  - [ ] 實作上傳後刪除機制

- [ ] 實作批次執行 API
  - [ ] POST `/api/execute/pending` - 批次執行待執行任務

### 階段四：監控與記錄 API
- [ ] 實作例外記錄查詢 API
  - [ ] GET `/api/exceptions` - 查詢例外列表
  - [ ] GET `/api/exceptions/{id}` - 查詢單一例外
  - [ ] PATCH `/api/exceptions/{id}/resolve` - 標記為已解決

- [ ] 實作執行歷史查詢 API
  - [ ] GET `/api/history` - 查詢執行歷史列表
  - [ ] GET `/api/history/{id}` - 查詢單一執行記錄
  - [ ] GET `/api/history/statistics` - 查詢執行統計

### 階段五：系統功能
- [ ] 實作排程任務執行狀態更新機制
  - [ ] 自動更新 NextExecuteTime
  - [ ] 執行狀態流轉邏輯
  - [ ] 執行計數器更新

- [ ] 實作健康檢查與監控
  - [ ] GET `/health` - API 健康檢查
  - [ ] GET `/health/db` - 資料庫連線檢查
  - [ ] GET `/api/status` - 系統狀態總覽

- [ ] 實作安全性機制
  - [ ] API 認證 (Bearer Token / API Key)
  - [ ] 密碼加密儲存 (SMTP/FTP 密碼)
  - [ ] 密碼解密機制

### 階段六：測試與文件
- [ ] 撰寫單元測試
  - [ ] CRUD API 測試
  - [ ] 執行服務測試
  - [ ] 資料驗證測試

- [ ] 撰寫整合測試
  - [ ] 端對端執行流程測試
  - [ ] 錯誤處理測試

- [ ] 建立 API 文件
  - [ ] Swagger / OpenAPI 文件
  - [ ] 使用範例
  - [ ] 錯誤碼說明

### 階段七：N8N 工作流程設定
- [ ] 建立 N8N 工作流程
  - [ ] 資料庫輪詢觸發器
  - [ ] HTTP 任務執行流程
  - [ ] Mail 任務執行流程
  - [ ] FTP 任務執行流程
  - [ ] 錯誤處理與通知

---

## 🔌 API 規格總覽

### 1. HTTP 排程任務管理 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/schedule/http` | 建立 HTTP 排程任務 |
| GET | `/api/schedule/http` | 查詢 HTTP 排程任務列表 |
| GET | `/api/schedule/http/{id}` | 查詢單一 HTTP 排程任務 |
| PUT | `/api/schedule/http/{id}` | 更新 HTTP 排程任務 |
| DELETE | `/api/schedule/http/{id}` | 刪除 HTTP 排程任務 |
| PATCH | `/api/schedule/http/{id}/status` | 啟用/停用 HTTP 排程任務 |

### 2. Mail 排程任務管理 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/schedule/mail` | 建立 Mail 排程任務 |
| GET | `/api/schedule/mail` | 查詢 Mail 排程任務列表 |
| GET | `/api/schedule/mail/{id}` | 查詢單一 Mail 排程任務 |
| PUT | `/api/schedule/mail/{id}` | 更新 Mail 排程任務 |
| DELETE | `/api/schedule/mail/{id}` | 刪除 Mail 排程任務 |
| PATCH | `/api/schedule/mail/{id}/status` | 啟用/停用 Mail 排程任務 |

### 3. FTP 排程任務管理 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/schedule/ftp` | 建立 FTP 排程任務 |
| GET | `/api/schedule/ftp` | 查詢 FTP 排程任務列表 |
| GET | `/api/schedule/ftp/{id}` | 查詢單一 FTP 排程任務 |
| PUT | `/api/schedule/ftp/{id}` | 更新 FTP 排程任務 |
| DELETE | `/api/schedule/ftp/{id}` | 刪除 FTP 排程任務 |
| PATCH | `/api/schedule/ftp/{id}/status` | 啟用/停用 FTP 排程任務 |

### 4. 執行服務 API (供 N8N 呼叫)
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/execute/http/{id}` | 執行 HTTP 請求任務 |
| POST | `/api/execute/mail/{id}` | 執行 Mail 發送任務 |
| POST | `/api/execute/ftp/{id}` | 執行 FTP 傳輸任務 |
| POST | `/api/execute/pending` | 批次執行待執行任務 |

### 5. 例外記錄查詢 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/exceptions` | 查詢例外記錄列表 |
| GET | `/api/exceptions/{id}` | 查詢單一例外記錄 |
| PATCH | `/api/exceptions/{id}/resolve` | 標記例外為已解決 |

### 6. 執行歷史查詢 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/history` | 查詢執行歷史列表 |
| GET | `/api/history/{id}` | 查詢單一執行歷史 |
| GET | `/api/history/statistics` | 查詢執行統計 |

### 7. 健康檢查與監控 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/health` | API 健康檢查 |
| GET | `/health/db` | 資料庫連線檢查 |
| GET | `/api/status` | 系統狀態總覽 |

---

## 📝 開發注意事項

### 資料驗證
- Cron 表達式驗證
- Email 格式驗證
- URL 格式驗證
- 檔案路徑驗證

### 安全性
- SMTP 和 FTP 密碼需使用加密儲存 (建議使用 Fernet 或 AES)
- 所有查詢使用參數化查詢防止 SQL 注入
- API 認證機制 (Bearer Token 或 API Key)

### 效能優化
- 定期清理 `tblScheduleExecutionHistory` 和 `tblScheduleException` 舊資料
- 定期重建索引維持查詢效能
- 考慮使用 PostgreSQL 資料表分割功能

### 錯誤處理
- 統一的錯誤回應格式
- 詳細的錯誤日誌記錄
- 例外記錄自動寫入 `tblScheduleException`

---

**最後更新**: 2025-10-05
