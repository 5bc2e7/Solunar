# Solunar API
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-05998b.svg)](https://fastapi.tiangolo.com/)
[![Powered by](https://img.shields.io/badge/Powered%20by-Skyfield-orange.svg)](https://rhodesmill.org/skyfield/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?logo=docker)](https://hub.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Solunar API** 是一个快速、轻量的API服务，旨在提供精确的日出日落、正午以及月相信息。它基于高性能的天文学库 [Skyfield](https://rhodesmill.org/skyfield/) 构建，并支持灵活的时区转换，确保数据符合用户所在地的实际情况。

---

## ✨ 主要特性

*   **太阳事件计算**：为全球任意经纬度计算精确的日出、日落和正午（太阳上中天）时间。
*   **月相信息**：提供月球被照亮的精确百分比、关键天文角度，并返回直观的月相名称（如新月、盈凸月等）。
*   **时区感知**：所有时间数据均可按指定的 [IANA 时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 输出。
*   **轻量高效**：专注于核心天文事件，无冗余计算，响应迅速。
*   **易于部署**：提供自动交互式API文档（Swagger UI / ReDoc），并支持直接部署和Docker容器化部署。

## 🚀 快速启动

### 1. 先决条件
*   Python 3.10+
*   Docker (推荐)

### 2. 克隆仓库
```bash
git clone https://github.com/5bc2e7/Solunar.git
cd Solunar
```

### 3. 使用 Docker 运行 (推荐)
这是启动服务最简单、最可靠的方式。

```bash
docker-compose up -d
```
服务将在 `http://localhost:8000` 上可用。

### 4. 本地运行 (不使用 Docker)

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 启动服务
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
服务启动后，API 将在 `http://localhost:8000` 上可用。

## 📖 API 使用指南

服务启动后，您可以访问以下地址查看自动生成的交互式 API 文档：

*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

---

### `GET /api/sun`
计算指定地点的日出、日落和正午时间。

#### 查询参数
| 名称         | 类型     | 必需 | 默认 | 描述                                         | 示例              |
| :----------- | :------- | :--- | :--- | :------------------------------------------- | :---------------- |
| `lat`        | `float`  | 是   | -    | 纬度 (`-90` to `90`)                         | `39.9` (北京)     |
| `lon`        | `float`  | 是   | -    | 经度 (`-180` to `180`)                       | `116.4` (北京)    |
| `target_date`| `string` | 否   | 今天 | 目标日期 (格式: `YYYY-MM-DD`)                | `2024-12-25`      |
| `tz`         | `string` | 否   | `UTC`| 输出时区 (IANA TZ database)                  | `Asia/Shanghai`   |

#### 示例请求
```bash
curl "http://localhost:8000/api/sun?lat=39.9&lon=116.4&tz=Asia/Shanghai"
```

#### 示例响应
```json
{
  "location": {
    "latitude": 39.9,
    "longitude": 116.4
  },
  "date": "2024-05-22",
  "timezone": "Asia/Shanghai",
  "times": {
    "sunrise": "2024-05-22T04:51:56+08:00",
    "noon": "2024-05-22T12:15:24+08:00",
    "sunset": "2024-05-22T19:38:53+08:00"
  }
}
```

---

### `GET /api/moon`
获取当前的月相信息。

#### 查询参数
| 名称 | 类型     | 必需 | 默认 | 描述                  | 示例            |
| :--- | :------- | :--- | :--- | :-------------------- | :-------------- |
| `tz` | `string` | 否   | `UTC`| 输出时区 (IANA TZ database) | `Asia/Shanghai` |

#### 示例请求
```bash
curl "http://localhost:8000/api/moon?tz=Asia/Shanghai"
```

#### 示例响应
```json
{
  "timestamp": "2024-05-22T15:30:00+08:00",
  "timezone": "Asia/Shanghai",
  "sun_moon_earth_angle_degrees": 170.5,
  "moon_phase_orbital_degrees": 175.8,
  "illumination_percent": 99.8,
  "phase_name": "盈凸月 (Waxing Gibbous)"
}
```
**响应字段说明:**
*   `sun_moon_earth_angle_degrees`: 太阳-月球-地球夹角 (0-180°)，决定亮度。越接近180°越亮。
*   `moon_phase_orbital_degrees`: 月球轨道相位角 (0-360°)，决定盈亏。`0°`是新月，`180°`是满月。
*   `illumination_percent`: 月球被照亮的百分比。
*   `phase_name`: 直观的月相名称。

## 🚀 部署指南

### 重要提示
*   **进程管理器**: 在生产环境，应使用 `systemd`, `Supervisor` 等工具管理 `uvicorn` 进程。
*   **反向代理**: 强烈建议在API前配置 `Nginx` 或 `Caddy` 来提供HTTPS、负载均衡和安全加固。
*   **星历数据**: Skyfield 首次运行会下载星历数据 (`.bsp` 文件)。在部署时，确保数据目录可写，或预先挂载数据文件。

### 部署方式一：Docker (强烈推荐)

使用 Docker 是最简单、最可靠的部署方式。

#### 使用 Docker Compose (最佳实践)
项目已包含一个 `docker-compose.yml` 文件。

```yaml
version: '3.8'

services:
  solunar-api:
    build: .
    container_name: solunar-api
    ports:
      - "8000:8000"
    volumes:
      - skyfield_data:/app/.skyfield
    restart: unless-stopped

volumes:
  skyfield_data:
    driver: local
```

**启动服务:**
```bash
docker compose up -d
```
**停止服务:**
```bash
docker compose down
```

#### 手动运行 Docker 容器
如果你不使用 Docker Compose，也可以手动运行。

```bash
# 1. 构建镜像
docker build -t solunar-api .

# 2. 运行容器
docker run -d \
  -p 8000:8000 \
  -v skyfield_data:/app/.skyfield \
  --name solunar-api-instance \
  --restart unless-stopped \
  solunar-api
```
*   `--restart unless-stopped`: 确保容器在意外退出或服务器重启后能自动恢复。
*   `-v skyfield_data:/app/.skyfield`: 使用命名卷持久化星历数据，避免重复下载。

### 部署方式二：直接部署 (使用 `systemd`)
这种方式适用于传统的Linux服务器环境。

#### 1. 准备环境
将项目代码部署到服务器，例如 `/opt/solunar-api/`，并安装依赖。

#### 2. 创建 `systemd` 服务文件
创建 `/etc/systemd/system/solunar-api.service`：
```ini
[Unit]
Description=Solunar API Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/solunar-api
ExecStart=/path/to/your/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=5s
Environment="HOME=/var/www" # 确保Skyfield有可写目录

[Install]
WantedBy=multi-user.target
```
*   **注意**: 替换 `User`, `Group` 和 `ExecStart` 中的Python路径。

#### 3. 启动并启用服务
```bash
sudo systemctl daemon-reload
sudo systemctl start solunar-api
sudo systemctl enable solunar-api
```

## 📜 版本历史
*   **V4.2.0 (当前)**
    *   修复日出日落时间在跨时区计算时的日期跳变问题。
    *   修正并新增了月相角度，使月相判断更精确。
*   **V4.1.0**
    *   引入时区转换功能。
*   **V4.0.0**
    *   项目初始化，提供日出日落和基础月相信息。

## 🤝 贡献
欢迎通过提交 Issues 或 Pull Requests 来为本项目贡献。

## 📄 许可
本项目采用 [MIT License](LICENSE)。
