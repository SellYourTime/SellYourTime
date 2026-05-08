-- ═══════════════════════════════════════════════
--  Timely Bot — Database Schema (PostgreSQL)
--  نسخه ۱.۰ | طراحی شده برای ۱۰۰٬۰۰۰+ کاربر
-- ═══════════════════════════════════════════════

-- ─── Extensions ───
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis; -- برای جستجوی مکانی GPS

-- ─── USERS ───────────────────────────────────────
CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    telegram_id     BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(64),
    nickname        VARCHAR(32) UNIQUE NOT NULL,       -- نیک‌نیم عمومی
    full_name       VARCHAR(128) NOT NULL,             -- هویت واقعی (محرمانه)
    national_id     VARCHAR(10) UNIQUE,                -- کد ملی (رمزنگاری شده)
    gender          VARCHAR(8) CHECK (gender IN ('male','female')),
    birth_date      DATE NOT NULL,
    city            VARCHAR(64),
    bio             TEXT,
    avatar_file_id  VARCHAR(256),                      -- Telegram file_id عکس
    price_per_hour  INTEGER DEFAULT 200000,            -- تومان
    min_hours       SMALLINT DEFAULT 1,
    max_hours       SMALLINT DEFAULT 6,
    pet_friendly    BOOLEAN DEFAULT FALSE,
    is_seller       BOOLEAN DEFAULT FALSE,             -- آیا وقت می‌فروشد؟
    is_verified     BOOLEAN DEFAULT FALSE,             -- تأیید هویت ادمین
    is_active       BOOLEAN DEFAULT TRUE,
    is_banned       BOOLEAN DEFAULT FALSE,
    ban_reason      TEXT,
    rating_avg      NUMERIC(3,2) DEFAULT 0,
    rating_count    INTEGER DEFAULT 0,
    balance         INTEGER DEFAULT 0,                 -- کیف پول (تومان)
    referral_code   VARCHAR(16) UNIQUE,
    referred_by     BIGINT REFERENCES users(id),
    referral_count  INTEGER DEFAULT 0,
    discount_pct    SMALLINT DEFAULT 0,               -- درصد تخفیف فعال
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    last_active     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_telegram ON users(telegram_id);
CREATE INDEX idx_users_city ON users(city);
CREATE INDEX idx_users_gender ON users(gender);
CREATE INDEX idx_users_seller ON users(is_seller) WHERE is_seller = TRUE;

-- ─── USER ACTIVITIES ─────────────────────────────
CREATE TABLE user_activities (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity    VARCHAR(64) NOT NULL,
    category    VARCHAR(32) NOT NULL,
    UNIQUE(user_id, activity)
);

