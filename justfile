default: add
    uvx pre-commit run -a

add:
    git add .

# Generate a new note with template
new name:
    uv run scripts/new_note.py "{{name}}"

# Generate a new note with template
open name editor='code':
    {{editor}} "$(uv run scripts/new_note.py '{{name}}')"

# Normalize YAML front matter in all notes
normalize:
    uv run scripts/normalize_yaml.py

# Generate notes index in README.md
index:
    uv run scripts/generate_notes_index.py

# Run all maintenance tasks
maintain:
    just normalize
    just index
