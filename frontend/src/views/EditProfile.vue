<template>
  <div class="container mx-auto p-4">
    <div v-if="isLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    <div v-else>
      <h1 class="text-2xl font-bold mb-6">Редактирование профиля</h1>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="space-y-4">
          <h2 class="text-xl font-semibold mb-4">Основная информация</h2>
          
          <div 
            class="bg-base-200 border-2 border-dashed rounded-box p-4 text-center transition"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <div class="avatar mb-4">
              <div class="w-32 h-32 rounded-full relative">
                <img 
                  :src="avatarPreview || (user.avatar_url && !isAvatarDeleted ? user.avatar_url : '/uploads/user_example.webp')" 
                  alt="avatar"
                  class="w-full h-full object-cover"
                />
              </div>
                <button 
                  v-if="(avatarPreview || user.avatar_url) && !isAvatarDeleted" 
                  @click="deleteAvatar" 
                  class="btn btn-circle btn-error btn-sm absolute top-0 right-0"
                  type="button"
                >
                  ✕
                </button>
            </div>
            <label class="label mb-2 block">Перетащите фото или выберите файл</label>
            <input type="file" class="hidden" ref="fileInput" @change="handleFile" accept="image/*">
            <button class="btn btn-primary" type="button" @click="$refs.fileInput.click()">
              Выбрать фото
            </button>
          </div>

          <form @submit.prevent="openSaveModal" class="space-y-4">
            <div>
              <label class="label">Имя</label>
              <label class="input validator w-full">
                <input
                  type="text"
                  v-model="form.name"
                  required
                  minlength="2"
                  maxlength="50"
                  pattern="[A-Za-zА-Яа-яЁё\- ]+"
                  placeholder="Ваше имя"
                />
              </label>
              <div class="validator-hint hidden mt-0">Имя может содержать только буквы и дефис</div>
            </div>

            <div>
              <label class="label">Email</label>
              <label class="input validator w-full">
                <input
                  type="email"
                  v-model="form.email"
                  required
                  pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
                  placeholder="your@email.com"
                />
              </label>
              <div class="validator-hint hidden mt-0">Введите корректный email адрес</div>
            </div>

            <div>
              <label class="label">Телефон</label>
              <label class="input validator w-full">
                <input
                  type="tel"
                  v-model="form.phone"
                  required
                  pattern="^\+?[0-9]{10,15}$"
                  placeholder="+79001234567"
                />
              </label>
              <div class="validator-hint hidden mt-0">Введите корректный номер телефона</div>
            </div>

            <div v-if="errorMessage" role="alert" class="alert alert-error mb-4">
              <span>{{ errorMessage }}</span>
              <button @click="errorMessage = ''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
            </div>

            <button type="submit" class="btn btn-primary w-full" :disabled="loading">
              {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </form>

          <dialog id="save-modal" class="modal modal-bottom sm:modal-middle">
            <div class="modal-box">
              <h3 class="font-bold text-lg">Сохранение изменений</h3>
              <p class="py-4">Вы уверены, что хотите сохранить изменения?</p>
              <div class="modal-action">
                <button class="btn" @click="closeSaveModal">Отмена</button>
                <button class="btn btn-primary" @click="confirmSave">Сохранить</button>
              </div>
            </div>
            <form method="dialog" class="modal-backdrop">
              <button>close</button>
            </form>
          </dialog>
        </div>

        <div class="space-y-4">
          <h2 class="text-xl font-semibold mb-4">Смена пароля</h2>
          <form @submit.prevent="updatePassword" class="space-y-4">
            <div>
              <label class="label">Текущий пароль</label>
              <label class="input validator w-full">
                <input
                  type="password"
                  v-model="passwordForm.currentPassword"
                  required
                  placeholder="Введите текущий пароль"
                  autocomplete="new-password"
                />
              </label>
            </div>

            <div>
              <label class="label">Новый пароль</label>
              <label class="input validator w-full">
                <input
                  type="password"
                  v-model="passwordForm.newPassword"
                  required
                  minlength="8"
                  pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                  placeholder="Новый пароль"
                  autocomplete="new-password"
                />
              </label>
              <div class="validator-hint hidden mt-0">
                Пароль должен быть минимум 8 символов в длину
                <br />
                Должен содержать:
                <br />
                Хотя бы одну цифру
                <br />
                Хотя бы одну строчную букву
                <br />
                Хотя бы одну заглавную букву
              </div>
            </div>

            <div>
              <label class="label">Подтверждение нового пароля</label>
              <label class="input validator w-full">
                <input
                  type="password"
                  v-model="passwordForm.confirmPassword"
                  required
                  placeholder="Повторите новый пароль"
                  autocomplete="new-password"
                />
              </label>
            </div>

            <div v-if="passwordErrorMessage" role="alert" class="alert mb-4" :class="{
              'alert-error': passwordErrorMessage !== 'Пароль успешно изменен',
              'alert-success': passwordErrorMessage === 'Пароль успешно изменен'
            }">
              <span>{{ passwordErrorMessage }}</span>
              <button @click="passwordErrorMessage = ''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
            </div>

            <button type="submit" class="btn btn-primary w-full" :disabled="passwordLoading">
              {{ passwordLoading ? 'Сохранение...' : 'Изменить пароль' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const loading = ref(false)
const passwordLoading = ref(false)
const errorMessage = ref('')
const passwordErrorMessage = ref('')
const avatarPreview = ref(null)
const avatarFile = ref(null)
const user = ref(null)
const isAvatarDeleted = ref(false)

const form = reactive({
  name: '',
  email: '',
  phone: ''
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

async function loadUserData() {
  try {
    const uuid = route.params.uuid
    if (authStore.user.uuid !== uuid && !authStore.user.is_admin) {
      router.push('/')
      return
    }

    const { data } = await api.get(`/users/${uuid}`)
    user.value = data
    form.name = data.name
    form.email = data.email
    form.phone = data.phone
  } catch (error) {
    console.error('Ошибка загрузки данных пользователя:', error)
    errorMessage.value = 'Не удалось загрузить данные пользователя'
  } finally {
    isLoading.value = false
  }
}

function handleFile(event) {
  const file = event.target.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Пожалуйста, выберите изображение'
    return
  }
  
  avatarFile.value = file
  avatarPreview.value = URL.createObjectURL(file)
}

function handleDrop(event) {
  event.preventDefault()
  const file = event.dataTransfer.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Пожалуйста, выберите изображение'
    return
  }
  
  avatarFile.value = file
  avatarPreview.value = URL.createObjectURL(file)
}

function deleteAvatar() {
  isAvatarDeleted.value = true
  avatarPreview.value = null
  avatarFile.value = null
}

function openSaveModal() {
  const modal = document.getElementById('save-modal')
  if (modal) modal.showModal()
}

function closeSaveModal() {
  const modal = document.getElementById('save-modal')
  if (modal) modal.close()
}

async function confirmSave() {
  closeSaveModal()
  await updateProfile()
}

async function updateProfile() {
  loading.value = true
  errorMessage.value = ''

  try {
    const uuid = route.params.uuid
    await api.put(`/users/${uuid}`, form)

    if (avatarFile.value) {
      const formData = new FormData()
      formData.append('file', avatarFile.value)
      await api.post(`/users/${uuid}/avatar`, formData)
    }
    
    if (isAvatarDeleted.value) {
      await api.delete(`/users/${uuid}/avatar`)
    }

    if (authStore.user.uuid === uuid) {
      await authStore.fetchUser()
    }

    router.push(`/user/${uuid}`)
  } catch (error) {
    console.error('Ошибка обновления профиля:', error)
    errorMessage.value = error.response?.data?.detail || 'Не удалось обновить профиль'
  } finally {
    loading.value = false
  }
}

async function updatePassword() {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordErrorMessage.value = 'Пароли не совпадают'
    return
  }

  passwordLoading.value = true
  passwordErrorMessage.value = ''

  try {
    const uuid = route.params.uuid
    await api.put(`/users/${uuid}/password`, {
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })

    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    document.querySelectorAll('.validator-hint').forEach(el => {
      el.classList.add('hidden')
    })
    document.querySelectorAll('.validator').forEach(el => {
      el.classList.remove('invalid')
    })

    passwordErrorMessage.value = 'Пароль успешно изменен'
  } catch (error) {
    console.error('Ошибка смены пароля:', error)
    passwordErrorMessage.value = error.response?.data?.detail || 'Не удалось изменить пароль'
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  loadUserData()
})
</script> 