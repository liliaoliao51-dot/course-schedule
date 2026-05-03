<template>
  <div class="h-screen flex flex-col app-shell">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="max-w-5xl mx-auto px-5 py-3 flex items-center justify-between">
        <h1 class="app-title">我的课表</h1>
        <button @click="showForm = true; editingCourse = null" class="app-add-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          <span>添加</span>
        </button>
      </div>
    </header>

    <!-- 课表主体 -->
    <main class="flex-1 overflow-hidden">
      <WeekView :courses="courses" @edit="onEdit" @delete="onDelete" />
    </main>

    <!-- 添加/编辑弹窗 -->
    <CourseForm
      v-if="showForm"
      :course="editingCourse"
      @save="onSave"
      @delete="onDelete"
      @close="showForm = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import WeekView from './components/WeekView.vue'
import CourseForm from './components/CourseForm.vue'
import { getCourses, createCourse, updateCourse, deleteCourse } from './services/api'

const courses = ref([])
const showForm = ref(false)
const editingCourse = ref(null)

async function loadCourses() {
  courses.value = await getCourses()
}

function onEdit(course) {
  editingCourse.value = course
  showForm.value = true
}

async function onSave(formData) {
  if (editingCourse.value) {
    await updateCourse(editingCourse.value.id, formData)
  } else {
    await createCourse(formData)
  }
  showForm.value = false
  await loadCourses()
}

async function onDelete(id) {
  if (!confirm('确定删除这门课程？')) return
  await deleteCourse(id)
  showForm.value = false
  await loadCourses()
}

onMounted(loadCourses)
</script>

<style>
.app-shell {
  background: linear-gradient(180deg, #f5f3f0 0%, #eceae6 100%);
}

.app-header {
  background: rgba(245, 243, 240, 0.85);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  padding-top: env(safe-area-inset-top);
}

.app-title {
  font-size: 20px;
  font-weight: 800;
  color: #2d2d2d;
  letter-spacing: -0.5px;
}

.app-add-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border-radius: 12px;
  background: rgba(143, 163, 160, 0.15);
  color: #5a7a72;
  font-size: 13px;
  font-weight: 600;
  transition: background 0.2s, transform 0.1s;
}
.app-add-btn:hover {
  background: rgba(143, 163, 160, 0.25);
}
.app-add-btn:active {
  transform: scale(0.95);
  background: rgba(143, 163, 160, 0.30);
}
</style>
