# 将官方 Python 运行时用作父镜像
FROM python:3.10

# 维护者信息
MAINTAINER zhaopengtao

# 设置工作目录
WORKDIR ./anjuke

# 将当前目录内容复制到位于 /myapps 中的容器中
ADD . .

# 安装 requirements.txt 中指定的任何所需软件包
RUN pip install -r requirements.txt

# 在容器启动时运行 crawler.py
ENTRYPOINT ["python3"]

CMD ["./anjuke/crawler.py"]
