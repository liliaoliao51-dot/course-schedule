<template>
  <div class="fixed inset-0 bg-black/40 flex items-end sm:items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white w-full sm:max-w-md rounded-t-2xl sm:rounded-2xl p-6 space-y-4 max-h-[90vh] overflow-y-auto">
      <h2 class="text-lg font-semibold text-gray-900">
        {{ isEdit ? '编辑课程' : '添加课程' }}
      </h2>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">课程名</label>
          <input
            v-model="form.name"
            required
            class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="例如：高等数学"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">教室</label>
          <input
            v-model="form.classroom"
            required
            class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="例如：教学楼A-301"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">老师</label>
          <input
            v-model="form.teacher"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="例如：张老师"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">星期</label>
          <select
            v-model.number="form.day_of_week"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          >
            <option v-for="d in 7" :key="d" :value="d">{{ dayNames[d - 1] }}</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">起始节次</label>
            <input
              v-model.number="form.start_period"
              type="number"
              min="1"
              max="20"
              required
              class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">持续节次</label>
            <input
              v-model.number="form.duration"
              type="number"
              min="1"
              max="10"
              required
              class="w-full rounded-lg border-gray-300 border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button
            type="submit"
            class="flex-1 bg-blue-600 text-white rounded-lg py-2.5 font-medium hover:bg-blue-700 active:bg-blue-800 transition"
          >
            {{ isEdit ? '保存' : '添加' }}
          </button>
          <button
            v-if="isEdit"
            type="button"
            @click="$emit('delete', course.id)"
            class="px-4 bg-red-50 text-red-600 rounded-lg py-2.5 font-medium hover:bg-red-100 transition"
          >
            删除
          </button>
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 bg-gray-100 text-gray-700 rounded-lg py-2.5 font-medium hover:bg-gray-200 transition"
          >
            取消
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  course: { type: Object, default: null },
})
const emit = defineEmits(['save', 'delete', 'close'])

const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const isEdit = !!props.course

const form = reactive({
  name: props.course?.name || '',
  classroom: props.course?.classroom || '',
  teacher: props.course?.teacher || '',
  day_of_week: props.course?.day_of_week || 1,
  start_period: props.course?.start_period || 1,
  duration: props.course?.duration || 2,
})

function handleSubmit() {
  emit('save', { ...form })
}
</script>
