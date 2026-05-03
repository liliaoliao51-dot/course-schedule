<template>
  <div class="flex flex-col h-full week-root">
    <!-- ===== 顶部：周数切换 ===== -->
    <div class="sticky top-0 z-20 week-header">
      <div class="flex items-center justify-between px-5 pt-3 pb-1">
        <button
          @click="changeWeek(-1)"
          :disabled="weekNum <= 1"
          class="nav-btn"
        >
          <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="week-title-wrap">
          <Transition name="week-fade" mode="out-in">
            <span :key="weekNum" class="week-title">第 {{ weekNum }} 周</span>
          </Transition>
        </div>
        <button
          @click="changeWeek(1)"
          class="nav-btn"
        >
          <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- 星期标签行 -->
      <div class="day-tabs">
        <div class="day-tabs-gutter"></div>
        <div
          v-for="(label, i) in dayLabels"
          :key="i"
          class="day-tab"
          :class="{ 'day-tab--active': activeDay === i + 1, 'day-tab--today': isToday(i + 1) }"
          @click="activeDay = i + 1"
        >
          <span class="day-tab-week">{{ shortLabels[i] }}</span>
          <span v-if="isToday(i + 1)" class="day-tab-today-badge">今</span>
        </div>
      </div>
    </div>

    <!-- ===== 课表网格 ===== -->
    <div class="flex-1 overflow-y-auto overflow-x-hidden px-1 pt-1" ref="gridWrap">
      <Transition name="grid-fade" mode="out-in">
        <div :key="weekNum" class="schedule-grid">
          <!-- 节次标签（左侧） -->
          <div
            v-for="p in totalPeriods"
            :key="'lbl-' + p"
            class="period-label"
            :style="{ gridRow: p + 1 }"
          >
            <span class="period-num">{{ p }}</span>
            <span class="period-time">{{ defaultPeriodTime(p) }}</span>
          </div>

          <!-- 背景格子 -->
          <template v-for="p in totalPeriods" :key="'row-' + p">
            <div
              v-for="d in 7"
              :key="'cell-' + d + '-' + p"
              class="grid-cell"
              :class="{ 'grid-cell--today': isToday(d) }"
              :style="{ gridColumn: d + 1, gridRow: p + 1 }"
            />
          </template>

          <!-- 课程卡片 -->
          <div
            v-for="c in courses"
            :key="c.id"
            class="course-card"
            :style="cardStyle(c)"
            @click="openDetail(c)"
          >
            <div class="course-card-name">{{ c.name }}</div>
            <div class="course-card-info">
              <svg class="w-[10px] h-[10px] opacity-60 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0l-4.243-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span class="truncate">{{ c.classroom }}</span>
            </div>
            <div class="course-card-time">
              {{ courseTimeDisplay(c) }}
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ===== 课程详情弹窗（底部抽屉） ===== -->
    <Teleport to="body">
      <Transition name="drawer">
        <div v-if="detail" class="drawer-mask" @click.self="detail = null">
          <div class="drawer-panel">
            <div class="drawer-accent" :style="{ background: morandiColor(detail.id, 0.7) }" />
            <div class="drawer-handle" />

            <div class="drawer-header">
              <div>
                <h3 class="drawer-title">{{ detail.name }}</h3>
                <p class="drawer-sub">
                  {{ dayLabels[detail.day_of_week - 1] }}
                  第{{ detail.start_period }}-{{ detail.start_period + detail.duration - 1 }}节
                </p>
              </div>
              <button @click="detail = null" class="drawer-close">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div class="drawer-body">
              <div class="drawer-row">
                <div class="drawer-icon" :style="iconBg(detail.id, 'loc')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0l-4.243-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <div class="drawer-row-label">教室</div>
                  <div class="drawer-row-value">{{ detail.classroom }}</div>
                </div>
              </div>

              <div class="drawer-row">
                <div class="drawer-icon" :style="iconBg(detail.id, 'person')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <div class="drawer-row-label">老师</div>
                  <div class="drawer-row-value">{{ detail.teacher || '未设置' }}</div>
                </div>
              </div>

              <div class="drawer-row">
                <div class="drawer-icon" :style="iconBg(detail.id, 'time')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <div class="drawer-row-label">时间</div>
                  <div class="drawer-row-value">
                    {{ dayLabels[detail.day_of_week - 1] }}
                    第{{ detail.start_period }}-{{ detail.start_period + detail.duration - 1 }}节
                    <span class="drawer-row-time">{{ courseTimeDisplay(detail) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="drawer-actions">
              <button @click="$emit('edit', detail); detail = null" class="drawer-btn drawer-btn--edit">编辑</button>
              <button @click="$emit('delete', detail.id); detail = null" class="drawer-btn drawer-btn--delete">删除</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  courses: { type: Array, default: () => [] },
})
defineEmits(['edit', 'delete'])

/* ---------- 常量 ---------- */
const dayLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const shortLabels = ['一', '二', '三', '四', '五', '六', '日']
const totalPeriods = 12

