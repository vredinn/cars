<template>
  <div class="moderations">
    <div class="flex flex-col sm:flex-row gap-2 justify-between items-center mb-6">
      <h2 class="font-bold">Модерация объявлений</h2>
      <div class="flex items-center space-x-4">
          <span class="badge badge-warning py-4">
            Предстоит проверить: {{ moderations.length }}
          </span>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="table min-w-full">
        <thead>
          <tr>
            <th class="tracking-wider">
              Объявление
            </th>
            <th class="tracking-wider">
              Пользователь
            </th>
            <th class="tracking-wider">
              Дата
            </th>
            <th class="tracking-wider">
              Действия
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in moderations" :key="item.id">
            <td>
              <div class="flex items-center">
                <img 
                  :src="item.car.preview_image_url || '/uploads/no_car_image.png'" 
                  class="w-12 h-12 object-cover rounded mr-4"
                />
                <div>
                  <router-link 
                    :to="{ name: 'car', params: { uuid: item.car.uuid }}" 
                    class="link font-medium"
                  >
                    {{ item.car?.brand_name }} {{ item.car?.model_name }}
                  </router-link>
                  <div class="text-sm">
                    {{ item.car?.year }} год, {{ formatPrice(item.car?.price) }}
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div class="flex items-center">
                <img 
                  :src="item.car?.user?.avatar_url || '/uploads/user_example.webp'" 
                  class="w-8 h-8 rounded-full mr-2"
                />
                <div>
                  <router-link 
                    :to="{ name: 'UserProfile', params: { uuid: item.car?.user_uuid }}" 
                    class="font-medium link"
                  >
                    {{ item.car?.user?.name || 'Пользователь не найден' }}
                  </router-link>
                  <div class="text-sm">{{ item.car?.user?.email || '' }}</div>
                </div>
              </div>
            </td>
            <td>
              {{ formatDate(item.moderation_date) }}
            </td>
            <td>
              <div class="flex items-center space-x-2">
                <button
                  v-if="item.status !== 'approved' && item.status !== 'Одобрено' && item.car_id"
                  @click="updateStatus(item.car_id, 'Одобрено')"
                  class="btn btn-success"
                >
                  Одобрить
                </button>
                <button
                  v-if="item.status !== 'rejected' && item.status !== 'Отклонено' && item.car_id"
                  @click="showRejectDialog(item)"
                  class="btn btn-error"
                >
                  Отклонить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <dialog id="reject-modal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">Отклонить объявление</h3>
        <div class="mb-4">
          <label class="label text-sm font-medium mb-2">
            Причина отклонения
          </label>
          <textarea
            v-model="rejectReason"
            rows="3"
            class="textarea w-full px-3 py-4"
            placeholder="Укажите причину отклонения..."
          ></textarea>
        </div>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn" @click="closeRejectModal">Отмена</button>
            <button class="btn btn-error" @click="confirmReject">Отклонить</button>
          </form>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>закрыть</button>
      </form>
    </dialog>
  </div>
  <div class="toast toast-end">
    <div v-if="showToast" :class="['alert', toastType]">
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const moderations = ref([])
const rejectReason = ref('')
const selectedItem = ref(null)

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('alert-info')

const showNotification = (message, type = 'info') => {
  toastMessage.value = message
  toastType.value = `alert-${type}`
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const fetchModerations = async () => {
  try {
    const response = await api.get('/moderation/pending')
    moderations.value = response.data
  } catch (error) {
    console.error('Не удалось загрузить список модераций:', error)
    showNotification('Не удалось загрузить список модераций', 'error')
  }
}

const updateStatus = async (carId, status) => {
  if (!carId) {
    showNotification('Ошибка: не найден ID объявления', 'error')
    return
  }

  try {
    await api.put(`/moderation/${carId}`, { status })
    await fetchModerations()
    showNotification(
      status === 'approved' ? 'Объявление одобрено' : 'Объявление отклонено',
      'success'
    )
  } catch (error) {
    console.error('Не удалось обновить статус:', error)
    showNotification('Не удалось обновить статус', 'error')
  }
}

const showRejectDialog = (item) => {
  if (!item?.car?.id) {
    showNotification('Ошибка: не найден ID объявления', 'error')
    return
  }
  selectedItem.value = item
  rejectReason.value = ''
  const modal = document.getElementById('reject-modal')
  modal?.showModal()
}

const closeRejectModal = () => {
  const modal = document.getElementById('reject-modal')
  modal?.close()
  selectedItem.value = null
  rejectReason.value = ''
}

const confirmReject = async () => {
  if (!selectedItem.value?.car?.id || !rejectReason.value.trim()) {
    showNotification('Укажите причину отклонения', 'warning')
    return
  }

  try {    await api.put(`/moderation/${selectedItem.value.car.id}`, {
      status: 'Отклонено',
      moderator_comment: rejectReason.value.trim()
    })
    await fetchModerations()
    showNotification('Объявление отклонено', 'success')
    closeRejectModal()
  } catch (error) {
    console.error('Failed to reject car:', error)
    showNotification('Не удалось отклонить объявление', 'error')
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatPrice = (price) => {
  if (!price) return '0 ₽'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(price)
}

onMounted(() => {
  fetchModerations()
})
</script>