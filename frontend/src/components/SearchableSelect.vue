<template>
  <div class="relative" ref="root">
    <div
      class="input rounded-box input-bordered w-full flex items-center justify-between cursor-text"
      :class="{ disabled, 'opacity-50 cursor-not-allowed': disabled }"
    >
      <input
        type="text"
        class="flex-grow bg-transparent outline-none"
        :placeholder="placeholder"
        v-model="searchQuery"
        @focus="open = true"
        @input="open = true"
        @blur="validateInput"
        :disabled="disabled"
        @click.stop
      />
      <!-- Стрелочка вниз -->
      <svg
        class="w-5 h-5 ml-2 text-gray-500 pointer-events-none"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <teleport to="body">
      <ul
        v-if="open && filteredOptions.length"
        class="absolute z-10 bg-base-300 border-1 border-base-100 rounded-box max-h-60 overflow-auto"
        :style="dropdownStyle"
      >
        <li
          v-for="(option, index) in filteredOptions"
          :key="optionKey(option)"
          @mousedown.prevent="selectOption(option)"
          :class="[
            'py-2 px-4 hover:bg-base-200 cursor-pointer',
            index !== 0 ? 'border-t border-base-100' : ''
          ]"
        >
          {{ optionLabel(option) }}
        </li>
      </ul>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

// Принимаем пропсы
const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  modelValue: {
    type: [String, Number, Object],
    default: null,
  },
  placeholder: {
    type: String,
    default: 'Выберите...',
  },
  labelKey: {
    type: String,
    default: 'name',
  },
  valueKey: {
    type: String,
    default: 'id',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

// Объявляем эмит
const emit = defineEmits(['update:modelValue'])

const root = ref(null)
const open = ref(false)
const searchQuery = ref('')
const dropdownPos = ref({ top: 0, left: 0, width: 0 })

// Получить лейбл опции
function optionLabel(option) {
  return typeof option === 'object' ? option[props.labelKey] : option
}

// Получить ключ опции
function optionKey(option) {
  return typeof option === 'object' ? option[props.valueKey] : option
}

// Фильтруем опции по поиску
const filteredOptions = computed(() =>
  props.options.filter(opt =>
    optionLabel(opt).toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

function updateDropdownPosition() {
  if (!root.value) return
  const rect = root.value.getBoundingClientRect()
  dropdownPos.value = {
    top: rect.bottom + window.scrollY,
    left: rect.left + window.scrollX,
    width: rect.width,
  }
}

watch(open, async (val) => {
  if (val) {
    await nextTick()
    updateDropdownPosition()
  }
})

function onScrollResize() {
  if (open.value) {
    updateDropdownPosition()
  }
}

// Выбор опции
function selectOption(option) {
  emit('update:modelValue', optionKey(option))
  searchQuery.value = optionLabel(option)
  open.value = false
}

// Валидация ввода
function validateInput() {
  const matched = props.options.find(
    o => optionLabel(o).toLowerCase() === searchQuery.value.toLowerCase()
  )
  if (searchQuery.value === '') {
    emit('update:modelValue', null)
  } else if (matched) {
    emit('update:modelValue', optionKey(matched))
  } else {
    // Невалидный ввод — очищаем
    emit('update:modelValue', null)
    searchQuery.value = ''
  }
  setTimeout(() => (open.value = false), 200)
}

// Обработка клика вне компонента
function onClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) {
    validateInput()
  }
}

const dropdownStyle = computed(() => ({
  position: 'absolute',
  top: `${dropdownPos.value.top}px`,
  left: `${dropdownPos.value.left}px`,
  width: `${dropdownPos.value.width}px`,
  zIndex: 50,
}))

// Следим за изменением modelValue, чтобы обновить searchQuery
watch(
  () => props.modelValue,
  (newVal) => {
    const selected = props.options.find(o => optionKey(o) === newVal)
    searchQuery.value = selected ? optionLabel(selected) : ''
  },
  { immediate: true }
)

// Слушатели для кликов вне компонента
onMounted(() => {
  window.addEventListener('resize', onScrollResize)
  window.addEventListener('scroll', onScrollResize, true)
  document.addEventListener('mousedown', onClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onScrollResize)
  window.removeEventListener('scroll', onScrollResize, true)
  document.removeEventListener('mousedown', onClickOutside)
})
</script>
