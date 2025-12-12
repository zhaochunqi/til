#!/usr/bin/env python3
"""
Add ULID to markdown files based on git add time.
If file already has ULID, do nothing.
If file is not tracked by git, use current time.
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import ulid


def get_git_add_time(file_path):
    """Get the git add time for a file."""
    try:
        # Get the author date of the first commit that added this file
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%at", "-1", "--", str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return int(result.stdout.strip())
    except subprocess.CalledProcessError:
        pass
    return None


def has_ulid(content):
    """Check if the file already has a ULID in the frontmatter."""
    # Look for id field in frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        return re.search(r'^id:\s*\w+', frontmatter, re.MULTILINE) is not None
    return False


def add_ulid_to_file(file_path):
    """Add ULID to a markdown file if it doesn't have one."""
    file_path = Path(file_path)
    
    # Only process markdown files in notes directory
    if not (file_path.suffix == '.md' and 'notes' in file_path.parts):
        return True
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has ULID
        if has_ulid(content):
            return True
        
        # Get time for ULID generation
        git_time = get_git_add_time(file_path)
        if git_time:
            timestamp = datetime.fromtimestamp(git_time)
        else:
            # Fallback to file modification time or current time
            timestamp = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        # Generate ULID with specific timestamp
        ulid_obj = ulid.from_timestamp(timestamp)
        ulid_str = str(ulid_obj)
        
        # Add ULID to frontmatter
        frontmatter_match = re.match(r'^(---\n.*?\n---)', content, re.DOTALL)
        
        if frontmatter_match:
            # File has frontmatter, add id field
            frontmatter = frontmatter_match.group(1)
            rest_content = content[len(frontmatter):]
            
            # Insert id after the opening --- or after existing fields
            if frontmatter.strip() == '---':
                new_frontmatter = f"---\nid: {ulid_str}\n---"
            else:
                # Insert after the first line or before the closing ---
                lines = frontmatter.split('\n')
                if len(lines) >= 2:
                    lines.insert(-1, f"id: {ulid_str}")
                new_frontmatter = '\n'.join(lines)
            
            new_content = new_frontmatter + rest_content
        else:
            # No frontmatter, create one
            new_content = f"---\nid: {ulid_str}\n---\n\n{content}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added ULID {ulid_str} to {file_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function for pre-commit hook."""
    if len(sys.argv) > 1:
        # Process specific files (pre-commit mode)
        files = sys.argv[1:]
        success = True
        for file_path in files:
            if not add_ulid_to_file(file_path):
                success = False
        sys.exit(0 if success else 1)
    else:
        print("Usage: python add_ulid.py <file1> [file2] ...")
        sys.exit(1)


if __name__ == "__main__":
    main()