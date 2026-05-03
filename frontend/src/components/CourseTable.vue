<template>
  <div class="bg-white rounded-xl shadow-sm overflow-hidden">
    <!-- 移动端：卡片布局 -->
    <div class="sm:hidden">
      <div v-if="courses.length === 0" class="p-8 text-center text-gray-400">
        暂无课程，点击右上角添加
      </div>
      <div v-for="day in 7" :key="day" v-show="getDayCourses(day).length > 0">
        <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-600">
          {{ dayNames[day - 1] }}
        </div>
        <div
          v-for="course in getDayCourses(day)"
          :key="course.id"
          class="px-4 py-3 border-b border-gray-100 flex items-center justify-between active:bg-gray-50"
          @click="$emit('edit', course)"
        >
          <div>
            <div class="font-medium text-gray-900">{{ course.name }}</div>
            <div class="text-sm text-gray-500">
              {{ course.classroom }} · 第{{ course.start_period }}-{{ course.start_period + course.duration - 1 }}节
            </div>
          </div>
          <div
            class="w-3 h-3 rounded-full flex-shrink-0"
            :class="colorMap[(course.id - 1) % colorMap.length]"
          ></div>
        </div>
      </div>
    </div>

    <!-- 桌面端：表格布局 -->
    <div class="hidden sm:block overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 text-gray-600">
            <th class="px-3 py-2 text-left font-medium w-16">节次</th>
            <th v-for="day in 7" :key="day" class="px-2 py-2 text-center font-medium min-w-[80px]">
              {{ dayNames[day - 1] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="period in maxPeriod" :key="period" class="border-t border-gray-100">
            <td class="px-3 py-2 text-gray-500 text-center">{{ period }}</td>
            <td
              v-for="day in 7"
              :key="day"
              class="px-1 py-1 text-center border-l border-gray-50 relative"
              :rowspan="getCellRowspan(day, period)"
              v-show="!isCoveredCell(day, period)"
            >
              <div
                v-if="getCourseAt(day, period)"
                class="rounded-lg px-2 py-1.5 text-white text-xs cursor-pointer hover:opacity-90 transition"
                :class="colorMap[(getCourseAt(day, period).id - 1) % colorMap.length]"
                @click="$emit('edit', getCourseAt(day, period))"
              >
                <div class="font-medium">{{ getCourseAt(day, period).name }}</div>
                <div class="opacity-80 text-[11px]">{{ getCourseAt(day, period).classroom }}</div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  courses: { type: Array, default: () => [] },
})
defineEmits(['edit'])

const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const colorMap = [
  'bg-blue-500', 'bg-emerald-500', 'bg-violet-500', 'bg-amber-500',
  'bg-rose-500', 'bg-cyan-500', 'bg-indigo-500', 'bg-pink-500',
]

const maxPeriod = 12

function getDayCourses(day) {
  return props.courses.filter(c => c.day_of_week === day)
}

function getCourseAt(day, period) {
  return props.courses.find(
    c => c.day_of_week === day && period >= c.start_period && period < c.start_period + c.duration
  )
}

function getCellRowspan(day, period) {
  const course = getCourseAt(day, period)
  if (course && course.start_period === period) {
    return course.duration
  }
  return 1
}

function isCoveredCell(day, period) {
  return props.courses.some(
    c => c.day_of_week === day && period > c.start_period && period < c.start_period + c.duration
  )
}
</script>
