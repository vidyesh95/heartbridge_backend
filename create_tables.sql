-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    email_id VARCHAR(255) UNIQUE,
    auth_provider VARCHAR(100),
    provider_id VARCHAR(255),
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    bookmarks TEXT,
    likes TEXT
);

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    profile_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    email_id VARCHAR(255),
    phone_number VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    birth_date DATE,
    height VARCHAR(20),
    country_currently_residing VARCHAR(100),
    citizen_of_countries TEXT,
    annual_income VARCHAR(50),
    personal_assets TEXT,
    medical_history TEXT,
    profession VARCHAR(100),
    education VARCHAR(100),
    religion VARCHAR(50),
    is_verification_requested BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email_id);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone_number);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_verified ON profiles(is_verified);