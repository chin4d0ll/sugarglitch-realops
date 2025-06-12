-- Database initialization script for SugarGlitch RealOps
-- This script will be automatically executed when the PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create basic tables for the application
CREATE TABLE IF NOT EXISTS app_status (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    details JSONB
);

CREATE TABLE IF NOT EXISTS extraction_logs (
    id SERIAL PRIMARY KEY,
    session_id UUID DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation_type VARCHAR(100) NOT NULL,
    target VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    data JSONB,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS dm_data (
    id SERIAL PRIMARY KEY,
    extraction_id UUID DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    message_text TEXT,
    message_date TIMESTAMP,
    metadata JSONB
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_app_status_timestamp ON app_status(timestamp);
CREATE INDEX IF NOT EXISTS idx_extraction_logs_timestamp ON extraction_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_extraction_logs_session ON extraction_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_dm_data_timestamp ON dm_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_dm_data_extraction ON dm_data(extraction_id);

-- Insert initial status record
INSERT INTO app_status (status, message, details) 
VALUES ('initialized', 'Database initialized successfully', '{"version": "1.0", "created_at": "' || CURRENT_TIMESTAMP || '"}')
ON CONFLICT DO NOTHING;

-- Grant permissions to the application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sguser;

-- Print completion message
DO $$
BEGIN
    RAISE NOTICE 'SugarGlitch RealOps database initialization completed successfully!';
END $$;
