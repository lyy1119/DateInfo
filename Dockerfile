# 使用官方 Python 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将本地代码复制到容器中
COPY . /app

# 安装所需的依赖项
RUN pip install --no-cache-dir -r ./requirements.txt

# 暴露容器的端口
EXPOSE 8000

# 启动 FastAPI 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
