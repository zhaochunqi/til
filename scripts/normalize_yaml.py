#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ruamel-yaml",
# ]
# ///
"""
脚本功能：标准化和排序 Markdown 文件的 YAML front matter
- 移除 id 字段（因为文件名已经是 ULID）
- 按 title/tags/date 顺序排序字段
- 标准化格式
"""

import os
import sys
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

def normalize_yaml_frontmatter(content):
    """标准化 YAML front matter"""
    # 检查是否有 YAML front matter
    if not content.startswith('---'):
        return content, False
    
    # 分离 front matter 和正文
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, False
    
    frontmatter_text = parts[1].strip()
    main_content = parts[2]
    
    try:
        # 使用 ruamel.yaml 解析 YAML
        yaml_processor = YAML()
        yaml_processor.indent(mapping=2, sequence=2, offset=2)
        yaml_processor.width = 4096
        yaml_processor.allow_unicode = True
        yaml_processor.default_flow_style = False
        yaml_processor.preserve_quotes = True
        
        # 解析 YAML
        frontmatter = yaml_processor.load(frontmatter_text)
        if frontmatter is None:
            frontmatter = {}
        
        # 移除 id 字段
        if 'id' in frontmatter:
            del frontmatter['id']
        
        # 按指定顺序排序字段
        field_order = ['title', 'tags', 'date']
        ordered_frontmatter = CommentedMap()
        
        # 先添加指定顺序的字段
        for key in field_order:
            if key in frontmatter:
                ordered_frontmatter[key] = frontmatter[key]
        
        # 添加其他字段
        for key in sorted(frontmatter.keys()):
            if key not in field_order:
                ordered_frontmatter[key] = frontmatter[key]
        
        # 重新生成 YAML front matter，保持缩进
        from io import StringIO
        string_stream = StringIO()
        yaml_processor.dump(ordered_frontmatter, string_stream)
        new_frontmatter = string_stream.getvalue().strip()
        
        # 重建完整内容，保持原有的换行结构
        if main_content.startswith('\n'):
            new_content = f"---\n{new_frontmatter}\n---{main_content}"
        else:
            new_content = f"---\n{new_frontmatter}\n---\n{main_content}"
        
        return new_content, new_content != content
        
    except Exception as e:
        print(f"❌ YAML 解析错误：{e}")
        return content, False

def process_markdown_file(file_path):
    """处理单个 Markdown 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 标准化 YAML front matter
        updated_content, changed = normalize_yaml_frontmatter(content)
        
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ 更新 YAML front matter: {file_path.name}")
            return True
        else:
            print(f"⏭️  跳过文件 (无需更新): {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 处理文件失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    notes_dir = Path("notes")
    
    if not notes_dir.exists():
        print(f"❌ 目录 {notes_dir} 不存在")
        sys.exit(1)
    
    # 查找所有 .md 文件
    md_files = list(notes_dir.glob("*.md"))
    
    if not md_files:
        print(f"❌ 在 {notes_dir} 目录中未找到 .md 文件")
        sys.exit(1)
    
    print(f"📝 找到 {len(md_files)} 个 Markdown 文件")
    print("=" * 60)
    
    updated_count = 0
    
    for file_path in sorted(md_files):
        if process_markdown_file(file_path):
            updated_count += 1
    
    print("=" * 60)
    print(f"✨ 处理完成！共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()