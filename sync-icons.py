#!/usr/bin/env python3
"""
Icon Sync Script
Synchronizes SVG icons from assets/icons/ to inline icons in index.html and NavigationSidebar.jsx
"""

import os
import re
from pathlib import Path

# Configuration
ICONS_DIR = Path('assets/icons')
HTML_FILE = Path('index.html')
REACT_FILE = Path('NavigationSidebar.jsx')

# Mapping of icon files to their usage identifiers in the code
ICON_MAPPINGS = {
    'home.svg': ['mask-home'],
    'search.svg': ['mask-search-builder'],
    'bell.svg': ['mask-bell-alerts'],
    'bookmark.svg': ['mask-bookmark-saved'],
    'star.svg': ['mask-star-interest'],
    'chat.svg': ['mask-chat', 'mask-chat-react'],
    'reports.svg': ['mask-reports', 'mask-reports-react'],
    'newspaper.svg': ['mask-newspaper-newsletters'],
    'chart.svg': ['mask-chart-companies', 'mask-chart-companies-react'],
    'user-gear.svg': ['mask-user-gear-admin'],
}

def read_svg_file(filepath):
    """Read and extract SVG content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def extract_svg_inner_content(svg_content):
    """Extract inner content from SVG (everything between <svg> tags)"""
    # Remove outer <svg> tag and extract inner content
    content_match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL)
    if content_match:
        return content_match.group(1).strip()
    return svg_content.strip()

def update_mask_id(content, old_mask_id, new_mask_id):
    """Update mask ID in SVG content"""
    # Replace all mask ID references
    content = re.sub(rf'id="{re.escape(old_mask_id)}"', f'id="{new_mask_id}"', content)
    content = re.sub(rf'id=\'{re.escape(old_mask_id)}\'', f'id="{new_mask_id}"', content)

    # Replace all mask URL references
    content = re.sub(rf'url\(#{re.escape(old_mask_id)}\)', f'url(#{new_mask_id})', content)

    return content

def prepare_icon_for_html(svg_content, mask_id):
    """Prepare icon content for HTML format"""
    inner_content = extract_svg_inner_content(svg_content)

    # Find existing mask ID in the SVG
    existing_mask = re.search(r'id="(mask[^"]*)"', inner_content)
    if existing_mask:
        old_mask_id = existing_mask.group(1)
        inner_content = update_mask_id(inner_content, old_mask_id, mask_id)

    # Ensure proper indentation (24 spaces for HTML inline icons)
    lines = inner_content.split('\n')
    indented_lines = []
    for line in lines:
        if line.strip():
            indented_lines.append(' ' * 24 + line.strip())

    return '\n'.join(indented_lines)

def prepare_icon_for_react(svg_content, mask_id):
    """Prepare icon content for React/JSX format"""
    inner_content = extract_svg_inner_content(svg_content)

    # Find existing mask ID in the SVG
    existing_mask = re.search(r'id="(mask[^"]*)"', inner_content)
    if existing_mask:
        old_mask_id = existing_mask.group(1)
        inner_content = update_mask_id(inner_content, old_mask_id, mask_id)

    # Convert HTML attributes to JSX
    inner_content = re.sub(r'style="mask-type:alpha"', 'style={{maskType: \'alpha\'}}', inner_content)
    inner_content = re.sub(r'stroke-width="', 'strokeWidth="', inner_content)
    inner_content = re.sub(r'stroke-linecap="', 'strokeLinecap="', inner_content)
    inner_content = re.sub(r'stroke-linejoin="', 'strokeLinejoin="', inner_content)

    # Ensure proper indentation (12-14 spaces for React inline icons)
    lines = inner_content.split('\n')
    indented_lines = []
    for line in lines:
        if line.strip():
            indented_lines.append(' ' * 14 + line.strip())

    return '\n'.join(indented_lines)

def find_and_replace_icon_in_html(html_content, mask_id, new_icon_content):
    """Find and replace an icon in HTML content"""
    # Pattern to match the SVG icon with specific mask ID
    # Matches from <svg...> to </svg> that contains the mask ID
    pattern = rf'(<svg width="16" height="16"[^>]*>)\s*<mask id="{re.escape(mask_id)}".*?</svg>'

    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        # Build new SVG
        new_svg = f'''<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
{new_icon_content}
                    </svg>'''

        # Replace in content
        html_content = re.sub(pattern, new_svg, html_content, count=1, flags=re.DOTALL)
        return html_content, True

    return html_content, False

def find_and_replace_icon_in_react(react_content, mask_id, new_icon_content):
    """Find and replace an icon in React/JSX content"""
    # Pattern to match the SVG icon with specific mask ID
    pattern = rf'(<svg width="16" height="16"[^>]*>)\s*<mask id="{re.escape(mask_id)}".*?</svg>'

    match = re.search(pattern, react_content, re.DOTALL)
    if match:
        # Build new SVG
        new_svg = f'''<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
{new_icon_content}
          </svg>'''

        # Replace in content
        react_content = re.sub(pattern, new_svg, react_content, count=1, flags=re.DOTALL)
        return react_content, True

    return react_content, False

def sync_icons():
    """Synchronize all icons from assets to HTML and React files"""
    print("🔄 Icon Sync Script")
    print("=" * 60)

    # Check if directories/files exist
    if not ICONS_DIR.exists():
        print(f"❌ Icons directory not found: {ICONS_DIR}")
        return False

    if not HTML_FILE.exists():
        print(f"❌ HTML file not found: {HTML_FILE}")
        return False

    if not REACT_FILE.exists():
        print(f"❌ React file not found: {REACT_FILE}")
        return False

    # Read file contents
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(REACT_FILE, 'r', encoding='utf-8') as f:
        react_content = f.read()

    html_updated = False
    react_updated = False

    # Process each icon
    print(f"\n📁 Reading icons from: {ICONS_DIR}\n")

    for icon_file, mask_ids in ICON_MAPPINGS.items():
        icon_path = ICONS_DIR / icon_file

        if not icon_path.exists():
            print(f"⚠️  {icon_file}: File not found, skipping...")
            continue

        print(f"📝 Processing: {icon_file}")
        svg_content = read_svg_file(icon_path)

        for mask_id in mask_ids:
            # Determine if this is for HTML or React based on mask_id suffix
            is_react = mask_id.endswith('-react')

            if is_react:
                # Update React file
                prepared_content = prepare_icon_for_react(svg_content, mask_id)
                react_content, replaced = find_and_replace_icon_in_react(react_content, mask_id, prepared_content)
                if replaced:
                    print(f"   ✓ Updated {mask_id} in React")
                    react_updated = True
                else:
                    print(f"   ⚠️  {mask_id} not found in React")
            else:
                # Update HTML file
                prepared_content = prepare_icon_for_html(svg_content, mask_id)
                html_content, replaced = find_and_replace_icon_in_html(html_content, mask_id, prepared_content)
                if replaced:
                    print(f"   ✓ Updated {mask_id} in HTML")
                    html_updated = True
                else:
                    print(f"   ⚠️  {mask_id} not found in HTML")

    # Write back updated contents
    if html_updated:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\n✅ Successfully updated {HTML_FILE}")
    else:
        print(f"\n⚠️  No changes made to {HTML_FILE}")

    if react_updated:
        with open(REACT_FILE, 'w', encoding='utf-8') as f:
            f.write(react_content)
        print(f"✅ Successfully updated {REACT_FILE}")
    else:
        print(f"⚠️  No changes made to {REACT_FILE}")

    if html_updated or react_updated:
        print("\n✨ Icon synchronization complete!")
        print("\n📋 Next steps:")
        print("  1. Review changes: git diff index.html NavigationSidebar.jsx")
        print("  2. Test locally: open index.html")
        print("  3. Commit: git add . && git commit -m 'Sync icons from assets'")
        return True
    else:
        print("\n❌ No icons were updated")
        return False

if __name__ == '__main__':
    sync_icons()
