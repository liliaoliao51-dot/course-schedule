# 部署指南

## 本地开发

### 1. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动后端（开发模式，自动重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 http://127.0.0.1:8000 运行

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动前端（开发模式）
npm run dev
```

前端将在 http://localhost:5173 运行

### 3. 访问应用

打开浏览器访问 http://localhost:5173

Vite 会自动把 `/api` 请求代理到后端 http://127.0.0.1:8000

---

## 部署到 Vercel + Railway

### 架构说明

```
┌─────────────────┐      ┌─────────────────┐
│     Vercel      │      │    Railway      │
│   (前端 Vue)    │ ──── │  (后端 FastAPI) │
│                 │      │                 │
│  your-app.      │      │  your-project.  │
│  vercel.app     │      │  up.railway.app │
└─────────────────┘      └─────────────────┘
```

### 步骤 1: 部署后端到 Railway

1. 注册 [Railway](https://railway.app) 账号

2. 创建新项目 → 从 GitHub 部署

3. 选择 `backend` 文件夹作为根目录

4. Railway 会自动：
   - 检测到 `requirements.txt` 并安装依赖
   - 使用 `Procfile` 或 `railway.json` 启动服务
   - 分配一个域名（如 `your-project.up.railway.app`）

5. 添加 PostgreSQL 数据库：
   - 在 Railway 项目中点击 "New" → "Database" → "PostgreSQL"
   - Railway 会自动设置 `DATABASE_URL` 环境变量

6. 记录 Railway 分配的域名（后续步骤需要）

### 步骤 2: 部署前端到 Vercel

1. 注册 [Vercel](https://vercel.com) 账号

2. 导入 GitHub 仓库

3. 配置项目：
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. 设置环境变量：
   - **Name**: `VITE_API_BASE`
   - **Value**: `https://your-project.up.railway.app`（替换为 Railway 实际域名）

5. 点击 "Deploy"

### 步骤 3: 更新 vercel.json（可选）

如果不想使用环境变量，可以在 `vercel.json` 中配置代理：

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://your-project.up.railway.app/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

这样前端代码不需要任何修改，所有 `/api` 请求会自动代理到 Railway。

---

## 数据库管理

### 本地数据库重置

如果本地数据库出现问题（如字段缺失），可以重置数据库：

```bash
cd backend

# 方式 1: 使用重置脚本（推荐）
python reset_db.py --confirm

# 方式 2: 手动删除并重启
rm courses.db
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Railway 数据库迁移

如果 Railway 上的数据库需要添加新字段（如 `start_time`、`end_time`），有两种方式：

#### 方式 1: 使用迁移脚本（推荐，保留数据）

```bash
# 在 Railway 的 Shell 中运行，或本地连接 Railway 数据库后运行
python migrate_db.py
```

#### 方式 2: 重置数据库（会丢失所有数据）

```bash
# 在 Railway 的 Shell 中运行
python reset_db.py --confirm
```

或者在 Railway 控制台中：
1. 删除 PostgreSQL 数据库服务
2. 重新添加 PostgreSQL 数据库
3. 重新部署后端服务

### 数据库字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id` | Integer | 主键，自增 |
| `name` | String | 课程名 |
| `classroom` | String | 教室 |
| `day_of_week` | Integer | 周几 (1=周一, 7=周日) |
| `start_period` | Integer | 起始节次 |
| `duration` | Integer | 持续节次 |
| `teacher` | String | 授课老师（可选） |
| `start_time` | String | 开始时间，如 '08:00'（可选） |
| `end_time` | String | 结束时间，如 '09:40'（可选） |

---

## 常见问题

### Q: 本地开发时出现 `ECONNREFUSED 127.0.0.1:8000`

**原因**: 后端没有启动

**解决**:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Q: 本地添加课程报 500 错误

**原因**: 数据库表结构不匹配，缺少 `start_time` 或 `end_time` 字段

**解决**:
```bash
cd backend
python reset_db.py --confirm
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Q: Vercel 部署后页面空白或 API 请求失败

**原因**: `VITE_API_BASE` 环境变量未设置或 Railway 后端未启动

**解决**:
1. 检查 Railway 后端是否正常运行（访问 `https://your-project.up.railway.app/`）
2. 在 Vercel 项目设置中确认 `VITE_API_BASE` 环境变量已正确设置
3. 重新部署 Vercel 项目

### Q: Railway 部署失败

**原因**: 可能是 `requirements.txt` 缺少依赖或 Python 版本不兼容

**解决**:
1. 检查 Railway 构建日志
2. 确保 `requirements.txt` 包含所有依赖
3. 在 Railway 设置中指定 Python 版本：`PYTHON_VERSION=3.11`

---

## 环境变量参考

### 后端 (Railway)

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DATABASE_URL` | 数据库连接地址 | `postgresql://user:pass@host:5432/db` |
| `ALLOWED_ORIGINS` | 允许的前端域名（逗号分隔） | `https://your-app.vercel.app` |

### 前端 (Vercel)

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `VITE_API_BASE` | 后端 API 地址 | `https://your-project.up.railway.app` |
