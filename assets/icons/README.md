# Icons

This folder contains SVG icons used in the navigation sidebar component.

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

## Usage

Icons are automatically loaded using the `data-icon` attribute:

```html
<div class="menu-item-icon" data-icon="home"></div>
```

The JavaScript function `loadIcons()` will fetch the SVG file and inject it inline, preserving the `currentColor` functionality for styling.

## Adding New Icons

1. Add your SVG file to this directory
2. Use the `data-icon` attribute with the filename (without .svg extension)
3. Ensure the SVG uses `stroke="currentColor"` or `fill="currentColor"` for proper styling
