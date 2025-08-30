# Semaphore Pro UI - Server-Side Repository Cloning

This document describes the user interface components for the server-side repository cloning feature in Semaphore Pro.

## 1. Project Settings - Repository Configuration

### Repository Settings Page

```
┌─────────────────────────────────────────────────────────────────┐
│ PROJECT SETTINGS                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ General | Repositories | Environment | Access Keys | Templates  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Repository Cloning Configuration                                │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Cloning Mode                                              │ │
│ │                                                           │ │
│ │ ○ Direct Cloning                                          │ │
│ │   Runners clone repositories directly from git servers   │ │
│ │                                                           │ │
│ │ ● Server-Side Cloning (Recommended) 🔧 PRO              │ │
│ │   Server clones repositories and provides them to        │ │
│ │   runners via secure download                             │ │
│ │                                                           │ │
│ │ ○ Auto-Detect                                            │ │
│ │   Automatically choose based on network connectivity     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Server-Side Cloning Options                                     │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                                                           │ │
│ │ Cache Duration: [1 hour          ▼] ⓘ                   │ │
│ │                                                           │ │
│ │ Compression: [gzip              ▼] ⓘ                    │ │
│ │                                                           │ │
│ │ ☐ Include Git Metadata (.git directory)                  │ │
│ │                                                           │ │
│ │ ☑ Enable fallback to direct cloning if server fails      │ │
│ │                                                           │ │
│ │ Maximum Repository Size: [500 MB        ] ⓘ             │ │
│ │                                                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Security Settings                                               │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                                                           │ │
│ │ ☑ Audit repository access                                 │ │
│ │                                                           │ │
│ │ ☑ Encrypt cached repositories                             │ │
│ │                                                           │ │
│ │ Rate Limit: [10] requests per minute per runner ⓘ        │ │
│ │                                                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│             [Cancel]                    [Save Changes]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Runner Dashboard

### Enhanced Runner Status Display

```
┌─────────────────────────────────────────────────────────────────┐
│ RUNNERS                                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ NAME         STATUS    CLONING MODE    MAX PARALLEL  ACTIONS    │
│                                                                 │
│ ○ Runner 1   Online    Server-Side     3            [🗑] [✏️]   │
│   Last seen: 2 minutes ago                                      │
│   Repository cloning: Ready                                     │
│   Cache hits: 15/20 (75%)                                       │
│                                                                 │
│ ○ Runner 2   Online    Auto-Detect     1            [🗑] [✏️]   │
│   Last seen: 30 seconds ago                                     │
│   Repository cloning: Fallback to direct                       │
│   Network: Limited connectivity                                 │
│                                                                 │
│ ● Runner 3   Busy      Server-Side     5            [🗑] [✏️]   │
│   Last seen: 5 seconds ago                                      │
│   Repository cloning: Downloading repo-xyz (45%)                │
│   ETA: 2 minutes                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Task Execution View

### Task Log with Repository Cloning Details

```
┌─────────────────────────────────────────────────────────────────┐
│ TASK EXECUTION - Build Application                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Repository Preparation                                          │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ✓ Server-side clone initiated                               │ │
│ │   Repository: https://github.com/company/app.git           │ │
│ │   Branch: main                                              │ │
│ │   Commit: abc123def (Latest)                                │ │
│ │                                                             │ │
│ │ ✓ Repository cloned on server                               │ │
│ │   Size: 45.2 MB                                             │ │
│ │   Duration: 8.3 seconds                                     │ │
│ │   Cache: Miss (first clone)                                 │ │
│ │                                                             │ │
│ │ ✓ Repository archive created                                │ │
│ │   Format: tar.gz                                            │ │
│ │   Compressed size: 12.8 MB                                  │ │
│ │                                                             │ │
│ │ ✓ Repository downloaded to runner                           │ │
│ │   Download speed: 1.2 MB/s                                  │ │
│ │   Extraction: 2.1 seconds                                   │ │
│ │                                                             │ │
│ │ Total repository preparation time: 15.2 seconds             │ │
│ │ (vs estimated direct clone: 25-30 seconds)                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Task Execution                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ $ cd /workspace/app                                         │ │
│ │ $ npm install                                               │ │
│ │ ...                                                         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 4. Repository Cache Management

### Server Administration - Repository Cache

```
┌─────────────────────────────────────────────────────────────────┐
│ ADMINISTRATION > SYSTEM > REPOSITORY CACHE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Cache Statistics                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Total Storage Used:    2.8 GB / 10 GB (28%)               │ │
│ │ Active Clones:         12                                   │ │
│ │ Cache Hit Rate:        78% (last 24h)                      │ │
│ │ Average Clone Time:    45 seconds                           │ │
│ │ Bandwidth Saved:       125 GB (this month)                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Active Repository Caches                       [🔄 Refresh]     │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ REPOSITORY                    SIZE    EXPIRES    ACTIONS    │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │ company/app.git (main)       45 MB   in 2h      [🗑] [📁]  │ │
│ │ company/api.git (develop)    23 MB   in 45m     [🗑] [📁]  │ │
│ │ external/lib.git (v1.2.0)   128 MB  in 3h       [🗑] [📁]  │ │
│ │ company/docs.git (main)      8 MB    in 1h       [🗑] [📁]  │ │
│ │                                                             │ │
│ │ Showing 4 of 12 cached repositories                         │ │
│ │                              [1] [2] [3] [Next >]          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Cache Management                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ [Clear All Expired]  [Force Cleanup]  [Export Cache Stats] │ │
│ │                                                             │ │
│ │ Automatic cleanup runs every 30 minutes                     │ │
│ │ Next cleanup: in 12 minutes                                │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 5. Error Handling UI

