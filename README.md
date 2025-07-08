# 轻量天文API (V4.2)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Skyfield](https://img.shields.io/badge/Skyfield-1.47-orange.svg)](https://rhodesmill.org/skyfield/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个快速、轻量的API服务，旨在提供精确的日出日落、正午以及月相信息。它基于高性能的天文学库 [Skyfield](https://rhodesmill.org/skyfield/) 构建，并支持灵活的时区转换，确保数据符合用户所在地的实际情况。

**版本：** `4.2.0` - 稳定且已修复日出日落和月相计算逻辑。

## ✨ 主要特性

*   **日出、日落与正午时间计算：**
    *   为全球任意经纬度计算精确的日出、日落和正午（太阳上中天）时间。
    *   支持指定日期查询，并能正确处理跨时区日期边界问题。
    *   结果可按指定的 [IANA 时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 输出。
*   **当前月相信息：**
    *   提供月球被照亮的精确百分比。
    *   提供两种关键月相角度：
        *   `sun_moon_earth_angle_degrees`：太阳-月球-地球的夹角（0-180度），以月球为顶点，直接影响月球亮度。
        *   `moon_phase_orbital_degrees`：月球在其轨道上相对于太阳的黄经差（0-360度），用于判断月球的盈亏趋势。
    *   根据照亮百分比和轨道角度，返回直观的月相名称（如新月、盈凸月、下弦月等）。
    *   结果可按指定的 [IANA 时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 输出。
*   **轻量与高效：** 无潮汐数据计算，专注于核心天文事件，响应迅速。
*   **易于部署：** 基于FastAPI，提供自动交互式API文档（Swagger UI / ReDoc），并支持直接部署和Docker容器化部署。

## 🚀 快速启动

### 1. 先决条件

*   Python 3.10 或更高版本
*   `pip` (Python 包管理器)

### 2. 克隆仓库

首先，将项目代码克隆到您的本地机器：

```bash
git clone https://github.com/5bc2e7/Solunar.git
cd celestial-api                                             # 进入项目目录
```

### 3. 安装依赖
使用 `pip` 安装所有必要的库：

```bash
pip install -r requirements.txt
```

### 4. 本地运行服务

安装依赖后，您可以使用 `uvicorn` 在本地启动API服务：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

*   `main:app`: 指定 `main.py` 文件中的 `app` 对象。
*   `--host 0.0.0.0`: 允许从任何网络接口访问API，而不仅仅是本地主机。
*   `--port 8000`: 将API服务运行在8000端口。

服务启动后，API 将在 `http://0.0.0.0:8000` 上可用。

## 📖 API 文档与使用说明

API 服务启动后，您可以访问以下地址查看自动生成的交互式 API 文档：

*   **Swagger UI:** `http://your-api-host:8000/docs`
*   **ReDoc:** `http://your-api-host:8000/redoc`

以下是主要API端点的详细说明：

### 基本信息

*   **API 名称:** 轻量天文API
*   **版本:** `4.2.0`
*   **基础 URL:** `http://your-api-host:8000` (请替换为您的实际主机和端口)
*   **认证:** 无需认证

### 1. 获取日出、日落和正午时间

#### `GET /api/sun`

计算指定地点的日出、日落和正午时间。

*   **描述:** 根据提供的经纬度、日期和时区，计算该日的日出、日落和太阳上中天（正午）时间。

*   **参数 (Query Parameters):**

    | 名称         | 类型     | 是否必需 | 默认值 | 描述                                         | 约束              |
    | :----------- | :------- | :------- | :----- | :------------------------------------------- | :---------------- |
    | `lat`        | `float`  | 是       | -      | 纬度，例如：`21.5` (北部湾)                  | `-90 <= lat <= 90` |
    | `lon`        | `float`  | 是       | -      | 经度，例如：`108.5` (北部湾)                 | `-180 <= lon <= 180` |
    | `target_date`| `date`   | 否       | 今天   | 目标日期 (格式：`YYYY-MM-DD`)                | -                 |
    | `tz`         | `string` | 否       | `UTC`  | 输出时区名称 (IANA TZ database，例如：`Asia/Shanghai`) | 有效时区名称      |

*   **示例请求:**

    ```bash
    curl "http://localhost:8000/api/sun?lat=20.41&lon=109.44&target_date=2025-07-08&tz=Asia/Shanghai"
    ```

*   **示例响应 (HTTP 200 OK):**

    ```json
    {
      "location": {
        "latitude": 20.41,
        "longitude": 109.44
      },
      "date": "2025-07-08",
      "timezone": "Asia/Shanghai",
      "times": {
        "sunrise": "2025-07-08T06:08:00+08:00",
        "noon": "2025-07-08T12:47:21+08:00",
        "sunset": "2025-07-08T19:26:35+08:00"
      }
    }
    ```

### 2. 获取月相信息

#### `GET /api/moon`

获取当前的月相信息。

*   **描述:** 返回当前时刻月球的照亮百分比、两种关键角度以及对应的月相名称。

*   **参数 (Query Parameters):**

    | 名称 | 类型     | 是否必需 | 默认值 | 描述                                         | 约束         |
    | :--- | :------- | :------- | :----- | :------------------------------------------- | :----------- |
    | `tz` | `string` | 否       | `UTC`  | 输出时区名称 (IANA TZ database，例如：`Asia/Shanghai`) | 有效时区名称 |

*   **示例请求:**

    ```bash
    curl "http://localhost:8000/api/moon?tz=Asia/Shanghai"
    ```

*   **示例响应 (HTTP 200 OK):**

    ```json
    {
      "timestamp": "2025-07-08T21:40:12+08:00",
      "timezone": "Asia/Shanghai",
      "sun_moon_earth_angle_degrees": 26.98,
      "moon_phase_orbital_degrees": 153.4,
      "illumination_percent": 94.56,
      "phase_name": "盈凸月 (Waxing Gibbous)"
    }
    ```

*   **响应字段说明:**
    *   `timestamp`: API 调用时的日期时间，已转换为指定时区。
    *   `timezone`: 请求中指定的输出时区。
    *   `sun_moon_earth_angle_degrees`: 太阳、月球和地球三者之间的夹角，以月球为顶点（0-180度）。此角度越接近0度，月球越接近新月；越接近180度，月球越接近满月。它直接决定了月球的照亮百分比。
    *   `moon_phase_orbital_degrees`: 月球在其轨道上相对于太阳的黄经差（0-360度），也被称为月龄角度。
        *   `0°` 左右：新月
        *   `90°` 左右：上弦月
        *   `180°` 左右：满月
        *   `270°` 左右：下弦月
        此角度用于判断月球处于盈（0-180度）还是亏（180-360度）阶段。
    *   `illumination_percent`: 月球被太阳照亮的百分比（0-100%）。
    *   `phase_name`: 根据照亮百分比和月龄轨道角度判断出的月相名称。

## 部署指南

### 重要提示：生产环境考虑

*   **进程管理器:** 在生产环境中，不应直接运行 `uvicorn` 命令。应使用进程管理器（如 `systemd`, `Supervisor`, `PM2` 等）来确保应用在崩溃时能自动重启，并在服务器启动时自动运行。
*   **反向代理:** 建议在API服务前配置反向代理服务器（如 `Nginx`, `Caddy`）。反向代理可以提供：
    *   SSL/TLS 加密 (HTTPS)
    *   域名映射
    *   负载均衡
    *   静态文件服务
    *   请求日志和限速等功能。
*   **日志:** 确保您的应用日志被正确收集和监控。
*   **星历数据:** Skyfield 首次运行时会下载星历数据（通常是 `de440s.bsp`），并存储在用户主目录下的 `.skyfield` 文件夹中。在部署时，确保这个目录是可写的，或者预先下载好数据文件并挂载。

### 部署方式一：直接部署 (使用 `systemd` 和 `uvicorn`)

这种方式适用于基于Linux的服务器。

#### 1. 安装依赖和项目

*   在服务器上安装 Python 3.10+ 和 `pip`。
*   将项目代码复制到服务器的某个目录，例如 `/opt/celestial-api/`。
*   进入项目目录并安装依赖：
    ```bash
    cd /opt/celestial-api/
    pip install -r requirements.txt
    ```

#### 2. 创建 `systemd` 服务文件

创建 `/etc/systemd/system/celestial-api.service` 文件：

```ini
[Unit]
Description=Celestial API Service
After=network.target

[Service]
User=www-data             # 建议创建一个非root用户来运行服务
Group=www-data            # 建议创建一个非root组来运行服务
WorkingDirectory=/opt/celestial-api
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 # --workers 根据CPU核心数调整
Restart=always
RestartSec=5s
Environment="PATH=/usr/local/bin:/usr/bin:/bin" # 确保python路径正确
Environment="HOME=/var/www" # 设置HOME环境变量，让skyfield在可写目录下载星历文件

[Install]
WantedBy=multi-user.target
```

*   **注意:**
    *   将 `User` 和 `Group` 替换为您的实际用户/组（例如 `ubuntu`, `nginx` 等），或者创建一个新用户 (`sudo adduser www-data`)。
    *   `ExecStart` 中的 Python 路径 (`/usr/bin/python3`) 可能需要根据您的系统环境调整。如果使用了虚拟环境，路径会不同。
    *   `--workers` 参数可以根据您的CPU核心数进行调整，以利用多核处理能力。
    *   `Environment="HOME=/var/www"` 是一个技巧，让 Skyfield 将 `.skyfield` 数据文件下载到 `/var/www/.skyfield` 目录，而不是默认的 `/root/.skyfield` (对于 `root` 用户) 或 `/home/youruser/.skyfield` (对于其他用户)，确保服务用户有写入权限。

#### 3. 启动并启用服务

```bash
sudo systemctl daemon-reload       # 重新加载systemd配置
sudo systemctl start celestial-api # 启动服务
sudo systemctl enable celestial-api# 设置服务开机自启
```

*   **检查服务状态：**
    ```bash
    sudo systemctl status celestial-api
    journalctl -u celestial-api -f # 查看实时日志
    ```

#### 4. 配置反向代理 (Nginx 示例)

如果您使用 Nginx 作为反向代理，创建 `/etc/nginx/sites-available/celestial-api` 文件：

```nginx
server {
    listen 80;
    server_name api.yourdomain.com; # 替换为您的域名

    location / {
        proxy_pass http://127.0.0.1:8000; # 转发到 uvicorn 运行的端口
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

*   **启用 Nginx 配置并重启：**

    ```bash
    sudo ln -s /etc/nginx/sites-available/celestial-api /etc/nginx/sites-enabled/
    sudo nginx -t                # 测试配置语法
    sudo systemctl restart nginx # 重启 Nginx
    ```

### 部署方式二：Docker 容器化部署

使用 Docker 部署可以提供更好的环境隔离和可移植性。

#### 1. 构建 Docker 镜像

在项目根目录下运行以下命令构建镜像：

```bash
docker build -t celestial-api .
```
这会创建一个名为 `celestial-api` 的镜像。

#### 2. 运行 Docker 容器

您可以直接运行容器：

```bash
docker run -d -p 8000:8000 --name celestial-api-instance celestial-api
```
*   `-d`: 后台运行容器。
*   `-p 8000:8000`: 将宿主机的8000端口映射到容器的8000端口。
*   `--name celestial-api-instance`: 为容器指定一个名称。

**为了持久化 Skyfield 星历数据**，建议将 `~/.skyfield` 目录挂载为 Docker 卷。这样即使容器被删除，数据也不会丢失，下次启动时无需重新下载。

```bash
# 首先在宿主机上创建一个目录用于存放数据，例如：
mkdir -p ~/skyfield_data

# 然后运行容器时挂载这个目录：
docker run -d -p 8000:8000 \
  -v ~/skyfield_data:/app/.skyfield \ # 宿主机目录:容器内目录
  --name celestial-api-instance \
  celestial-api
```
**注意：** 确保宿主机上挂载的目录 `~/skyfield_data` 对于容器内运行的用户（通常是 `root`，或您在 `Dockerfile` 中设置的用户）是可写的。

#### 4. 使用 Docker Compose (推荐多服务或更便捷管理)

如果您使用 Docker Compose 管理多个服务或希望更方便地管理容器，可以创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  celestial-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - skyfield_data:/app/.skyfield # 挂载卷用于持久化Skyfield数据
    environment:
      # 确保容器内的Skyfield使用这个挂载点
      - SKYFIELD_DATA=/app/.skyfield
    restart: unless-stopped # 容器退出时自动重启，除非手动停止

volumes:
  skyfield_data: # 定义一个命名卷
```

*   **启动服务：**

    ```bash
    docker-compose up -d
    ```

*   **停止服务：**

    ```bash
    docker-compose down
    ```

无论哪种 Docker 部署方式，您都可以像前面描述的那样，在容器前配置反向代理（如 Nginx），将请求转发到 Docker 映射的端口（例如宿主机的 8000 端口）。

## 历史版本更新

*   **V4.2.0 (当前版本)**
    *   **修复：** 解决了 `/api/sun` 端点日出日落时间（特别是正午）在跨时区计算时的日期跳变问题，确保返回当日正确的时间。
    *   **修复：** 修正了 `/api/moon` 端点月相角度 `phase_angle_degrees` 的含义，将其更名为 `sun_moon_earth_angle_degrees`，并新增了更准确的月龄角度 `moon_phase_orbital_degrees`。
    *   **优化：** 改进了 `get_moon_phase_name` 函数的逻辑，使其能根据照亮百分比和月龄轨道角度更精确地判断并返回月相名称。
    *   **修复：** 修正了 `illumination.percent` 的错误调用，现在正确处理 `almanac.fraction_illuminated` 返回的浮点数。
*   **V4.1.0**
    *   引入时区转换功能。
    *   初步优化月相判断逻辑。
*   **V4.0.0**
    *   项目初始化，提供日出日落和基础月相信息。
    *   采用DE440s星历表。

## 🤝 贡献

欢迎通过提交问题（Issues）或拉取请求（Pull Requests）来为本项目贡献。

## 📄 许可协议

本项目采用 MIT 许可协议。
