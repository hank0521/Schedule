## **\[0.1.0\] \- 2025-10-08**

* 開發與測試環境
  * API 文件 (Swagger UI): http://localhost:8000/docs

  * 資料庫管理 (pgAdmin): http://localhost:5050
### **✨ 新增 (Added)**

* **郵件任務執行功能**:  
  * 新增 POST /api/execute/mail/trigger-due 端點，用於批次觸發所有到期的郵件任務。

 測試用的insert sql: (sender一定要用hello@demomailtrap.co)
```
INSERT INTO public.tblschedulemail (
    progcode,
    sender,
    recipients,
    subject,
    body,
    isenabled,
    nextexecutetime,
    executionstatus
) VALUES (
    'TEST_MAILTRAP_LIVE',
    'hello@demomailtrap.co',
    'posping@gmail.com',
    '來自 Mailtrap 正式環境的測試信',
    '<h1>測試成功</h1><p>這封信是透過 Mailtrap 的 live.smtp.mailtrap.io 伺服器發送的。</p>',
    true,
    '2025-10-07 11:00:00',
    'Pending'
);
```

  * 新增 POST /api/execute/mail/{id} 端點，用於手動觸發單一郵件任務的立即發送。  


* **郵件排程 CRUD API**:  
  * 實作了完整的郵件排程任務 (tblschedulemail) 的 CRUD (新增、查詢、更新、刪除) 功能。  
  * API 路徑遵循 /api/schedule/mail 規範。  
  * 新增 PATCH /api/schedule/mail/{id}/status 端點，用於快速啟用或停用任務。  
  
* **核心郵件發送服務**:  
  * 建立 email\_sender.py 服務，封裝所有 smtplib 郵件發送邏輯。  
  * 實作預設 SMTP 伺服器 fallback 機制：當資料庫記錄中未指定 SMTP 設定時，會自動從 .env 檔案讀取預設值。  
  * 支援 STARTTLS 加密連線流程，相容 Mailtrap 沙盒及正式環境。  
* **高併發處理機制**:  
  * 在批次觸發 API 中，採用 SELECT ... FOR UPDATE SKIP LOCKED 搭配 UPDATE ... RETURNING 的原子性查詢，有效避免在高併發環境下的競爭條件 (Race Condition) 和重複發信問題。  
* **模組化專案結構**:  
  * 新增 schemas, models, crud, routers, services 等資料夾，將資料驗證、資料庫模型、資料庫操作、API 路由及商業 logique 清晰分離。  
* **專案文件**:  
  * 新增 README.md，深入說明郵件排程核心機制的運作原理及高併發解決方案。  
  * 新增此 CHANGELOG.md 檔案，以追蹤版本變更。

### **🐛 修正 (Fixed)**

* **API 路由順序**: 修正 execute.py 中因路由順序錯誤，導致 trigger-due 被誤判為 {id} 的 422 錯誤。  
* **背景任務資料庫連線**: 修正背景任務因使用已關閉的資料庫 Session 而導致的 500 內部伺服器錯誤。現在背景任務會自行建立獨立的 Session。  
* **SQLAlchemy 語法**: 修正 UPDATE 語句中錯誤使用 .with\_for\_update 的 AttributeError。  
* **SMTP 連線**: 修正因 SSL/TLS 設定不符伺服器要求而導致的 Connection unexpectedly closed 錯誤。

### **🔄 變更 (Changed)**

* **Pydantic V2 相容性**: 將 Pydantic 模型中的 orm\_mode \= True 更新為 from\_attributes \= True，以消除版本警告。  
* **Docker 開發環境**:  
  * 在 docker-compose.yml 中為 api 服務加入 volumes 掛載，實現本機程式碼與容器的即時同步。  
  * 在 Dockerfile 中為 uvicorn 啟動指令加上 \--reload 參數，確保在 Windows 環境下檔案變更能穩定觸發服務重載。  
  * 在 docker-compose.yml、.env 及 config.py 中加入預設 SMTP 伺服器設定，並確保其能正確傳遞至 API 服務中。