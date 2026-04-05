-- Database initialization script for Open_Source-Tech
-- This runs automatically when the PostgreSQL container starts for the first time.

CREATE TABLE IF NOT EXISTS items (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS features (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL UNIQUE,
    enabled     BOOLEAN DEFAULT FALSE,
    description TEXT,
    config      JSONB DEFAULT '{}',
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Seed a few default feature flags
INSERT INTO features (name, enabled, description) VALUES
    ('dark_mode',        FALSE, 'Enable dark mode for the web app'),
    ('beta_dashboard',   FALSE, 'Show the beta dashboard to users'),
    ('api_rate_limiting', TRUE,  'Enforce API rate limiting')
ON CONFLICT (name) DO NOTHING;
