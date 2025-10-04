-- =============================================
-- 新增執行狀態追蹤欄位
-- =============================================

-- 1. tblScheduleHttp 新增欄位
ALTER TABLE tblScheduleHttp
ADD COLUMN ExecutionStatus VARCHAR(20) DEFAULT 'Pending' CHECK (ExecutionStatus IN ('Pending', 'Processing', 'Completed', 'Failed', 'Cancelled')),
ADD COLUMN CurrentRetryCount INT DEFAULT 0;

-- 建立索引
CREATE INDEX idx_schedulehttp_executionstatus ON tblScheduleHttp(ExecutionStatus);
CREATE INDEX idx_schedulehttp_progcode ON tblScheduleHttp(ProgCode);

-- 註解
COMMENT ON COLUMN tblScheduleHttp.ExecutionStatus IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';
COMMENT ON COLUMN tblScheduleHttp.CurrentRetryCount IS '當前重試次數';


-- 2. tblScheduleMail 新增欄位
ALTER TABLE tblScheduleMail
ADD COLUMN ExecutionStatus VARCHAR(20) DEFAULT 'Pending' CHECK (ExecutionStatus IN ('Pending', 'Processing', 'Completed', 'Failed', 'Cancelled')),
ADD COLUMN CurrentRetryCount INT DEFAULT 0;

-- 建立索引
CREATE INDEX idx_schedulemail_executionstatus ON tblScheduleMail(ExecutionStatus);
CREATE INDEX idx_schedulemail_progcode ON tblScheduleMail(ProgCode);

-- 註解
COMMENT ON COLUMN tblScheduleMail.ExecutionStatus IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';
COMMENT ON COLUMN tblScheduleMail.CurrentRetryCount IS '當前重試次數';


-- 3. tblScheduleFTP 新增欄位
ALTER TABLE tblScheduleFTP
ADD COLUMN ExecutionStatus VARCHAR(20) DEFAULT 'Pending' CHECK (ExecutionStatus IN ('Pending', 'Processing', 'Completed', 'Failed', 'Cancelled')),
ADD COLUMN CurrentRetryCount INT DEFAULT 0;

-- 建立索引
CREATE INDEX idx_scheduleftp_executionstatus ON tblScheduleFTP(ExecutionStatus);
CREATE INDEX idx_scheduleftp_progcode ON tblScheduleFTP(ProgCode);

-- 註解
COMMENT ON COLUMN tblScheduleFTP.ExecutionStatus IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';
COMMENT ON COLUMN tblScheduleFTP.CurrentRetryCount IS '當前重試次數';
