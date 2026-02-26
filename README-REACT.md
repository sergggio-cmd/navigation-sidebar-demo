# Navigation Sidebar - React Component

Este es un componente de navegación lateral (sidebar) completamente funcional construido con React.

## Características

- ✅ Navegación con menús desplegables (acordeón)
- ✅ Solo un menú puede estar expandido a la vez
- ✅ Solo un elemento puede estar seleccionado a la vez
- ✅ Iconos SVG inline con máscaras para renderizado correcto
- ✅ Transiciones suaves de expansión/colapso
- ✅ Tipografía Inter con peso semi-bold (600)
- ✅ Altura responsiva (86vh)
- ✅ Estilos consistentes con gap de 8px

## Archivos

- `NavigationSidebar.jsx` - Componente principal de navegación
- `NavigationSidebar.css` - Estilos del componente
- `App.jsx` - Ejemplo de uso del componente
- `App.css` - Estilos globales de la aplicación

## Instalación

### 1. Instalar dependencias

```bash
npm install react react-dom
```

### 2. Importar el componente

```jsx
import NavigationSidebar from './NavigationSidebar';
import './NavigationSidebar.css';

function App() {
  return (
    <div>
      <NavigationSidebar />
    </div>
  );
}
```

## Uso

El componente es completamente autónomo y maneja su propio estado internamente usando React hooks (`useState`).

### Estado Inicial

Por defecto, el componente inicia con:
- Menú "Interest" expandido
- Item "Tesla Inc." seleccionado

### Personalización

Para cambiar el estado inicial, modifica los valores en el componente:

```jsx
const [expandedMenu, setExpandedMenu] = useState('interest'); // null para ninguno expandido
const [selectedItem, setSelectedItem] = useState('tesla'); // null para ninguno seleccionado
```

### Eventos

El componente registra en la consola cuando se selecciona un item (puedes modificar esto para integrarlo con tu aplicación):

```jsx
console.log('Selected:', itemId);
```

## Estructura de Datos

### Items del Menú Principal

- `home` - Home
- `search` - Search Builder
- `alerts` - Alerts
- `saved` - Saved

### Menús Desplegables

**Interest:**
- `tesla` - Tesla Inc.
- `nvidia` - NVIDIA Corporation
- `openai` - OpenAI LLC

**Newsletters:**
- `newsletter-builder` - Newsletter Builder
- `view-newsletters` - View Newsletters

**Companies/Markets:**
- `companies-screening` - Companies Screening
- `executives` - Executives
- `quotes` - Quotes
- `market-charts` - Market Data Charts

**Administrator:**
- `group-manager` - Group Manager
- `custom-billing` - Custom Client Billing
- `reader-external` - Reader (External)
- `registration` - Registration

## Estilos

Los estilos están completamente encapsulados en `NavigationSidebar.css` y pueden ser personalizados según tus necesidades:

```css
/* Colores principales */
--bg-color: white;
--border-color: #e0e0e0;
--text-color: #28333f;
--hover-bg: #f5f5f5;
--active-bg: #e8f4f8;
--icon-color: #1E1E24;
```

## Integración con React Router

Para integrar con React Router, puedes envolver el componente y pasar callbacks:

```jsx
import { useNavigate } from 'react-router-dom';

function NavigationSidebarWithRouter() {
  const navigate = useNavigate();

  const handleItemClick = (itemId) => {
    // Navega a la ruta correspondiente
    navigate(`/${itemId}`);
  };

  return <NavigationSidebar onItemClick={handleItemClick} />;
}
```

## Soporte de Navegadores

- Chrome/Edge (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)

## Licencia

MIT
