import reflex as rx
from .user import User
from .operator_logs import OperatorLogs,add_operator_log,get_operator_logs
from .system import System,Settings


def init_db():
    try:
        with rx.session() as sess:
            user = sess.exec(User.select().where(User.name == "admin")).first()
            if user:
                pass
            else:
                sess.expire_on_commit = False  # Make sure the user object is accessible. https://sqlalche.me/e/14/bhk3
                user = User(name="admin", password="123456",worker_id="-1",class_group="-1",is_superuser=True)
                sess.add(user)
                sess.commit()
            system = sess.exec(System.select()).first()
            if system is None:
                settings = Settings(open_log_record=True)
                system = System(settings=settings.model_dump())
                sess.add(system)
                sess.commit()
        
        add_operator_log(worker_name="system", worker_id = "00000", class_group = "0", operation_content = "系统初始化成功", operation_type = "system_init",  operation_result = "success")
    except:
        print("warning: db has not init, please run reflex db init first")