// 默认节次时间映射（中国高校常见作息）
const defaultTimes = {
  1:  { start: '08:00', end: '08:45' },
  2:  { start: '08:55', end: '09:40' },
  3:  { start: '10:00', end: '10:45' },
  4:  { start: '10:55', end: '11:40' },
  5:  { start: '14:00', end: '14:45' },
  6:  { start: '14:55', end: '15:40' },
  7:  { start: '16:00', end: '16:45' },
  8:  { start: '16:55', end: '17:40' },
  9:  { start: '19:00', end: '19:45' },
  10: { start: '19:55', end: '20:40' },
  11: { start: '20:50', end: '21:35' },
  12: { start: '21:45', end: '22:30' },
}

// 莫兰迪色系 — 低饱和度、高级灰调
const morandi = [
  { base: '#8fa3a0', light: '#b5c7c4' },  // 雾松绿
  { base: '#b5838d', light: '#d4a5ad' },  // 玫瑰灰
  { base: '#8a9eb5', light: '#adc1d6' },  // 静谧蓝
  { base: '#c0a888', light: '#d6c7ad' },  // 暖杏驼
  { base: '#9a8cb5', light: '#bfb3d4' },  // 淡藤紫
  { base: '#7ea3a3', light: '#a5c4c4' },  // 雾霭青
  { base: '#b59f8a', light: '#d4bfb0' },  // 摩卡棕
  { base: '#8da09a', light: '#b0c2bc' },  // 烟灰绿
]

/* ---------- 状态 ---------- */
const weekNum = ref(1)
const activeDay = ref(((new Date().getDay() + 6) % 7) + 1)
const detail = ref(null)
const gridWrap = ref(null)

/* ---------- 工具函数 ---------- */
function isToday(d) {
  return ((new Date().getDay() + 6) % 7) + 1 === d
}

function changeWeek(delta) {
  const next = weekNum.value + delta
  if (next >= 1) weekNum.value = next
}

function getMorandi(id) {
  return morandi[(id - 1) % morandi.length]
}

function morandiColor(id, alpha = 1) {
  const c = getMorandi(id)
  if (alpha >= 1) return c.base
  // hex → rgba
  const r = parseInt(c.base.slice(1, 3), 16)
  const g = parseInt(c.base.slice(3, 5), 16)
  const b = parseInt(c.base.slice(5, 7), 16)
  return `rgba(${r},${g},${b},${alpha})`
}

function cardStyle(c) {
  return {
    gridColumn: c.day_of_week + 1,
    gridRow: `${c.start_period + 1} / span ${c.duration}`,
    '--card-accent': morandiColor(c.id, 0.85),
    '--card-glow': morandiColor(c.id, 0.25),
  }
}

function iconBg(id, variant) {
  const m = getMorandi(id)
  const bgMap = { loc: 0.12, person: 0.10, time: 0.10 }
  const bg = bgMap[variant] || 0.10
  const r = parseInt(m.base.slice(1, 3), 16)
  const g = parseInt(m.base.slice(3, 5), 16)
  const b = parseInt(m.base.slice(5, 7), 16)
  return {
    background: `rgba(${r},${g},${b},${bg})`,
    color: m.base,
  }
}

function defaultPeriodTime(p) {
  const t = defaultTimes[p]
  return t ? t.start : ''
}

function courseTimeDisplay(c) {
  // 优先用课程自带时间，否则用默认映射
  if (c.start_time && c.end_time) {
    return `${c.start_time} - ${c.end_time}`
  }
  const t = defaultTimes[c.start_period]
  if (t) return `${t.start} - ${t.end}`
  return ''
}

function openDetail(c) {
  detail.value = c
}
</script>

<style scoped>
/* ===== 根背景 ===== */
.week-root {
  background: linear-gradient(180deg, #f5f3f0 0%, #eceae6 100%);
}

/* ===== 顶部栏（磨砂玻璃） ===== */
.week-header {
  background: rgba(245, 243, 240, 0.82);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.week-title-wrap {
  min-width: 5rem;
  text-align: center;
}
.week-title {
  font-size: 16px;
  font-weight: 700;
  color: #3d3d3d;
  letter-spacing: 0.5px;
}

/* 周数切换淡入淡出 */
.week-fade-enter-active,
.week-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.week-fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.week-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.nav-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #7a7a7a;
  transition: background 0.15s, color 0.15s;
}
.nav-btn:hover { background: rgba(0,0,0,0.04); }
.nav-btn:active { background: rgba(0,0,0,0.07); color: #3d3d3d; }
.nav-btn:disabled { opacity: 0.25; pointer-events: none; }

/* ===== 星期标签行 ===== */
.day-tabs {
  display: grid;
  grid-template-columns: 2.25rem repeat(7, 1fr);
}
.day-tabs-gutter { /* 占位 */ }

.day-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0 6px;
  cursor: pointer;
  user-select: none;
  position: relative;
  transition: color 0.2s;
}
.day-tab-week {
  font-size: 12px;
  font-weight: 500;
  color: #a0a0a0;
  transition: color 0.2s, font-weight 0.2s;
}
.day-tab--active .day-tab-week {
  color: #3d3d3d;
  font-weight: 700;
}
.day-tab--today .day-tab-week {
  color: #5a7a72;
}

.day-tab-today-badge {
  margin-top: 2px;
  font-size: 9px;
  font-weight: 700;
  color: #fff;
  background: #8fa3a0;
  border-radius: 6px;
  padding: 0 5px;
  line-height: 16px;
}

/* ===== 课表网格 ===== */
.schedule-grid {
  display: grid;
  grid-template-columns: 2.25rem repeat(7, 1fr);
  grid-template-rows: 0px repeat(12, var(--cell-h, 4.2rem));
  width: 100%;
  gap: 3px;
}
@media (min-width: 640px) {
  .schedule-grid { --cell-h: 3.25rem; gap: 4px; }
}

.period-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  user-select: none;
}
.period-num {
  font-size: 11px;
  font-weight: 600;
  color: #a0a0a0;
}
.period-time {
  font-size: 8px;
  font-weight: 400;
  color: #c0c0c0;
  letter-spacing: 0.2px;
}

