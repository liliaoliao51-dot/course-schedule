<template>
  <div class="flex flex-col h-full bg-gray-50">
    <!-- ===== 顶部：周数切换 ===== -->
    <div class="sticky top-0 z-20 bg-white shadow-sm">
      <div class="flex items-center justify-between px-4 py-2">
        <button
          @click="weekNum > 1 && weekNum--"
          :disabled="weekNum <= 1"
          class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 active:bg-gray-200 text-gray-500 disabled:opacity-30 transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <span class="text-base font-semibold text-gray-800 select-none">第 {{ weekNum }} 周</span>
        <button
          @click="weekNum++"
          class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 active:bg-gray-200 text-gray-500 transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
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
          :class="{ 'day-tab--active': activeDay === i + 1 }"
          @click="activeDay = i + 1"
        >
          <span class="day-tab-label">{{ label }}</span>
          <span v-if="isToday(i + 1)" class="day-tab-dot"></span>
        </div>
      </div>
    </div>

    <!-- ===== 课表网格 ===== -->
    <div class="flex-1 overflow-y-auto overflow-x-hidden" ref="gridWrap">
      <div class="schedule-grid">
        <!-- 节次标签（左侧） -->
        <div
          v-for="p in totalPeriods"
          :key="'lbl-' + p"
          class="period-label"
          :style="{ gridRow: p + 1 }"
        >
          {{ p }}
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
          <div class="course-card-room">{{ c.classroom }}</div>
        </div>
      </div>
    </div>

    <!-- ===== 课程详情弹窗（底部抽屉） ===== -->
    <Teleport to="body">
      <Transition name="drawer">
        <div v-if="detail" class="drawer-mask" @click.self="detail = null">
          <div class="drawer-panel">
            <!-- 色条 -->
            <div class="drawer-accent" :style="{ background: colorOf(detail.id) }" />

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
                <div class="drawer-icon drawer-icon--blue">
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
                <div class="drawer-icon drawer-icon--green">
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
                <div class="drawer-icon drawer-icon--amber">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <div class="drawer-row-label">时间</div>
                  <div class="drawer-row-value">
                    {{ dayLabels[detail.day_of_week - 1] }}
                    第{{ detail.start_period }}-{{ detail.start_period + detail.duration - 1 }}节
                  </div>
                </div>
              </div>
            </div>

            <div class="drawer-actions">
              <button
                @click="$emit('edit', detail); detail = null"
                class="drawer-btn drawer-btn--edit"
              >编辑</button>
              <button
                @click="$emit('delete', detail.id); detail = null"
                class="drawer-btn drawer-btn--delete"
              >删除</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  courses: { type: Array, default: () => [] },
})
defineEmits(['edit', 'delete'])

/* ---------- 常量 ---------- */
const dayLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const totalPeriods = 12

const palette = [
  '#0ea5e9', // sky-500
  '#10b981', // emerald-500
  '#8b5cf6', // violet-500
  '#f59e0b', // amber-500
  '#f43f5e', // rose-500
  '#14b8a6', // teal-500
  '#6366f1', // indigo-500
  '#ec4899', // pink-500
]

/* ---------- 状态 ---------- */
const weekNum = ref(1)
const activeDay = ref(((new Date().getDay() + 6) % 7) + 1) // 1=周一
const detail = ref(null)
const gridWrap = ref(null)

/* ---------- 工具函数 ---------- */
function isToday(d) {
  return ((new Date().getDay() + 6) % 7) + 1 === d
}

function colorOf(id) {
  return palette[(id - 1) % palette.length]
}

function cardStyle(c) {
  return {
    gridColumn: c.day_of_week + 1,
    gridRow: `${c.start_period + 1} / span ${c.duration}`,
    background: colorOf(c.id),
  }
}

function openDetail(c) {
  detail.value = c
}
</script>

<style scoped>
/* ========== 星期标签行 ========== */
.day-tabs {
  display: grid;
  grid-template-columns: 2.5rem repeat(7, 1fr);
  border-top: 1px solid #f3f4f6;
}
.day-tabs-gutter {
  background: #fafafa;
}
.day-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 0 4px;
  font-size: 12px;
  font-weight: 500;
  color: #9ca3af;
  cursor: pointer;
  position: relative;
  transition: color 0.15s;
  user-select: none;
}
.day-tab:active {
  background: #f9fafb;
}
.day-tab--active {
  color: #2563eb;
}
.day-tab--active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25%;
  right: 25%;
  height: 2px;
  border-radius: 1px;
  background: #2563eb;
}
.day-tab-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #2563eb;
  margin-top: 2px;
}

/* ========== 课表网格 ========== */
.schedule-grid {
  display: grid;
  grid-template-columns: 2.5rem repeat(7, 1fr);
  /* 第一行是表头高度（隐藏，靠 sticky 顶栏替代），后面 12 行是节次 */
  grid-template-rows: 0px repeat(12, var(--cell-h, 4rem));
  width: 100%;
}

@media (min-width: 640px) {
  .schedule-grid {
    --cell-h: 3.25rem;
  }
}

.period-label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #9ca3af;
  background: #fafafa;
  border-bottom: 1px solid #f3f4f6;
  user-select: none;
}

.grid-cell {
  border-bottom: 1px solid #f3f4f6;
  border-right: 1px solid #f9fafb;
}
.grid-cell--today {
  background: #eff6ff;
}

/* ========== 课程卡片 ========== */
.course-card {
  margin: 2px;
  padding: 4px 6px;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 1;
  transition: transform 0.1s, box-shadow 0.1s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}
.course-card:active {
  transform: scale(0.96);
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
}
.course-card-name {
  font-size: 11px;
  font-weight: 600;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.course-card-room {
  font-size: 10px;
  opacity: 0.8;
  margin-top: 1px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========== 底部抽屉 ========== */
.drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
@media (min-width: 640px) {
  .drawer-mask {
    align-items: center;
  }
}
.drawer-panel {
  position: relative;
  background: #fff;
  width: 100%;
  max-width: 24rem;
  border-radius: 1.25rem 1.25rem 0 0;
  padding: 1.5rem 1.5rem 2rem;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}
@media (min-width: 640px) {
  .drawer-panel {
    border-radius: 1.25rem;
  }
}
.drawer-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.drawer-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}
.drawer-sub {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}
.drawer-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #9ca3af;
  transition: background 0.15s;
}
.drawer-close:hover {
  background: #f3f4f6;
}

.drawer-body {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.drawer-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}
.drawer-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.drawer-icon--blue {
  background: #eff6ff;
  color: #3b82f6;
}
.drawer-icon--green {
  background: #ecfdf5;
  color: #10b981;
}
.drawer-icon--amber {
  background: #fffbeb;
  color: #f59e0b;
}
.drawer-row-label {
  font-size: 11px;
  color: #9ca3af;
}
.drawer-row-value {
  font-weight: 600;
  color: #1f2937;
}

.drawer-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}
.drawer-btn {
  flex: 1;
  padding: 10px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.15s;
}
.drawer-btn--edit {
  background: #f3f4f6;
  color: #374151;
}
.drawer-btn--edit:active {
  background: #e5e7eb;
}
.drawer-btn--delete {
  background: #fef2f2;
  color: #dc2626;
}
.drawer-btn--delete:active {
  background: #fee2e2;
}

/* ========== 抽屉动画 ========== */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.25s ease;
}
.drawer-enter-active .drawer-panel,
.drawer-leave-active .drawer-panel {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
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
    transform: translateY(24px) scale(0.96);
  }
}
</style>
