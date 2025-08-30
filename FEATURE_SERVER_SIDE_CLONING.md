# Server-Side Repository Cloning Feature

## Overview

This feature allows Semaphore Pro runners to clone repositories through the Semaphore Server instead of connecting directly to git servers. This is particularly useful in environments where runners are deployed in restricted networks that cannot access external git servers directly.

## Use Cases

1. **Corporate Networks**: Runners deployed in corporate environments with strict firewall rules
2. **Air-Gapped Environments**: Isolated networks where only the Semaphore Server has external access
3. **Security Compliance**: Environments requiring all external connections to go through a central point
4. **Network Optimization**: Reducing bandwidth usage by having the server cache repositories

## Architecture

### Current Flow
```
Runner → Git Server → Repository
```

### New Flow (Server-Side Cloning)
```
Runner → Semaphore Server → Git Server → Repository
         ↓
         Cache/Proxy
```

## Implementation Components

### 1. Server-Side Repository Service

#### API Endpoints

##### Clone Repository
```http
POST /api/v1/repositories/clone
Content-Type: application/json

{
  "repository_url": "https://github.com/user/repo.git",
  "branch": "main",
  "commit": "abc123",
  "credentials": {
    "type": "token|ssh|basic",
    "data": "..."
  }
}
```

Response:
```http
200 OK
{
  "clone_id": "uuid-123",
  "status": "cloning|ready|error",
  "download_url": "/api/v1/repositories/download/uuid-123",
  "expires_at": "2025-08-30T16:00:00Z"
}
```

##### Download Repository Archive
```http
GET /api/v1/repositories/download/{clone_id}
Authorization: Bearer <runner_token>
```

Response: ZIP or TAR.GZ archive of the repository

##### Clone Status
```http
GET /api/v1/repositories/clone/{clone_id}/status
```

Response:
```http
200 OK
{
  "clone_id": "uuid-123",
  "status": "cloning|ready|error",
  "progress": 75,
  "error_message": null,
  "download_url": "/api/v1/repositories/download/uuid-123",
  "expires_at": "2025-08-30T16:00:00Z"
}
```

### 2. Runner Configuration

#### Project Configuration
```yaml
# semaphore-project.yml
server_side_cloning:
  enabled: true
  cache_duration: "1h"  # How long server keeps the repository
  compression: "gzip"   # Archive format: gzip, none
  include_git_metadata: false  # Include .git directory
```

#### Runner Settings
```yaml
# runner-config.yml
repository:
  cloning_mode: "server_side"  # direct, server_side, auto
  fallback_to_direct: true     # Fallback if server-side fails
  timeout: "300s"              # Timeout for server-side cloning
```

### 3. Web UI Components

#### Project Settings
- Toggle for "Server-Side Repository Cloning"
- Configuration options for cache duration
- Security settings for repository access

#### Runner Status
- Display cloning mode in runner status
- Show repository cloning progress
- Error reporting for cloning failures

### 4. Security Considerations

#### Authentication & Authorization
- Runners must authenticate with valid tokens
- Repository access follows existing permission model
- Audit logging for all repository access

#### Data Security
- Temporary storage with automatic cleanup
- Encrypted storage for sensitive repositories
- Rate limiting to prevent abuse

#### Network Security
- Server validates repository URLs
- Support for private CA certificates
- Configurable network policies

## Configuration Examples

### Environment Variables

```bash
# Server Configuration
SEMAPHORE_SERVER_SIDE_CLONING=true
SEMAPHORE_CLONE_STORAGE_PATH=/tmp/semaphore-clones
SEMAPHORE_CLONE_MAX_SIZE=1GB
SEMAPHORE_CLONE_CLEANUP_INTERVAL=15m

# Runner Configuration
SEMAPHORE_RUNNER_CLONING_MODE=server_side
SEMAPHORE_RUNNER_CLONE_TIMEOUT=300s
SEMAPHORE_RUNNER_FALLBACK_DIRECT=true
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  semaphore:
    image: semaphoreui/semaphore:latest
    environment:
      - SEMAPHORE_SERVER_SIDE_CLONING=true
      - SEMAPHORE_CLONE_STORAGE_PATH=/app/clone-cache
    volumes:
      - ./clone-cache:/app/clone-cache
    
  runner:
    image: semaphoreui/runner:latest
    environment:
      - SEMAPHORE_RUNNER_CLONING_MODE=server_side
      - SEMAPHORE_SERVER_URL=http://semaphore:3000
```

## Deployment Scenarios

### 1. Corporate Network Deployment
```
Internet → Corporate Firewall → Semaphore Server → Internal Network → Runners
```

### 2. Multi-Zone Deployment
```
Public Cloud → Semaphore Server → Private Subnet → Runners
```

### 3. Hybrid Deployment
```
On-Premises Git → DMZ Semaphore Server → Container Platform → Runners
```

## Benefits

1. **Network Isolation**: Runners don't need direct internet access
2. **Centralized Control**: All repository access goes through Semaphore Server
3. **Caching**: Reduces bandwidth usage and improves performance
4. **Security**: Better audit trail and access control
5. **Compliance**: Meets enterprise security requirements

## Limitations

1. **Additional Storage**: Server needs storage for repository caches
2. **Latency**: Additional hop may increase clone time for small repositories
3. **Server Load**: Increased CPU and memory usage on server
4. **Single Point of Failure**: Server becomes critical for repository access

## Migration Path

1. **Phase 1**: Deploy server-side cloning as opt-in feature
2. **Phase 2**: Enable auto-detection based on network connectivity
3. **Phase 3**: Make server-side cloning the default for Pro users
4. **Phase 4**: Deprecate direct cloning in restricted environments

## Monitoring & Metrics

- Repository clone success/failure rates
- Cache hit/miss ratios
- Storage usage and cleanup metrics
- Network bandwidth savings
- Clone time comparisons (direct vs server-side)

## Testing Strategy

1. **Unit Tests**: API endpoints and core functionality
2. **Integration Tests**: End-to-end cloning workflows
3. **Performance Tests**: Large repository handling
4. **Security Tests**: Authentication and authorization
5. **Network Tests**: Firewall and connectivity scenarios