from PyQt5 import QtCore, QtGui, QtWidgets

# Color Schemes
GREEN = {
    "background": "#848C67",
    "button_background": "#5C6249",
    "text": "#E1DBCA",
    "border": "#9BA186"
}

SAGE = {
    "background": "#B5C99A",
    "button_background": "#718355",
    "text": "#F5F5DC",
    "border": "#8FA36C"
}

DUSTY_ROSE = {
    "background": "#D4A5A5",
    "button_background": "#9B6B6B",
    "text": "#FFFFFF",
    "border": "#B88E8E"
}

SLATE_BLUE = {
    "background": "#A6B1C2",
    "button_background": "#6B7A8F",
    "text": "#FFFFFF",
    "border": "#8899AA"
}

TERRACOTTA = {
    "background": "#C89F91",
    "button_background": "#A67C6D",
    "text": "#FFFFFF",
    "border": "#B38E81"
}

LAVENDER_GRAY = {
    "background": "#C5B9D4",
    "button_background": "#8E7BA3",
    "text": "#FFFFFF",
    "border": "#A997B8"
}

SEAFOAM = {
    "background": "#A8C5B8",
    "button_background": "#6B9080",
    "text": "#FFFFFF",
    "border": "#89AA9B"
}

BLACK_GOLD = {
    "background": "#2C2C2C",
    "button_background": "#1A1A1A",
    "text": "#D4AF37",
    "border": "#B8860B"
}

def get_color_scheme(color_number):
    """
    Get color scheme by number
    
    Args:
        color_number: Integer representing the color scheme
            1 = GREEN
            2 = SAGE
            3 = DUSTY_ROSE
            4 = SLATE_BLUE
            5 = TERRACOTTA
            6 = LAVENDER_GRAY
            7 = SEAFOAM
            8 = BLACK_GOLD
    
    Returns:
        Dictionary with color scheme
    """
    schemes = {
        1: GREEN,
        2: SAGE,
        3: DUSTY_ROSE,
        4: SLATE_BLUE,
        5: TERRACOTTA,
        6: LAVENDER_GRAY,
        7: SEAFOAM,
        8: BLACK_GOLD
    }
    return schemes.get(color_number, GREEN)  # Default to GREEN if invalid number

def get_all_color_schemes():
    """
    Get all available color schemes
    Returns: Dictionary of all color schemes
    """
    return {
        1: GREEN,
        2: SAGE,
        3: DUSTY_ROSE,
        4: SLATE_BLUE,
        5: TERRACOTTA,
        6: LAVENDER_GRAY,
        7: SEAFOAM,
        8: BLACK_GOLD
    }

def set_background(background, color_number):
    """
    Set solid color background based on color scheme number
    
    Args:
        background: QLabel widget to set background
        color_number: Integer for color scheme (1-7)
    """
    color_scheme = get_color_scheme(color_number)
    background.setStyleSheet(f"background-color: {color_scheme['background']};")
    background.lower()


def style_button(button, color_number, border_radius=30):
    """
    Style a button with rounded corners based on color scheme
    
    Args:
        button: QPushButton to style
        color_number: Integer for color scheme (1-7)
        border_radius: Radius for rounded corners (default 30)
    """
    color_scheme = get_color_scheme(color_number)
    
    # Get current font size
    font_size = button.font().pointSize()
    
    stylesheet = f"""
        QPushButton {{
            background-color: {color_scheme['button_background']};
            color: {color_scheme['text']};
            border-radius: {border_radius}px;
            border: 4px solid {color_scheme['border']};
            padding: 10px;
            font-size: {font_size}pt;
            outline: none;
        }}
        QPushButton:hover {{
            background-color: {lighten_color(color_scheme['button_background'], 15)};
            border: 4px solid {lighten_color(color_scheme['border'], 15)};
        }}
        QPushButton:pressed {{
            background-color: {darken_color(color_scheme['button_background'], 15)};
            border: 4px solid {darken_color(color_scheme['border'], 15)};
        }}
        QPushButton:focus {{
            outline: none;
        }}
    """
    button.setStyleSheet(stylesheet)


