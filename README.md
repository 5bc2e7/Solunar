# Solunar API

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-05998b.svg)](https://fastapi.tiangolo.com/)
[![Powered by](https://img.shields.io/badge/Powered%20by-Skyfield-orange.svg)](https://rhodesmill.org/skyfield/)
[![Docker](https://img.shields.io/badge/Docker-Optimized-blue.svg?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Solunar API** 是一个快速、轻量的API服务，旨在提供精确的太阳和月球天文事件信息。它基于高性能天文学库 [Skyfield](https://rhodesmill.org/skyfield/) 构建，并支持灵活的时区转换，确保数据符合用户所在地的实际情况。

---

## ✨ 主要特性

*   **太阳事件**：为全球任意经纬度计算精确的日出、日落和正午时间。
*   **月球事件**：为全球任意经纬度计算精确的月出、月落和中天时间。
*   **月相信息**：提供基于中天时刻计算的精确月相，包括照亮百分比和直观的月相名称。
*   **时区感知**：所有时间数据均可按指定的 [IANA 时区名称](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 输出。
*   **Docker 优化**：采用多阶段构建和 `.dockerignore`，实现最小化的生产镜像体积。
*   **易于部署**：提供包含健康检查的 `docker-compose.yml`，实现一键启动。

## 🚀 快速启动

### 1. 先决条件
*   Docker 和 Docker Compose

### 2. 获取项目
```bash
git clone https://github.com/5bc2e7/SolunarAPI.git
cd SolunarAPI
```

### 3. 启动服务
这是启动服务最简单、最可靠的方式。`--build` 参数会确保使用最新的代码和依赖构建镜像。

```bash
docker compose up --build -d
```
服务将在 `http://localhost:8000` 上可用。

服务启动后，您可以访问以下地址查看自动生成的交互式 API 文档：

*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

---

## 📖 API 使用指南

### `GET /api/sun`
计算指定地点的日出、日落和正午时间。

#### 查询参数
| 名称         | 类型     | 必需 | 默认 | 描述                                         | 示例              |
| :----------- | :------- | :--- | :--- | :------------------------------------------- | :---------------- |
| `lat`        | `float`  | 是   | -    | 纬度 (`-90` to `90`)                         | `39.9` (北京)     |
| `lon`        | `float`  | 是   | -    | 经度 (`-180` to `180`)                       | `116.4` (北京)    |
| `target_date`| `string` | 否   | 今天 | 目标日期 (格式: `YYYY-MM-DD`)                | `2025-07-10`      |
| `tz`         | `string` | 否   | `UTC`| 输出时区 (IANA TZ database)                  | `Asia/Shanghai`   |

#### 示例请求
```bash
curl "http://localhost:8000/api/sun?lat=39.9&lon=116.4&target_date=2025-07-10&tz=Asia/Shanghai"
```

---

### `GET /api/moon`
计算指定地点的月出、月落、中天时间，并提供当日的月相信息。

#### 查询参数
| 名称         | 类型     | 必需 | 默认 | 描述                                         | 示例              |
| :----------- | :------- | :--- | :--- | :------------------------------------------- | :---------------- |
| `lat`        | `float`  | 是   | -    | 纬度 (`-90` to `90`)                         | `21.91` (南海)    |
| `lon`        | `float`  | 是   | -    | 经度 (`-180` to `180`)                       | `114.29` (南海)   |
| `target_date`| `string` | 否   | 今天 | 目标日期 (格式: `YYYY-MM-DD`)                | `2025-07-11`      |
| `tz`         | `string` | 否   | `UTC`| 输出时区 (IANA TZ database)                  | `Asia/Shanghai`   |

#### 示例请求
```bash
curl "http://localhost:8000/api/moon?lat=21.91&lon=114.29&target_date=2025-07-11&tz=Asia/Shanghai"
```

#### 示例响应
```json
{
  "location": {
    "latitude": 21.91,
    "longitude": 114.29
  },
  "date": "2025-07-11",
  "timezone": "Asia/Shanghai",
  "times": {
    "moonrise": "2025-07-11T19:48:23+08:00",
    "moontransit": "2025-07-11T00:21:48+08:00",
    "moonset": "2025-07-11T05:45:43+08:00"
  },
  "phase_info_at_transit": {
    "timestamp_for_phase_calc": "2025-07-11T00:21:48+08:00",
    "sun_moon_earth_angle_degrees": 4.99,
    "moon_phase_orbital_degrees": 177.9,
    "illumination_percent": 99.81,
    "phase_name": "满月 (Full Moon)"
  }
}
```
**注意**: 月相信息 (`phase_info_at_transit`) 优先使用当天月球中天时刻计算。若当天无中天事件，则自动使用 UTC 中午12点作为基准。

---

## 🐳 部署与配置

本项目推荐使用 **Docker Compose** 进行部署。

### `docker-compose.yml`
项目根目录下的 `docker-compose.yml` 文件已为您配置好一切：

```yaml
services:
  solunar-api:
    build: .
    container_name: solunar-api
    ports:
      - "8000:8000"
    volumes:
      # 将星历数据持久化到命名卷，避免重复下载
      - skyfield_data:/home/appuser/.skyfield
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  skyfield_data:
    driver: local
```

### 反向代理
在生产环境中，强烈建议在 API 前配置 `Nginx` 或 `Caddy` 等反向代理，以提供 HTTPS、负载均衡和安全加固。

---

## 📜 版本历史
*   **V5.0.0 (当前)**
    *   **功能增强**: `/api/moon` 现已支持计算月出、月落和中天时间。
    *   **Docker 优化**: 采用多阶段构建和 `.dockerignore`，将镜像体积从 `425MB` 优化至 `~230MB`。
    *   **部署优化**: 更新 `docker-compose.yml`，增加健康检查并修正数据卷路径。
    *   **文档更新**: 全面重写 `README.md` 以反映最新功能和最佳实践。
*   **V4.2.0**
    *   修复日出日落时间在跨时区计算时的日期跳变问题。
    *   修正并新增了月相角度，使月相判断更精确。

## 🤝 贡献
欢迎通过提交 Issues 或 Pull Requests 来为本项目贡献。

## 📄 许可
本项目采用 [MIT License](LICENSE)。
