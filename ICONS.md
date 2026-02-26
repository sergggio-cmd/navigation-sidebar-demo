# Icon Management Guide

This project uses an inline SVG sprite system for icons. This guide explains how to add and update icons.

## Quick Start

### Adding or Updating Icons

1. **Add/edit your SVG file** in `assets/icons/`:
   ```bash
   # Example: Edit an icon
   nano assets/icons/bell.svg
   ```

2. **Run the sync script**:
   ```bash
   python3 sync-icons.py
   ```

3. **Test the changes**:
   ```bash
   open index.html
   ```

4. **Commit the changes**:
   ```bash
   git add index.html assets/icons/
   git commit -m "Update bell icon"
   git push origin main
   ```

## How It Works

### Icon System Architecture

1. **Source files**: Individual SVG files in `assets/icons/`
2. **Inline sprite**: All icons compiled into a `<symbol>` sprite in `index.html`
3. **Usage**: Icons referenced with `<use href="#icon-name"/>`

### Why This Approach?

✅ **No CORS issues** - Works with `file://` protocol
✅ **No HTTP requests** - Better performance
✅ **GitHub Pages compatible** - Works everywhere
✅ **CSS control** - Uses `currentColor` for styling

## The Sync Script

### What `sync-icons.py` Does

1. Reads all `.svg` files from `assets/icons/`
2. Extracts SVG content and viewBox
3. Converts hard-coded colors to `currentColor`
4. Makes mask IDs unique (adds icon name suffix)
5. Generates `<symbol>` elements
6. Updates the inline sprite in `index.html`

### Script Options

Run the script:
```bash
python3 sync-icons.py
```

The script will:
- ✅ Process all icons in `assets/icons/`
- ✅ Show progress for each icon
- ✅ Update `index.html` automatically
- ✅ Provide next steps

## Icon Guidelines

### SVG Best Practices

1. **Use currentColor**: Replace fill/stroke colors with `currentColor`
   ```xml
   <!-- ❌ Bad -->
   <path fill="#000000" />

   <!-- ✅ Good -->
   <path fill="currentColor" />
   ```

2. **Standard viewBox**: Use `viewBox="0 0 16 16"` for consistency

3. **Unique mask IDs**: The script will make them unique automatically

4. **Clean SVG**: Remove unnecessary attributes and metadata

### Example Icon

```xml
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2 8L8 2.5L14 8M4 6.5V13H7V10H9V13H12V6.5"
          stroke="currentColor"
          stroke-width="1.25"
          stroke-linecap="round"
          stroke-linejoin="round"/>
</svg>
```

## Using Icons in HTML

### Basic Usage

```html
<div class="menu-item-icon">
    <svg width="16" height="16"><use href="#icon-home"/></svg>
</div>
```

### Available Icons

Run the script to see all processed icons:
```bash
python3 sync-icons.py
```

Current icons:
- `icon-home` - Home icon
- `icon-search` - Search icon
- `icon-bell` - Notifications/alerts icon
- `icon-bookmark` - Saved/bookmark icon
- `icon-star` - Interest/favorites icon
- `icon-newspaper` - Newsletter icon
- `icon-chart` - Companies/markets icon
- `icon-user-gear` - Administrator icon
- `icon-caret-down` - Dropdown arrow icon

## Troubleshooting

### Icons not showing?

1. **Run the sync script**:
   ```bash
   python3 sync-icons.py
   ```

2. **Check browser cache**: Hard refresh with `Cmd+Shift+R`

3. **Verify the icon exists** in `assets/icons/`

4. **Check the sprite**: Look for `<symbol id="icon-name">` in `index.html`

### Colors not working?

- Ensure your SVG uses `currentColor` instead of hard-coded colors
- Re-run the sync script (it auto-replaces colors)

### Mask conflicts?

- The script automatically makes mask IDs unique
- Re-run the sync script if you see conflicts

## Advanced: Manual Sprite Editing

If you need to manually edit the sprite in `index.html`:

1. Find the SVG sprite section (starts with `<!-- SVG Sprite (hidden) -->`)
2. Add/edit a `<symbol>` element:
   ```html
   <symbol id="icon-name" viewBox="0 0 16 16">
       <!-- SVG paths here -->
   </symbol>
   ```
3. Use in HTML: `<use href="#icon-name"/>`

**Note**: Manual edits will be overwritten by the sync script!

## Contributing Icons

When adding new icons to the project:

1. Add the source SVG to `assets/icons/`
2. Run `python3 sync-icons.py`
3. Test locally
4. Commit both the source file and updated `index.html`
5. Update this document's icon list

## Questions?

Check the `assets/icons/README.md` for more details about the icon system.
