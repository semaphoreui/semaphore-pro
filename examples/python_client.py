#!/usr/bin/env python3
"""
Semaphore Pro - Server-Side Repository Cloning Python Client

This example demonstrates how to integrate server-side repository cloning
into your Python applications and CI/CD workflows.
"""

import json
import time
import requests
import os
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class CloneOptions:
    """Configuration options for repository cloning."""
    cache_duration: str = "1h"
    compression: str = "gzip"
    shallow: bool = True
    depth: int = 1
    include_git_metadata: bool = False
    exclude_patterns: Optional[list] = None


@dataclass
class CloneResult:
    """Result of a repository clone operation."""
    clone_id: str
    status: str
    download_url: Optional[str] = None
    size: Optional[int] = None
    error_message: Optional[str] = None
    expires_at: Optional[str] = None


class SemaphoreRepositoryClient:
    """Client for Semaphore Pro server-side repository cloning."""
    
    def __init__(self, server_url: str, token: str):
        """
        Initialize the client.
        
        Args:
            server_url: Semaphore server URL
            token: Runner authentication token
        """
        self.server_url = server_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'SemaphoreProClient/1.0'
        })
    
    def clone_repository(
        self,
        repository_url: str,
        branch: Optional[str] = None,
        commit: Optional[str] = None,
        tag: Optional[str] = None,
        options: Optional[CloneOptions] = None
    ) -> CloneResult:
        """
        Initiate server-side repository cloning.
        
        Args:
            repository_url: Git repository URL
            branch: Branch to clone (optional)
            commit: Specific commit to clone (optional)
            tag: Specific tag to clone (optional)
            options: Clone configuration options
            
        Returns:
            CloneResult with clone ID and initial status
            
        Raises:
            requests.RequestException: If the API request fails
        """
        if not options:
            options = CloneOptions()
        
        payload = {
            "repository_url": repository_url,
            "shallow": options.shallow,
            "depth": options.depth,
            "include_git_metadata": options.include_git_metadata,
            "options": {
                "cache_duration": options.cache_duration,
                "compression": options.compression
            }
        }
        
        if branch:
            payload["branch"] = branch
        if commit:
            payload["commit"] = commit
        if tag:
            payload["tag"] = tag
        if options.exclude_patterns:
            payload["options"]["exclude_patterns"] = options.exclude_patterns
        
        response = self.session.post(
            f"{self.server_url}/api/v1/repositories/clone",
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        return CloneResult(
            clone_id=data["clone_id"],
            status=data["status"],
            download_url=data.get("download_url"),
            expires_at=data.get("expires_at")
        )
    
    def get_clone_status(self, clone_id: str) -> CloneResult:
        """
        Get the current status of a clone operation.
        
        Args:
            clone_id: Unique clone identifier
            
        Returns:
            CloneResult with current status and details
        """
        response = self.session.get(
            f"{self.server_url}/api/v1/repositories/clone/{clone_id}/status"
        )
        response.raise_for_status()
        
        data = response.json()
        return CloneResult(
            clone_id=data["clone_id"],
            status=data["status"],
            download_url=data.get("download_url"),
            size=data.get("size"),
            error_message=data.get("error_message"),
            expires_at=data.get("expires_at")
        )
    
    def wait_for_clone(
        self,
        clone_id: str,
        timeout: int = 300,
        poll_interval: int = 2
    ) -> CloneResult:
        """
        Wait for a clone operation to complete.
        
        Args:
            clone_id: Unique clone identifier
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            CloneResult when clone is complete
            
        Raises:
            TimeoutError: If clone doesn't complete within timeout
            RuntimeError: If clone fails
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.get_clone_status(clone_id)
            
            if result.status == "ready":
                return result
            elif result.status == "error":
                raise RuntimeError(f"Clone failed: {result.error_message}")
            elif result.status in ["expired", "cancelled"]:
                raise RuntimeError(f"Clone was {result.status}")
            
            print(f"Clone status: {result.status}")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Clone did not complete within {timeout} seconds")
    
    def download_repository(
        self,
        clone_id: str,
        output_path: str,
        format: str = "tar.gz"
    ) -> str:
        """
        Download the cloned repository archive.
        
        Args:
            clone_id: Unique clone identifier
            output_path: Path to save the downloaded file
            format: Archive format (zip or tar.gz)
            
        Returns:
            Path to the downloaded file
        """
        params = {"format": format} if format != "tar.gz" else {}
        
        response = self.session.get(
            f"{self.server_url}/api/v1/repositories/download/{clone_id}",
            params=params,
            stream=True
        )
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return output_path
    
    def clone_and_download(
        self,
        repository_url: str,
        output_path: str,
        branch: Optional[str] = None,
        options: Optional[CloneOptions] = None,
        timeout: int = 300
    ) -> tuple[CloneResult, str]:
        """
        Convenience method to clone and download a repository in one call.
        
        Args:
            repository_url: Git repository URL
            output_path: Path to save the downloaded archive
            branch: Branch to clone
            options: Clone configuration options
            timeout: Maximum time to wait for clone completion
            
        Returns:
            Tuple of (CloneResult, downloaded_file_path)
        """
        print(f"🚀 Initiating server-side clone of {repository_url}")
        
        # Start clone
        result = self.clone_repository(
            repository_url=repository_url,
            branch=branch,
            options=options
        )
        print(f"✅ Clone initiated with ID: {result.clone_id}")
        
        # Wait for completion
        print("⏳ Waiting for clone to complete...")
        result = self.wait_for_clone(result.clone_id, timeout)
        print(f"✅ Clone completed! Size: {result.size:,} bytes")
        
        # Download archive
        print("📦 Downloading repository archive...")
        downloaded_file = self.download_repository(result.clone_id, output_path)
        print(f"✅ Repository downloaded to: {downloaded_file}")
        
        return result, downloaded_file


def main():
    """Example usage of the Semaphore repository client."""
    # Configuration from environment variables
    server_url = os.getenv("SEMAPHORE_SERVER_URL", "http://localhost:3000")
    token = os.getenv("RUNNER_TOKEN", "your-runner-token")
    
    # Initialize client
    client = SemaphoreRepositoryClient(server_url, token)
    
    # Clone options
    options = CloneOptions(
        cache_duration="2h",
        shallow=True,
        include_git_metadata=False,
        exclude_patterns=["*.log", "node_modules/", ".env"]
    )
    
    try:
        # Example 1: Clone a public repository
        print("=" * 60)
        print("Example 1: Cloning public repository")
        print("=" * 60)
        
        result, file_path = client.clone_and_download(
            repository_url="https://github.com/semaphoreui/semaphore-demo.git",
            output_path="/tmp/semaphore-demo.tar.gz",
            branch="main",
            options=options
        )
        
        print(f"Clone ID: {result.clone_id}")
        print(f"Status: {result.status}")
        print(f"File: {file_path}")
        print(f"Expires: {result.expires_at}")
        
        # Example 2: Monitor clone progress manually
        print("\n" + "=" * 60)
        print("Example 2: Manual clone monitoring")
        print("=" * 60)
        
        result = client.clone_repository(
            repository_url="https://github.com/semaphoreui/semaphore-demo.git",
            branch="main",
            options=options
        )
        
        print(f"Clone started: {result.clone_id}")
        
        # Poll for status updates
        while True:
            status = client.get_clone_status(result.clone_id)
            print(f"Status: {status.status}")
            
            if status.status == "ready":
                print("✅ Clone ready for download!")
                break
            elif status.status == "error":
                print(f"❌ Clone failed: {status.error_message}")
                break
            
            time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    print("\n🎉 Examples completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())