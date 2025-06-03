<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="font-bold">Марки</h2>
      <button class="btn btn-primary" @click="showAddModal = true">Добавить марку</button>
    </div>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Название</th>
            <th>Логотип</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="brand in brands" :key="brand.id">
            <td>{{ brand.name }}</td>
            <td>
              <img :src="`${brand.image_url}`" alt="logo" class="w-12 h-12 object-contain" v-if="brand.image_url" />
            </td>
            <td>
              <button class="btn btn-primary" @click="startEdit(brand)">Редактировать</button>
              <button class="btn btn-error ml-2" @click="deleteBrand(brand.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <dialog class="modal" :class="{ 'modal-open': showAddModal }">
      <div class="modal-box">
        <h3 class="font-bold text-lg">{{ editMode ? 'Редактировать марку' : 'Добавить марку' }}</h3>
        <form @submit.prevent="saveBrand" class="space-y-4 mt-4">
          <input v-model="form.name" type="text" placeholder="Название марки" class="input input-bordered w-full" required />

          <div
            class="bg-base-200 border-2 border-dashed rounded-box p-4 text-center"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <div class="avatar mb-4">
              <div class="w-24 h-24 rounded-full relative mx-auto">
                <img
                  :src="previewImage || form.image_url"
                  alt="preview"
                  class="w-full h-full object-cover"
                  v-if="previewImage || form.image_url"
                />
              </div>
              
                <button
                  v-if="(previewImage || form.image_url)"
                  @click.prevent="removeImage"
                  class="btn btn-circle btn-error btn-sm absolute top-0 right-0"
                >✕</button>
            </div>
            
            <label class="label mb-2 block">Перетащите фото или выберите файл</label>
            <input type="file" class="hidden" ref="fileInput" @change="handleFile" accept="image/*">
            <button class="btn btn-primary" type="button" @click="$refs.fileInput.click()">
              Выбрать фото
            </button>
          </div>

          <div class="modal-action">
            <button type="submit" class="btn btn-primary">Сохранить</button>
            <button type="button" class="btn" @click="closeModal">Отмена</button>
          </div>
        </form>
      </div>
    </dialog>
    <dialog id="delete-brand-modal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box">
        <h3 class="font-bold text-lg text-error mb-4">Удаление марки</h3>
        <p>Вы уверены, что хотите удалить эту марку? Это действие нельзя отменить.</p>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn" @click="closeDeleteModal">Отмена</button>
            <button class="btn btn-error" @click="confirmDeleteBrand">Удалить</button>
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
import { useFiltersStore } from '@/stores/filters'

const filtersStore = useFiltersStore()
const brands = computed(() => filtersStore.brands)
const showAddModal = ref(false)
const editMode = ref(false)
const form = ref({ id: null, name: '', image_url: '' })
let file = null
const previewImage = ref(null)
const brandToDelete = ref(null)

const fetchBrands = async () => {
  await filtersStore.loadAll()
}

const handleFile = (event) => {
  file = event.target.files[0]
  if (file && file.type.startsWith('image/')) {
    previewImage.value = URL.createObjectURL(file)
  }
}

const handleDrop = (event) => {
  file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    previewImage.value = URL.createObjectURL(file)
  }
}

const removeImage = () => {
  file = null
  previewImage.value = null
  form.value.image_url = ''
}

const uploadImage = async () => {
  if (!file) return null
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/brands/upload', formData)
  return data
}

const saveBrand = async () => {
  try {
    if (editMode.value && (form.value.image_url)) {
      const filename = form.value.image_url.split('/').pop()
      await api.delete(`/brands/image/${filename}`)
    }
    if (file) {
      form.value.image_url = await uploadImage()
    }

    if (editMode.value) {
      await api.put(`/brands/${form.value.id}`, form.value)
    } else {
      await api.post('/brands/', form.value)
    }

    closeModal()
    await filtersStore.loadAll() 
  } catch (error) {
    console.error('Error saving brand:', error)
  }
}

const startEdit = (brand) => {
  form.value = { ...brand }
  previewImage.value = null
  showAddModal.value = true
  editMode.value = true
}
const closeModal = () => {
  showAddModal.value = false
  editMode.value = false
  form.value = { id: null, name: '', image_url: '' }
  previewImage.value = null
  file = null
}

const deleteBrand = (id) => {
  brandToDelete.value = id
  const modal = document.getElementById('delete-brand-modal')
  modal?.showModal()
}

const closeDeleteModal = () => {
  brandToDelete.value = null
  const modal = document.getElementById('delete-brand-modal')
  modal?.close()
}

const confirmDeleteBrand = async () => {
  if (!brandToDelete.value) return
  
  try {
    const brand = brands.value.find(b => b.id === brandToDelete.value)
    if (brand.image_url) {      
      const filename = brand.image_url.split('/').pop()
      await api.delete(`/brands/image/${filename}`)
    }
    await api.delete(`/brands/${brandToDelete.value}`)
    await filtersStore.loadAll()
  } catch (error) {
    console.error('Ошибка удаления марки:', error)
  } finally {
    closeDeleteModal()
  }
}

onMounted(fetchBrands)
</script>
