# CSS Modular Structure - PSv2 Flask Application

## Overview
The CSS has been successfully refactored into a professional modular structure for better maintainability and scalability.

## File Structure

### Core CSS Files (loaded in base.html)
```
app/static/css/
├── base.css        # Global styles, variables, typography, buttons, utilities
├── navbar.css      # Navigation bar, mobile menu, scroll animations
└── theme.css       # Theme configuration, light/dark mode (placeholder)
```

### Page-Specific CSS Files (loaded via {% block extra_css %})
```
├── home.css        # Homepage layout, hero section, features grid
├── admin.css       # Admin dashboard, management tables, forms
└── forms.css       # Login/register forms, form validation styles
```

## CSS Loading Order in base.html
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/navbar.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
{% block extra_css %}{% endblock %}
```

## Page-Specific CSS Usage
```html
<!-- In home.html -->
{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}

<!-- In admin/dashboard.html -->
{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/admin.css') }}">
{% endblock %}

<!-- For auth forms (when implemented) -->
{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/forms.css') }}">
{% endblock %}
```

## CSS Variables (Consistent Across All Files)
```css
:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --accent: #93c5fd;
    --accent-hover: #60a5fa;
    --border: rgba(241, 245, 249, 0.1);
    --shadow: rgba(0, 0, 0, 0.25);
    --blur-bg: rgba(30, 41, 59, 0.9);
    --navbar-bg: rgba(30, 41, 59, 0.95);
    --brand-primary: #3b82f6;
    --brand-secondary: #1e40af;
    --brand-accent: #60a5fa;
}
```

## Key Features Preserved
✅ All animations and transitions maintained
✅ Responsive design for mobile/tablet/desktop
✅ Smooth navbar scroll animations
✅ Color scheme consistency
✅ Flask url_for() integration
✅ Light/dark theme support
✅ Flash message styling (self-contained in _flash.html)

## Benefits of Modular Structure
- **Maintainability**: Easy to update specific components
- **Performance**: Pages only load required CSS
- **Scalability**: Simple to add new page-specific styles
- **Organization**: Clear separation of concerns
- **Team Collaboration**: Developers can work on different style modules
- **Caching**: Static CSS files can be cached by browsers

## Future Enhancements
- Light/dark mode toggle functionality in theme.css
- Additional page-specific CSS files as needed
- CSS optimization and minification for production
- Advanced theming system for client customization

## Testing Status
✅ Application builds and runs successfully
✅ All CSS files load correctly
✅ Navbar animations and responsive behavior intact
✅ Homepage styling properly applied
✅ Admin dashboard styling updated
✅ Visual consistency maintained across pages