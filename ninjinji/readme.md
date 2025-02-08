## 打包代码

```bash

# 打包项目
tar --exclude='.venv' --exclude='.web' -cvf ninjinji.tar /workspace/zmq_rpc/ninjinji
tar --exclude='.venv' --exclude='.web' -cvf ninjinji.tar /home/ubuntu/projects/ninjinji
tar --exclude='.venv' --exclude='.web' -cvf ninjinji.tar /root/projects/zmq_rpc/ninjinji

# 启动
docker compose up
cd front_end
uv sync
uv run reflex run
```


# YnpQtACbwQGhwoX8DxKB.wQEomeAEeXZ
# 2YZA.DLsElXAlQ60W7HsHs3JEhuM19Pw