<template>
    <div class="join flex justify-center mt-6 space-x-2">
      <button class="join-item btn rounded-full bg-neutral text-neutral-content" 
              :class="{ 'btn-disabled': currentPage === 1 }"
              @click="$emit('page-changed', currentPage - 1)">
        «
      </button>
      <button class="join-item btn rounded-full" 
              v-for="page in pagesToShow" 
              :key="page"
              :class="{ 'btn-active': page === currentPage }"
              @click="$emit('page-changed', page)">
        {{ page }}
      </button>
      <button class="join-item btn rounded-full bg-neutral text-neutral-content" 
              :class="{ 'btn-disabled': currentPage === totalPages }"
              @click="$emit('page-changed', currentPage + 1)">
        »
      </button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      currentPage: Number,
      totalPages: Number
    },
    computed: {
      pagesToShow() {
        const pages = []
        const maxVisiblePages = 5
        
        let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2))
        let endPage = startPage + maxVisiblePages - 1
        
        if (endPage > this.totalPages) {
          endPage = this.totalPages
          startPage = Math.max(1, endPage - maxVisiblePages + 1)
        }
        
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i)
        }
        
        return pages
      }
    }
  }
  </script>