# Icons

This folder contains SVG icon source files for the navigation sidebar component.

## Available Icons

- `home.svg` - Home icon
- `search.svg` - Search/magnifying glass icon
- `bell.svg` - Alerts/notifications icon
- `bookmark.svg` - Saved/bookmark icon
- `star.svg` - Interest/favorites icon
- `newspaper.svg` - Newsletter icon
- `chart.svg` - Companies/markets/chart icon
- `user-gear.svg` - Administrator/user settings icon
- `caret-down.svg` - Dropdown arrow icon

## Icon System

The component uses an **SVG sprite system** with icons defined inline in the HTML for maximum compatibility. Icons are defined as `<symbol>` elements in a hidden SVG at the top of the page and referenced using `<use>` tags.

### Usage

To use an icon in the component:

```html
<div class="menu-item-icon">
    <svg width="16" height="16"><use href="#icon-home"/></svg>
</div>
```

### Benefits

- ✅ Works without a web server (no CORS issues)
- ✅ Works on GitHub Pages and all hosting platforms
- ✅ Preserves `currentColor` for dynamic styling
- ✅ Better performance (no HTTP requests)
- ✅ Easy to maintain and update

## Adding New Icons

1. Add your SVG file to this directory as a source file
2. Convert the SVG to a `<symbol>` in the inline sprite (in `index.html`)
3. Reference it using `<use href="#icon-name"/>`
4. Ensure paths use `stroke="currentColor"` and `fill="none"` for proper styling

## Example: Adding a New Icon

1. Save `new-icon.svg` to this folder
2. Add to the sprite in `index.html`:
   ```html
   <symbol id="icon-new-icon" viewBox="0 0 16 16">
       <path d="..." stroke="currentColor" stroke-width="1.25" fill="none"/>
   </symbol>
   ```
3. Use it:
   ```html
   <svg width="16" height="16"><use href="#icon-new-icon"/></svg>
   ```
