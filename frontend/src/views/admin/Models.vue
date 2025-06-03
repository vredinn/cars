<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="font-bold">Модели</h2>
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по названию..."
            class="input input-bordered"
            @input="handleSearch"
          />
        </div>
        <button class="btn btn-primary" @click="showAddModal = true">Добавить модель</button>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th class="tracking-wider">Марка</th>
            <th class="tracking-wider">Название</th>
            <th class="tracking-wider">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="model in models" :key="model.id">
            <td>{{ getBrandName(model.brand_id) }}</td>
            <td>{{ model.name }}</td>
            <td>
              <button class="btn btn-primary" @click="startEdit(model)">Редактировать</button>
              <button class="btn btn-error ml-2" @click="deleteModel(model.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <dialog class="modal z-4" :class="{ 'modal-open': showAddModal }">
      <div class="modal-box">
        <h3 class="font-bold text-lg">{{ editMode ? 'Редактировать модель' : 'Добавить модель' }}</h3>
        <form @submit.prevent="saveModel" class="space-y-4 mt-4">
          <SearchableSelect
            v-model="form.brand_id"
            :options="brands"
            placeholder="Марка"
            label-key="name"
            value-key="id"
            class="w-full"
          />

          <input
            v-model="form.name"
            type="text"
            placeholder="Название модели"
            class="input input-bordered w-full"
            required
          />

          <div class="modal-action">
            <button type="submit" class="btn btn-primary">Сохранить</button>
            <button type="button" class="btn" @click="closeModal">Отмена</button>
          </div>
        </form>
      </div>
    </dialog>

    <dialog id="delete-model-modal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box">
        <h3 class="font-bold text-lg text-error mb-4">Удаление модели</h3>
        <p>Вы уверены, что хотите удалить эту модель? Это действие нельзя отменить.</p>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn" @click="closeDeleteModal">Отмена</button>
            <button class="btn btn-error" @click="confirmDeleteModel">Удалить</button>
          </form>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>закрыть</button>
      </form>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'
import SearchableSelect from '@/components/SearchableSelect.vue'
import { useFiltersStore } from '@/stores/filters'

const filtersStore = useFiltersStore()
const models = computed(() => filtersStore.models)
const brands = computed(() => filtersStore.brands)
const showAddModal = ref(false)
const editMode = ref(false)
const form = ref({ id: null, name: '', brand_id: '' })
const searchQuery = ref('')
const modelToDelete = ref(null)

const fetchModels = async (search = '') => {
  try {
    await filtersStore.loadAll()
  } catch (error) {
    console.error('Failed to fetch models:', error)
  }
}

const fetchBrands = async () => {
  await filtersStore.loadAll()
}

const handleSearch = async () => {
  await fetchModels(searchQuery.value)
}

const saveModel = async () => {
  try {
    if (editMode.value) {
      await api.put(`/models/${form.value.id}`, form.value)
    } else {
      await api.post('/models/', form.value)
    }
    closeModal()
    await filtersStore.loadAll() 
  } catch (error) {
    console.error('Failed to save model:', error)
  }
}

const startEdit = (model) => {
  form.value = { ...model }
  showAddModal.value = true
  editMode.value = true
}

const closeModal = () => {
  showAddModal.value = false
  editMode.value = false
  form.value = { id: null, name: '', brand_id: '' }
}

const getBrandName = (id) => {
  const brand = brands.value.find(b => b.id === id)
  return brand?.name || '—'
}

const deleteModel = (id) => {
  modelToDelete.value = id
  const modal = document.getElementById('delete-model-modal')
  modal?.showModal()
}

const closeDeleteModal = () => {
  modelToDelete.value = null
  const modal = document.getElementById('delete-model-modal')
  modal?.close()
}

const confirmDeleteModel = async () => {
  if (!modelToDelete.value) return
  
  try {
    await api.delete(`/models/${modelToDelete.value}`)
    await filtersStore.loadAll() 
  } catch (error) {
    console.error('Ошибка удаления модели:', error)
  } finally {
    closeDeleteModal()
  }
}

onMounted(async () => {
  await filtersStore.loadAll()
})
</script>