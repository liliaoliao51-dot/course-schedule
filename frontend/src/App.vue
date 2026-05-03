<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm sticky top-0 z-30">
      <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <h1 class="text-lg font-bold text-gray-900">我的课表</h1>
        <button
          @click="showForm = true; editingCourse = null"
          class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700 active:bg-blue-800 transition font-medium"
        >
          + 添加课程
        </button>
      </div>
    </header>

    <!-- 课表主体：WeekView 占满剩余空间 -->
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
