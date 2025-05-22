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

    <ul
      v-if="open && filteredOptions.length"
      class="absolute z-10 w-full bg-base-300 border-1 border-base-100 rounded-box mt-1 max-h-60 overflow-auto"
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
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

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
}

// Обработка клика вне компонента
function onClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) {
    validateInput()
    open.value = false
  }
}

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
  document.addEventListener('mousedown', onClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onClickOutside)
})
</script>
