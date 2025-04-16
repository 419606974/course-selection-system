# 使用 Python 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制所有项目文件到容器
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 暴露 Flask 服务端口
EXPOSE 8888

# 运行 Flask 应用
CMD ["python", "app.py"]