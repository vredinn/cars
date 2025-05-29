<template>
  <div class="join w-full">
    <button 
      type="button"
      :class="[
        'join-item btn',
        hasError ? 'btn-error' : 'btn-outline border-base-content/20 hover:border-base-content/20 hover:bg-base-content/10'
      ]"
      @click="decrease"
      :disabled="disabled || (modelValue <= min)"
    >-</button>
    <label :class="['join-item input w-full', {'input-error': hasError}]">
      <input
        type="number"
        v-model="localValue"
        :min="min"
        :max="max"
        :step="step"
        :required="required"
        :disabled="disabled"
        :placeholder="placeholder"
        class="w-full text-center [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
        @blur="onBlur"
      />
    </label>
    <button 
      type="button"
      :class="[
        'join-item btn',
        hasError ? 'btn-error' : 'btn-outline border-base-content/20 hover:border-base-content/20 hover:bg-base-content/10'
      ]"
      @click="increase"
      :disabled="disabled || (modelValue >= max)"
    >+</button>
  </div>
  <div v-if="validatorHint" class="validator-hint text-xs text-error mt-1" :class="{'hidden': !hasError}">{{ validatorHint }}</div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  min: {
    type: Number,
    default: -Infinity
  },
  max: {
    type: Number,
    default: Infinity
  },
  step: {
    type: Number,
    default: 1
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  validatorHint: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const localValue = ref(props.modelValue)
const hasError = computed(() => {
  if (props.required && (localValue.value === null || localValue.value === undefined || localValue.value === '')) return true
  if (localValue.value !== null && localValue.value !== undefined && localValue.value !== '') {
    const value = Number(localValue.value)
    if (isNaN(value)) return true
    if (value < props.min) return true
    if (value > props.max) return true
  }
  return false
})

watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal === null ? '' : newVal
})

watch(localValue, (newValue) => {
  const value = newValue === '' ? null : Number(newValue)
  if (value === null || !isNaN(value)) {
    emit('update:modelValue', value)
  }
})

const increase = () => {
  const currentValue = Number(localValue.value) || 0
  const newValue = currentValue + props.step
  if (newValue <= props.max) {
    localValue.value = newValue
  }
}

const decrease = () => {
  const currentValue = Number(localValue.value) || 0
  const newValue = currentValue - props.step
  if (newValue >= props.min) {
    localValue.value = newValue
  }
}

const onBlur = () => {
  // Если поле пустое и не обязательное, оставляем пустым
  if (localValue.value === '' && !props.required) {
    emit('update:modelValue', null)
    return
  }
  
  // Конвертируем в число
  let value = Number(localValue.value)
  
  // Если значение невалидное и поле обязательное, устанавливаем минимальное или 0
  if (isNaN(value)) {
    if (props.required) {
      value = props.min > 0 ? props.min : 0
    } else {
      emit('update:modelValue', null)
      return
    }
  }
  
  // Проверяем границы только если значение не null
  if (value !== null) {
    if (value < props.min) value = props.min
    if (value > props.max) value = props.max
  }
  
  localValue.value = value === null ? '' : value
  emit('update:modelValue', value)
}
</script> 