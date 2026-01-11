#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ulid-py",
# ]
# ///
"""
脚本功能：创建新的笔记文件
- 生成 ULID 作为文件名
- 创建包含标题、标签、日期的模板
"""

import os
import sys
from datetime import datetime
import ulid


def main():
    # Get the name argument
    if len(sys.argv) != 2:
        print("Usage: python new_note.py <title>")
        sys.exit(1)

    name = sys.argv[1]

    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Generate ULID for the filename
    ulid_str = str(ulid.new())

    # Template content with title (no id field since filename is ULID)
    template = '---\ntitle: "{}"\ndisplay: true\ntags:\n  - \ndate: {}\n---\n\n'.format(
        name, current_date
    )

    # Create the file path using ULID as filename
    if ulid_str:
        file_path = f"notes/{ulid_str}.md"
    else:
        file_path = f"notes/{name}.md"

    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File '{file_path}' already exists!")
        sys.exit(1)

    # Write the template to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(file_path)


if __name__ == "__main__":
    main()
