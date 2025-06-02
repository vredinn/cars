<template>
  <div class="users">
    <div class="flex justify-between items-center mb-6">
      <h2 class="font-bold">Пользователи</h2>
      <div class="relative">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск..."
          class="input"
          @input="handleSearch"
        />
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th class="tracking-wider">
              Пользователь
            </th>
            <th class="tracking-wider">
              Дата регистрации
            </th>
            <th class="tracking-wider">
              Объявления
            </th>
            <th class="tracking-wider">
              Действия
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="px-6 py-4">
              <div class="flex items-center">
                <img 
                  :src="user.avatar_url || '/uploads/user_example.webp'" 
                  class="w-10 h-10 object-cover rounded-full mr-3"
                />
                <div>                    
                  <router-link 
                    :to="{ name: 'UserProfile', params: { uuid: user.uuid }}" 
                    class="link font-medium"
                  >
                  {{ user.name }}
                  </router-link>
                  <div class="text-sm">{{ user.email }}</div>
                </div>
              </div>
            </td>
            <td>
              {{ formatDate(user.registration_date) }}
            </td>
            <td>
              <div class="flex items-center space-x-2">
                <span class="text-sm">{{ user.cars_count || 0 }}</span>
              </div>
            </td>
            <td>
              <div class="flex items-center space-x-2">
                <button
                  @click="editUser(user.uuid)"
                  class="btn btn-primary"
                  title="Редактировать пользователя"
                >
                Редактировать
                </button>
                <button
                  @click="showDeleteDialog(user)"
                  class="btn btn-error"
                  title="Удалить пользователя"
                >
                Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div

    <!-- Диалог удаления пользователя -->
    <div v-if="showDeleteForm" class="fixed inset-0 flex items-center justify-center backdrop-blur-sm">
      <div class="bg-base-300 rounded-box p-6 w-full max-w-lg">
        <h3 class="text-lg font-bold mb-4">Удалить пользователя</h3>
        <div class="mb-4">
          <p>
            Вы действительно хотите удалить пользователя {{ selectedUser?.name }}?
            Это действие нельзя отменить.
          </p>
        </div>
        <div class="flex justify-end space-x-3">
          <button
            @click="closeDeleteDialog"
            class="btn btn-primary"
          >
            Отмена
          </button>
          <button
            @click="confirmDelete"
            class="btn btn-error"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>

    <!-- Toast container -->
    <div class="toast toast-end">
      <div v-if="showToast" :class="['alert', toastType]">
        <span>{{ toastMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const users = ref([])
const searchQuery = ref('')
const showDeleteForm = ref(false)
const selectedUser = ref(null)

// Toast state
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('alert-info')

// Toast function
const showNotification = (message, type = 'info') => {
  toastMessage.value = message
  toastType.value = `alert-${type}`
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Failed to fetch users:', error)
    showNotification('Не удалось загрузить список пользователей', 'error')
  }
}

const handleSearch = async () => {
  if (!searchQuery.value) {
    await fetchUsers()
    return
  }

  try {
    const response = await api.get(`/users/search?q=${searchQuery.value}`)
    users.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
    showNotification('Ошибка при поиске', 'error')
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const editUser = (uuid) => {
  if (!uuid) {
    showNotification('Ошибка: не найден ID пользователя', 'error')
    return
  }
  router.push({ name: 'EditProfile', params: { uuid }})
}

const showDeleteDialog = (user) => {
  selectedUser.value = user
  showDeleteForm.value = true
}

const closeDeleteDialog = () => {
  showDeleteForm.value = false
  selectedUser.value = null
}

const confirmDelete = async () => {
  if (!selectedUser.value?.uuid) {
    showNotification('Ошибка: не найден ID пользователя', 'error')
    return
  }

  try {
    await api.delete(`/users/${selectedUser.value.uuid}`)
    await fetchUsers() // Обновляем список после удаления
    showNotification('Пользователь успешно удален', 'success')
    closeDeleteDialog()
  } catch (error) {
    console.error('Failed to delete user:', error)
    showNotification('Не удалось удалить пользователя', 'error')
  }
}

onMounted(() => {
  fetchUsers()
})
</script> 