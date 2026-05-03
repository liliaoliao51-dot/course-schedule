<template>
  <div class="form-mask" @click.self="$emit('close')">
    <div class="form-panel">
      <div class="form-handle" />
      <h2 class="form-title">{{ isEdit ? '编辑课程' : '添加课程' }}</h2>

      <form @submit.prevent="handleSubmit" class="form-body">
        <div>
          <label class="form-label">课程名</label>
          <input v-model="form.name" required class="form-input" placeholder="例如：高等数学" />
        </div>

        <div>
          <label class="form-label">教室</label>
          <input v-model="form.classroom" required class="form-input" placeholder="例如：教学楼A-301" />
        </div>

        <div>
          <label class="form-label">老师</label>
          <input v-model="form.teacher" class="form-input" placeholder="例如：张老师" />
        </div>

        <div>
          <label class="form-label">星期</label>
          <select v-model.number="form.day_of_week" class="form-input">
            <option v-for="d in 7" :key="d" :value="d">{{ dayNames[d - 1] }}</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="form-label">起始节次</label>
            <input v-model.number="form.start_period" type="number" min="1" max="20" required class="form-input" />
          </div>
          <div>
            <label class="form-label">持续节次</label>
            <input v-model.number="form.duration" type="number" min="1" max="10" required class="form-input" />
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="form-btn form-btn--primary">
            {{ isEdit ? '保存' : '添加' }}
          </button>
          <button v-if="isEdit" type="button" @click="$emit('delete', course.id)" class="form-btn form-btn--danger">
            删除
          </button>
          <button type="button" @click="$emit('close')" class="form-btn form-btn--ghost">
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

<style scoped>
.form-mask {
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
  .form-mask { align-items: center; }
}

.form-panel {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px) saturate(1.5);
  -webkit-backdrop-filter: blur(20px) saturate(1.5);
  width: 100%;
  max-width: 26rem;
  border-radius: 24px 24px 0 0;
  padding: 12px 24px calc(env(safe-area-inset-bottom, 0px) + 28px);
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 -4px 32px rgba(0, 0, 0, 0.10);
}
@media (min-width: 640px) {
  .form-panel {
    border-radius: 24px;
    padding-bottom: 28px;
  }
}

.form-handle {
  width: 36px;
  height: 4px;
  border-radius: 2px;
  background: #d5d5d5;
  margin: 0 auto 20px;
}

.form-title {
  font-size: 20px;
  font-weight: 800;
  color: #2d2d2d;
  letter-spacing: -0.3px;
  margin-bottom: 24px;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #999;
  margin-bottom: 6px;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 10px 14px;
  font-size: 15px;
  color: #2d2d2d;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-input::placeholder {
  color: #c5c5c5;
}
.form-input:focus {
  border-color: rgba(143, 163, 160, 0.5);
  box-shadow: 0 0 0 3px rgba(143, 163, 160, 0.12);
}

.form-actions {
  display: flex;
  gap: 10px;
  padding-top: 6px;
}

.form-btn {
  flex: 1;
  padding: 12px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.15s, transform 0.1s;
}
.form-btn:active { transform: scale(0.97); }

.form-btn--primary {
  background: #8fa3a0;
  color: #fff;
}
.form-btn--primary:hover { background: #7e9491; }

.form-btn--danger {
  background: rgba(181, 131, 141, 0.12);
  color: #b5838d;
}
.form-btn--danger:hover { background: rgba(181, 131, 141, 0.20); }

.form-btn--ghost {
  background: #f0eeeb;
  color: #666;
}
.form-btn--ghost:hover { background: #e8e6e2; }
</style>
