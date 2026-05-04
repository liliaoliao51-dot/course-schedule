/**
 * API 配置
 *
 * 本地开发: VITE_API_BASE=/api，由 vite proxy 转发到 http://127.0.0.1:8000
 * 生产部署: VITE_API_BASE=https://your-railway-url.up.railway.app
 */

const BASE = import.meta.env.VITE_API_BASE || '/api'

async function request(url, options = {}) {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `请求失败 (${res.status})`)
  }

  if (res.status === 204) return null
  return res.json()
}

export const getCourses = () => request('/courses')

export const createCourse = (data) =>
  request('/courses', { method: 'POST', body: JSON.stringify(data) })

export const updateCourse = (id, data) =>
  request(`/courses/${id}`, { method: 'PUT', body: JSON.stringify(data) })

export const deleteCourse = (id) =>
  request(`/courses/${id}`, { method: 'DELETE' })
