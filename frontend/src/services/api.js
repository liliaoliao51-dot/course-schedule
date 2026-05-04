/**
 * API 配置说明：
 *
 * 本地开发:
 *   - VITE_API_BASE=/api（默认值）
 *   - Vite 代理会把 /api 转发到 http://127.0.0.1:8000
 *   - 需要先启动后端: cd backend && uvicorn main:app --reload
 *
 * Vercel 部署:
 *   - 在 Vercel 环境变量中设置 VITE_API_BASE=https://your-backend.up.railway.app
 *   - 或者使用 vercel.json 中的 rewrites 代理（当前配置）
 *
 * Railway 部署后端:
 *   - 部署 backend 文件夹到 Railway
 *   - Railway 会自动设置 DATABASE_URL（PostgreSQL）
 *   - 获取 Railway 分配的域名，更新 Vercel 环境变量
 */

// 获取 API 基础地址
// 优先使用环境变量，本地开发默认用 /api（由 vite proxy 转发）
const getBaseUrl = () => {
  const envBase = import.meta.env.VITE_API_BASE
  if (envBase) return envBase

  // 生产环境（Vercel）使用相对路径 /api，由 vercel.json rewrites 代理
  // 开发环境也使用 /api，由 vite proxy 转发
  return '/api'
}

const BASE = getBaseUrl()

async function request(url, options = {}) {
  const fullUrl = BASE + url

  try {
    const res = await fetch(fullUrl, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }))
      throw new Error(err.detail || `请求失败 (${res.status})`)
    }

    if (res.status === 204) return null
    return res.json()
  } catch (error) {
    // 网络错误时提供更友好的提示
    if (error.message === 'Failed to fetch') {
      throw new Error('无法连接到服务器，请检查后端是否启动')
    }
    throw error
  }
}

export const getCourses = () => request('/courses')

export const createCourse = (data) =>
  request('/courses', { method: 'POST', body: JSON.stringify(data) })

export const updateCourse = (id, data) =>
  request(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) })

export const deleteCourse = (id) =>
  request(`/courses/${id}`, { method: 'DELETE' })
