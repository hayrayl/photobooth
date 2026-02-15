from PyQt5 import QtCore, QtGui, QtWidgets

# Color Schemes
GREEN = {
    "background": "#848C67",
    "button_background": "#5C6249",
    "text": "#E1DBCA",
    "border": "#9BA186"
}

PINK = {
    "background": "#FFB6C1",
    "button_background": "#FF69B4",
    "text": "#FFFFFF",
    "border": "#FF1493"
}

PURPLE = {
    "background": "#DDA0DD",
    "button_background": "#9370DB",
    "text": "#FFFFFF",
    "border": "#8B008B"
}

BLUE = {
    "background": "#87CEEB",
    "button_background": "#4682B4",
    "text": "#FFFFFF",
    "border": "#1E90FF"
}

PEACH = {
    "background": "#FFDAB9",
    "button_background": "#FF7F50",
    "text": "#FFFFFF",
    "border": "#FF6347"
}

LAVENDER = {
    "background": "#E6E6FA",
    "button_background": "#BA55D3",
    "text": "#FFFFFF",
    "border": "#9370DB"
}

MINT = {
    "background": "#98FF98",
    "button_background": "#3CB371",
    "text": "#FFFFFF",
    "border": "#2E8B57"
}

ROSE_GOLD = {
    "background": "#B76E79",
    "button_background": "#96505A",
    "text": "#FFFFFF",
    "border": "#D4919A"
}

def get_color_scheme(color_number):
    """
    Get color scheme by number
    
    Args:
        color_number: Integer representing the color scheme
            1 = GREEN
            2 = PINK
            3 = PURPLE
            4 = BLUE
            5 = PEACH
            6 = LAVENDER
            7 = MINT
    
    Returns:
        Dictionary with color scheme
    """
    schemes = {
        1: GREEN,
        2: PINK,
        3: PURPLE,
        4: BLUE,
        5: PEACH,
        6: LAVENDER,
        7: MINT
    }
    return schemes.get(color_number, PINK)  # Default to PINK if invalid number

def get_all_color_schemes():
    """
    Get all available color schemes
    Returns: Dictionary of all color schemes
    """
    return {
        1: GREEN,
        2: PINK,
        3: PURPLE,
        4: BLUE,
        5: PEACH,
        6: LAVENDER,
        7: MINT,
        8: ROSE_GOLD
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
        }}
        QPushButton:hover {{
            background-color: {lighten_color(color_scheme['button_background'], 15)};
            border: 4px solid {lighten_color(color_scheme['border'], 15)};
        }}
        QPushButton:pressed {{
            background-color: {darken_color(color_scheme['button_background'], 15)};
            border: 4px solid {darken_color(color_scheme['border'], 15)};
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

