#!/usr/bin/env python3
"""
Icon Synchronization Script

Automatically synchronizes SVG icons from assets/icons/ directory to inline SVG
icons in both index.html and NavigationSidebar.jsx files.

This script:
- Reads SVG files from the assets/icons/ directory
- Updates inline SVG icons in HTML with proper indentation
- Converts and updates inline SVG icons in React/JSX with JSX-compatible attributes
- Maintains unique mask IDs to prevent conflicts
- Preserves proper formatting for each file type

Usage:
    python3 sync-icons.py
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ============================================================================
# Configuration
# ============================================================================

ICONS_DIR = Path('assets/icons')
HTML_FILE = Path('index.html')
REACT_FILE = Path('NavigationSidebar.jsx')

# Icon file to mask ID mappings
# Maps each SVG file to its corresponding mask IDs in the codebase
# Suffix '-react' indicates the mask ID is used in the React component
ICON_MAPPINGS: Dict[str, List[str]] = {
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

# Indentation levels for different file formats
HTML_INDENT = 24  # Spaces for HTML inline icons
REACT_INDENT = 14  # Spaces for React/JSX inline icons


# ============================================================================
# File Operations
# ============================================================================

def read_file(filepath: Path) -> str:
    """
    Read and return the contents of a file.

    Args:
        filepath: Path to the file to read

    Returns:
        File contents as a string
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath: Path, content: str) -> None:
    """
    Write content to a file.

    Args:
        filepath: Path to the file to write
        content: Content to write to the file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


# ============================================================================
# SVG Content Processing
# ============================================================================

def extract_svg_inner_content(svg_content: str) -> str:
    """
    Extract the inner content from an SVG string.

    Removes the outer <svg> tags and returns only the inner elements.

    Args:
        svg_content: Complete SVG markup as a string

    Returns:
        Inner SVG content without outer <svg> tags
    """
    content_match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL)
    if content_match:
        return content_match.group(1).strip()
    return svg_content.strip()


def update_mask_id(content: str, old_mask_id: str, new_mask_id: str) -> str:
    """
    Replace all occurrences of a mask ID in SVG content.

    Updates both the mask ID definition and all references to it.

    Args:
        content: SVG content to update
        old_mask_id: Current mask ID to replace
        new_mask_id: New mask ID to use

    Returns:
        Updated SVG content with new mask ID
    """
    # Replace mask ID definition (both single and double quotes)
    content = re.sub(rf'id="{re.escape(old_mask_id)}"', f'id="{new_mask_id}"', content)
    content = re.sub(rf'id=\'{re.escape(old_mask_id)}\'', f'id="{new_mask_id}"', content)

    # Replace mask URL references
    content = re.sub(rf'url\(#{re.escape(old_mask_id)}\)', f'url(#{new_mask_id})', content)

    return content


def apply_indentation(content: str, indent_level: int) -> str:
    """
    Apply consistent indentation to multi-line content.

    Args:
        content: Content to indent
        indent_level: Number of spaces to indent

    Returns:
        Indented content
    """
    lines = content.split('\n')
    indented_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped:
            indented_lines.append(' ' * indent_level + stripped)

    return '\n'.join(indented_lines)


def convert_to_jsx_attributes(content: str) -> str:
    """
    Convert HTML attributes to JSX-compatible format.

    Transforms:
    - style="mask-type:alpha" -> style={{maskType: 'alpha'}}
    - stroke-width -> strokeWidth
    - stroke-linecap -> strokeLinecap
    - stroke-linejoin -> strokeLinejoin

    Args:
        content: SVG content with HTML attributes

    Returns:
        SVG content with JSX-compatible attributes
    """
    # Convert style attribute to JSX object notation
    content = re.sub(
        r'style="mask-type:alpha"',
        'style={{maskType: \'alpha\'}}',
        content
    )

    # Convert hyphenated attributes to camelCase
    content = re.sub(r'stroke-width="', 'strokeWidth="', content)
    content = re.sub(r'stroke-linecap="', 'strokeLinecap="', content)
    content = re.sub(r'stroke-linejoin="', 'strokeLinejoin="', content)

    return content


# ============================================================================
# Icon Preparation
# ============================================================================

def prepare_icon_for_html(svg_content: str, mask_id: str) -> str:
    """
    Prepare SVG icon content for HTML format.

    Extracts inner content, updates mask ID, and applies HTML indentation.

    Args:
        svg_content: Original SVG content from file
        mask_id: Target mask ID for this icon instance

    Returns:
        Formatted SVG content ready for HTML insertion
    """
    inner_content = extract_svg_inner_content(svg_content)

    # Update mask ID if present
    existing_mask = re.search(r'id="(mask[^"]*)"', inner_content)
    if existing_mask:
        old_mask_id = existing_mask.group(1)
        inner_content = update_mask_id(inner_content, old_mask_id, mask_id)

    return apply_indentation(inner_content, HTML_INDENT)


def prepare_icon_for_react(svg_content: str, mask_id: str) -> str:
    """
    Prepare SVG icon content for React/JSX format.

    Extracts inner content, updates mask ID, converts to JSX attributes,
    and applies React indentation.

    Args:
        svg_content: Original SVG content from file
        mask_id: Target mask ID for this icon instance

    Returns:
        Formatted SVG content ready for React/JSX insertion
    """
    inner_content = extract_svg_inner_content(svg_content)

    # Update mask ID if present
    existing_mask = re.search(r'id="(mask[^"]*)"', inner_content)
    if existing_mask:
        old_mask_id = existing_mask.group(1)
        inner_content = update_mask_id(inner_content, old_mask_id, mask_id)

    # Convert to JSX format
    inner_content = convert_to_jsx_attributes(inner_content)

    return apply_indentation(inner_content, REACT_INDENT)


# ============================================================================
# Icon Replacement
# ============================================================================

def find_and_replace_icon(
    content: str,
    mask_id: str,
    new_icon_content: str,
    closing_tag_indent: str
) -> Tuple[str, bool]:
    """
    Find and replace an icon in file content.

    Args:
        content: File content to search in
        mask_id: Mask ID to locate the icon
        new_icon_content: New icon content to insert
        closing_tag_indent: Indentation for the closing </svg> tag

    Returns:
        Tuple of (updated_content, was_replaced)
    """
    # Pattern matches SVG element containing the specific mask ID
    pattern = rf'(<svg width="16" height="16"[^>]*>)\s*<mask id="{re.escape(mask_id)}".*?</svg>'

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return content, False

    # Build new SVG with proper formatting
    new_svg = f'''<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
{new_icon_content}
{closing_tag_indent}</svg>'''

    # Replace in content
    updated_content = re.sub(pattern, new_svg, content, count=1, flags=re.DOTALL)
    return updated_content, True


def replace_html_icon(html_content: str, mask_id: str, new_icon_content: str) -> Tuple[str, bool]:
    """
    Replace an icon in HTML content.

    Args:
        html_content: HTML file content
        mask_id: Mask ID to locate the icon
        new_icon_content: New icon content to insert

    Returns:
        Tuple of (updated_content, was_replaced)
    """
    return find_and_replace_icon(html_content, mask_id, new_icon_content, ' ' * 20)


def replace_react_icon(react_content: str, mask_id: str, new_icon_content: str) -> Tuple[str, bool]:
    """
    Replace an icon in React/JSX content.

    Args:
        react_content: React component file content
        mask_id: Mask ID to locate the icon
        new_icon_content: New icon content to insert

    Returns:
        Tuple of (updated_content, was_replaced)
    """
    return find_and_replace_icon(react_content, mask_id, new_icon_content, ' ' * 10)


# ============================================================================
# Main Synchronization Logic
# ============================================================================

def validate_environment() -> bool:
    """
    Validate that required directories and files exist.

    Returns:
        True if environment is valid, False otherwise
    """
    if not ICONS_DIR.exists():
        print(f"❌ Icons directory not found: {ICONS_DIR}")
        return False

    if not HTML_FILE.exists():
        print(f"❌ HTML file not found: {HTML_FILE}")
        return False

    if not REACT_FILE.exists():
        print(f"❌ React file not found: {REACT_FILE}")
        return False

    return True


def process_icon(
    icon_file: str,
    mask_ids: List[str],
    html_content: str,
    react_content: str
) -> Tuple[str, str, bool, bool]:
    """
    Process a single icon file and update content.

    Args:
        icon_file: Name of the icon file
        mask_ids: List of mask IDs for this icon
        html_content: Current HTML content
        react_content: Current React content

    Returns:
        Tuple of (updated_html, updated_react, html_changed, react_changed)
    """
    icon_path = ICONS_DIR / icon_file

    if not icon_path.exists():
        print(f"⚠️  {icon_file}: File not found, skipping...")
        return html_content, react_content, False, False

    print(f"📝 Processing: {icon_file}")
    svg_content = read_file(icon_path)

    html_changed = False
    react_changed = False

    for mask_id in mask_ids:
        is_react = mask_id.endswith('-react')

        if is_react:
            # Update React file
            prepared_content = prepare_icon_for_react(svg_content, mask_id)
            react_content, replaced = replace_react_icon(react_content, mask_id, prepared_content)

            if replaced:
                print(f"   ✓ Updated {mask_id} in React")
                react_changed = True
            else:
                print(f"   ⚠️  {mask_id} not found in React")
        else:
            # Update HTML file
            prepared_content = prepare_icon_for_html(svg_content, mask_id)
            html_content, replaced = replace_html_icon(html_content, mask_id, prepared_content)

            if replaced:
                print(f"   ✓ Updated {mask_id} in HTML")
                html_changed = True
            else:
                print(f"   ⚠️  {mask_id} not found in HTML")

    return html_content, react_content, html_changed, react_changed


def sync_icons() -> bool:
    """
    Main function to synchronize all icons.

    Reads icons from assets directory and updates both HTML and React files
    with the latest icon content.

    Returns:
        True if any files were updated, False otherwise
    """
    print("🔄 Icon Synchronization Script")
    print("=" * 60)

    # Validate environment
    if not validate_environment():
        return False

    # Read file contents
    html_content = read_file(HTML_FILE)
    react_content = read_file(REACT_FILE)

    # Track changes
    html_updated = False
    react_updated = False

    # Process each icon
    print(f"\n📁 Reading icons from: {ICONS_DIR}\n")

    for icon_file, mask_ids in ICON_MAPPINGS.items():
        html_content, react_content, html_changed, react_changed = process_icon(
            icon_file, mask_ids, html_content, react_content
        )
        html_updated = html_updated or html_changed
        react_updated = react_updated or react_changed

    # Write updated contents
    if html_updated:
        write_file(HTML_FILE, html_content)
        print(f"\n✅ Successfully updated {HTML_FILE}")
    else:
        print(f"\n⚠️  No changes made to {HTML_FILE}")

    if react_updated:
        write_file(REACT_FILE, react_content)
        print(f"✅ Successfully updated {REACT_FILE}")
    else:
        print(f"⚠️  No changes made to {REACT_FILE}")

    # Display results
    if html_updated or react_updated:
        print("\n✨ Icon synchronization complete!")
        print("\n📋 Next steps:")
        print("  1. Review changes: git diff index.html NavigationSidebar.jsx")
        print("  2. Test locally: open index.html")
        print("  3. Commit changes: git add . && git commit -m 'Sync icons from assets'")
        return True
    else:
        print("\n❌ No icons were updated")
        return False


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    sync_icons()
