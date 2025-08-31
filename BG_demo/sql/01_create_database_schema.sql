-- ===================================================================
-- SAM Snowsight Intelligence Demo - Complete Database Setup
-- Unified database and schema creation for complete demo
-- ===================================================================

-- Create database and schema
CREATE DATABASE IF NOT EXISTS FSI_DEMOS;
USE DATABASE FSI_DEMOS;
CREATE SCHEMA IF NOT EXISTS SAM_DEMO;
USE SCHEMA SAM_DEMO;

-- Enable Cortex functions
-- Note: Ensure your account has access to Snowflake Cortex features