def style_all_buttons(widget, color_number, border_radius=30):
    """
    Apply styling to all buttons in a widget
    
    Args:
        widget: Parent widget containing buttons
        color_number: Integer for color scheme (1-7)
        border_radius: Radius for rounded corners (default 30)
    """
    buttons = widget.findChildren(QtWidgets.QPushButton)
    for button in buttons:
        style_button(button, color_number, border_radius)


def style_label(label, color_number):
    """
    Style a label text to match the color scheme
    
    Args:
        label: QLabel to style
        color_number: Integer for color scheme (1-7)
    """
    color_scheme = get_color_scheme(color_number)
    
    # Get current font size
    font_size = label.font().pointSize()
    
    stylesheet = f"""
        QLabel {{
            color: {color_scheme['text']};
            font-size: {font_size}pt;
        }}
    """
    label.setStyleSheet(stylesheet)


def style_all_labels(widget, color_number):
    """
    Apply text color styling to all labels in a widget
    
    Args:
        widget: Parent widget containing labels
        color_number: Integer for color scheme (1-7)
    """
    labels = widget.findChildren(QtWidgets.QLabel)
    for label in labels:
        # Don't style the background label or image labels
        if label.objectName() not in ['background', 'label_image_1', 'label_image_2', 'label_image_3', 'label_countdown', 'label_countdown_2']:
            style_label(label, color_number)


def style_line_edit(line_edit, color_number, border_radius=15):
    """
    Style a line edit (text input) to match the color scheme
    
    Args:
        line_edit: QLineEdit to style
        color_number: Integer for color scheme (1-7)
        border_radius: Radius for rounded corners (default 15)
    """
    color_scheme = get_color_scheme(color_number)
    
    # Get current font size
    font_size = line_edit.font().pointSize()
    
    stylesheet = f"""
        QLineEdit {{
            border: 4px solid {color_scheme['border']};
            border-radius: {border_radius}px;
            padding: 10px;
            background-color: white;
            color: {color_scheme['button_background']};
            font-size: {font_size}pt;
        }}
        QLineEdit:focus {{
            border: 4px solid {color_scheme['button_background']};
        }}
    """
    line_edit.setStyleSheet(stylesheet)


def style_all_line_edits(widget, color_number, border_radius=15):
    """
    Apply styling to all line edits in a widget
    
    Args:
        widget: Parent widget containing line edits
        color_number: Integer for color scheme (1-7)
        border_radius: Radius for rounded corners (default 15)
    """
    line_edits = widget.findChildren(QtWidgets.QLineEdit)
    for line_edit in line_edits:
        style_line_edit(line_edit, color_number, border_radius)


def lighten_color(hex_color, percent):
    """
    Lighten a hex color by a percentage
    
    Args:
        hex_color: Hex color string (e.g., "#FF69B4")
        percent: Percentage to lighten (0-100)
    
    Returns:
        Lightened hex color string
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    r = min(255, int(r + (255 - r) * percent / 100))
    g = min(255, int(g + (255 - g) * percent / 100))
    b = min(255, int(b + (255 - b) * percent / 100))
    
    return f"#{r:02x}{g:02x}{b:02x}"


def darken_color(hex_color, percent):
    """
    Darken a hex color by a percentage
    
    Args:
        hex_color: Hex color string (e.g., "#FF69B4")
        percent: Percentage to darken (0-100)
    
    Returns:
        Darkened hex color string
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    r = max(0, int(r * (1 - percent / 100)))
    g = max(0, int(g * (1 - percent / 100)))
    b = max(0, int(b * (1 - percent / 100)))
    
    return f"#{r:02x}{g:02x}{b:02x}"