-- ─── BOOKINGS ────────────────────────────────────
CREATE TABLE bookings (
    id              BIGSERIAL PRIMARY KEY,
    buyer_id        BIGINT NOT NULL REFERENCES users(id),
    seller_id       BIGINT NOT NULL REFERENCES users(id),
    activity        VARCHAR(64) NOT NULL,
    hours           SMALLINT NOT NULL CHECK (hours BETWEEN 1 AND 6),
    price_per_hour  INTEGER NOT NULL,
    total_amount    INTEGER NOT NULL,                 -- مبلغ کل (تومان)
    platform_fee    INTEGER NOT NULL,                 -- کارمزد ۲۵٪
    seller_amount   INTEGER NOT NULL,                 -- سهم فروشنده ۷۵٪
    discount_pct    SMALLINT DEFAULT 0,
    scheduled_at    TIMESTAMPTZ,                      -- زمان قرار
    status          VARCHAR(24) DEFAULT 'pending' CHECK (
                        status IN (
                            'pending',       -- منتظر تأیید فروشنده
                            'confirmed',     -- تأیید شده - منتظر پرداخت
                            'paid',          -- پرداخت شده - منتظر قرار
                            'gps_waiting',   -- GPS فعال - در راه
                            'in_progress',   -- قرار در حال انجام
                            'completed',     -- قرار کامل شد
                            'cancelled',     -- لغو شده
                            'disputed'       -- اختلاف
                        )
                    ),
    cancelled_by    BIGINT REFERENCES users(id),
    cancel_reason   TEXT,
    gps_started_at  TIMESTAMPTZ,                     -- شروع GPS
    started_at      TIMESTAMPTZ,                     -- شروع تایمر
    ended_at        TIMESTAMPTZ,                     -- پایان تایمر
    buyer_confirmed BOOLEAN DEFAULT FALSE,           -- تأیید خریدار
    seller_confirmed BOOLEAN DEFAULT FALSE,          -- تأیید فروشنده
    payment_ref     VARCHAR(128),                    -- شماره پیگیری پرداخت
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_bookings_buyer ON bookings(buyer_id);
CREATE INDEX idx_bookings_seller ON bookings(seller_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_scheduled ON bookings(scheduled_at);

-- ─── RATINGS ─────────────────────────────────────
CREATE TABLE ratings (
    id              BIGSERIAL PRIMARY KEY,
    booking_id      BIGINT UNIQUE NOT NULL REFERENCES bookings(id),
    rater_id        BIGINT NOT NULL REFERENCES users(id),
    rated_id        BIGINT NOT NULL REFERENCES users(id),
    stars           SMALLINT NOT NULL CHECK (stars BETWEEN 1 AND 5),
    reasons         TEXT[],                          -- دلایل نارضایتی (اگه < 4)
    note            TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- trigger: بروزرسانی خودکار میانگین امتیاز
CREATE OR REPLACE FUNCTION update_user_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users SET
        rating_avg = (SELECT AVG(stars) FROM ratings WHERE rated_id = NEW.rated_id),
        rating_count = (SELECT COUNT(*) FROM ratings WHERE rated_id = NEW.rated_id)
    WHERE id = NEW.rated_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_rating
AFTER INSERT ON ratings
FOR EACH ROW EXECUTE FUNCTION update_user_rating();

-- ─── DUAL EVENTS (ایونت دونفره) ──────────────────
CREATE TABLE dual_events (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(128) NOT NULL,
    event_type  VARCHAR(32),                        -- سینما، کنسرت، تئاتر...
    venue       VARCHAR(256),
    city        VARCHAR(64),
    event_date  TIMESTAMPTZ NOT NULL,
    price       INTEGER NOT NULL,
    discount_pct SMALLINT DEFAULT 0,
    total_spots  SMALLINT DEFAULT 10,
    filled_spots SMALLINT DEFAULT 0,
    image_url   VARCHAR(512),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── GROUP EVENTS (تور گروهی) ─────────────────────
CREATE TABLE group_events (
    id              BIGSERIAL PRIMARY KEY,
    leader_id       BIGINT NOT NULL REFERENCES users(id),
    title           VARCHAR(128) NOT NULL,
    category        VARCHAR(32),
    description     TEXT,
    location        VARCHAR(256),
    city            VARCHAR(64),
    event_date      TIMESTAMPTZ NOT NULL,
    duration_hours  SMALLINT,
    price           INTEGER NOT NULL,
    discount_pct    SMALLINT DEFAULT 0,
    leader_bio      TEXT,
    status          VARCHAR(16) DEFAULT 'pending'
                    CHECK (status IN ('pending','approved','rejected','cancelled','completed')),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE group_event_participants (
    id          BIGSERIAL PRIMARY KEY,
    event_id    BIGINT NOT NULL REFERENCES group_events(id),
    user_id     BIGINT NOT NULL REFERENCES users(id),
    status      VARCHAR(16) DEFAULT 'registered',
    payment_ref VARCHAR(128),
    joined_at   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);

-- ─── GPS SESSIONS ─────────────────────────────────
CREATE TABLE gps_sessions (
    id              BIGSERIAL PRIMARY KEY,
    booking_id      BIGINT UNIQUE NOT NULL REFERENCES bookings(id),
    buyer_lat       DOUBLE PRECISION,
    buyer_lng       DOUBLE PRECISION,
    buyer_updated   TIMESTAMPTZ,
    seller_lat      DOUBLE PRECISION,
    seller_lng      DOUBLE PRECISION,
    seller_updated  TIMESTAMPTZ,
    distance_meters INTEGER,
    proximity_hit   BOOLEAN DEFAULT FALSE,           -- آیا ۵۰ متر رسیدن؟
    proximity_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── PAYMENTS ─────────────────────────────────────
CREATE TABLE payments (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id),
    booking_id      BIGINT REFERENCES bookings(id),
    amount          INTEGER NOT NULL,
    type            VARCHAR(16) CHECK (type IN ('charge','withdraw','refund','fee')),
    status          VARCHAR(16) DEFAULT 'pending'
                    CHECK (status IN ('pending','success','failed')),
    gateway_ref     VARCHAR(128),
    description     TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── REPORTS / FLAGS ──────────────────────────────
CREATE TABLE reports (
    id              BIGSERIAL PRIMARY KEY,
    reporter_id     BIGINT NOT NULL REFERENCES users(id),
    reported_id     BIGINT NOT NULL REFERENCES users(id),
    booking_id      BIGINT REFERENCES bookings(id),
    reason          VARCHAR(64),
    description     TEXT,
    status          VARCHAR(16) DEFAULT 'open'
                    CHECK (status IN ('open','reviewing','resolved','dismissed')),
    resolved_by     BIGINT REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── ADMIN ACTIONS LOG ────────────────────────────
CREATE TABLE admin_logs (
    id          BIGSERIAL PRIMARY KEY,
    admin_id    BIGINT NOT NULL,
    action      VARCHAR(64),
    target_type VARCHAR(32),
    target_id   BIGINT,
    note        TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── REFERRALS ────────────────────────────────────
CREATE TABLE referrals (
    id              BIGSERIAL PRIMARY KEY,
    referrer_id     BIGINT NOT NULL REFERENCES users(id),
    referred_id     BIGINT NOT NULL REFERENCES users(id),
    is_successful   BOOLEAN DEFAULT FALSE,          -- آیا اولین رزرو انجام شد؟
    discount_granted SMALLINT DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(referred_id)
);
