#!/usr/bin/env python3
"""
Icon Sync Script
Synchronizes SVG icons from assets/icons/ to the inline sprite in index.html
"""

import os
import re
from pathlib import Path

# Configuration
ICONS_DIR = Path('assets/icons')
HTML_FILE = Path('index.html')

def read_svg_file(filepath):
    """Read and extract SVG content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def extract_svg_content(svg_content):
    """Extract viewBox and inner content from SVG"""
    # Extract viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_content)
    viewbox = viewbox_match.group(1) if viewbox_match else "0 0 16 16"

    # Extract content between <svg> tags
    content_match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL)
    if content_match:
        inner_content = content_match.group(1).strip()
    else:
        inner_content = svg_content

    return viewbox, inner_content

def replace_colors_with_current(content):
    """Replace hard-coded colors with currentColor"""
    # Replace common fill colors
    content = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', content)
    content = re.sub(r'fill="#[0-9A-Fa-f]{3}"', 'fill="currentColor"', content)

    # Replace common stroke colors
    content = re.sub(r'stroke="#[0-9A-Fa-f]{6}"', 'stroke="currentColor"', content)
    content = re.sub(r'stroke="#[0-9A-Fa-f]{3}"', 'stroke="currentColor"', content)

    # Update mask IDs to avoid conflicts
    # Replace generic mask IDs with unique ones based on icon name

    return content

def make_mask_ids_unique(content, icon_name):
    """Make mask IDs unique by adding icon name"""
    # Find all mask id definitions and usages
    mask_ids = re.findall(r'id="(mask[^"]*)"', content)

    for mask_id in mask_ids:
        new_mask_id = f"{mask_id}-{icon_name}"
        # Replace id definition
        content = content.replace(f'id="{mask_id}"', f'id="{new_mask_id}"')
        # Replace url reference
        content = content.replace(f'url(#{mask_id})', f'url(#{new_mask_id})')

    return content

def generate_sprite(icons_dir):
    """Generate SVG sprite from icon files"""
    symbols = []

    # Get all SVG files
    svg_files = sorted(icons_dir.glob('*.svg'))

    for svg_file in svg_files:
        icon_name = svg_file.stem  # filename without extension

        print(f"Processing: {icon_name}")

        svg_content = read_svg_file(svg_file)
        viewbox, inner_content = extract_svg_content(svg_content)

        # Replace colors with currentColor
        inner_content = replace_colors_with_current(inner_content)

        # Make mask IDs unique
        inner_content = make_mask_ids_unique(inner_content, icon_name)

        # Create symbol
        symbol = f'            <symbol id="icon-{icon_name}" viewBox="{viewbox}">\n'

        # Indent inner content
        for line in inner_content.split('\n'):
            if line.strip():
                symbol += f'                {line}\n'

        symbol += '            </symbol>'

        symbols.append(symbol)

    # Generate complete sprite
    sprite = '    <!-- SVG Sprite (hidden) -->\n'
    sprite += '    <svg style="display: none;" xmlns="http://www.w3.org/2000/svg">\n'
    sprite += '        <defs>\n'
    sprite += '\n'.join(symbols)
    sprite += '\n        </defs>\n'
    sprite += '    </svg>\n'

    return sprite

def update_html(html_file, new_sprite):
    """Update HTML file with new sprite"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find and replace the sprite section
    # Pattern matches from <!-- SVG Sprite --> to </svg> (inclusive)
    pattern = r'(\s*)<!-- SVG Sprite.*?</svg>\n'

    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        # Replace with new sprite
        updated_html = re.sub(pattern, new_sprite, html_content, count=1, flags=re.DOTALL)

        # Write back
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)

        print(f"\n✅ Successfully updated {html_file}")
        return True
    else:
        print(f"\n❌ Could not find sprite section in {html_file}")
        print("   Make sure the HTML contains: <!-- SVG Sprite (hidden) -->")
        return False

def main():
    print("🔄 Icon Sync Script")
    print("=" * 50)

    # Check if directories exist
    if not ICONS_DIR.exists():
        print(f"❌ Icons directory not found: {ICONS_DIR}")
        return

    if not HTML_FILE.exists():
        print(f"❌ HTML file not found: {HTML_FILE}")
        return

    # Generate sprite
    print(f"\n📁 Reading icons from: {ICONS_DIR}")
    sprite = generate_sprite(ICONS_DIR)

    # Update HTML
    print(f"\n📝 Updating: {HTML_FILE}")
    success = update_html(HTML_FILE, sprite)

    if success:
        print("\n✨ Icon synchronization complete!")
        print("\nNext steps:")
        print("  1. Review changes: git diff index.html")
        print("  2. Test locally: open index.html")
        print("  3. Commit: git add index.html && git commit -m 'Update icon sprite'")
    else:
        print("\n❌ Synchronization failed")

if __name__ == '__main__':
    main()
