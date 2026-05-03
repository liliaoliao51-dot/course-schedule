FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令：建表 + 运行 uvicorn
CMD ["sh", "-c", "python -c 'from database import engine, Base; import models; Base.metadata.create_all(bind=engine)' && uvicorn main:app --host 0.0.0.0 --port 8000"]
