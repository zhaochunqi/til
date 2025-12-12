# Generate a new note with template
new name:
    #!/usr/bin/env python3
    import os
    import sys
    import subprocess
    from datetime import datetime
    
    # Get the name argument (justfile passes it as environment variable)
    name = "{{name}}"
    
    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate ULID for the new file
    try:
        result = subprocess.run(["uv", "run", "-q", "python3", "-c", 
                               "import ulid; from datetime import datetime; print(str(ulid.from_timestamp(datetime.now())))"], 
                              capture_output=True, text=True, check=True)
        ulid_str = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to generate ULID: {e}")
        ulid_str = ""
    
    # Template content with ULID
    if ulid_str:
        template = "---\ntags:\n  - \ndate: {}\nid: {}\n---\n# {}\n\n".format(current_date, ulid_str, name)
    else:
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