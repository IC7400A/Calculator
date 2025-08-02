# ui/theme.py
# Final theme file supporting the new acrylic/blur effect.

LIGHT_THEME = {
    "bg_color": "rgba(240, 242, 245, 0.85)", "text_color": "#000000",
    "expr_color": "#555555", "btn_bg": "rgba(255, 255, 255, 0.7)",
    "op_bg": "rgba(231, 241, 255, 0.7)", "op_text": "#005bb5",
    "shift_bg": "rgba(254, 240, 200, 0.8)", "shift_text": "#b56e00",
    "eq_bg": "rgba(0, 120, 215, 0.9)", "eq_text": "#ffffff",
    "del_bg": "rgba(255, 220, 220, 0.7)", "del_text": "#c50f1f",
}

DARK_THEME = {
    "bg_color": "rgba(32, 33, 36, 0.85)", "text_color": "#e8eaed",
    "expr_color": "#969ba1", "btn_bg": "rgba(60, 64, 67, 0.7)",
    "op_bg": "rgba(46, 74, 110, 0.7)", "op_text": "#8ab4f8",
    "shift_bg": "rgba(83, 58, 1, 0.8)", "shift_text": "#fddc6c",
    "eq_bg": "rgba(138, 180, 248, 0.9)", "eq_text": "#202124",
    "del_bg": "rgba(80, 40, 40, 0.7)", "del_text": "#f75252",
}

def get_stylesheet(t):
    return f'''
        #background {{ background-color: {t['bg_color']}; border-radius: 12px; }}
        QLabel {{ background-color: transparent; color: {t['text_color']}; }}
        #mainDisplay {{ font-size: 48px; font-weight: 300; }}
        #expressionLabel {{ font-size: 16px; color: {t['expr_color']}; }}
        #indicator {{ font-size: 12px; font-weight: 600; color: {t['op_text']}; padding: 2px 5px; }}
        
        QPushButton {{
            font-size: 16px; font-weight: 500; background-color: {t['btn_bg']};
            color: {t['text_color']}; border: none; border-radius: 8px; min-height: 40px;
        }}
        QPushButton:pressed {{ background-color: rgba(0, 0, 0, 0.1); }}

        QPushButton[text="SHIFT"], QPushButton[text="hyp"] {{ background-color: {t['shift_bg']}; color: {t['shift_text']}; }}
        QPushButton[text~="sin"], QPushButton[text~="cos"], QPushButton[text~="tan"],
        QPushButton[text~="log"], QPushButton[text~="ln"], QPushButton[text="xʸ"], QPushButton[text="√"],
        QPushButton[text="π"], QPushButton[text="e"], QPushButton[text="!"], QPushButton[text="x²"], QPushButton[text="x⁻¹"] {{
            background-color: {t['op_bg']}; color: {t['op_text']};
        }}
        QPushButton[text="="] {{ background-color: {t['eq_bg']}; color: {t['eq_text']}; font-weight: 600; }}
        QPushButton[text="DEL"], QPushButton[text="AC"] {{ background-color: {t['del_bg']}; color: {t['del_text']}; }}
        
        #themeToggle {{ background-color: transparent; border: none; font-size: 20px; }}
    '''