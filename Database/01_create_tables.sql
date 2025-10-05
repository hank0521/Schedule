-- Table: public.tblscheduleexception

-- DROP TABLE IF EXISTS public.tblscheduleexception;

CREATE TABLE IF NOT EXISTS public.tblscheduleexception
(
    id SERIAL NOT NULL,
    servicetype character varying(20) COLLATE pg_catalog."default" NOT NULL,
    servicetaskid integer NOT NULL,
    progcode character varying(200) COLLATE pg_catalog."default",
    exceptiontype character varying(100) COLLATE pg_catalog."default",
    exceptionmessage text COLLATE pg_catalog."default" NOT NULL,
    stacktrace text COLLATE pg_catalog."default",
    innerexception text COLLATE pg_catalog."default",
    httpurl text COLLATE pg_catalog."default",
    httpmethod character varying(10) COLLATE pg_catalog."default",
    httpstatus integer,
    mailrecipients text COLLATE pg_catalog."default",
    mailsubject character varying(500) COLLATE pg_catalog."default",
    ftphost character varying(200) COLLATE pg_catalog."default",
    ftplocalpath text COLLATE pg_catalog."default",
    ftpremotepath text COLLATE pg_catalog."default",
    occurreddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    isresolved boolean DEFAULT false,
    resolvedby character varying(100) COLLATE pg_catalog."default",
    resolveddate timestamp without time zone,
    resolvenote text COLLATE pg_catalog."default",
    CONSTRAINT tblscheduleexception_pkey PRIMARY KEY (id),
    CONSTRAINT tblscheduleexception_servicetype_check CHECK (servicetype::text = ANY (ARRAY['HTTP'::character varying, 'MAIL'::character varying, 'FTP'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblscheduleexception
    OWNER to sa;

COMMENT ON TABLE public.tblscheduleexception
    IS '排程例外記錄表';

COMMENT ON COLUMN public.tblscheduleexception.servicetype
    IS '服務類型 (HTTP/MAIL/FTP)';

COMMENT ON COLUMN public.tblscheduleexception.servicetaskid
    IS '對應的任務 ID';

COMMENT ON COLUMN public.tblscheduleexception.exceptiontype
    IS '例外類型';

COMMENT ON COLUMN public.tblscheduleexception.exceptionmessage
    IS '例外訊息';

COMMENT ON COLUMN public.tblscheduleexception.stacktrace
    IS '堆疊追蹤';

COMMENT ON COLUMN public.tblscheduleexception.isresolved
    IS '是否已解決';
-- Index: idx_scheduleexception_isresolved

-- DROP INDEX IF EXISTS public.idx_scheduleexception_isresolved;

CREATE INDEX IF NOT EXISTS idx_scheduleexception_isresolved
    ON public.tblscheduleexception USING btree
    (isresolved ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleexception_occurreddate

-- DROP INDEX IF EXISTS public.idx_scheduleexception_occurreddate;

CREATE INDEX IF NOT EXISTS idx_scheduleexception_occurreddate
    ON public.tblscheduleexception USING btree
    (occurreddate ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleexception_servicetaskid

-- DROP INDEX IF EXISTS public.idx_scheduleexception_servicetaskid;

CREATE INDEX IF NOT EXISTS idx_scheduleexception_servicetaskid
    ON public.tblscheduleexception USING btree
    (servicetaskid ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleexception_servicetype

-- DROP INDEX IF EXISTS public.idx_scheduleexception_servicetype;

CREATE INDEX IF NOT EXISTS idx_scheduleexception_servicetype
    ON public.tblscheduleexception USING btree
    (servicetype COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;


-- Table: public.tblscheduleexecutionhistory

-- DROP TABLE IF EXISTS public.tblscheduleexecutionhistory;

CREATE TABLE IF NOT EXISTS public.tblscheduleexecutionhistory
(
    id SERIAL NOT NULL,
    servicetype character varying(20) COLLATE pg_catalog."default" NOT NULL,
    servicetaskid integer NOT NULL,
    progcode character varying(200) COLLATE pg_catalog."default",
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone,
    durationms integer,
    issuccess boolean NOT NULL,
    errormessage text COLLATE pg_catalog."default",
    httpstatus integer,
    responsesize integer,
    emailssent integer,
    filestransferred integer,
    bytestransferred bigint,
    executiondetails jsonb,
    createddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT tblscheduleexecutionhistory_pkey PRIMARY KEY (id),
    CONSTRAINT tblscheduleexecutionhistory_servicetype_check CHECK (servicetype::text = ANY (ARRAY['HTTP'::character varying, 'MAIL'::character varying, 'FTP'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblscheduleexecutionhistory
    OWNER to sa;

COMMENT ON TABLE public.tblscheduleexecutionhistory
    IS '排程執行歷史記錄表';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.servicetype
    IS '服務類型 (HTTP/MAIL/FTP)';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.servicetaskid
    IS '對應的任務 ID';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.starttime
    IS '開始時間';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.endtime
    IS '結束時間';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.durationms
    IS '執行時長 (毫秒)';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.issuccess
    IS '是否成功';

COMMENT ON COLUMN public.tblscheduleexecutionhistory.executiondetails
    IS '執行詳情 (JSON 格式)';
-- Index: idx_schedulehistory_issuccess

-- DROP INDEX IF EXISTS public.idx_schedulehistory_issuccess;

CREATE INDEX IF NOT EXISTS idx_schedulehistory_issuccess
    ON public.tblscheduleexecutionhistory USING btree
    (issuccess ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehistory_servicetaskid

-- DROP INDEX IF EXISTS public.idx_schedulehistory_servicetaskid;

CREATE INDEX IF NOT EXISTS idx_schedulehistory_servicetaskid
    ON public.tblscheduleexecutionhistory USING btree
    (servicetaskid ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehistory_servicetype

-- DROP INDEX IF EXISTS public.idx_schedulehistory_servicetype;

CREATE INDEX IF NOT EXISTS idx_schedulehistory_servicetype
    ON public.tblscheduleexecutionhistory USING btree
    (servicetype COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehistory_starttime

-- DROP INDEX IF EXISTS public.idx_schedulehistory_starttime;

CREATE INDEX IF NOT EXISTS idx_schedulehistory_starttime
    ON public.tblscheduleexecutionhistory USING btree
    (starttime ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;


-- Table: public.tblscheduleftp

-- DROP TABLE IF EXISTS public.tblscheduleftp;

CREATE TABLE IF NOT EXISTS public.tblscheduleftp
(
    id SERIAL NOT NULL,
    progcode character varying(200) COLLATE pg_catalog."default" NOT NULL,
    ftphost character varying(200) COLLATE pg_catalog."default" NOT NULL,
    ftpport integer DEFAULT 21,
    ftpusername character varying(200) COLLATE pg_catalog."default" NOT NULL,
    ftppassword character varying(500) COLLATE pg_catalog."default",
    ftpprotocol character varying(10) COLLATE pg_catalog."default" DEFAULT 'FTP'::character varying,
    ftpmode character varying(10) COLLATE pg_catalog."default" DEFAULT 'Passive'::character varying,
    ftpencoding character varying(50) COLLATE pg_catalog."default" DEFAULT 'UTF-8'::character varying,
    ftptimeoutseconds integer DEFAULT 30,
    localfilepath text COLLATE pg_catalog."default" NOT NULL,
    remotefilepath text COLLATE pg_catalog."default" NOT NULL,
    transfermode character varying(10) COLLATE pg_catalog."default" DEFAULT 'Binary'::character varying,
    overwriteexisting boolean DEFAULT true,
    createremotedirectory boolean DEFAULT true,
    deletelocalafterupload boolean DEFAULT false,
    retrycount integer DEFAULT 0,
    retryintervalseconds integer DEFAULT 5,
    lastexecutetime timestamp without time zone,
    lastsuccesstime timestamp without time zone,
    lasttransferredfiles text COLLATE pg_catalog."default",
    lasttransferredbytes bigint,
    lasterrormessage text COLLATE pg_catalog."default",
    executecount integer DEFAULT 0,
    successcount integer DEFAULT 0,
    failurecount integer DEFAULT 0,
    isenabled boolean DEFAULT true,
    schedulecron character varying(100) COLLATE pg_catalog."default",
    nextexecutetime timestamp without time zone,
    createdby character varying(100) COLLATE pg_catalog."default",
    createddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    modifiedby character varying(100) COLLATE pg_catalog."default",
    modifieddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    remark text COLLATE pg_catalog."default",
    executionstatus character varying(20) COLLATE pg_catalog."default" DEFAULT 'Pending'::character varying,
    currentretrycount integer DEFAULT 0,
    CONSTRAINT tblscheduleftp_pkey PRIMARY KEY (id),
    CONSTRAINT tblscheduleftp_executionstatus_check CHECK (executionstatus::text = ANY (ARRAY['Pending'::character varying, 'Processing'::character varying, 'Completed'::character varying, 'Failed'::character varying, 'Cancelled'::character varying]::text[])),
    CONSTRAINT tblscheduleftp_ftpmode_check CHECK (ftpmode::text = ANY (ARRAY['Active'::character varying, 'Passive'::character varying]::text[])),
    CONSTRAINT tblscheduleftp_ftpprotocol_check CHECK (ftpprotocol::text = ANY (ARRAY['FTP'::character varying, 'FTPS'::character varying, 'SFTP'::character varying]::text[])),
    CONSTRAINT tblscheduleftp_transfermode_check CHECK (transfermode::text = ANY (ARRAY['Binary'::character varying, 'ASCII'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblscheduleftp
    OWNER to sa;

COMMENT ON TABLE public.tblscheduleftp
    IS 'FTP 傳輸排程表';

COMMENT ON COLUMN public.tblscheduleftp.id
    IS '主鍵 ID';

COMMENT ON COLUMN public.tblscheduleftp.progcode
    IS '程式代碼';

COMMENT ON COLUMN public.tblscheduleftp.ftphost
    IS 'FTP 主機位址';

COMMENT ON COLUMN public.tblscheduleftp.ftpport
    IS 'FTP 連接埠';

COMMENT ON COLUMN public.tblscheduleftp.ftpusername
    IS 'FTP 使用者名稱';

COMMENT ON COLUMN public.tblscheduleftp.ftppassword
    IS 'FTP 密碼';

COMMENT ON COLUMN public.tblscheduleftp.ftpprotocol
    IS 'FTP 協定 (FTP/FTPS/SFTP)';

COMMENT ON COLUMN public.tblscheduleftp.ftpmode
    IS 'FTP 模式 (Active/Passive)';

COMMENT ON COLUMN public.tblscheduleftp.localfilepath
    IS '本地檔案路徑';

COMMENT ON COLUMN public.tblscheduleftp.remotefilepath
    IS '遠端檔案路徑';

COMMENT ON COLUMN public.tblscheduleftp.transfermode
    IS '傳輸模式 (Binary/ASCII)';

COMMENT ON COLUMN public.tblscheduleftp.overwriteexisting
    IS '是否覆寫現有檔案';

COMMENT ON COLUMN public.tblscheduleftp.createremotedirectory
    IS '是否自動建立遠端目錄';

COMMENT ON COLUMN public.tblscheduleftp.deletelocalafterupload
    IS '上傳後是否刪除本地檔案';

COMMENT ON COLUMN public.tblscheduleftp.executionstatus
    IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';

COMMENT ON COLUMN public.tblscheduleftp.currentretrycount
    IS '當前重試次數';
-- Index: idx_scheduleftp_createddate

-- DROP INDEX IF EXISTS public.idx_scheduleftp_createddate;

CREATE INDEX IF NOT EXISTS idx_scheduleftp_createddate
    ON public.tblscheduleftp USING btree
    (createddate ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleftp_executionstatus

-- DROP INDEX IF EXISTS public.idx_scheduleftp_executionstatus;

CREATE INDEX IF NOT EXISTS idx_scheduleftp_executionstatus
    ON public.tblscheduleftp USING btree
    (executionstatus COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleftp_isenabled

-- DROP INDEX IF EXISTS public.idx_scheduleftp_isenabled;

CREATE INDEX IF NOT EXISTS idx_scheduleftp_isenabled
    ON public.tblscheduleftp USING btree
    (isenabled ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleftp_nextexecutetime

-- DROP INDEX IF EXISTS public.idx_scheduleftp_nextexecutetime;

CREATE INDEX IF NOT EXISTS idx_scheduleftp_nextexecutetime
    ON public.tblscheduleftp USING btree
    (nextexecutetime ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_scheduleftp_progcode

-- DROP INDEX IF EXISTS public.idx_scheduleftp_progcode;

CREATE INDEX IF NOT EXISTS idx_scheduleftp_progcode
    ON public.tblscheduleftp USING btree
    (progcode COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;

-- Table: public.tblschedulehttp

-- DROP TABLE IF EXISTS public.tblschedulehttp;

CREATE TABLE IF NOT EXISTS public.tblschedulehttp
(
    id SERIAL NOT NULL,
    progcode character varying(200) COLLATE pg_catalog."default" NOT NULL,
    url text COLLATE pg_catalog."default" NOT NULL,
    httpmethod character varying(10) COLLATE pg_catalog."default" NOT NULL DEFAULT 'GET'::character varying,
    headers jsonb,
    requestbody text COLLATE pg_catalog."default",
    contenttype character varying(100) COLLATE pg_catalog."default" DEFAULT 'application/json'::character varying,
    encoding character varying(50) COLLATE pg_catalog."default" DEFAULT 'UTF-8'::character varying,
    timeoutseconds integer DEFAULT 30,
    retrycount integer DEFAULT 0,
    retryintervalseconds integer DEFAULT 5,
    expectedhttpstatus integer DEFAULT 200,
    lastexecutetime timestamp without time zone,
    lasthttpstatus integer,
    lastresponsebody text COLLATE pg_catalog."default",
    lasterrormessage text COLLATE pg_catalog."default",
    executecount integer DEFAULT 0,
    successcount integer DEFAULT 0,
    failurecount integer DEFAULT 0,
    isenabled boolean DEFAULT true,
    schedulecron character varying(100) COLLATE pg_catalog."default",
    nextexecutetime timestamp without time zone,
    createdby character varying(100) COLLATE pg_catalog."default",
    createddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    modifiedby character varying(100) COLLATE pg_catalog."default",
    modifieddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    remark text COLLATE pg_catalog."default",
    executionstatus character varying(20) COLLATE pg_catalog."default" DEFAULT 'Pending'::character varying,
    currentretrycount integer DEFAULT 0,
    CONSTRAINT tblschedulehttp_pkey PRIMARY KEY (id),
    CONSTRAINT tblschedulehttp_executionstatus_check CHECK (executionstatus::text = ANY (ARRAY['Pending'::character varying, 'Processing'::character varying, 'Completed'::character varying, 'Failed'::character varying, 'Cancelled'::character varying]::text[])),
    CONSTRAINT tblschedulehttp_httpmethod_check CHECK (httpmethod::text = ANY (ARRAY['GET'::character varying, 'POST'::character varying, 'PUT'::character varying, 'DELETE'::character varying, 'PATCH'::character varying, 'HEAD'::character varying, 'OPTIONS'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblschedulehttp
    OWNER to sa;

COMMENT ON TABLE public.tblschedulehttp
    IS 'HTTP 請求排程表';

COMMENT ON COLUMN public.tblschedulehttp.id
    IS '主鍵 ID';

COMMENT ON COLUMN public.tblschedulehttp.progcode
    IS '程式代碼';

COMMENT ON COLUMN public.tblschedulehttp.url
    IS '目標 URL';

COMMENT ON COLUMN public.tblschedulehttp.httpmethod
    IS 'HTTP 方法 (GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS)';

COMMENT ON COLUMN public.tblschedulehttp.headers
    IS 'HTTP Headers (JSON 格式)';

COMMENT ON COLUMN public.tblschedulehttp.requestbody
    IS '請求內容';

COMMENT ON COLUMN public.tblschedulehttp.contenttype
    IS 'Content-Type';

COMMENT ON COLUMN public.tblschedulehttp.encoding
    IS '編碼格式';

COMMENT ON COLUMN public.tblschedulehttp.timeoutseconds
    IS '逾時秒數';

COMMENT ON COLUMN public.tblschedulehttp.retrycount
    IS '重試次數';

COMMENT ON COLUMN public.tblschedulehttp.retryintervalseconds
    IS '重試間隔秒數';

COMMENT ON COLUMN public.tblschedulehttp.expectedhttpstatus
    IS '預期 HTTP 狀態碼';

COMMENT ON COLUMN public.tblschedulehttp.lastexecutetime
    IS '最後執行時間';

COMMENT ON COLUMN public.tblschedulehttp.lasthttpstatus
    IS '最後 HTTP 狀態碼';

COMMENT ON COLUMN public.tblschedulehttp.lastresponsebody
    IS '最後回應內容';

COMMENT ON COLUMN public.tblschedulehttp.lasterrormessage
    IS '最後錯誤訊息';

COMMENT ON COLUMN public.tblschedulehttp.isenabled
    IS '是否啟用';

COMMENT ON COLUMN public.tblschedulehttp.schedulecron
    IS 'Cron 排程表達式';

COMMENT ON COLUMN public.tblschedulehttp.nextexecutetime
    IS '下次執行時間';

COMMENT ON COLUMN public.tblschedulehttp.executionstatus
    IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';

COMMENT ON COLUMN public.tblschedulehttp.currentretrycount
    IS '當前重試次數';
-- Index: idx_schedulehttp_createddate

-- DROP INDEX IF EXISTS public.idx_schedulehttp_createddate;

CREATE INDEX IF NOT EXISTS idx_schedulehttp_createddate
    ON public.tblschedulehttp USING btree
    (createddate ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehttp_executionstatus

-- DROP INDEX IF EXISTS public.idx_schedulehttp_executionstatus;

CREATE INDEX IF NOT EXISTS idx_schedulehttp_executionstatus
    ON public.tblschedulehttp USING btree
    (executionstatus COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehttp_isenabled

-- DROP INDEX IF EXISTS public.idx_schedulehttp_isenabled;

CREATE INDEX IF NOT EXISTS idx_schedulehttp_isenabled
    ON public.tblschedulehttp USING btree
    (isenabled ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehttp_nextexecutetime

-- DROP INDEX IF EXISTS public.idx_schedulehttp_nextexecutetime;

CREATE INDEX IF NOT EXISTS idx_schedulehttp_nextexecutetime
    ON public.tblschedulehttp USING btree
    (nextexecutetime ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulehttp_progcode

-- DROP INDEX IF EXISTS public.idx_schedulehttp_progcode;

CREATE INDEX IF NOT EXISTS idx_schedulehttp_progcode
    ON public.tblschedulehttp USING btree
    (progcode COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;

-- Table: public.tblschedulemail

-- DROP TABLE IF EXISTS public.tblschedulemail;

CREATE TABLE IF NOT EXISTS public.tblschedulemail
(
    id SERIAL NOT NULL,
    progcode character varying(200) COLLATE pg_catalog."default" NOT NULL,
    sender character varying(200) COLLATE pg_catalog."default" NOT NULL,
    sendername character varying(200) COLLATE pg_catalog."default",
    recipients text COLLATE pg_catalog."default" NOT NULL,
    cc text COLLATE pg_catalog."default",
    bcc text COLLATE pg_catalog."default",
    replyto character varying(200) COLLATE pg_catalog."default",
    subject character varying(500) COLLATE pg_catalog."default" NOT NULL,
    body text COLLATE pg_catalog."default" NOT NULL,
    bodytype character varying(10) COLLATE pg_catalog."default" DEFAULT 'HTML'::character varying,
    priority character varying(10) COLLATE pg_catalog."default" DEFAULT 'Normal'::character varying,
    encoding character varying(50) COLLATE pg_catalog."default" DEFAULT 'UTF-8'::character varying,
    attachmentpaths text COLLATE pg_catalog."default",
    smtphost character varying(200) COLLATE pg_catalog."default",
    smtpport integer DEFAULT 587,
    smtpusername character varying(200) COLLATE pg_catalog."default",
    smtppassword character varying(500) COLLATE pg_catalog."default",
    smtpenablessl boolean DEFAULT true,
    smtptimeoutseconds integer DEFAULT 30,
    lastexecutetime timestamp without time zone,
    lastsuccesstime timestamp without time zone,
    lasterrormessage text COLLATE pg_catalog."default",
    executecount integer DEFAULT 0,
    successcount integer DEFAULT 0,
    failurecount integer DEFAULT 0,
    isenabled boolean DEFAULT true,
    schedulecron character varying(100) COLLATE pg_catalog."default",
    nextexecutetime timestamp without time zone,
    createdby character varying(100) COLLATE pg_catalog."default",
    createddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    modifiedby character varying(100) COLLATE pg_catalog."default",
    modifieddate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    remark text COLLATE pg_catalog."default",
    executionstatus character varying(20) COLLATE pg_catalog."default" DEFAULT 'Pending'::character varying,
    currentretrycount integer DEFAULT 0,
    CONSTRAINT tblschedulemail_pkey PRIMARY KEY (id),
    CONSTRAINT tblschedulemail_bodytype_check CHECK (bodytype::text = ANY (ARRAY['HTML'::character varying, 'TEXT'::character varying]::text[])),
    CONSTRAINT tblschedulemail_executionstatus_check CHECK (executionstatus::text = ANY (ARRAY['Pending'::character varying, 'Processing'::character varying, 'Completed'::character varying, 'Failed'::character varying, 'Cancelled'::character varying]::text[])),
    CONSTRAINT tblschedulemail_priority_check CHECK (priority::text = ANY (ARRAY['Low'::character varying, 'Normal'::character varying, 'High'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tblschedulemail
    OWNER to sa;

COMMENT ON TABLE public.tblschedulemail
    IS 'Email 發送排程表';

COMMENT ON COLUMN public.tblschedulemail.id
    IS '主鍵 ID';

COMMENT ON COLUMN public.tblschedulemail.progcode
    IS '程式代碼';

COMMENT ON COLUMN public.tblschedulemail.sender
    IS '寄件者信箱';

COMMENT ON COLUMN public.tblschedulemail.sendername
    IS '寄件者名稱';

COMMENT ON COLUMN public.tblschedulemail.recipients
    IS '收件者 (多個以分號分隔)';

COMMENT ON COLUMN public.tblschedulemail.cc
    IS '副本收件者 (多個以分號分隔)';

COMMENT ON COLUMN public.tblschedulemail.bcc
    IS '密件副本收件者 (多個以分號分隔)';

COMMENT ON COLUMN public.tblschedulemail.replyto
    IS '回覆信箱';

COMMENT ON COLUMN public.tblschedulemail.subject
    IS '郵件主旨';

COMMENT ON COLUMN public.tblschedulemail.body
    IS '郵件內容';

COMMENT ON COLUMN public.tblschedulemail.bodytype
    IS '郵件格式 (HTML/TEXT)';

COMMENT ON COLUMN public.tblschedulemail.priority
    IS '優先順序 (Low/Normal/High)';

COMMENT ON COLUMN public.tblschedulemail.attachmentpaths
    IS '附件路徑 (多個以分號分隔)';

COMMENT ON COLUMN public.tblschedulemail.executionstatus
    IS '執行狀態 (Pending/Processing/Completed/Failed/Cancelled)';

COMMENT ON COLUMN public.tblschedulemail.currentretrycount
    IS '當前重試次數';
-- Index: idx_schedulemail_createddate

-- DROP INDEX IF EXISTS public.idx_schedulemail_createddate;

CREATE INDEX IF NOT EXISTS idx_schedulemail_createddate
    ON public.tblschedulemail USING btree
    (createddate ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulemail_executionstatus

-- DROP INDEX IF EXISTS public.idx_schedulemail_executionstatus;

CREATE INDEX IF NOT EXISTS idx_schedulemail_executionstatus
    ON public.tblschedulemail USING btree
    (executionstatus COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulemail_isenabled

-- DROP INDEX IF EXISTS public.idx_schedulemail_isenabled;

CREATE INDEX IF NOT EXISTS idx_schedulemail_isenabled
    ON public.tblschedulemail USING btree
    (isenabled ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulemail_nextexecutetime

-- DROP INDEX IF EXISTS public.idx_schedulemail_nextexecutetime;

CREATE INDEX IF NOT EXISTS idx_schedulemail_nextexecutetime
    ON public.tblschedulemail USING btree
    (nextexecutetime ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_schedulemail_progcode

-- DROP INDEX IF EXISTS public.idx_schedulemail_progcode;

CREATE INDEX IF NOT EXISTS idx_schedulemail_progcode
    ON public.tblschedulemail USING btree
    (progcode COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;