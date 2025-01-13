import reflex as rx
from front_end.models.user import User


class RegisterState(rx.State):
    # jwt:str = ""    # 推荐
    user:dict = {}
    name_field:str
    password_field:str

    def log_in(self):
        if not(self.name_field and self.password_field):
            print(self.name_field, self.password_field)
            return rx.window_alert("请输入用户名及密码")
        with rx.session() as sess:
            user = sess.exec(User.select().where(User.name == self.name_field)).first()
            if user and user.password == self.password_field:
                self.user = user.dict()
                return rx.redirect("/control")
            else:
                return rx.window_alert("用户名或密码错误")

    def sign_up(self):
        with rx.session() as sess:
            user = sess.exec(User.select().where(User.name == self.name_field)).first()
            if user:
                return rx.window_alert(f"{self.name_field}已经注册，请不要重复注册")
            else:
                sess.expire_on_commit = False  # Make sure the user object is accessible. https://sqlalche.me/e/14/bhk3
                user = User(name=self.name_field, password=self.password_field)
                self.user = user
                sess.add(user)
                sess.commit()
                return rx.window_alert(f"{self.name_field}注册成功")

    def log_out(self):
        self.user = None
        return rx.redirect("/login")