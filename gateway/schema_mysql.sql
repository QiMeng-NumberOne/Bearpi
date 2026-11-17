-- FreshChain MySQL 8.x schema
-- Optional: the current gateway uses SQLite by default (freshchain.db).
-- This file only creates the equivalent tables if you choose to move the
-- storage layer to MySQL later.

CREATE DATABASE IF NOT EXISTS freshchain
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE freshchain;

CREATE TABLE IF NOT EXISTS telemetry (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  received_ms BIGINT NOT NULL,
  node VARCHAR(16) NOT NULL,
  payload JSON NOT NULL,
  PRIMARY KEY (id),
  KEY idx_telemetry_node_time (node, received_ms DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS events (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  received_ms BIGINT NOT NULL,
  node VARCHAR(16) NULL,
  level VARCHAR(16) NOT NULL,
  message VARCHAR(512) NOT NULL,
  payload JSON NULL,
  PRIMARY KEY (id),
  KEY idx_events_time (received_ms DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS commands (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  sent_ms BIGINT NOT NULL,
  node VARCHAR(16) NOT NULL,
  payload JSON NOT NULL,
  PRIMARY KEY (id),
  KEY idx_commands_time (sent_ms DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS runs (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  label VARCHAR(128) NULL,
  route_name VARCHAR(128) NULL,
  started_ms BIGINT NOT NULL,
  ended_ms BIGINT NULL,
  status VARCHAR(16) NOT NULL,
  notes TEXT NULL,
  PRIMARY KEY (id),
  KEY idx_runs_time (started_ms DESC),
  CONSTRAINT chk_runs_status CHECK (status IN ('active','completed','aborted'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS route_points (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  run_id BIGINT UNSIGNED NOT NULL,
  seq INT NOT NULL,
  gps_ms BIGINT NOT NULL,
  latitude DOUBLE NOT NULL,
  longitude DOUBLE NOT NULL,
  ia1_ms BIGINT NULL,
  temperature DOUBLE NULL,
  humidity DOUBLE NULL,
  lux DOUBLE NULL,
  ia1_delta_ms INT NULL,
  quality VARCHAR(16) NOT NULL DEFAULT 'ok',
  PRIMARY KEY (id),
  KEY idx_route_run_seq (run_id, seq),
  KEY idx_route_run_time (run_id, gps_ms),
  CONSTRAINT fk_route_run FOREIGN KEY (run_id) REFERENCES runs(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS forecasts (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  run_id BIGINT UNSIGNED NULL,
  created_ms BIGINT NOT NULL,
  target_ms BIGINT NULL,
  horizon_min INT NOT NULL,
  latitude DOUBLE NULL,
  longitude DOUBLE NULL,
  metric VARCHAR(16) NOT NULL,
  value DOUBLE NOT NULL,
  lower DOUBLE NULL,
  upper DOUBLE NULL,
  model VARCHAR(64) NOT NULL,
  confidence DOUBLE NULL,
  PRIMARY KEY (id),
  KEY idx_forecast_run_metric (run_id, metric, created_ms DESC),
  CONSTRAINT fk_forecast_run FOREIGN KEY (run_id) REFERENCES runs(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alerts (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  run_id BIGINT UNSIGNED NULL,
  ts_ms BIGINT NOT NULL,
  level VARCHAR(16) NOT NULL,
  metric VARCHAR(16) NOT NULL,
  current_value DOUBLE NULL,
  predicted_value DOUBLE NULL,
  threshold DOUBLE NULL,
  message VARCHAR(512) NOT NULL,
  action VARCHAR(128) NULL,
  source VARCHAR(16) NULL,
  confidence DOUBLE NULL,
  acknowledged_ms BIGINT NULL,
  payload JSON NULL,
  PRIMARY KEY (id),
  KEY idx_alerts_time (ts_ms DESC),
  KEY idx_alerts_metric_level (metric, level, ts_ms DESC),
  CONSTRAINT chk_alerts_level CHECK (level IN ('watch','warning','critical'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
