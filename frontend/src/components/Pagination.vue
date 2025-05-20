<template>
  <div class="join flex justify-center mt-6 space-x-2">
    <button
      class="join-item btn rounded-full bg-neutral text-neutral-content"
      :class="{ 'btn-disabled': currentPage === 1 }"
      @click="$emit('page-changed', currentPage - 1)"
      :disabled="currentPage === 1"
    >
      «
    </button>

    <button
      v-for="page in pagesToShow"
      :key="page"
      class="join-item btn rounded-full"
      :class="{ 'btn-active': page === currentPage }"
      @click="$emit('page-changed', page)"
    >
      {{ page }}
    </button>

    <button
      class="join-item btn rounded-full bg-neutral text-neutral-content"
      :class="{ 'btn-disabled': currentPage === totalPages }"
      @click="$emit('page-changed', currentPage + 1)"
      :disabled="currentPage === totalPages"
    >
      »
    </button>
  </div>
</template>

<script setup>
import { computed, defineProps, defineEmits } from 'vue'

const props = defineProps({
  currentPage: Number,
  totalPages: Number,
})

const emit = defineEmits(['page-changed'])

const pagesToShow = computed(() => {
  const pages = []
  const maxVisiblePages = 5

  let startPage = Math.max(1, props.currentPage - Math.floor(maxVisiblePages / 2))
  let endPage = startPage + maxVisiblePages - 1

  if (endPage > props.totalPages) {
    endPage = props.totalPages
    startPage = Math.max(1, endPage - maxVisiblePages + 1)
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }

  return pages
})
</script>
