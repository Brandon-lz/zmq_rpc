import reflex as rx
from front_end.models.user import User


class AppState(rx.State):
    _user: User | None = None
    
    def get_user(self)->User:
        return self._user

    @rx.cached_var
    def current_user_name(self) -> str:
        if self._user:
            return self._user.name
        return "未登录"

    @rx.cached_var
    def is_admin(self):
        if self._user and self._user.is_superuser:
            return True
        return False

    def login(self, user: User):
        self._user = user

    def logout(self):
        self._user = None
        return rx.redirect("/login")

    def require_admin(self):
        if not self.is_admin:
            return rx.redirect("/")

    def require_login(self):
        if self._user is None:
            return rx.redirect("/")

    @rx.cached_var
    def is_login(self):
        return self._user is not None
