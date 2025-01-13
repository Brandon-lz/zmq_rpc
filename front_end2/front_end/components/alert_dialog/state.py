import reflex as rx

class AlertDialogState(rx.State):
    """如果有多个继承，需要重新定义show变量名，否则会导致数据错乱，因为在子类中也能影响到"""
    show:bool = False

    def change(self):
        self.show = not self.show

    def close(self):
        self.show = False

    def open(self):
        self.show = True