import reflex as rx
from sqlmodel import select
from front_end.models.user import User
from front_end.state import AppState


class AdminState(rx.State):
    """The app state."""

    _id: int
    name_field: str = ""
    worker_id_field: str = ""
    class_group_field: str = ""
    password_field: str = ""
    is_admin_field:bool = False       
    users: list[User] = []
    sort_value: str = ""
    num_Users: int

    def load_entries(self):
        """Get all users from the database."""
        with rx.session() as session:
            self.users = session.exec(select(User).where(User.name != "admin")).all()
            self.num_Users = len(self.users)
            if self.sort_value:
                self.users = sorted(
                    self.users, key=lambda user: getattr(user, self.sort_value).lower()
                )

    def sort_values(self, sort_value: str):
        item_map = {
            "姓名": "name",
            "工号": "worker_id",
            "班组": "class_group",
        }
        self.sort_value = item_map[sort_value]
        self.load_entries()

    def set_user_vars(self, user: User):
        self._id = user.id
        self.name_field = user.name
        self.worker_id_field = user.worker_id
        self.class_group_field = user.class_group
        self.is_admin_field = user.is_superuser

    def add_User(self):
        """Add a User to the database."""
        try:
            return self._add_User()
        except:
            return self._add_User()
    
    def _add_User(self):
        """Add a User to the database."""
        with rx.session() as session:
            if session.exec(
                select(User).where(User.worker_id == self.worker_id_field)
            ).first():
                return rx.window_alert("不可重复添加用户")
            session.add(
                User(
                    name=self.name_field,
                    password=self.password_field,
                    worker_id=self.worker_id_field,
                    class_group=self.class_group_field,
                )
            )
            session.commit()
        self.load_entries()
        # return rx.window_alert(f"User {self.name_field}:{self.worker_id_field} has been added.")

    def update_User(self):
        """Update a User in the database."""
        with rx.session() as session:
            user = session.exec(select(User).where(User.id == self._id)).first()
            user.name = self.name_field
            user.worker_id = self.worker_id_field
            user.class_group = self.class_group_field
            user.is_superuser = self.is_admin_field
            session.add(user)
            session.commit()
        self.load_entries()

    def delete_User(self, worker_id: str):
        """Delete a User from the database."""
        with rx.session() as session:
            user = session.exec(select(User).where(User.worker_id == worker_id)).first()
            session.delete(user)
            session.commit()
        self.load_entries()

    async def on_load(self):
        self.load_entries()
