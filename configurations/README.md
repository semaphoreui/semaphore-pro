# Server-Side Repository Cloning Configuration Examples

This directory contains configuration examples for implementing server-side repository cloning in different environments.

## Basic Configuration

### 1. Environment Variables

```bash
# Server Configuration
export SEMAPHORE_SERVER_SIDE_CLONING=true
export SEMAPHORE_CLONE_STORAGE_PATH=/var/lib/semaphore/clones
export SEMAPHORE_CLONE_MAX_SIZE=2GB
export SEMAPHORE_CLONE_CLEANUP_INTERVAL=30m
export SEMAPHORE_CLONE_DEFAULT_TTL=1h
export SEMAPHORE_CLONE_MAX_CONCURRENT=10

# Security
export SEMAPHORE_CLONE_ALLOWED_HOSTS="github.com,gitlab.com,bitbucket.org"
export SEMAPHORE_CLONE_RATE_LIMIT=10  # requests per minute per runner

# Runner Configuration
export SEMAPHORE_RUNNER_CLONING_MODE=server_side
export SEMAPHORE_RUNNER_CLONE_TIMEOUT=600s
export SEMAPHORE_RUNNER_FALLBACK_DIRECT=true
export SEMAPHORE_RUNNER_MAX_RETRIES=3
```

### 2. Configuration File (semaphore-config.yaml)

```yaml
server:
  repository_cloning:
    enabled: true
    storage:
      path: "/var/lib/semaphore/clones"
      max_size: "2GB"
      cleanup_interval: "30m"
    
    defaults:
      ttl: "1h"
      compression: "gzip"
      shallow: true
      depth: 1
    
    limits:
      max_concurrent_clones: 10
      max_repository_size: "500MB"
      rate_limit: 10  # per minute per runner
    
    security:
      allowed_hosts:
        - "github.com"
        - "gitlab.com"
        - "bitbucket.org"
        - "*.internal.company.com"
      require_authentication: true
      audit_logging: true

runner:
  repository:
    cloning_mode: "server_side"  # auto, direct, server_side
    timeout: "600s"
    fallback_to_direct: true
    max_retries: 3
    retry_delay: "30s"
```

## Docker Configuration

### 1. Docker Compose

```yaml
version: '3.8'

services:
  semaphore-server:
    image: semaphoreui/semaphore:v2.10.0-pro
    container_name: semaphore-server
    environment:
      SEMAPHORE_DB_HOST: postgres
      SEMAPHORE_DB_NAME: semaphore
      SEMAPHORE_DB_USER: semaphore
      SEMAPHORE_DB_PASS: semaphore123
      SEMAPHORE_ADMIN_PASSWORD: admin123
      SEMAPHORE_ADMIN_NAME: admin
      SEMAPHORE_ADMIN_EMAIL: admin@example.com
      
      # Server-side cloning configuration
      SEMAPHORE_SERVER_SIDE_CLONING: "true"
      SEMAPHORE_CLONE_STORAGE_PATH: "/app/clone-cache"
      SEMAPHORE_CLONE_MAX_SIZE: "2GB"
      SEMAPHORE_CLONE_CLEANUP_INTERVAL: "15m"
      SEMAPHORE_CLONE_DEFAULT_TTL: "1h"
      SEMAPHORE_CLONE_MAX_CONCURRENT: "5"
      
    volumes:
      - semaphore-data:/var/lib/semaphore
      - clone-cache:/app/clone-cache
      - ./config:/etc/semaphore:ro
    ports:
      - "3000:3000"
    depends_on:
      - postgres
    networks:
      - semaphore-network

  semaphore-runner-1:
    image: semaphoreui/runner:v2.10.0-pro
    container_name: semaphore-runner-1
    environment:
      SEMAPHORE_SERVER_URL: http://semaphore-server:3000
      SEMAPHORE_RUNNER_TOKEN: "runner-token-123"
      SEMAPHORE_RUNNER_CLONING_MODE: "server_side"
      SEMAPHORE_RUNNER_FALLBACK_DIRECT: "false"
      SEMAPHORE_RUNNER_CLONE_TIMEOUT: "300s"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - runner-workspace:/workspace
    depends_on:
      - semaphore-server
    networks:
      - semaphore-network

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: semaphore
      POSTGRES_USER: semaphore
      POSTGRES_PASSWORD: semaphore123
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - semaphore-network

volumes:
  semaphore-data:
  clone-cache:
  runner-workspace:
  postgres-data:

networks:
  semaphore-network:
    driver: bridge
```

## Enterprise Configuration

### 1. Security-Hardened Configuration

```yaml
server:
  repository_cloning:
    enabled: true
    storage:
      path: "/var/lib/semaphore/clones"
      encryption: true
      encryption_key_file: "/etc/semaphore/clone-encryption.key"
    
    security:
      allowed_hosts:
        - "gitlab.internal.company.com"
        - "git.secure.internal"
      blocked_hosts:
        - "github.com"  # Block public repositories
        - "*public*"
      
      require_authentication: true
      audit_logging: true
      audit_log_file: "/var/log/semaphore/clone-audit.log"
      
      network_policy:
        allow_private_networks: false
        allowed_cidrs:
          - "10.0.0.0/8"
          - "192.168.0.0/16"
      
      content_scanning:
        enabled: true
        max_file_size: "100MB"
        scan_timeout: "5m"
        quarantine_suspicious: true
    
    limits:
      max_concurrent_clones: 5
      max_repository_size: "500MB"
      rate_limit: 5  # per minute per runner
      rate_limit_burst: 2

tls:
  cert_file: "/etc/ssl/certs/semaphore.crt"
  key_file: "/etc/ssl/private/semaphore.key"
  ca_file: "/etc/ssl/certs/ca.crt"
```

## Monitoring Configuration

### 1. Prometheus Metrics

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'semaphore'
    static_configs:
      - targets: ['semaphore-server:3000']
    metrics_path: '/api/metrics'
    scrape_interval: 30s

# Example metrics exposed:
# semaphore_clone_requests_total{status="success|error"}
# semaphore_clone_duration_seconds{status="success|error"}
# semaphore_clone_size_bytes{repository="repo_name"}
# semaphore_clone_cache_hits_total
# semaphore_clone_cache_misses_total
# semaphore_clone_storage_used_bytes
# semaphore_clone_active_operations
```