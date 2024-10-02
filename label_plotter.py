import math

class LabelPlotter:
    def __init__(self, radius: float, angle_step: float, start_angle: float = 90, font_size = 10):
        self.start_angle = start_angle
        self.font_size = font_size
        self.start_text = ''
        self.radius = radius
        self.angle_step = angle_step
      
    def calc_angle_mid(self, angle: float):
        return self.start_angle - ((self.start_angle - angle) / 2) + (self.angle_step / 2)

    def label_plot(self, ax: any, text: str, angle: float, angle_ofs: float, alignment: str):
        r_a = math.radians(angle)

        x = self.radius * math.cos(r_a)
        y = self.radius * math.sin(r_a)

        ax.text(x, y, text,
                size=self.font_size, rotation=angle + angle_ofs,
                horizontalalignment=alignment, verticalalignment='center',
                rotation_mode='anchor',
                transform=ax.transData)

    def eval_label_plot(self, ax: any, text: str, angle: float, angle_ofs: float, alignment: str):
        if self.start_text == '':
            self.start_text = text
        elif self.start_text != text:
            self.label_plot(ax, self.start_text, self.calc_angle_mid(angle), angle_ofs, alignment)
            
            self.start_text = text
            self.start_angle = angle

    def final_label_plot(self, ax: any, angle: float, angle_ofs: float, alignment: str):
        self.label_plot(ax, self.start_text, self.calc_angle_mid(angle), angle_ofs, alignment)
