# Database 資料庫環境建置指南

本指南將協助您快速建立 PostgreSQL 資料庫環境，並透過 pgAdmin 管理介面進行連線。

---

## 📋 目錄

1. [環境需求](#環境需求)
2. [啟動 PostgreSQL 資料庫](#啟動-postgresql-資料庫)
3. [使用本地 pgAdmin 連線（推薦）](#使用本地-pgadmin-連線推薦)
4. [使用 Docker pgAdmin 連線](#使用-docker-pgadmin-連線)
5. [驗證資料庫](#驗證資料庫)
6. [常用操作](#常用操作)
7. [疑難排解](#疑難排解)

---

## 環境需求

- Docker Desktop（已安裝並啟動）

---

## 啟動 PostgreSQL 資料庫

### 步驟 1：建立環境變數檔案

**首次使用時，需要先建立 `.env` 檔案：**

```bash
# 複製環境變數範本
cp .env.example .env
```

您可以直接使用預設值，或修改 `.env` 檔案中的設定：

```env
POSTGRES_DB=SYSDATA                    # 資料庫名稱
POSTGRES_USER=sa                       # 資料庫使用者
POSTGRES_PASSWORD=your_secure_password # ⚠️ 建議修改為強密碼
POSTGRES_PORT=5432                     # PostgreSQL Port
```

### 步驟 2：啟動資料庫容器

在專案根目錄執行以下指令：

```bash
docker-compose up -d postgres
```

**指令說明：**
- `docker-compose up`：啟動 Docker Compose 定義的服務
- `-d`：在背景執行（不會佔用終端機視窗）
- `postgres`：只啟動 PostgreSQL 服務（不啟動其他服務）

### 步驟 3：確認容器狀態

```bash
docker-compose ps
```

**預期輸出：**
```
NAME                IMAGE                 STATUS
schedule_postgres   postgres:15-alpine    Up X minutes (healthy)
```

⚠️ 狀態必須顯示 `Up` 且包含 `(healthy)` 才表示啟動成功。

### 步驟 4：查看初始化日誌

```bash
docker-compose logs postgres
```

**確認以下訊息表示初始化成功：**
- `database system is ready to accept connections`
- `running /docker-entrypoint-initdb.d/01_create_tables.sql`
- `running /docker-entrypoint-initdb.d/02_add_execution_status.sql`

如果看到 `CREATE TABLE` 和 `CREATE INDEX` 訊息，代表資料表已自動建立完成。

---

## 使用本地 pgAdmin 連線（推薦）

如果您的電腦已安裝 pgAdmin，可以直接使用本地版本連線到 Docker 中的資料庫。

### 步驟 1：開啟本地 pgAdmin

啟動您電腦上已安裝的 pgAdmin 應用程式。

### 步驟 2：新增伺服器

1. 在左側樹狀選單中，**右鍵點擊「Servers」**
2. 選擇 **「Register」 → 「Server...」**

### 步驟 3：填寫伺服器資訊

#### General 頁籤
- **Name**：`Schedule (Docker)` （可自訂名稱，方便識別）

#### Connection 頁籤
填寫以下連線參數：

| 欄位 | 值 | 說明 |
|------|-----|------|
| **Host name/address** | `localhost` | 因為 Docker 已將容器 5432 port 映射到本機 |
| **Port** | `5432` | PostgreSQL 預設埠號 |
| **Maintenance database** | `SYSDATA` | 資料庫名稱（根據 .env 設定）|
| **Username** | `sa` | 資料庫使用者名稱（根據 .env 設定）|
| **Password** | `your_secure_password` | 您在 .env 中設定的密碼 |

✅ **建議勾選：**
- ☑ Save password（儲存密碼，下次不用重新輸入）

#### SSL 頁籤
- **SSL mode**：選擇 `Prefer`（建議設定）

### 步驟 4：儲存並連線

點擊 **「Save」** 按鈕，pgAdmin 會自動嘗試連線。

### 步驟 5：確認連線成功

連線成功後，在左側樹狀選單會看到：

```
Servers
└── Schedule (Docker)
    └── Databases (1)
        └── SYSDATA
            └── Schemas
                └── public
                    └── Tables (5)
                        ├── tblscheduleexception
                        ├── tblscheduleexecutionhistory
                        ├── tblscheduleftp
                        ├── tblschedulehttp
                        └── tblschedulemail
```

✅ 如果看到 5 個資料表，代表連線成功且資料庫已正確初始化！

---

## 使用 Docker pgAdmin 連線

如果您的電腦沒有安裝 pgAdmin，可以使用 Docker 版本的 pgAdmin。

### 步驟 1：啟動 Docker pgAdmin

```bash
docker-compose --profile tools up -d pgadmin
```

**指令說明：**
- `--profile tools`：啟動標記為 tools 的服務（pgAdmin 被設定為選用工具）
- `pgadmin`：指定啟動 pgAdmin 服務

### 步驟 2：確認 pgAdmin 容器狀態

```bash
docker-compose ps
```

**預期輸出：**
```
NAME                IMAGE                   STATUS
schedule_pgadmin    dpage/pgadmin4:latest   Up X minutes
schedule_postgres   postgres:15-alpine      Up X minutes (healthy)
```

### 步驟 3：開啟 pgAdmin 網頁介面

在瀏覽器中開啟：

```
http://localhost:5050
```

### 步驟 4：登入 pgAdmin

使用以下帳號密碼登入：

- **Email Address / Username**：`admin@example.com`
- **Password**：`admin`

### 步驟 5：新增伺服器連線

登入後，依照以下步驟設定資料庫連線：

1. 在左側樹狀選單中，**右鍵點擊「Servers」**
2. 選擇 **「Register」 → 「Server...」**

### 步驟 6：填寫伺服器資訊

#### General 頁籤
- **Name**：`Schedule DB`（可自訂名稱）

#### Connection 頁籤

⚠️ **重要：Docker 版本的 pgAdmin 連線設定與本地版本不同！**

| 欄位 | 值 | 說明 |
|------|-----|------|
| **Host name/address** | `postgres` | ⚠️ 使用服務名稱，不是 localhost |
| **Port** | `5432` | PostgreSQL 預設埠號 |
| **Maintenance database** | `SYSDATA` | 資料庫名稱（根據 .env 設定）|
| **Username** | `sa` | 資料庫使用者名稱（根據 .env 設定）|
| **Password** | `your_secure_password` | 您在 .env 中設定的密碼 |

✅ **建議勾選：**
- ☑ Save password

### 步驟 7：儲存並連線

點擊 **「Save」**，連線成功後會在左側看到資料庫樹狀結構。

---

## 驗證資料庫

### 方法 1：透過 pgAdmin 查看（圖形化介面）

在 pgAdmin 中：

1. 展開 **Servers → Schedule DB → Databases → SYSDATA → Schemas → public → Tables**
2. 確認以下 5 個資料表存在：
   - `tblscheduleexception`
   - `tblscheduleexecutionhistory`
   - `tblscheduleftp`
   - `tblschedulehttp`
   - `tblschedulemail`

### 方法 2：透過指令列查看

```bash
# 進入 PostgreSQL 容器的 psql 命令列
docker-compose exec postgres psql -U sa -d SYSDATA
```

進入後執行以下指令：

```sql
-- 查看所有資料表
\dt

-- 查看特定資料表的結構
\d tblschedulehttp

-- 查看資料表數量
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';

-- 離開 psql
\q
```

**預期輸出：**
```
                      List of relations
 Schema |            Name              | Type  | Owner
--------+------------------------------+-------+-------
 public | tblscheduleexception         | table | sa
 public | tblscheduleexecutionhistory  | table | sa
 public | tblscheduleftp               | table | sa
 public | tblschedulehttp              | table | sa
 public | tblschedulemail              | table | sa
(5 rows)
```

---

## 常用操作

### 停止服務

```bash
# 停止所有服務（保留資料）
docker-compose down

# 只停止 PostgreSQL
docker-compose stop postgres

# 只停止 pgAdmin
docker-compose stop pgadmin
```

### 重新啟動服務

```bash
# 重新啟動 PostgreSQL
docker-compose restart postgres

# 重新啟動 pgAdmin
docker-compose restart pgadmin
```

### 完全重置資料庫

⚠️ **警告：此操作會刪除所有資料，無法復原！**

```bash
# 停止服務並刪除所有資料（包含 Volume）
docker-compose down -v

# 重新啟動（會重新執行初始化 SQL）
docker-compose up -d postgres
```

初始化 SQL 檔案會按照檔名順序自動執行：
1. `01_create_tables.sql` - 建立所有資料表
2. `02_add_execution_status.sql` - 新增執行狀態欄位

### 備份資料庫

```bash
# 備份整個資料庫（自動加上時間戳記）
docker-compose exec postgres pg_dump -U sa SYSDATA > backup_$(date +%Y%m%d_%H%M%S).sql

# Windows PowerShell 版本
docker-compose exec postgres pg_dump -U sa SYSDATA > backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql
```

備份檔案會儲存在當前目錄。

### 還原資料庫

```bash
# 還原指定的備份檔案
docker-compose exec -T postgres psql -U sa SYSDATA < backup_20251005_120000.sql
```

### 查看即時日誌

```bash
# 持續顯示 PostgreSQL 日誌（按 Ctrl+C 離開）
docker-compose logs -f postgres

# 只顯示最後 50 行日誌
docker-compose logs --tail 50 postgres
```

---

## 疑難排解

### ❌ 問題 1：無法連線到資料庫

**檢查步驟：**

```bash
# 1. 確認容器是否正在執行
docker-compose ps
```

如果狀態不是 `Up` 或沒有 `(healthy)`，請查看日誌：

```bash
docker-compose logs postgres
```

**常見原因：**
- Port 5432 被其他服務佔用

**解決方法（Windows）：**
```bash
# 檢查 Port 5432 是否被佔用
netstat -ano | findstr :5432

# 如果被佔用，修改 .env 檔案中的 POSTGRES_PORT 為其他值（如 5433）
# 然後重新啟動
docker-compose down
docker-compose up -d postgres
```

### ❌ 問題 2：pgAdmin 顯示「Unable to connect to server」

**本地 pgAdmin 連線失敗：**
- 確認 Host 使用 `localhost` 或 `127.0.0.1`
- 確認 Port 為 `5432`（或您在 .env 中設定的值）

**Docker pgAdmin 連線失敗：**
- ⚠️ 確認 Host 使用 `postgres`（服務名稱），**不是 localhost**
- 確認 Port 為 `5432`

### ❌ 問題 3：資料表沒有自動建立

**檢查初始化 SQL 是否掛載成功：**

```bash
docker-compose exec postgres ls -la /docker-entrypoint-initdb.d/
```

**預期輸出：**
```
-rw-r--r-- 1 root root  XXXX  01_create_tables.sql
-rw-r--r-- 1 root root  XXXX  02_add_execution_status.sql
```

如果檔案不存在，請確認：
1. SQL 檔案確實存在於 `Database/` 目錄
2. `docker-compose.yml` 中的 volumes 設定正確

**解決方法：**
```bash
# 完全重置後重新初始化
docker-compose down -v
docker-compose up -d postgres
```

### ❌ 問題 4：Docker pgAdmin 無法開啟（localhost:5050）

**檢查步驟：**

```bash
# 1. 確認 pgAdmin 容器是否啟動
docker-compose ps

# 2. 如果沒有看到 schedule_pgadmin，代表沒有使用 --profile tools 啟動
docker-compose --profile tools up -d pgadmin

# 3. 查看 pgAdmin 日誌
docker-compose logs pgadmin
```

### ❌ 問題 5：密碼錯誤或使用者不存在

確認您使用的連線資訊與 `.env` 檔案一致：

**檢查 .env 檔案內容：**
```bash
cat .env
```

**應該包含以下設定：**
```
POSTGRES_DB=SYSDATA
POSTGRES_USER=sa
POSTGRES_PASSWORD=your_secure_password
POSTGRES_PORT=5432
```

如果修改了 `.env` 檔案，必須重新建立容器：

```bash
docker-compose down -v
docker-compose up -d postgres
```

---

## 連線資訊快速參考

### 從本地應用程式連線（Python、N8N 等）

**連線字串：**
```
postgresql://sa:your_secure_password@localhost:5432/SYSDATA
```

**連線參數：**
```python
HOST = "localhost"
PORT = 5432
DATABASE = "SYSDATA"
USER = "sa"
PASSWORD = "your_secure_password"  # 來自 .env 檔案
```

### 從 Docker 容器內的應用程式連線（如 N8N）

**連線字串：**
```
postgresql://sa:your_secure_password@postgres:5432/SYSDATA
```

**連線參數：**
```python
HOST = "postgres"  # ⚠️ 使用服務名稱，不是 localhost
PORT = 5432
DATABASE = "SYSDATA"
USER = "sa"
PASSWORD = "your_secure_password"  # 來自 .env 檔案
```

---

## 📚 延伸閱讀

- **資料表結構詳細說明**：[TABLE_SCHEMA.md](TABLE_SCHEMA.md)
- **Docker Compose 設定檔**：[../docker-compose.yml](../docker-compose.yml)
- **環境變數範例**：[../.env.example](../.env.example)

---

## 🎯 快速指令總覽

```bash
# 啟動資料庫
docker-compose up -d postgres

# 啟動 pgAdmin（Docker 版本）
docker-compose --profile tools up -d pgadmin

# 查看狀態
docker-compose ps

# 查看日誌
docker-compose logs -f postgres

# 進入 psql 命令列
docker-compose exec postgres psql -U sa -d SYSDATA

# 完全重置（刪除所有資料）
docker-compose down -v && docker-compose up -d postgres

# 停止所有服務
docker-compose down

# 備份資料庫
docker-compose exec postgres pg_dump -U sa SYSDATA > backup.sql

# 還原資料庫
docker-compose exec -T postgres psql -U sa SYSDATA < backup.sql
```

---

**最後更新日期：** 2025-10-05
