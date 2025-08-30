#!/bin/bash

# Example: Server-Side Repository Cloning Demo
# This script demonstrates how the server-side cloning feature works

set -e

# Configuration
SEMAPHORE_SERVER_URL="${SEMAPHORE_SERVER_URL:-http://localhost:3000}"
RUNNER_TOKEN="${RUNNER_TOKEN:-your-runner-token}"
REPOSITORY_URL="${REPOSITORY_URL:-https://github.com/semaphoreui/semaphore-demo.git}"
BRANCH="${BRANCH:-main}"

echo "🚀 Semaphore Pro - Server-Side Repository Cloning Demo"
echo "======================================================="
echo "Server URL: $SEMAPHORE_SERVER_URL"
echo "Repository: $REPOSITORY_URL"
echo "Branch: $BRANCH"
echo ""

# Step 1: Initiate server-side clone
echo "📥 Step 1: Initiating server-side clone..."
CLONE_RESPONSE=$(curl -s -X POST "$SEMAPHORE_SERVER_URL/api/v1/repositories/clone" \
  -H "Authorization: Bearer $RUNNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"repository_url\": \"$REPOSITORY_URL\",
    \"branch\": \"$BRANCH\",
    \"shallow\": true,
    \"options\": {
      \"cache_duration\": \"1h\",
      \"compression\": \"gzip\"
    }
  }")

CLONE_ID=$(echo "$CLONE_RESPONSE" | jq -r '.clone_id')
echo "✅ Clone initiated successfully!"
echo "   Clone ID: $CLONE_ID"
echo ""

# Step 2: Monitor clone progress
echo "⏳ Step 2: Monitoring clone progress..."
while true; do
  STATUS_RESPONSE=$(curl -s "$SEMAPHORE_SERVER_URL/api/v1/repositories/clone/$CLONE_ID/status" \
    -H "Authorization: Bearer $RUNNER_TOKEN")
  
  STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
  PROGRESS=$(echo "$STATUS_RESPONSE" | jq -r '.progress // 0')
  
  echo "   Status: $STATUS (${PROGRESS}%)"
  
  case $STATUS in
    "ready")
      echo "✅ Repository cloned successfully!"
      DOWNLOAD_URL=$(echo "$STATUS_RESPONSE" | jq -r '.download_url')
      SIZE=$(echo "$STATUS_RESPONSE" | jq -r '.size')
      echo "   Download URL: $DOWNLOAD_URL"
      echo "   Repository size: $(($SIZE / 1024 / 1024)) MB"
      break
      ;;
    "error")
      ERROR_MSG=$(echo "$STATUS_RESPONSE" | jq -r '.error_message')
      echo "❌ Clone failed: $ERROR_MSG"
      exit 1
      ;;
    "cloning")
      echo "   Cloning in progress..."
      sleep 2
      ;;
    *)
      echo "   Waiting for clone to start..."
      sleep 1
      ;;
  esac
done
echo ""

# Step 3: Download repository archive
echo "📦 Step 3: Downloading repository archive..."
DOWNLOAD_FILE="/tmp/repository-$(date +%s).tar.gz"
curl -s -o "$DOWNLOAD_FILE" "$SEMAPHORE_SERVER_URL$DOWNLOAD_URL" \
  -H "Authorization: Bearer $RUNNER_TOKEN"

DOWNLOAD_SIZE=$(stat -c%s "$DOWNLOAD_FILE" 2>/dev/null || stat -f%z "$DOWNLOAD_FILE")
echo "✅ Repository downloaded successfully!"
echo "   File: $DOWNLOAD_FILE"
echo "   Size: $(($DOWNLOAD_SIZE / 1024 / 1024)) MB"
echo ""

# Step 4: Extract and verify
echo "📂 Step 4: Extracting repository..."
EXTRACT_DIR="/tmp/extracted-$(date +%s)"
mkdir -p "$EXTRACT_DIR"
tar -xzf "$DOWNLOAD_FILE" -C "$EXTRACT_DIR"

echo "✅ Repository extracted successfully!"
echo "   Directory: $EXTRACT_DIR"

# List contents
echo ""
echo "📋 Repository contents:"
ls -la "$EXTRACT_DIR"

# Show git info if available
if [ -d "$EXTRACT_DIR/.git" ]; then
  echo ""
  echo "🔍 Git information:"
  cd "$EXTRACT_DIR"
  echo "   Branch: $(git rev-parse --abbrev-ref HEAD)"
  echo "   Commit: $(git rev-parse HEAD)"
  echo "   Date: $(git log -1 --format=%cd)"
else
  echo ""
  echo "ℹ️  Git metadata not included (shallow clone without .git directory)"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up..."
rm -f "$DOWNLOAD_FILE"
rm -rf "$EXTRACT_DIR"

echo "✅ Demo completed successfully!"
echo ""
echo "🎉 Server-side repository cloning provides:"
echo "   • Network isolation for runners"
echo "   • Centralized access control"
echo "   • Bandwidth optimization through caching"
echo "   • Enhanced security and audit capabilities"