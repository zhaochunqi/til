# Generate a new note with template
new name:
    #!/usr/bin/env python3
    import os
    import sys
    from datetime import datetime
    
    # Get the name argument (justfile passes it as environment variable)
    name = "{{name}}"
    
    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Template content
    template = "---\ntags:\n  - \ndate: {}\n---\n# {}\n\n".format(current_date, name)
    
    # Create the file path
    file_path = f"notes/{name}.md"
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File '{file_path}' already exists!")
        exit(1)
    
    # Write the template to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Created new note: {file_path}")