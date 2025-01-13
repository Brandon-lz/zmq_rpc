# 打开注释来更新镜像  docker compose build --no-cache ， 然后关闭注释再次使用docker compose build --no-cache && docker compose up -d 启动项目
# build line
FROM python:3.11   

# FROM ninjinji-font

ENV PYTHONUNBUFFERED 1

# build line
ENV https_proxy=http://10.30.24.88:7890
ENV http_proxy=http://10.30.24.88:7890
ENV no_proxy="localhost,127.0.0.1,192.168.70.*"

RUN rm -rf /app
WORKDIR /app

COPY . .

RUN rm -rf /app/.web && rm -rf /app/alembic.ini && rm -rf /app/alembic
# RUN rm -rf /app/alembic.ini && rm -rf /app/alembic/

# build line
RUN pip install --upgrade pip --proxy="http://10.30.24.88:7890" && pip install -r requirements.txt --proxy="http://10.30.24.88:7890" --no-cache

RUN reflex init

STOPSIGNAL SIGKILL

CMD reflex db init && reflex db makemigrations && reflex db migrate && reflex run --env prod