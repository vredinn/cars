<template>
  <div class="bg-base-300 rounded-box p-4">
    <h2 class="text-2xl font-bold mb-4">Отзывы о продавце</h2>
    
    <div v-if="isLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <!-- Общий рейтинг -->
      <div class="flex items-center gap-4 mb-4 bg-base-100 rounded-box w-min">
        <div class="stats">
          <div class="stat">
            <div class="stat-title">Средний рейтинг</div>
            <div class="stat-value text-primary">{{ averageRating.toFixed(1) }}</div>
            <div class="stat-desc">На основе {{ totalReviews }} отзывов</div>
          </div>
        </div>
        <div class="rating rating-lg">
          <template v-for="i in 5" :key="i">
            <input 
              type="radio"
              :name="'average-rating'"
              class="mask mask-star-2"
              :class="{ 'bg-orange-400': i <= averageRating, 'bg-gray-300': i > averageRating }"
              :checked="i === Math.round(averageRating)"
              disabled
            />
          </template>
        </div>
      </div>

      <!-- Коллапс для отзывов -->
      <div class="collapse collapse-arrow">
        <input type="checkbox" /> 
        <div class="collapse-title text-xl font-medium">
          Показать все отзывы ({{ totalReviews }})
        </div>
        <div class="collapse-content px-0">
          <!-- Список отзывов -->
          <div v-if="reviews.length > 0" class="space-y-4">
            <div v-for="review in reviews" :key="review.id" class="card bg-base-100">
              <div class="card-body p-4">
                <div class="flex items-center gap-2 mb-2">
                  <div class="avatar">
                    <div class="w-10 h-10 rounded-full">
                      <img :src="review.user_avatar_url || '/uploads/user_example.webp'" :alt="review.user_name">
                    </div>
                  </div>
                  <div>
                    <h3 class="font-semibold">{{ review.user_name }}</h3>
                    <div class="rating rating-sm">
                      <template v-for="i in 5" :key="i">
                        <input 
                          type="radio"
                          :name="'review-rating-' + review.id"
                          class="mask mask-star-2"
                          :class="{ 'bg-orange-400': i <= review.rating, 'bg-gray-300': i > review.rating }"
                          :checked="i === Math.round(review.rating)"
                          disabled
                        />
                      </template>
                    </div>
                  </div>
                  <div class="ml-auto text-sm text-gray-500">
                    {{ formatDate(review.review_date) }}
                  </div>
                </div>
                <p class="text-sm">{{ review.review_text }}</p>
              </div>
            </div>
          </div>

          <!-- Если нет отзывов -->
          <div v-else class="text-center py-8 text-gray-500">
            У этого продавца пока нет отзывов
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  reviews: {
    type: Array,
    required: true,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    required: true
  },
  totalReviews: {
    type: Number,
    required: true
  }
});

const averageRating = computed(() => {
  if (!props.reviews || props.reviews.length === 0) return 0;
  const sum = props.reviews.reduce((acc, review) => acc + review.rating, 0);
  return sum / props.reviews.length;
});

function formatDate(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
}
</script> 