### Repository Clone Failure Dialog

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️  Repository Clone Failed                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ The server was unable to clone the repository for this task.   │
│                                                                 │
│ Repository: https://github.com/company/private-repo.git        │
│ Error: Authentication failed (401 Unauthorized)                │
│ Attempted at: 2025-08-30 14:30:15 UTC                         │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Troubleshooting Steps:                                      │ │
│ │                                                             │ │
│ │ • Verify repository access credentials                      │ │
│ │ • Check if repository URL is correct                        │ │
│ │ • Ensure server has network access to git provider         │ │
│ │ • Try fallback to direct cloning if enabled                │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Fallback Options:                                               │
│ [🔄 Retry Server Clone]  [🔀 Use Direct Clone]  [❌ Cancel]    │
│                                                                 │
│ [📋 Copy Error Details]  [📧 Contact Support]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Settings Migration Wizard

### Migrating Existing Projects

```
┌─────────────────────────────────────────────────────────────────┐
│ 🚀 Enable Server-Side Repository Cloning                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Step 2 of 3: Configure Projects                                │
│                                                                 │
│ Select projects to enable server-side cloning:                 │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ☑ Production App (12 templates)        Recommended         │ │
│ │   Current runners: 3 with network restrictions             │ │
│ │                                                             │ │
│ │ ☑ API Service (5 templates)            Recommended         │ │
│ │   Current runners: 2 with limited bandwidth                │ │
│ │                                                             │ │
│ │ ☐ Test Project (2 templates)           Not recommended     │ │
│ │   Current runners: 1 with direct access                    │ │
│ │                                                             │ │
│ │ ☑ Documentation (3 templates)          Recommended         │ │
│ │   Large repository size benefits from caching              │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Configuration Preview:                                          │
│ • 3 projects will use server-side cloning                      │
│ • Estimated storage needed: ~500 MB                            │
│ • Estimated bandwidth savings: 60-80%                          │
│ • Fallback to direct cloning: Enabled                          │
│                                                                 │
│ [< Previous]              [Next: Review >]              [Skip] │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 7. Real-time Monitoring Dashboard

### Repository Cloning Analytics

```
┌─────────────────────────────────────────────────────────────────┐
│ ANALYTICS > REPOSITORY CLONING                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Time Range: [Last 7 days ▼]                    [📊 Export]     │
│                                                                 │
│ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────┐ │
│ │ Clone Success Rate  │ │ Average Clone Time  │ │ Cache Hit   │ │
│ │                     │ │                     │ │ Rate        │ │
│ │      98.5%          │ │     23 seconds      │ │    82%      │ │
│ │   ↑ 2.1% vs last    │ │  ↓ 15s vs last     │ │ ↑ 8% vs     │ │
│ │      week           │ │     week            │ │   last week │ │
│ └─────────────────────┘ └─────────────────────┘ └─────────────┘ │
│                                                                 │
│ Clone Time Comparison                                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 120s │                                                     │ │
│ │      │ Direct   ████████████████                           │ │
│ │ 100s │ Clone    ████████████████                           │ │
│ │      │          ████████████████                           │ │
│ │  80s │          ████████████████                           │ │
│ │      │          ████████████████                           │ │
│ │  60s │          ████████████████                           │ │
│ │      │ Server   ████████████                               │ │
│ │  40s │ Clone    ████████████                               │ │
│ │      │          ████████████                               │ │
│ │  20s │          ████████████                               │ │
│ │      │          ████████████                               │ │
│ │   0s └──────────┴─────────────────────────────────────────┘ │ │
│      Small    Medium    Large    Very Large   Repositories   │ │
│     (<10MB)  (10-50MB) (50-200MB)  (>200MB)                  │ │
│                                                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Storage Usage Trends                                            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 5GB  │                                               ████  │ │
│ │      │                                         ████████    │ │
│ │ 4GB  │                                   ████████          │ │
│ │      │                             ████████                │ │
│ │ 3GB  │                       ████████                      │ │
│ │      │                 ████████                            │ │
│ │ 2GB  │           ████████                                  │ │
│ │      │     ████████                                        │ │
│ │ 1GB  │ ████                                                │ │
│ │      └─────────────────────────────────────────────────────┘ │
│ │      Mon  Tue  Wed  Thu  Fri  Sat  Sun                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key UI Features

### 1. Clear Visual Indicators
- **Pro Badge**: Clear indication that this is a Pro feature
- **Status Icons**: Visual representation of cloning modes and health
- **Progress Bars**: Real-time progress for clone operations

### 2. Contextual Help
- **Tooltips**: Explain technical terms and recommendations
- **Info Icons**: Provide additional context without cluttering
- **Guided Setup**: Step-by-step wizard for initial configuration

### 3. Performance Insights
- **Comparison Charts**: Show benefits of server-side cloning
- **Analytics Dashboard**: Detailed metrics and trends
- **Real-time Monitoring**: Live status of clone operations

### 4. Error Handling
- **Clear Error Messages**: Explain what went wrong
- **Actionable Solutions**: Provide specific steps to resolve issues
- **Fallback Options**: Offer alternatives when primary method fails

### 5. Enterprise Features
- **Audit Logging**: Track all repository access
- **Security Controls**: Granular permissions and restrictions
- **Resource Management**: Monitor and control storage usage