# 开发者文档
## 初始账号密码 admin/123456

## start
```shell
reflex init
reflex db init
reflex db makemigrations
reflex db migrate
```

## docker打包
每次更新代码后，需要重新打包docker镜像
```shell
docker compose up --build
docker compose stop
docker commit ninjinji-font-app reflex-env:0.x
```
然后修改Dockerfile文件，将reflex-env:0.x替换为自己的镜像名
```shell
docker compose up --build -d
```