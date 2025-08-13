#!/usr/bin/env python3
"""
Script to remove all emojis from the project files
"""

import re
import os
from pathlib import Path

def remove_emojis_from_text(text):
    """Remove all emojis from text"""
    # Unicode ranges for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Various symbols
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "]+", 
        flags=re.UNICODE
    )
    
    # Remove emojis but keep the space if there was one
    cleaned_text = emoji_pattern.sub(' ', text)
    
    # Clean up multiple spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Clean up lines that start with space after removing emoji
    lines = cleaned_text.split('\n')
    cleaned_lines = []
    for line in lines:
        # If line starts with space after emoji removal, clean it
        if line.startswith(' ') and not line.strip().startswith(' '):
            line = line.lstrip()
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def process_file(file_path):
    """Process a single file to remove emojis"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        cleaned_content = remove_emojis_from_text(content)
        
        if cleaned_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"✓ Processed: {file_path}")
            return True
        else:
            print(f"- No emojis found: {file_path}")
            return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all project files"""
    project_root = Path(__file__).parent
    
    # Files to process
    files_to_process = [
        'main.py',
        'demo.py', 
        'test_run.py',
        'README.md',
    ]
    
    # Also process Python files in subdirectories
    for subdir in ['models', 'services', 'utils']:
        subdir_path = project_root / subdir
        if subdir_path.exists():
            for py_file in subdir_path.glob('*.py'):
                files_to_process.append(str(py_file.relative_to(project_root)))
    
    print(f"🧹 Removing emojis from {len(files_to_process)} files...")
    print("=" * 50)
    
    processed_count = 0
    
    for file_path in files_to_process:
        full_path = project_root / file_path
        if full_path.exists():
            if process_file(full_path):
                processed_count += 1
        else:
            print(f"✗ File not found: {file_path}")
    
    print("=" * 50)
    print(f"🎉 Completed! Processed {processed_count} files.")
    print("All emojis have been removed from the project.")

if __name__ == "__main__":
    main()