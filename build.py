#!/usr/bin/env python3
"""
Build script for Odyssey Virtual Try-On
Injects the Odyssey API key from environment variable into index.html
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    # Get API key from environment variable
    api_key = os.environ.get('ODYSSEY_API_KEY')
    if not api_key:
        print("ERROR: ODYSSEY_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    print(f"Building with API key: {api_key[:10]}...")

    # Create public directory
    public_dir = Path('public')
    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir()

    # Read index.html
    index_html = Path('index.html').read_text(encoding='utf-8')

    # Replace placeholder with actual API key
    placeholder = 'ODYSSEY_API_KEY_PLACEHOLDER'
    if placeholder not in index_html:
        print(f"ERROR: Placeholder '{placeholder}' not found in index.html", file=sys.stderr)
        sys.exit(1)

    index_html = index_html.replace(placeholder, api_key)

    # Write to public/index.html
    (public_dir / 'index.html').write_text(index_html, encoding='utf-8')
    print("✓ Created public/index.html with injected API key")

    # Copy clothing-config.json
    shutil.copy2('clothing-config.json', public_dir / 'clothing-config.json')
    print("✓ Copied clothing-config.json")

    # Copy assets directory
    if Path('assets').exists():
        shutil.copytree('assets', public_dir / 'assets')
        print("✓ Copied assets/ directory")
    else:
        print("WARNING: assets/ directory not found", file=sys.stderr)

    print("\n✅ Build complete! Output in public/ directory")
    print(f"   Files created: {len(list(public_dir.rglob('*')))} total")

if __name__ == '__main__':
    main()
