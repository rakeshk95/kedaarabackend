#!/usr/bin/env python3
"""
Script to update all pydantic Config classes to use the new v2 model_config syntax.
"""

import os
import re

def update_pydantic_configs():
    """Update all pydantic Config classes to use model_config."""
    
    # Files to update
    schema_files = [
        "app/schemas/reviewer_selection.py",
        "app/schemas/notification.py",
        "app/schemas/feedback_form.py"
    ]
    
    for file_path in schema_files:
        if os.path.exists(file_path):
            print(f"Updating {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace class Config: with model_config
            updated_content = re.sub(
                r'    class Config:\s*\n\s*from_attributes = True',
                '    model_config = {\n        "from_attributes": True\n    }',
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated {file_path}")

if __name__ == "__main__":
    update_pydantic_configs()
    print("✅ All pydantic configs updated!")
