# Schedule 資料表結構說明文件

## 目錄
1. [tblScheduleHttp - HTTP 請求排程表](#1-tblschedulehttp---http-請求排程表)
2. [tblScheduleMail - Email 發送排程表](#2-tblschedulemail---email-發送排程表)
3. [tblScheduleFTP - FTP 傳輸排程表](#3-tblscheduleftp---ftp-傳輸排程表)
4. [tblScheduleException - 例外記錄表](#4-tblscheduleexception---例外記錄表)
5. [tblScheduleExecutionHistory - 執行歷史記錄表](#5-tblscheduleexecutionhistory---執行歷史記錄表)

---

## 1. tblScheduleHttp - HTTP 請求排程表

### 用途
管理 HTTP/HTTPS 請求的自動化排程任務，支援多種 HTTP 方法和豐富的請求設定。

### 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Id** | SERIAL | ✓ | AUTO | 主鍵 ID，自動遞增 |
| **ProgCode** | VARCHAR(200) | ✓ | - | 程式代碼，用於識別任務 |
| **Url** | TEXT | ✓ | - | 目標 URL 位址 |
| **HttpMethod** | VARCHAR(10) | ✓ | 'GET' | HTTP 方法：GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS |
| **Headers** | JSONB | ✗ | NULL | HTTP Headers，JSON 格式儲存 |
| **RequestBody** | TEXT | ✗ | NULL | 請求內容 (用於 POST/PUT/PATCH) |
| **ContentType** | VARCHAR(100) | ✗ | 'application/json' | Content-Type 標頭 |
| **Encoding** | VARCHAR(50) | ✗ | 'UTF-8' | 編碼格式 |
| **TimeoutSeconds** | INT | ✗ | 30 | 請求逾時秒數 |
| **RetryCount** | INT | ✗ | 0 | 失敗時的重試次數 |
| **RetryIntervalSeconds** | INT | ✗ | 5 | 重試間隔秒數 |
| **ExpectedHttpStatus** | INT | ✗ | 200 | 預期的 HTTP 狀態碼 |

#### 執行結果欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **LastExecuteTime** | TIMESTAMP | 最後執行時間 |
| **LastHttpStatus** | INT | 最後回應的 HTTP 狀態碼 |
| **LastResponseBody** | TEXT | 最後回應的內容 |
| **LastErrorMessage** | TEXT | 最後錯誤訊息 |
| **ExecuteCount** | INT | 總執行次數 |
| **SuccessCount** | INT | 成功次數 |
| **FailureCount** | INT | 失敗次數 |

#### 排程設定欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **IsEnabled** | BOOLEAN | 是否啟用此任務 |
| **ScheduleCron** | VARCHAR(100) | Cron 排程表達式 |
| **NextExecuteTime** | TIMESTAMP | 下次執行時間 |

#### 系統欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **CreatedBy** | VARCHAR(100) | 建立者 |
| **CreatedDate** | TIMESTAMP | 建立時間 |
| **ModifiedBy** | VARCHAR(100) | 修改者 |
| **ModifiedDate** | TIMESTAMP | 修改時間 |
| **Remark** | TEXT | 備註 |

### 索引
- `idx_schedulehttp_isenabled`: IsEnabled
- `idx_schedulehttp_nextexecutetime`: NextExecuteTime
- `idx_schedulehttp_createddate`: CreatedDate

### 使用範例

```sql
-- 插入一個 GET 請求任務
INSERT INTO tblScheduleHttp (ProgCode, Url, HttpMethod, IsEnabled)
VALUES ('API_CHECK_001', 'https://api.example.com/health', 'GET', TRUE);

-- 插入一個 POST 請求任務
INSERT INTO tblScheduleHttp (
    ProgCode, Url, HttpMethod, Headers, RequestBody, ContentType
)
VALUES (
    'WEBHOOK_001',
    'https://webhook.site/xxx',
    'POST',
    '{"Authorization": "Bearer token123"}'::jsonb,
    '{"event": "test", "data": "hello"}',
    'application/json'
);
```

---

## 2. tblScheduleMail - Email 發送排程表

### 用途
管理自動化郵件發送任務，支援多收件者、副本、密件副本及附件功能。

### 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Id** | SERIAL | ✓ | AUTO | 主鍵 ID，自動遞增 |
| **ProgCode** | VARCHAR(200) | ✓ | - | 程式代碼，用於識別任務 |

#### 郵件設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Sender** | VARCHAR(200) | ✓ | - | 寄件者信箱 |
| **SenderName** | VARCHAR(200) | ✗ | NULL | 寄件者顯示名稱 |
| **Recipients** | TEXT | ✓ | - | 收件者信箱，多個以分號(;)分隔 |
| **CC** | TEXT | ✗ | NULL | 副本收件者，多個以分號(;)分隔 |
| **BCC** | TEXT | ✗ | NULL | 密件副本收件者，多個以分號(;)分隔 |
| **ReplyTo** | VARCHAR(200) | ✗ | NULL | 回覆信箱 |

#### 郵件內容

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Subject** | VARCHAR(500) | ✓ | - | 郵件主旨 |
| **Body** | TEXT | ✓ | - | 郵件內容 |
| **BodyType** | VARCHAR(10) | ✗ | 'HTML' | 郵件格式：HTML 或 TEXT |
| **Priority** | VARCHAR(10) | ✗ | 'Normal' | 優先順序：Low, Normal, High |
| **Encoding** | VARCHAR(50) | ✗ | 'UTF-8' | 編碼格式 |

#### 附件設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **AttachmentPaths** | TEXT | ✗ | NULL | 附件檔案路徑，多個以分號(;)分隔 |

#### SMTP 設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **SmtpHost** | VARCHAR(200) | ✗ | NULL | SMTP 主機位址 |
| **SmtpPort** | INT | ✗ | 587 | SMTP 連接埠 |
| **SmtpUsername** | VARCHAR(200) | ✗ | NULL | SMTP 帳號 |
| **SmtpPassword** | VARCHAR(500) | ✗ | NULL | SMTP 密碼 (建議加密儲存) |
| **SmtpEnableSsl** | BOOLEAN | ✗ | TRUE | 是否啟用 SSL/TLS |
| **SmtpTimeoutSeconds** | INT | ✗ | 30 | SMTP 連線逾時秒數 |

#### 執行結果欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **LastExecuteTime** | TIMESTAMP | 最後執行時間 |
| **LastSuccessTime** | TIMESTAMP | 最後成功時間 |
| **LastErrorMessage** | TEXT | 最後錯誤訊息 |
| **ExecuteCount** | INT | 總執行次數 |
| **SuccessCount** | INT | 成功次數 |
| **FailureCount** | INT | 失敗次數 |

#### 排程設定欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **IsEnabled** | BOOLEAN | 是否啟用此任務 |
| **ScheduleCron** | VARCHAR(100) | Cron 排程表達式 |
| **NextExecuteTime** | TIMESTAMP | 下次執行時間 |

#### 系統欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **CreatedBy** | VARCHAR(100) | 建立者 |
| **CreatedDate** | TIMESTAMP | 建立時間 |
| **ModifiedBy** | VARCHAR(100) | 修改者 |
| **ModifiedDate** | TIMESTAMP | 修改時間 |
| **Remark** | TEXT | 備註 |

### 索引
- `idx_schedulemail_isenabled`: IsEnabled
- `idx_schedulemail_nextexecutetime`: NextExecuteTime
- `idx_schedulemail_createddate`: CreatedDate

### 使用範例

```sql
-- 插入一個簡單的郵件任務
INSERT INTO tblScheduleMail (
    ProgCode, Sender, Recipients, Subject, Body
)
VALUES (
    'DAILY_REPORT_001',
    'system@example.com',
    'user1@example.com;user2@example.com',
    '每日報表',
    '<h1>這是每日報表</h1><p>詳細內容...</p>'
);

-- 插入帶附件和 CC 的郵件任務
INSERT INTO tblScheduleMail (
    ProgCode, Sender, Recipients, CC, Subject, Body, AttachmentPaths, SmtpHost, SmtpPort
)
VALUES (
    'MONTHLY_REPORT_001',
    'report@example.com',
    'manager@example.com',
    'team@example.com',
    '月報告',
    '<p>請查閱附件</p>',
    'C:\Reports\monthly.pdf;C:\Reports\summary.xlsx',
    'smtp.gmail.com',
    587
);
```

---

## 3. tblScheduleFTP - FTP 傳輸排程表

### 用途
管理 FTP/FTPS/SFTP 檔案傳輸的自動化任務，支援檔案上傳及各種傳輸設定。

### 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Id** | SERIAL | ✓ | AUTO | 主鍵 ID，自動遞增 |
| **ProgCode** | VARCHAR(200) | ✓ | - | 程式代碼，用於識別任務 |

#### FTP 連線設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **FtpHost** | VARCHAR(200) | ✓ | - | FTP 主機位址 |
| **FtpPort** | INT | ✗ | 21 | FTP 連接埠 |
| **FtpUsername** | VARCHAR(200) | ✓ | - | FTP 使用者名稱 |
| **FtpPassword** | VARCHAR(500) | ✗ | NULL | FTP 密碼 (建議加密儲存) |
| **FtpProtocol** | VARCHAR(10) | ✗ | 'FTP' | FTP 協定：FTP, FTPS, SFTP |
| **FtpMode** | VARCHAR(10) | ✗ | 'Passive' | FTP 模式：Active, Passive |
| **FtpEncoding** | VARCHAR(50) | ✗ | 'UTF-8' | FTP 編碼格式 |
| **FtpTimeoutSeconds** | INT | ✗ | 30 | FTP 連線逾時秒數 |

#### 傳輸設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **LocalFilePath** | TEXT | ✓ | - | 本地檔案路徑 (支援萬用字元，如 *.txt) |
| **RemoteFilePath** | TEXT | ✓ | - | 遠端檔案路徑 |
| **TransferMode** | VARCHAR(10) | ✗ | 'Binary' | 傳輸模式：Binary, ASCII |
| **OverwriteExisting** | BOOLEAN | ✗ | TRUE | 是否覆寫遠端現有檔案 |
| **CreateRemoteDirectory** | BOOLEAN | ✗ | TRUE | 是否自動建立遠端目錄 |
| **DeleteLocalAfterUpload** | BOOLEAN | ✗ | FALSE | 上傳後是否刪除本地檔案 |

#### 進階設定

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **RetryCount** | INT | ✗ | 0 | 失敗時的重試次數 |
| **RetryIntervalSeconds** | INT | ✗ | 5 | 重試間隔秒數 |

#### 執行結果欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **LastExecuteTime** | TIMESTAMP | 最後執行時間 |
| **LastSuccessTime** | TIMESTAMP | 最後成功時間 |
| **LastTransferredFiles** | TEXT | 最後傳輸的檔案清單 |
| **LastTransferredBytes** | BIGINT | 最後傳輸的位元組數 |
| **LastErrorMessage** | TEXT | 最後錯誤訊息 |
| **ExecuteCount** | INT | 總執行次數 |
| **SuccessCount** | INT | 成功次數 |
| **FailureCount** | INT | 失敗次數 |

#### 排程設定欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **IsEnabled** | BOOLEAN | 是否啟用此任務 |
| **ScheduleCron** | VARCHAR(100) | Cron 排程表達式 |
| **NextExecuteTime** | TIMESTAMP | 下次執行時間 |

#### 系統欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **CreatedBy** | VARCHAR(100) | 建立者 |
| **CreatedDate** | TIMESTAMP | 建立時間 |
| **ModifiedBy** | VARCHAR(100) | 修改者 |
| **ModifiedDate** | TIMESTAMP | 修改時間 |
| **Remark** | TEXT | 備註 |

### 索引
- `idx_scheduleftp_isenabled`: IsEnabled
- `idx_scheduleftp_nextexecutetime`: NextExecuteTime
- `idx_scheduleftp_createddate`: CreatedDate

### 使用範例

```sql
-- 插入一個基本的 FTP 上傳任務
INSERT INTO tblScheduleFTP (
    ProgCode, FtpHost, FtpUsername, FtpPassword, LocalFilePath, RemoteFilePath
)
VALUES (
    'FTP_BACKUP_001',
    'ftp.example.com',
    'ftpuser',
    'password123',
    'C:\Backup\*.zip',
    '/backup/'
);

-- 插入一個 SFTP 任務，上傳後刪除本地檔案
INSERT INTO tblScheduleFTP (
    ProgCode, FtpHost, FtpPort, FtpUsername, FtpPassword, FtpProtocol,
    LocalFilePath, RemoteFilePath, DeleteLocalAfterUpload
)
VALUES (
    'SFTP_UPLOAD_001',
    'sftp.example.com',
    22,
    'sftpuser',
    'securepass',
    'SFTP',
    'C:\Export\data_*.csv',
    '/import/data/',
    TRUE
);
```

---

## 4. tblScheduleException - 例外記錄表

### 用途
統一記錄所有排程服務 (HTTP/Mail/FTP) 執行時發生的例外錯誤，便於追蹤和診斷問題。

### 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Id** | SERIAL | ✓ | AUTO | 主鍵 ID，自動遞增 |
| **ServiceType** | VARCHAR(20) | ✓ | - | 服務類型：HTTP, MAIL, FTP |
| **ServiceTaskId** | INT | ✓ | - | 對應的任務 ID (來自各服務表的 Id) |
| **ProgCode** | VARCHAR(200) | ✗ | NULL | 程式代碼 |

#### 例外資訊

| 欄位名稱 | 資料型別 | 必填 | 說明 |
|---------|---------|------|------|
| **ExceptionType** | VARCHAR(100) | ✗ | 例外類型 (如 TimeoutError, ConnectionError) |
| **ExceptionMessage** | TEXT | ✓ | 例外錯誤訊息 |
| **StackTrace** | TEXT | ✗ | 堆疊追蹤資訊 |
| **InnerException** | TEXT | ✗ | 內部例外訊息 |

#### HTTP 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **HttpUrl** | TEXT | HTTP 請求的 URL |
| **HttpMethod** | VARCHAR(10) | HTTP 方法 |
| **HttpStatus** | INT | HTTP 狀態碼 |

#### Mail 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **MailRecipients** | TEXT | 郵件收件者 |
| **MailSubject** | VARCHAR(500) | 郵件主旨 |

#### FTP 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **FtpHost** | VARCHAR(200) | FTP 主機位址 |
| **FtpLocalPath** | TEXT | 本地檔案路徑 |
| **FtpRemotePath** | TEXT | 遠端檔案路徑 |

#### 系統欄位

| 欄位名稱 | 資料型別 | 預設值 | 說明 |
|---------|---------|--------|------|
| **OccurredDate** | TIMESTAMP | CURRENT_TIMESTAMP | 例外發生時間 |
| **IsResolved** | BOOLEAN | FALSE | 是否已解決 |
| **ResolvedBy** | VARCHAR(100) | NULL | 解決者 |
| **ResolvedDate** | TIMESTAMP | NULL | 解決時間 |
| **ResolveNote** | TEXT | NULL | 解決備註 |

### 索引
- `idx_scheduleexception_servicetype`: ServiceType
- `idx_scheduleexception_servicetaskid`: ServiceTaskId
- `idx_scheduleexception_occurreddate`: OccurredDate
- `idx_scheduleexception_isresolved`: IsResolved

### 使用範例

```sql
-- 記錄一個 HTTP 服務的例外
INSERT INTO tblScheduleException (
    ServiceType, ServiceTaskId, ProgCode, ExceptionType, ExceptionMessage,
    HttpUrl, HttpMethod, HttpStatus
)
VALUES (
    'HTTP', 1, 'API_CHECK_001', 'TimeoutError', 'Request timeout after 30 seconds',
    'https://api.example.com/health', 'GET', 0
);

-- 查詢未解決的例外
SELECT * FROM tblScheduleException
WHERE IsResolved = FALSE
ORDER BY OccurredDate DESC;

-- 標記例外為已解決
UPDATE tblScheduleException
SET IsResolved = TRUE, ResolvedBy = 'Admin', ResolvedDate = CURRENT_TIMESTAMP,
    ResolveNote = '已重新設定 API 端點'
WHERE Id = 1;
```

---

## 5. tblScheduleExecutionHistory - 執行歷史記錄表

### 用途
記錄所有排程任務的執行歷史，包含執行時間、結果、效能指標等詳細資訊，用於監控和分析。

### 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 預設值 | 說明 |
|---------|---------|------|--------|------|
| **Id** | SERIAL | ✓ | AUTO | 主鍵 ID，自動遞增 |
| **ServiceType** | VARCHAR(20) | ✓ | - | 服務類型：HTTP, MAIL, FTP |
| **ServiceTaskId** | INT | ✓ | - | 對應的任務 ID (來自各服務表的 Id) |
| **ProgCode** | VARCHAR(200) | ✗ | NULL | 程式代碼 |

#### 執行資訊

| 欄位名稱 | 資料型別 | 必填 | 說明 |
|---------|---------|------|------|
| **StartTime** | TIMESTAMP | ✓ | 開始執行時間 |
| **EndTime** | TIMESTAMP | ✗ | 結束執行時間 |
| **DurationMs** | INT | ✗ | 執行時長 (毫秒) |
| **IsSuccess** | BOOLEAN | ✓ | 是否執行成功 |
| **ErrorMessage** | TEXT | ✗ | 錯誤訊息 (如果失敗) |

#### HTTP 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **HttpStatus** | INT | HTTP 狀態碼 |
| **ResponseSize** | INT | 回應大小 (位元組) |

#### Mail 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **EmailsSent** | INT | 成功發送的郵件數量 |

#### FTP 專用欄位

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **FilesTransferred** | INT | 傳輸的檔案數量 |
| **BytesTransferred** | BIGINT | 傳輸的位元組數 |

#### 執行結果詳情

| 欄位名稱 | 資料型別 | 說明 |
|---------|---------|------|
| **ExecutionDetails** | JSONB | 執行詳情，JSON 格式儲存額外資訊 |

#### 系統欄位

| 欄位名稱 | 資料型別 | 預設值 | 說明 |
|---------|---------|--------|------|
| **CreatedDate** | TIMESTAMP | CURRENT_TIMESTAMP | 記錄建立時間 |

### 索引
- `idx_schedulehistory_servicetype`: ServiceType
- `idx_schedulehistory_servicetaskid`: ServiceTaskId
- `idx_schedulehistory_starttime`: StartTime
- `idx_schedulehistory_issuccess`: IsSuccess

### 使用範例

```sql
-- 記錄一次 HTTP 任務執行
INSERT INTO tblScheduleExecutionHistory (
    ServiceType, ServiceTaskId, ProgCode, StartTime, EndTime, DurationMs,
    IsSuccess, HttpStatus, ResponseSize
)
VALUES (
    'HTTP', 1, 'API_CHECK_001', '2025-10-04 10:00:00', '2025-10-04 10:00:02',
    2000, TRUE, 200, 1024
);

-- 查詢最近 7 天的執行歷史
SELECT * FROM tblScheduleExecutionHistory
WHERE StartTime >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY StartTime DESC;

-- 統計各任務的成功率
SELECT
    ServiceType,
    ServiceTaskId,
    ProgCode,
    COUNT(*) as TotalExecutions,
    SUM(CASE WHEN IsSuccess THEN 1 ELSE 0 END) as SuccessCount,
    ROUND(SUM(CASE WHEN IsSuccess THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) as SuccessRate,
    AVG(DurationMs) as AvgDurationMs
FROM tblScheduleExecutionHistory
WHERE StartTime >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY ServiceType, ServiceTaskId, ProgCode
ORDER BY SuccessRate ASC;

-- 查詢執行時間超過 5 秒的任務
SELECT * FROM tblScheduleExecutionHistory
WHERE DurationMs > 5000
ORDER BY DurationMs DESC;
```

---

## 資料表關聯圖

```
┌─────────────────────┐
│ tblScheduleHttp     │
│ - Id (PK)           │───┐
│ - ProgCode          │   │
│ - Url               │   │
│ - ...               │   │
└─────────────────────┘   │
                          │
┌─────────────────────┐   │
│ tblScheduleMail     │   │
│ - Id (PK)           │───┤
│ - ProgCode          │   │    ┌──────────────────────────┐
│ - Recipients        │   ├───→│ tblScheduleException     │
│ - ...               │   │    │ - ServiceType            │
└─────────────────────┘   │    │ - ServiceTaskId (FK)     │
                          │    └──────────────────────────┘
┌─────────────────────┐   │
│ tblScheduleFTP      │   │
│ - Id (PK)           │───┤
│ - ProgCode          │   │    ┌──────────────────────────┐
│ - LocalFilePath     │   │    │ tblScheduleExecutionHist │
│ - ...               │   └───→│ - ServiceType            │
└─────────────────────┘        │ - ServiceTaskId (FK)     │
                               └──────────────────────────┘
```

## 注意事項

### 安全性
1. **密碼欄位加密**：`SmtpPassword` 和 `FtpPassword` 建議使用加密方式儲存
2. **存取權限**：建議對敏感欄位設定適當的資料庫權限
3. **SQL 注入防護**：所有查詢應使用參數化查詢

### 效能優化
1. **定期清理歷史記錄**：`tblScheduleExecutionHistory` 和 `tblScheduleException` 應定期清理舊資料
2. **索引維護**：定期重建索引以維持查詢效能
3. **分割大型資料表**：若歷史記錄表資料量龐大，考慮使用 PostgreSQL 的資料表分割功能

### 維護建議
1. **備份策略**：定期備份所有資料表
2. **監控告警**：監控 `tblScheduleException` 的未解決例外數量
3. **效能分析**：定期分析 `tblScheduleExecutionHistory` 的執行時長，找出效能瓶頸

---

## 版本歷史

| 版本 | 日期 | 說明 |
|-----|------|------|
| 1.0 | 2025-10-04 | 初始版本 |

---

**文件產生日期**: 2025-10-04
**資料庫版本**: PostgreSQL 12+
