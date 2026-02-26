# Navigation Sidebar Demo

A responsive navigation sidebar component with expandable sections, smooth transitions, and accordion behavior.

🔗 **Live Demo**: https://sergggio-cmd.github.io/navigation-sidebar-demo/

## Features

✨ **Smooth Animations** - CSS transitions for dropdown expand/collapse
🎯 **Accordion Behavior** - Only one dropdown open at a time
🎨 **SVG Icon System** - Inline sprite with automated sync script
📱 **Responsive Design** - 1024px fixed height with overflow scroll
🎛️ **Consistent Spacing** - 8px gaps throughout the component
🚀 **Zero Dependencies** - Pure HTML, CSS, and JavaScript

## Project Structure

```
navigation-sidebar-demo/
├── index.html           # Main component file
├── assets/
│   └── icons/          # SVG icon source files
│       ├── bell.svg
│       ├── bookmark.svg
│       ├── caret-down.svg
│       ├── chart.svg
│       ├── home.svg
│       ├── newspaper.svg
│       ├── search.svg
│       ├── star.svg
│       ├── user-gear.svg
│       └── README.md
├── sync-icons.py       # Icon synchronization script
├── ICONS.md            # Icon management guide
└── README.md           # This file
```

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sergggio-cmd/navigation-sidebar-demo.git
   cd navigation-sidebar-demo
   ```

2. **Start local server**:
   ```bash
   python3 -m http.server 8000
   ```

3. **Open in browser**:
   ```
   http://localhost:8000
   ```

### Working with Icons

When you add or update icons:

1. **Edit the SVG** in `assets/icons/`:
   ```bash
   nano assets/icons/bell.svg
   ```

2. **Run the sync script**:
   ```bash
   python3 sync-icons.py
   ```

3. **Test and commit**:
   ```bash
   open index.html
   git add index.html assets/icons/
   git commit -m "Update bell icon"
   ```

📖 **Full guide**: See [ICONS.md](ICONS.md) for detailed icon management instructions.

## Deployment

### GitHub Pages (Current)

Already deployed at: https://sergggio-cmd.github.io/navigation-sidebar-demo/

To update:
```bash
git push origin main
```

Changes will be live in ~1 minute.

### Other Options

**Netlify Drop**:
1. Go to https://app.netlify.com/drop
2. Drag and drop `index.html`

**Vercel**:
```bash
npx vercel --prod
```

## Component Features

### Menu Structure

- **Home** - Navigation to home page
- **Search Builder** - Advanced search interface
- **Alerts** - Notification center
- **Saved** - Bookmarked items
- **Interest** ▾ - Expandable dropdown
  - Tesla Inc.
  - NVIDIA Corporation
  - OpenAI LLC
- **Newsletters** ▾ - Expandable dropdown
  - Newsletter Builder
  - View Newsletters
- **Companies/Markets** ▾ - Expandable dropdown
  - Companies Screening
  - Executives
  - Quotes
  - Market Data Charts
- **Administrator** ▾ - Expandable dropdown
  - Group Manager
  - Custom Client Billing
  - Reader (External)
  - Registration

### Behavior

- **Accordion Mode**: Only one dropdown can be expanded at a time
- **Smooth Transitions**: 0.3-0.4s CSS animations
- **Highlight States**: Active menu items and selected submenu items
- **Keyboard Accessible**: Proper ARIA labels and semantic HTML

## Technical Details

### Icon System

Uses an **inline SVG sprite** for optimal performance:

- ✅ No HTTP requests
- ✅ No CORS issues
- ✅ Works with `file://` protocol
- ✅ Dynamic coloring with `currentColor`
- ✅ Automated sync script

**Adding icons**:
```bash
# 1. Add SVG to assets/icons/
# 2. Run sync script
python3 sync-icons.py
```

### CSS Architecture

- **Flexbox Layout**: For consistent spacing and alignment
- **CSS Transitions**: For smooth animations
- **CSS Variables Ready**: Easy to add custom properties
- **BEM-like Naming**: Clear component structure

### JavaScript

- **Vanilla JS**: No frameworks required
- **Event Delegation**: Efficient event handling
- **Accordion Logic**: Automatic dropdown management
- **Highlight Management**: Active state tracking

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Commit with descriptive messages
6. Push and create a Pull Request

## License

MIT License - feel free to use in your projects!

## Credits

Built with assistance from Claude Sonnet 4.5
