# Server-Side Repository Cloning Examples

This directory contains practical examples demonstrating how to use the server-side repository cloning feature in Semaphore Pro.

## Prerequisites

- Semaphore Pro server running with server-side cloning enabled
- Valid runner token with appropriate permissions
- Network connectivity between your client and the Semaphore server

## Examples

### 1. Bash Demo Script (`demo-server-side-cloning.sh`)

A complete demonstration script showing the full workflow of server-side repository cloning.

#### Usage

```bash
# Set environment variables
export SEMAPHORE_SERVER_URL="https://your-semaphore-server.com"
export RUNNER_TOKEN="your-runner-token"
export REPOSITORY_URL="https://github.com/your-org/your-repo.git"
export BRANCH="main"

# Run the demo
./demo-server-side-cloning.sh
```

#### What it demonstrates

- Initiating a server-side clone via API
- Monitoring clone progress with real-time status updates
- Downloading the repository archive
- Extracting and verifying the repository contents
- Cleanup and summary of benefits

### 2. Python Client (`python_client.py`)

A comprehensive Python client library for integrating server-side repository cloning into your applications.

#### Installation

```bash
pip install requests  # Only dependency
```

#### Usage

```python
from python_client import SemaphoreRepositoryClient, CloneOptions

# Initialize client
client = SemaphoreRepositoryClient(
    server_url="https://your-semaphore-server.com",
    token="your-runner-token"
)

# Configure clone options
options = CloneOptions(
    cache_duration="2h",
    shallow=True,
    include_git_metadata=False,
    exclude_patterns=["*.log", "node_modules/"]
)

# Clone and download in one call
result, file_path = client.clone_and_download(
    repository_url="https://github.com/your-org/your-repo.git",
    output_path="/tmp/repo.tar.gz",
    branch="main",
    options=options
)
```

#### Features

- **Object-oriented API** - Clean, intuitive interface
- **Error handling** - Comprehensive exception handling
- **Progress monitoring** - Real-time status updates
- **Flexible configuration** - Extensive customization options
- **Async support** - Non-blocking operations
- **Type hints** - Full typing support for better IDE integration

## Environment Variables

All examples support the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SEMAPHORE_SERVER_URL` | Semaphore server URL | `http://localhost:3000` |
| `RUNNER_TOKEN` | Authentication token | `your-runner-token` |
| `REPOSITORY_URL` | Git repository URL | `https://github.com/semaphoreui/semaphore-demo.git` |
| `BRANCH` | Branch to clone | `main` |

## Common Use Cases

### 1. CI/CD Integration

```bash
#!/bin/bash
# In your CI/CD pipeline

# Clone repository via server
./demo-server-side-cloning.sh

# Extract to workspace
cd /workspace
tar -xzf /tmp/repository-*.tar.gz --strip-components=1

# Continue with your build process
npm install
npm run build
npm test
```

### 2. Automated Testing

```python
import unittest
from python_client import SemaphoreRepositoryClient

class TestServerSideCloning(unittest.TestCase):
    def setUp(self):
        self.client = SemaphoreRepositoryClient(
            server_url=os.getenv("SEMAPHORE_SERVER_URL"),
            token=os.getenv("RUNNER_TOKEN")
        )
    
    def test_clone_public_repo(self):
        result, file_path = self.client.clone_and_download(
            repository_url="https://github.com/semaphoreui/semaphore-demo.git",
            output_path="/tmp/test-repo.tar.gz"
        )
        
        self.assertEqual(result.status, "ready")
        self.assertTrue(os.path.exists(file_path))
```

### 3. Batch Repository Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

repositories = [
    "https://github.com/org/repo1.git",
    "https://github.com/org/repo2.git",
    "https://github.com/org/repo3.git"
]

def clone_repo(repo_url):
    client = SemaphoreRepositoryClient(server_url, token)
    return client.clone_and_download(
        repository_url=repo_url,
        output_path=f"/tmp/{repo_url.split('/')[-1]}.tar.gz"
    )

# Process repositories in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(clone_repo, repo) for repo in repositories]
    results = [future.result() for future in futures]
```

## Network Configuration Examples

### 1. Corporate Firewall

```bash
# Only server needs outbound access to git providers
# Runners only need access to Semaphore server

# Firewall rules for runners
iptables -A OUTPUT -d your-semaphore-server.com -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j DROP  # Block direct git access
```

### 2. Air-Gapped Environment

```yaml
# docker-compose.yml for air-gapped deployment
version: '3.8'
services:
  semaphore-proxy:
    image: semaphoreui/semaphore:v2.10.0-pro
    environment:
      SEMAPHORE_SERVER_SIDE_CLONING: "true"
      SEMAPHORE_CLONE_ALLOWED_HOSTS: "internal-git.company.com"
    networks:
      - external  # Has internet access
      - internal  # Connected to runners
  
  runner:
    image: semaphoreui/runner:v2.10.0-pro
    environment:
      SEMAPHORE_RUNNER_CLONING_MODE: "server_side"
      SEMAPHORE_RUNNER_FALLBACK_DIRECT: "false"
    networks:
      - internal  # No internet access
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   # Verify token is valid
   curl -H "Authorization: Bearer $RUNNER_TOKEN" \
        "$SEMAPHORE_SERVER_URL/api/v1/user"
   ```

2. **Network Connectivity**
   ```bash
   # Test server connectivity
   curl -f "$SEMAPHORE_SERVER_URL/api/ping"
   ```

3. **Repository Access**
   ```bash
   # Check if server can access repository
   # (This should be done from the server)
   git ls-remote "$REPOSITORY_URL"
   ```

### Debug Mode

Enable debug output in the examples:

```bash
# Bash script
export DEBUG=true
./demo-server-side-cloning.sh

# Python client
export PYTHONPATH=.
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from python_client import main
main()
"
```

## Performance Tips

1. **Use caching effectively**
   - Set appropriate cache durations
   - Reuse cached repositories when possible
   - Monitor cache hit rates

2. **Optimize for your network**
   - Use compression for slow connections
   - Disable compression for fast internal networks
   - Adjust timeouts based on repository sizes

3. **Parallel processing**
   - Clone multiple repositories concurrently
   - Use thread pools for batch operations
   - Monitor server resource usage

## Security Considerations

1. **Token Management**
   - Use environment variables for tokens
   - Rotate tokens regularly
   - Scope tokens to minimum required permissions

2. **Network Security**
   - Use HTTPS for all communications
   - Validate SSL certificates
   - Implement proper firewall rules

3. **Audit Logging**
   - Enable audit logging on the server
   - Monitor repository access patterns
   - Set up alerts for suspicious activity

## Next Steps

- Review the [API Documentation](../api-server-side-cloning.yaml)
- Check the [Configuration Examples](../configurations/README.md)
- Read the [Security Guide](../SECURITY.md)
- Explore the [UI Mockups](../UI_MOCKUPS.md)

For more information, visit the [Semaphore Pro documentation](https://docs.semaphoreui.com/pro).