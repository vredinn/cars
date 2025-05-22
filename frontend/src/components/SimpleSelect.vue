<template>
  <div class="relative" ref="root">
    
    <div
      class="input rounded-box input-bordered w-full flex items-center justify-between cursor-text"
      :class="{ disabled, 'opacity-50 cursor-not-allowed': disabled }"
    >
      <button
      type="button"
      class="w-full text-left flex justify-between items-center"
      :class="{ 'opacity-50 cursor-not-allowed': disabled }"
      @click="toggle"
      :disabled="disabled"
    >
      <span class="text-neutral-content">{{ selectedLabel || placeholder }}</span>
    </button>
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
        v-if="open"
        class="absolute bg-base-300 border border-base-100 rounded-box mt-1 max-h-60 overflow-auto"
        :style="dropdownStyle"
      >
        <li
          v-for="(option, index) in props.options"
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

const emit = defineEmits(['update:modelValue'])

const root = ref(null)
const open = ref(false)
const dropdownPos = ref({ top: 0, left: 0, width: 0 })

function optionLabel(option) {
  return typeof option === 'object' ? option[props.labelKey] : option
}

function optionKey(option) {
  return typeof option === 'object' ? option[props.valueKey] : option
}

const selectedLabel = computed(() => {
  const selected = props.options.find(o => optionKey(o) === props.modelValue)
  return selected ? optionLabel(selected) : ''
})

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

function selectOption(option) {
  emit('update:modelValue', optionKey(option))
  open.value = false
}

function toggle() {
  if (!props.disabled) {
    open.value = !open.value
  }
}

function onClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) {
    open.value = false
  }
}

const dropdownStyle = computed(() => ({
  position: 'absolute',
  top: `${dropdownPos.value.top}px`,
  left: `${dropdownPos.value.left}px`,
  width: `${dropdownPos.value.width}px`,
  zIndex: 50,
}))

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
