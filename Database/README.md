# Database 資料庫設定

## 快速開始

### 1. 複製環境變數檔案
```bash
cp .env.example .env
```

### 2. 修改 `.env` 檔案（選用）
```env
POSTGRES_DB=schedule
POSTGRES_USER=scheduleuser
POSTGRES_PASSWORD=your_secure_password  # 建議修改密碼
POSTGRES_PORT=5432
```

### 3. 啟動 PostgreSQL
```bash
# 只啟動 PostgreSQL
docker-compose up -d postgres

# 查看啟動狀態
docker-compose ps

# 查看日誌
docker-compose logs -f postgres
```

### 4. 驗證資料庫
```bash
# 進入 PostgreSQL 容器
docker-compose exec postgres psql -U scheduleuser -d schedule

# 查看已建立的資料表
\dt

# 離開
\q
```

## 資料表初始化

SQL 腳本會在容器首次啟動時**自動執行**（依檔名排序）:

1. `01_create_tables.sql` - 建立主要資料表
2. `02_add_execution_status.sql` - 新增執行狀態欄位（如已執行過 01，需手動執行）

### 手動執行 SQL（如果需要）
```bash
# 執行特定 SQL 檔案
docker-compose exec -T postgres psql -U scheduleuser -d schedule < Database/02_add_execution_status.sql
```

## 使用 pgAdmin（選用）

### 啟動 pgAdmin
```bash
# 使用 --profile tools 啟動 pgAdmin
docker-compose --profile tools up -d pgadmin
```

### 存取 pgAdmin
1. 開啟瀏覽器：http://localhost:5050
2. 登入帳號：`admin@example.com` / `admin`（可在 .env 修改）
3. 新增伺服器連線：
   - Host name/address: `postgres`
   - Port: `5432`
   - Username: `scheduleuser`
   - Password: `.env 中的密碼`

## 常用指令

### 重置資料庫
```bash
# 停止並刪除容器及 Volume（會清空資料！）
docker-compose down -v

# 重新啟動（會重新執行初始化 SQL）
docker-compose up -d postgres
```

### 備份資料庫
```bash
# 備份整個資料庫
docker-compose exec postgres pg_dump -U scheduleuser schedule > backup_$(date +%Y%m%d_%H%M%S).sql

# 備份特定資料表
docker-compose exec postgres pg_dump -U scheduleuser -t tblScheduleHttp schedule > http_backup.sql
```

### 還原資料庫
```bash
# 還原備份
docker-compose exec -T postgres psql -U scheduleuser schedule < backup_20251004_120000.sql
```

### 查看資料庫連線資訊
```bash
# 從 Python 連線字串
postgresql://scheduleuser:schedulepass@localhost:5432/schedule

# 從 N8N 連線
Host: localhost (或容器內使用 postgres)
Port: 5432
Database: schedule
User: scheduleuser
Password: schedulepass
```

## 資料表結構

詳細資料表欄位說明請參考：[TABLE_SCHEMA.md](TABLE_SCHEMA.md)

### 主要資料表
1. **tblScheduleHttp** - HTTP 請求排程
2. **tblScheduleMail** - Email 發送排程
3. **tblScheduleFTP** - FTP 傳輸排程
4. **tblScheduleException** - 例外記錄
5. **tblScheduleExecutionHistory** - 執行歷史

## 疑難排解

### 容器無法啟動
```bash
# 查看詳細錯誤
docker-compose logs postgres

# 檢查 Port 是否被佔用
netstat -ano | findstr :5432  # Windows
lsof -i :5432                  # macOS/Linux
```

### 資料表沒有自動建立
```bash
# 確認 SQL 檔案是否正確掛載
docker-compose exec postgres ls -la /docker-entrypoint-initdb.d/

# 手動執行 SQL
docker-compose exec -T postgres psql -U scheduleuser schedule < Database/01_create_tables.sql
```

### 重置管理員密碼
```bash
# 修改 .env 中的密碼後重啟
docker-compose down
docker-compose up -d postgres
```

## 注意事項

⚠️ **安全性提醒**
- 生產環境請使用強密碼
- 不要將 `.env` 檔案提交到版本控制
- 定期備份資料庫

📊 **效能建議**
- 定期清理 `tblScheduleExecutionHistory` 歷史記錄
- 監控 `tblScheduleException` 錯誤數量
- 使用索引優化查詢效能