.grid-cell {
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.45);
  transition: background 0.3s;
}
.grid-cell--today {
  background: rgba(143, 163, 160, 0.10);
  box-shadow: inset 0 0 0 1.5px rgba(143, 163, 160, 0.18);
}

/* ===== 网格切换淡入 ===== */
.grid-fade-enter-active,
.grid-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.grid-fade-enter-from {
  opacity: 0;
  transform: scale(0.98);
}
.grid-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}

/* ===== 课程卡片（玻璃拟态） ===== */
.course-card {
  margin: 2px;
  padding: 6px 8px;
  border-radius: 14px;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 1;
  position: relative;

  /* 莫兰迪底色 + 玻璃质感 */
  background: var(--card-accent);
  backdrop-filter: blur(8px) saturate(1.2);
  -webkit-backdrop-filter: blur(8px) saturate(1.2);

  color: #fff;
  box-shadow:
    0 2px 8px var(--card-glow),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.12);

  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s;
}
.course-card:active {
  transform: scale(0.94);
  box-shadow: 0 1px 4px var(--card-glow);
}
.course-card-name {
  font-size: 11px;
  font-weight: 700;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: 0.2px;
}
.course-card-info {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 9px;
  opacity: 0.8;
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.course-card-time {
  font-size: 8px;
  opacity: 0.6;
  margin-top: 1px;
  letter-spacing: 0.2px;
}

/* ===== 底部抽屉 ===== */
.drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: rgba(60, 60, 60, 0.25);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
@media (min-width: 640px) {
  .drawer-mask { align-items: center; }
}

.drawer-panel {
  position: relative;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px) saturate(1.5);
  -webkit-backdrop-filter: blur(20px) saturate(1.5);
  width: 100%;
  max-width: 24rem;
  border-radius: 24px 24px 0 0;
  padding: 12px 24px calc(env(safe-area-inset-bottom, 0px) + 24px);
  box-shadow: 0 -4px 32px rgba(0, 0, 0, 0.10);
  overflow: hidden;
}
@media (min-width: 640px) {
  .drawer-panel { border-radius: 24px; padding-bottom: 24px; }
}

.drawer-handle {
  width: 36px;
  height: 4px;
  border-radius: 2px;
  background: #d5d5d5;
  margin: 0 auto 16px;
}

.drawer-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.drawer-title {
  font-size: 20px;
  font-weight: 800;
  color: #2d2d2d;
  letter-spacing: -0.3px;
}
.drawer-sub {
  font-size: 13px;
  color: #999;
  margin-top: 3px;
}
.drawer-close {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #aaa;
  transition: background 0.15s;
}
.drawer-close:hover { background: rgba(0,0,0,0.04); }

.drawer-body {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.drawer-row {
  display: flex;
  align-items: center;
  gap: 14px;
}
.drawer-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.drawer-row-label {
  font-size: 11px;
  color: #aaa;
  margin-bottom: 1px;
}
.drawer-row-value {
  font-size: 15px;
  font-weight: 600;
  color: #2d2d2d;
}
.drawer-row-time {
  display: inline-block;
  font-size: 12px;
  font-weight: 400;
  color: #999;
  margin-left: 6px;
}

.drawer-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
}
.drawer-btn {
  flex: 1;
  padding: 12px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.15s, transform 0.1s;
}
.drawer-btn:active { transform: scale(0.97); }
.drawer-btn--edit {
  background: #f0eeeb;
  color: #3d3d3d;
}
.drawer-btn--edit:hover { background: #e8e6e2; }
.drawer-btn--delete {
  background: rgba(181, 131, 141, 0.12);
  color: #b5838d;
}
.drawer-btn--delete:hover { background: rgba(181, 131, 141, 0.20); }

/* ===== 抽屉动画 ===== */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.3s ease;
}
.drawer-enter-active .drawer-panel,
.drawer-leave-active .drawer-panel {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}
.drawer-enter-from .drawer-panel,
.drawer-leave-to .drawer-panel {
  transform: translateY(100%);
}
@media (min-width: 640px) {
  .drawer-enter-from .drawer-panel,
  .drawer-leave-to .drawer-panel {
    transform: translateY(20px) scale(0.96);
  }
}
</style>
