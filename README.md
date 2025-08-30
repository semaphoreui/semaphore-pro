<div align="center">
  
  # Semaphore Pro
  
  **Modern UI and powerful API for Ansible, Terraform, OpenTofu, PowerShell and other DevOps tools**
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Documentation](https://img.shields.io/badge/docs-semaphoreui.com-blue)](https://docs.semaphoreui.com)
  [![Pro Features](https://img.shields.io/badge/Pro-Features-orange)](https://semaphoreui.com/pro)
  
</div>

## 🚀 New Pro Feature: Server-Side Repository Cloning

Semaphore Pro now supports **server-side repository cloning**, allowing runners to access repositories through the Semaphore Server instead of connecting directly to git servers. This is perfect for:

- **Corporate Networks**: Environments with strict firewall rules
- **Air-Gapped Deployments**: Isolated networks where only the server has external access
- **Security Compliance**: Organizations requiring centralized repository access control
- **Network Optimization**: Reducing bandwidth usage through intelligent caching

### 📋 Quick Start

Enable server-side cloning in your project settings:

```yaml
# semaphore-project.yml
server_side_cloning:
  enabled: true
  cache_duration: "1h"
  compression: "gzip"
  include_git_metadata: false
```

Configure your runners:

```bash
export SEMAPHORE_RUNNER_CLONING_MODE=server_side
export SEMAPHORE_RUNNER_FALLBACK_DIRECT=true
```

### 📚 Documentation

- **[📖 Feature Specification](FEATURE_SERVER_SIDE_CLONING.md)** - Complete technical specification
- **[🔧 API Documentation](api-server-side-cloning.yaml)** - OpenAPI specification for developers
- **[⚙️ Configuration Examples](configurations/README.md)** - Deployment scenarios and examples
- **[🎨 UI Mockups](UI_MOCKUPS.md)** - User interface design and workflows
- **[🔒 Security Guide](SECURITY.md)** - Security architecture and compliance

### 🏗️ Deployment Examples

<details>
<summary>Docker Compose</summary>

```yaml
version: '3.8'
services:
  semaphore-server:
    image: semaphoreui/semaphore:v2.10.0-pro
    environment:
      SEMAPHORE_SERVER_SIDE_CLONING: "true"
      SEMAPHORE_CLONE_STORAGE_PATH: "/app/clone-cache"
    volumes:
      - clone-cache:/app/clone-cache
    ports:
      - "3000:3000"

  runner:
    image: semaphoreui/runner:v2.10.0-pro
    environment:
      SEMAPHORE_RUNNER_CLONING_MODE: "server_side"
      SEMAPHORE_SERVER_URL: "http://semaphore-server:3000"
```

</details>

<details>
<summary>Kubernetes</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: semaphore-server
spec:
  template:
    spec:
      containers:
      - name: semaphore
        image: semaphoreui/semaphore:v2.10.0-pro
        env:
        - name: SEMAPHORE_SERVER_SIDE_CLONING
          value: "true"
        volumeMounts:
        - name: clone-storage
          mountPath: /var/lib/semaphore/clones
```

</details>

## 🏃 Project Runners

<div align="center">
  
  ### Enhanced Runner Management
  
  #### Advanced runner features for enterprise environments
  
  <img src="https://github.com/user-attachments/assets/174ac491-1b70-47b7-8488-b00b49e27811">
  
</div>

- **Server-Side Repository Cloning** - Clone repos through the server for restricted networks
- **Advanced Monitoring** - Real-time performance metrics and health checks
- **Resource Management** - CPU, memory, and storage optimization
- **High Availability** - Multi-runner deployments with load balancing

## 🔐 Two-Factor Authentication

<div align="center">

  ### Enterprise Security
  
  #### Advanced authentication and access control
  
  ![image](https://github.com/user-attachments/assets/51df1fc9-5303-483d-9239-045ba922840c)

</div>

- **2FA Integration** - TOTP, SMS, and hardware token support
- **SSO Integration** - SAML, OIDC, and LDAP authentication
- **Role-Based Access Control** - Granular permissions and project isolation
- **Audit Logging** - Comprehensive security and compliance reporting

## 📜 Advanced Logging & Analytics

<div align="center">

  ### Comprehensive Insights
  
  #### Advanced logging, monitoring, and analytics
  
  ![image](https://github.com/user-attachments/assets/bae31939-1090-4fb9-97d2-18db1511c90f)

</div>

- **Log Export** - Multiple formats (JSON, CSV, Syslog)
- **Real-time Analytics** - Performance metrics and trend analysis
- **Custom Dashboards** - Grafana and Prometheus integration
- **Compliance Reporting** - SOC 2, ISO 27001, and GDPR compliance

## 👨‍💻 Premium Support

<div align="center">
  
  ### Enterprise Support
  #### We will assist you with setup and provide guidance on best practices
  
</div>

- **24/7 Support** - Priority technical support for Pro customers
- **Implementation Services** - Expert guidance for enterprise deployments
- **Custom Development** - Feature prioritization and custom integrations
- **Training & Consulting** - Best practices and workflow optimization

## 🌟 Why Choose Semaphore Pro?

| Feature | Community | Pro |
|---------|-----------|-----|
| Basic CI/CD | ✅ | ✅ |
| Project Runners | Limited | ✅ Enhanced |
| Server-Side Cloning | ❌ | ✅ |
| Two-Factor Auth | ❌ | ✅ |
| Advanced Logging | ❌ | ✅ |
| Enterprise Support | ❌ | ✅ |
| Custom Integrations | ❌ | ✅ |

## 🚀 Get Started

1. **[Request a Demo](https://semaphoreui.com/pro/demo)** - See Semaphore Pro in action
2. **[Start Free Trial](https://semaphoreui.com/pro/trial)** - 30-day trial with full features
3. **[Contact Sales](https://semaphoreui.com/pro/contact)** - Custom enterprise solutions

---

<div align="center">
  
  **Ready to upgrade your DevOps workflow?**
  
  [Get Semaphore Pro](https://semaphoreui.com/pro) | [Documentation](https://docs.semaphoreui.com) | [Support](https://semaphoreui.com/support)
  
</div>
