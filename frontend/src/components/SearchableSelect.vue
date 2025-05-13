<template>
    <div class="relative" ref="root">
        <input
            type="text"
            class="input rounded-box input-bordered w-full"
            :class="['input rounded-box input-bordered w-full', { 'disabled': disabled }]"
            :placeholder="placeholder"
            v-model="searchQuery"
            @focus="open = true"
            @input="open = true"
            @blur="validateInput"
            :disabled="disabled"
        />

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

<script>
export default {
  name: 'SearchableSelect',
  props: {
    options: Array,
    modelValue: [String, Number, Object],
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
        default: false
    }
  },
  data() {
    return {
      open: false,
      searchQuery: '',
    }
  },
  computed: {
    filteredOptions() {
      return this.options.filter(opt =>
        this.optionLabel(opt).toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
  },
methods: {
  optionLabel(option) {
    return typeof option === 'object' ? option[this.labelKey] : option
  },
  optionKey(option) {
    return typeof option === 'object' ? option[this.valueKey] : option
  },
  selectOption(option) {
    this.$emit('update:modelValue', this.optionKey(option))
    this.searchQuery = this.optionLabel(option)
    this.open = false
  },
  validateInput() {
    const matched = this.options.find(
      o => this.optionLabel(o).toLowerCase() === this.searchQuery.toLowerCase()
    )
    if (this.searchQuery === '') {
      this.$emit('update:modelValue', null)
    } else if (matched) {
      this.$emit('update:modelValue', this.optionKey(matched))
    } else {
      // Невалидный ввод — очищаем
      this.$emit('update:modelValue', null)
      this.searchQuery = ''
    }
  },
  onClickOutside(e) {
    if (!this.$refs.root.contains(e.target)) {
      this.validateInput()
      this.open = false
    }
  }
},
  mounted() {
    document.addEventListener('mousedown', this.onClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('mousedown', this.onClickOutside)
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(newVal) {
        const selected = this.options.find(o => this.optionKey(o) === newVal)
        this.searchQuery = selected ? this.optionLabel(selected) : ''
      },
    },
  },
}
</script>
