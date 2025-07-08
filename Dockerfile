# Dockerfile

# 使用官方Python基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装系统依赖（对于netCDF4等库可能需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnetcdf-dev \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 运行命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
