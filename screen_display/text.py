from enums import Colors, Styles, Wrap_styles

class Text_style:
    def __init__(self, fore_color=Colors.DEFAULT, back_color=Colors.DEFAULT, text_type=Styles.DEFAULT):
        self.fore_color = Colors(fore_color)
        self.back_color = Colors(back_color)
        self.text_type = Styles(text_type)
        