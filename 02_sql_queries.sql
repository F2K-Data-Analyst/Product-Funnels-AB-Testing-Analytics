-- 02_sql_queries.sql
-- Schema + example analytical queries for Product Analytics project.

-- Example: core tables (simplified)
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP,
    email VARCHAR(255),
    country VARCHAR(50),
    signup_source VARCHAR(50),
    plan_type VARCHAR(50),
    is_active BOOLEAN
);

CREATE TABLE sessions (
    session_id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    device_id BIGINT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    referrer VARCHAR(255),
    utm_source VARCHAR(50),
    utm_medium VARCHAR(50),
    utm_campaign VARCHAR(50)
);

CREATE TABLE events (
    event_id BIGINT PRIMARY KEY,
    session_id BIGINT REFERENCES sessions(session_id),
    user_id BIGINT REFERENCES users(user_id),
    event_name VARCHAR(100),
    event_timestamp TIMESTAMP,
    page_url VARCHAR(500),
    product_id BIGINT,
    metadata_json JSON
);

CREATE TABLE purchases (
    purchase_id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    session_id BIGINT REFERENCES sessions(session_id),
    product_id BIGINT,
    amount_usd NUMERIC(10,2),
    currency VARCHAR(10),
    purchased_at TIMESTAMP,
    payment_method VARCHAR(50)
);

CREATE TABLE error_events (
    error_event_id BIGINT PRIMARY KEY,
    error_type_id BIGINT,
    user_id BIGINT REFERENCES users(user_id),
    session_id BIGINT REFERENCES sessions(session_id),
    event_id BIGINT REFERENCES events(event_id),
    product_id BIGINT,
    occurred_at TIMESTAMP,
    message TEXT,
    stack_trace TEXT,
    http_status_code INT,
    client_info_json JSON
);

-- Example: Daily Active Users (DAU)
SELECT
    DATE(event_timestamp) AS activity_date,
    COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY DATE(event_timestamp)
ORDER BY activity_date;

-- Example: Signup -> Report funnel conversion
WITH signup AS (
    SELECT DISTINCT user_id
    FROM events
    WHERE event_name = 'signup_completed'
),
first_report AS (
    SELECT DISTINCT user_id
    FROM events
    WHERE event_name = 'create_report'
)
SELECT
    (SELECT COUNT(*) FROM signup) AS users_signed_up,
    (SELECT COUNT(*) FROM first_report) AS users_created_report,
    (SELECT COUNT(*) FROM first_report) * 1.0 / NULLIF((SELECT COUNT(*) FROM signup), 0) AS conversion_rate;

-- Example: Error rate per 1,000 events
WITH event_counts AS (
    SELECT DATE(event_timestamp) AS d, COUNT(*) AS total_events
    FROM events
    GROUP BY DATE(event_timestamp)
),
error_counts AS (
    SELECT DATE(occurred_at) AS d, COUNT(*) AS total_errors
    FROM error_events
    GROUP BY DATE(occurred_at)
)
SELECT
    e.d,
    e.total_events,
    COALESCE(err.total_errors, 0) AS total_errors,
    COALESCE(err.total_errors, 0) * 1000.0 / NULLIF(e.total_events, 0) AS errors_per_1000_events
FROM event_counts e
LEFT JOIN error_counts err ON e.d = err.d
ORDER BY e.d;
