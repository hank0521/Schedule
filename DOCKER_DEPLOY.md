# Docker 部署指南

## 📦 專案架構

```
Schedule/
├── API/                    # FastAPI 應用程式
│   ├── Dockerfile          # API Docker 映像檔
│   └── ...
├── Database/               # 資料庫初始化 SQL
├── docker-compose.yml      # Docker Compose 配置
├── .env                    # 環境變數 (需自行建立)
└── .env.example            # 環境變數範本
```

## 🚀 快速部署

### 1. 設定環境變數

```bash
# 複製環境變數範本
cp .env.example .env
```

編輯 `.env` 檔案,至少需要設定:

```env
# 資料庫密碼
POSTGRES_PASSWORD=your_strong_password

# API 加密金鑰 (使用下方指令產生)
ENCRYPTION_KEY=your-encryption-key-here
```

#### 產生加密金鑰

```bash
# 使用 Python 產生 (需要先安裝 cryptography)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 或使用 Docker 產生
docker run --rm python:3.10-slim python -c "from cryptography import fernet; print(fernet.Fernet.generate_key().decode())"
```

將產生的金鑰複製到 `.env` 的 `ENCRYPTION_KEY`

### 2. 啟動所有服務

```bash
# 啟動 PostgreSQL + FastAPI
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f
```

### 3. 僅啟動特定服務

```bash
# 僅啟動資料庫
docker-compose up -d postgres

# 僅啟動 API
docker-compose up -d api

# 啟動資料庫 + API
docker-compose up -d postgres api
```

### 4. 啟動 pgAdmin (可選)

```bash
docker-compose --profile tools up -d pgadmin
```

## 🔍 驗證部署

### 檢查服務狀態

```bash
docker-compose ps
```

預期輸出:
```
NAME                IMAGE                   STATUS
schedule_api        schedule-api            Up (healthy)
schedule_postgres   postgres:15-alpine      Up (healthy)
```

### 測試 API 健康檢查

```bash
# 使用 curl
curl http://localhost:8000/health

# 使用瀏覽器
# 訪問 http://localhost:8000/health
```

預期回應:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-05T12:00:00.000000",
  "version": "1.0.0"
}
```

### 測試資料庫連線

```bash
curl http://localhost:8000/health/db
```

預期回應:
```json
{
  "database_connected": true,
  "message": "Database connection is healthy"
}
```

### 訪問 API 文件

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **根路徑**: http://localhost:8000/

## 📋 服務說明

### 服務列表

| 服務名稱 | 容器名稱 | 對外端口 | 說明 |
|---------|---------|---------|------|
| postgres | schedule_postgres | 5432 | PostgreSQL 資料庫 |
| api | schedule_api | 8000 | FastAPI 應用程式 |
| pgadmin | schedule_pgadmin | 5050 | PostgreSQL 管理介面 (可選) |

### 網路配置

所有服務都在 `schedule_network` 網路中,可以透過服務名稱互相通訊。

例如:
- API 連接資料庫: `postgres:5432`
- 外部訪問 API: `localhost:8000`

## 🔧 常用操作

### 查看日誌

```bash
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f api
docker-compose logs -f postgres

# 查看最後 50 行日誌
docker-compose logs --tail 50 api
```

### 重新啟動服務

```bash
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart api
```

### 停止服務

```bash
# 停止所有服務 (保留資料)
docker-compose down

# 停止並刪除資料 (⚠️ 危險操作)
docker-compose down -v
```

### 重新建置 API

當修改程式碼後:

```bash
# 重新建置並啟動
docker-compose up -d --build api

# 或分開執行
docker-compose build api
docker-compose up -d api
```

### 進入容器內部

```bash
# 進入 API 容器
docker-compose exec api bash

# 進入資料庫容器
docker-compose exec postgres bash

# 在 API 容器中執行 Python
docker-compose exec api python
```

### 查看容器資源使用

```bash
docker stats schedule_api schedule_postgres
```

## 📝 環境變數說明

### 資料庫相關

| 變數名稱 | 預設值 | 說明 |
|---------|--------|------|
| POSTGRES_DB | SYSDATA | 資料庫名稱 |
| POSTGRES_USER | sa | 資料庫使用者 |
| POSTGRES_PASSWORD | - | 資料庫密碼 (必須設定) |
| POSTGRES_PORT | 5432 | 對外端口 |

### API 相關

| 變數名稱 | 預設值 | 說明 |
|---------|--------|------|
| API_PORT | 8000 | API 對外端口 |
| API_DEBUG | False | 除錯模式 |
| API_SECRET_KEY | - | API 密鑰 |
| API_KEY | - | API 認證金鑰 |
| ENCRYPTION_KEY | - | 加密金鑰 (必須設定) |
| LOG_LEVEL | INFO | 日誌等級 |

## 🛠️ 疑難排解

### API 無法啟動

1. 檢查日誌:
   ```bash
   docker-compose logs api
   ```

2. 檢查資料庫是否健康:
   ```bash
   docker-compose ps postgres
   ```

3. 檢查環境變數是否正確:
   ```bash
   docker-compose config
   ```

### 資料庫連線失敗

1. 確認資料庫容器正在運行:
   ```bash
   docker-compose ps postgres
   ```

2. 確認資料庫已初始化:
   ```bash
   docker-compose logs postgres | grep "database system is ready"
   ```

3. 手動測試資料庫連線:
   ```bash
   docker-compose exec postgres psql -U sa -d SYSDATA -c "SELECT 1;"
   ```

### 健康檢查失敗

如果容器一直重啟,可能是健康檢查失敗:

```bash
# 查看容器狀態
docker inspect schedule_api | grep Health -A 10

# 暫時停用健康檢查重新部署
# 編輯 docker-compose.yml,註解掉 healthcheck 部分
```

### 端口衝突

如果端口被佔用,可以在 `.env` 中修改:

```env
API_PORT=8001
POSTGRES_PORT=5433
```

## 🔄 更新與維護

### 更新應用程式

```bash
# 1. 停止服務
docker-compose down

# 2. 拉取最新程式碼
git pull

# 3. 重新建置並啟動
docker-compose up -d --build
```

### 備份資料庫

```bash
# 備份
docker-compose exec postgres pg_dump -U sa SYSDATA > backup_$(date +%Y%m%d).sql

# 還原
docker-compose exec -T postgres psql -U sa SYSDATA < backup_20251005.sql
```

### 查看磁碟使用

```bash
# 查看 Volume 使用情況
docker volume ls
docker system df -v
```

## 📊 監控

### 即時日誌監控

```bash
# API 日誌
docker-compose logs -f api

# 資料庫日誌
docker-compose logs -f postgres
```

### API 日誌檔案

API 日誌會保存在主機的 `./API/logs/` 目錄:

```bash
# 查看日誌
tail -f API/logs/schedule_api.log

# Windows PowerShell
Get-Content API/logs/schedule_api.log -Wait
```

## ✅ 部署檢查清單

- [ ] 已複製並編輯 `.env` 檔案
- [ ] 已設定 `POSTGRES_PASSWORD`
- [ ] 已產生並設定 `ENCRYPTION_KEY`
- [ ] 已執行 `docker-compose up -d`
- [ ] 服務狀態顯示 `Up (healthy)`
- [ ] API 健康檢查正常 (`/health`)
- [ ] 資料庫連線正常 (`/health/db`)
- [ ] 可以訪問 API 文件 (`/docs`)

---

**部署完成!** 🎉

下一步可以開始開發 CRUD API 功能。
