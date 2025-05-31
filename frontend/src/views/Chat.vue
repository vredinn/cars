<template>
  <!-- Основной контейнер с фиксированной высотой -->
  <div class="container mx-auto pt-0 h-[calc(100dvh-64px)] max-h-[calc(100dvh-64px)] flex">
    <div class="flex w-full h-full">
      <div class="flex flex-col h-full min-h-0 w-full">
        <!-- Заглушка, если данные чата загружаются или ошибка -->
        <div v-if="!car || !otherUser" class="flex-1 flex items-center justify-center min-h-0">
          <div class="text-center">
            <span class="loading loading-spinner loading-lg"></span>
            <p class="text-gray-500 mt-4">{{ errorMessage || 'Загрузка чата...' }}</p>
          </div>
        </div>
        <!-- Окно чата, если данные загружены -->
        <div v-else class="flex flex-col h-full min-h-0">
          <!-- Информация об автомобиле и собеседнике -->
          <div class="flex items-center gap-2 p-1 px-4 bg-base-300 rounded-t-box">
            <router-link :to="{ name: 'ChatList' }" class="btn btn-lg btn-primary h-8 w-8 flex items-center justify-center p-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 7 L 10 12 L 14 17"/>
              </svg>
            </router-link>

            <div class="avatar-group items-center -space-x-6">
              <div class="avatar">
                <div class="w-14 h-12">
                  <img :src="car.image_url || '/uploads/no_car_image.png'" alt="Автомобиль">
                </div>
              </div>
              <div class="avatar">
                <div class="w-12 h-12 rounded-full">
                  <img 
                    :src="otherUser.avatar_url || '/uploads/user_example.webp'" 
                    alt="avatar" 
                    class="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>

            <!-- ВАЖНО: flex-1 и min-w-0 -->
            <div class="flex-1 min-w-0">
              <p class="font-semibold truncate" :title="car.brand_name + ' ' + car.model_name">
                {{ car.brand_name }} {{ car.model_name }}
              </p>
              <p class="text-sm truncate" :title="otherUser.name">
                {{ otherUser.name }}
              </p>
            </div>

            <!-- Кнопки для сделки -->
            <div class="flex gap-2" v-if="car && isSeller">
              <button 
                v-if="!car.is_sold"
                class="btn btn-primary btn-sm" 
                @click="showConfirmDialog = true"
                :disabled="isCreatingDeal"
              >
                {{ isCreatingDeal ? 'Подтверждение...' : 'Подтвердить продажу' }}
              </button>
            </div>

            <!-- Кнопка оставить отзыв для покупателя -->
            <div class="flex gap-2" v-if="car?.is_sold && !isSeller && !hasReview">
              <button 
                class="btn btn-primary btn-sm"
                @click="showReviewDialog = true"
              >
                Оставить отзыв
              </button>
            </div>

            <!-- Статус продажи и отзыва -->
            <div class="flex items-center gap-2">
              <div v-if="car?.is_sold" class="badge badge-info">
                Продано
              </div>
              <div v-if="car?.is_sold && hasReview" class="badge badge-success">
                Отзыв оставлен
              </div>
            </div>
          </div>

          <!-- Отображение отзыва, если он есть -->
          <div v-if="car?.is_sold && hasReview && review" class="bg-base-200 p-4 border-x-2 border-base-300">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
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
                <span class="text-sm opacity-70">{{ formatDate(review.review_date) }}</span>
              </div>
              <!-- Кнопка редактирования -->
              <button 
                v-if="review.user_uuid === authUser.uuid" 
                class="btn btn-ghost btn-sm"
                @click="editReview"
                title="Редактировать отзыв"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
            </div>
            <p class="text-sm">{{ review.review_text }}</p>
          </div>

          <div v-if="errorMessage" class="alert alert-error mx-4 mb-4">
            {{ errorMessage }}
          </div>
          <!-- Контейнер сообщений -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto px-4 pb-2 min-h-0 flex flex-col-reverse border-x-2 border-base-300">
            <div class="chat"
              :class="{ 'chat-start': message.sender_uuid !== userUuid, 'chat-end': message.sender_uuid === userUuid }"
              v-for="message in reversedMessages" :key="message.uuid">
              <div class="chat-bubble" :class="{ 'chat-bubble-primary': message.sender_uuid === userUuid }">
                <p>{{ message.message_text }}</p>
                <span class="text-xs text-gray-500">{{ new Date(message.sent_at).toLocaleString() }}</span>
              </div>
            </div>
          </div>
          <!-- Поле ввода -->
          <div class="form-control px-4 py-2 border-x-2 border-base-300">
            <div class="input-group flex gap-2">
              <input v-model="newMessage" type="text" placeholder="Напишите сообщение..."
                class="input input-bordered w-full" @keyup.enter="sendMessage" />
              <button class="btn btn-primary" @click="sendMessage">Отправить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Модальное окно подтверждения -->
  <dialog :class="{ 'modal': true, 'modal-open': showConfirmDialog }">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Подтверждение продажи</h3>
      <p class="py-4" v-if="car && otherUser">
        Вы уверены, что хотите подтвердить продажу автомобиля {{ car.brand_name }} {{ car.model_name }} пользователю {{ otherUser.name }}?
        <br><br>
        <strong class="text-warning">Внимание:</strong> После подтверждения продажи отменить её будет невозможно.
      </p>
      <div class="modal-action">
        <button class="btn btn-error" @click="showConfirmDialog = false">Отмена</button>
        <button 
          class="btn btn-primary" 
          @click="confirmDeal"
          :disabled="isCreatingDeal || !car || !otherUser"
        >
          Подтвердить
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="showConfirmDialog = false">закрыть</button>
    </form>
  </dialog>

  <!-- Модальное окно отзыва -->
  <dialog :class="{ 'modal': true, 'modal-open': showReviewDialog }">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Оставить отзыв о продавце</h3>
      <form @submit.prevent="submitReview" class="py-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Оценка</span>
          </label>
          <div class="rating rating-lg">
            <input type="radio" v-model="reviewRating" name="rating" class="mask mask-star-2 bg-orange-400" :value="1" />
            <input type="radio" v-model="reviewRating" name="rating" class="mask mask-star-2 bg-orange-400" :value="2" />
            <input type="radio" v-model="reviewRating" name="rating" class="mask mask-star-2 bg-orange-400" :value="3" />
            <input type="radio" v-model="reviewRating" name="rating" class="mask mask-star-2 bg-orange-400" :value="4" />
            <input type="radio" v-model="reviewRating" name="rating" class="mask mask-star-2 bg-orange-400" :value="5" />
          </div>
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Текст отзыва</span>
          </label>
          <textarea 
            v-model="reviewText" 
            class="textarea textarea-bordered h-24" 
            placeholder="Опишите ваш опыт работы с продавцом"
          ></textarea>
        </div>
        <div class="modal-action">
          <button type="button" class="btn btn-error" @click="showReviewDialog = false">Отмена</button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isSubmittingReview || !reviewText.trim() || !reviewRating"
          >
            {{ isSubmittingReview ? 'Отправка...' : 'Отправить отзыв' }}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="showReviewDialog = false">закрыть</button>
    </form>
  </dialog>

  <!-- Модальное окно редактирования отзыва -->
  <dialog :class="{ 'modal': true, 'modal-open': showEditReviewDialog }">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Редактирование отзыва</h3>
      <form @submit.prevent="updateReview" class="py-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Оценка</span>
          </label>
          <div class="rating rating-lg">
            <template v-for="i in 5" :key="i">
              <input 
                type="radio" 
                v-model="editReviewRating" 
                :name="'edit-rating'" 
                class="mask mask-star-2 bg-orange-400" 
                :value="i" 
              />
            </template>
          </div>
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Текст отзыва</span>
          </label>
          <textarea 
            v-model="editReviewText" 
            class="textarea textarea-bordered h-24" 
            placeholder="Опишите ваш опыт работы с продавцом"
          ></textarea>
        </div>
        <div class="modal-action">
          <button type="button" class="btn btn-error" @click="showEditReviewDialog = false">Отмена</button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isUpdatingReview || !editReviewText.trim() || !editReviewRating"
          >
            {{ isUpdatingReview ? 'Сохранение...' : 'Сохранить отзыв' }}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="showEditReviewDialog = false">закрыть</button>
    </form>
  </dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const userUuid = computed(() => String(authStore.user?.uuid));
const authUser = computed(() => authStore.user);
const messages = ref([]);
const newMessage = ref('');
const websocket = ref(null);
const errorMessage = ref('');
const car = ref(null);
const otherUser = ref(null);
const messagesContainer = ref(null);

// Состояния для сделок
const activeDeal = ref(null);
const isCreatingDeal = ref(false);
const isRespondingToDeal = ref(false);
const isCompletingDeal = ref(false);
const isCancellingDeal = ref(false);
const showReviewDialog = ref(false);
const isSubmittingReview = ref(false);
const reviewText = ref('');
const reviewRating = ref(0);
const hasReview = ref(false);
const deal = ref(null);
const review = ref(null);

// Вычисляемые свойства для сделок
const isInitiator = computed(() => {
  if (!activeDeal.value) return false;
  return activeDeal.value.initiator_uuid === userUuid.value;
});

const canCreateDeal = computed(() => {
  if (!activeDeal.value) return true;
  return ['Отклонена', 'Отменена'].includes(activeDeal.value.status);
});

// Computed property for reversed messages
const reversedMessages = computed(() => [...messages.value].reverse());

// Вычисляемые свойства
const isSeller = computed(() => {
  if (!car.value || !authStore.user) return false;
  return car.value.user_id === authStore.user.id;
});

// Загрузка данных для активного чата
async function loadChatData(carUuid, otherUserUuid) {
  if (!isValidUUID(carUuid) || !isValidUUID(otherUserUuid)) {
    errorMessage.value = 'Некорректные параметры чата';
    return;
  }
  try {
    const [carResponse, userResponse] = await Promise.all([
      api.get(`/cars/${carUuid}`),
      api.get(`/users/${otherUserUuid}`),
    ]);
    car.value = carResponse.data;
    car.value.image_url = carResponse.data.images?.length > 0 ? carResponse.data.images[0].image_url : null;
    otherUser.value = userResponse.data;

    // Если машина продана, проверяем наличие отзыва
    if (car.value.is_sold) {
      try {
        const dealResponse = await api.get(`/deals/car/${carUuid}`);
        deal.value = dealResponse.data;
        if (deal.value) {
          try {
            const reviewResponse = await api.get(`/reviews/deal/${deal.value.uuid}`);
            review.value = reviewResponse.data;
            hasReview.value = true;
          } catch (error) {
            if (error.response?.status === 404) {
              hasReview.value = false;
              review.value = null;
            } else {
              console.error('Ошибка загрузки информации об отзыве:', error);
            }
          }
        }
      } catch (error) {
        if (error.response?.status !== 404) {
          console.error('Ошибка загрузки информации о сделке:', error);
        }
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки данных чата:', error);
    errorMessage.value = 'Не удалось загрузить данные чата';
  }
}

// Загрузка сообщений
async function loadMessages(carUuid, otherUserUuid) {
  if (!isValidUUID(carUuid) || !isValidUUID(otherUserUuid)) {
    errorMessage.value = 'Некорректные параметры чата';
    return;
  }
  try {
    const response = await api.get(`/messages/chat/${carUuid}/${otherUserUuid}`);
    messages.value = response.data;
    // Scroll to bottom after messages are loaded
    nextTick(() => {
      scrollToBottom();
    });
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error);
    errorMessage.value = 'Ошибка загрузки сообщений';
  }
}

// Подключение WebSocket
async function connectWebSocket(carUuid, otherUserUuid) {
  if (!isValidUUID(carUuid) || !isValidUUID(otherUserUuid)) {
    errorMessage.value = 'Некорректные параметры чата';
    return;
  }
  if (websocket.value) {
    websocket.value.close();
    websocket.value = null;
  }
  
  // Use the API path for WebSocket connection
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${wsProtocol}//${window.location.host}/api/messages/ws/${userUuid.value}/${carUuid}/${otherUserUuid}`;
  
  console.log('Connecting to WebSocket:', wsUrl);
  websocket.value = new WebSocket(wsUrl);

  websocket.value.onopen = () => {
    console.log('WebSocket подключен');
  };
  websocket.value.onmessage = handleWebSocketMessage;
  websocket.value.onerror = (error) => {
    console.error('Ошибка WebSocket:', error);
    errorMessage.value = 'Ошибка подключения к чату';
  };
  websocket.value.onclose = (event) => {
    console.log('WebSocket закрыт:', event.code, event.reason);
    if (event.code === 1008) {
      errorMessage.value = 'Ошибка авторизации';
    }
    // Попытка переподключения через 1 секунду
    setTimeout(() => {
      if (route.params.carUuid && route.params.otherUserUuid) {
        connectWebSocket(route.params.carUuid, route.params.otherUserUuid);
      }
    }, 1000);
  };
}

// Отправка сообщения
async function sendMessage() {
  if (!newMessage.value.trim()) return;
  if (!websocket.value || websocket.value.readyState !== WebSocket.OPEN) {
    errorMessage.value = 'Чат не подключен';
    return;
  }
  const messageData = { message_text: newMessage.value };
  websocket.value.send(JSON.stringify(messageData));
  newMessage.value = '';
}

// Прокрутка к последнему сообщению
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = 0;
  }
}

function isValidUUID(str) {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return typeof str === 'string' && uuidRegex.test(str);
}

// Инициализация компонента
onMounted(async () => {

  const { carUuid, otherUserUuid } = route.params;
  if (carUuid && otherUserUuid) {
    await Promise.all([
      loadMessages(carUuid, otherUserUuid),
      loadChatData(carUuid, otherUserUuid),
      connectWebSocket(carUuid, otherUserUuid)
    ]);
  }
});

async function loadActiveDeal() {
  try {
    const { carUuid, otherUserUuid } = route.params;
    const response = await api.get(`/deals/active/${carUuid}/${otherUserUuid}`);
    activeDeal.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки активной сделки:', error);
    // Если сделки нет или она не активна, это нормально
    if (error.response?.status === 404) {
      activeDeal.value = null;
    } else {
      errorMessage.value = 'Ошибка загрузки информации о сделке';
    }
  }
}

async function createDeal() {
  if (isCreatingDeal.value) return;
  isCreatingDeal.value = true;
  try {
    const { carUuid, otherUserUuid } = route.params;
    const response = await api.post('/deals/create', {
      car_uuid: carUuid,
      other_user_uuid: otherUserUuid
    });
    activeDeal.value = response.data;
    // Отправляем системное сообщение о создании сделки
    const messageData = { 
      message_text: 'Создана новая сделка. Ожидается подтверждение.',
      is_system: true 
    };
    websocket.value.send(JSON.stringify(messageData));
  } catch (error) {
    console.error('Ошибка создания сделки:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось создать сделку';
  } finally {
    isCreatingDeal.value = false;
  }
}

async function respondToDeal(accept) {
  if (isRespondingToDeal.value || !activeDeal.value) return;
  isRespondingToDeal.value = true;
  try {
    const response = await api.post(`/deals/${activeDeal.value.uuid}/${accept ? 'accept' : 'reject'}`);
    activeDeal.value = response.data;
    // Отправляем системное сообщение о решении
    const messageData = { 
      message_text: `Сделка ${accept ? 'принята' : 'отклонена'}.`,
      is_system: true 
    };
    websocket.value.send(JSON.stringify(messageData));
  } catch (error) {
    console.error('Ошибка ответа на сделку:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось обработать ответ на сделку';
  } finally {
    isRespondingToDeal.value = false;
  }
}

async function completeDeal() {
  if (isCompletingDeal.value || !activeDeal.value) return;
  isCompletingDeal.value = true;
  try {
    const response = await api.post(`/deals/${activeDeal.value.uuid}/complete`);
    activeDeal.value = response.data;
    // Отправляем системное сообщение о завершении сделки
    const messageData = { 
      message_text: 'Сделка успешно завершена.',
      is_system: true 
    };
    websocket.value.send(JSON.stringify(messageData));
  } catch (error) {
    console.error('Ошибка завершения сделки:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось завершить сделку';
  } finally {
    isCompletingDeal.value = false;
  }
}

async function cancelDeal() {
  if (isCancellingDeal.value || !car.value) return;
  isCancellingDeal.value = true;
  try {
    await api.post(`/deals/${car.value.uuid}/cancel`);
    
    // Обновляем статус машины
    car.value.is_sold = false;
    
    // Отправляем системное сообщение об отмене
    if (websocket.value?.readyState === WebSocket.OPEN) {
      const messageData = { 
        message_text: 'Продажа отменена.',
        is_system: true 
      };
      websocket.value.send(JSON.stringify(messageData));
    }
    
    showCancelDialog.value = false;
  } catch (error) {
    console.error('Ошибка отмены продажи:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось отменить продажу';
  } finally {
    isCancellingDeal.value = false;
  }
}

const showConfirmDialog = ref(false);
const showCancelDialog = ref(false);

async function confirmDeal() {
  if (isCreatingDeal.value || !car.value || !otherUser.value) return;
  isCreatingDeal.value = true;
  try {
    const response = await api.post('/deals/create', {
      car_uuid: car.value.uuid,
      buyer_uuid: otherUser.value.uuid
    });
    
    // Обновляем статус машины
    car.value.is_sold = true;
    
    // Отправляем системное сообщение о продаже
    if (websocket.value?.readyState === WebSocket.OPEN) {
      const messageData = { 
        message_text: 'Автомобиль продан.',
        is_system: true 
      };
      websocket.value.send(JSON.stringify(messageData));
    }
    
    showConfirmDialog.value = false;
  } catch (error) {
    console.error('Ошибка подтверждения продажи:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось подтвердить продажу';
  } finally {
    isCreatingDeal.value = false;
  }
}

async function submitReview() {
  if (isSubmittingReview.value || !deal.value || !reviewText.value.trim() || !reviewRating.value) return;
  
  // Validate rating is between 1 and 5
  const rating = Number(reviewRating.value);
  if (rating < 1 || rating > 5) {
    errorMessage.value = 'Оценка должна быть от 1 до 5';
    return;
  }

  const reviewData = {
    deal_uuid: deal.value.uuid,
    review_text: reviewText.value.trim(),
    rating: rating
  };
  
  isSubmittingReview.value = true;
  try {
    const response = await api.post('/reviews/create', reviewData);
    review.value = response.data;
    
    // Отправляем системное сообщение об отзыве
    if (websocket.value?.readyState === WebSocket.OPEN) {
      const messageData = { 
        message_text: 'Покупатель оставил отзыв о продавце.',
        is_system: true,
        review: response.data // Добавляем данные отзыва в сообщение
      };
      websocket.value.send(JSON.stringify(messageData));
    }
    
    hasReview.value = true;
    showReviewDialog.value = false;
    reviewText.value = '';
    reviewRating.value = 0;
  } catch (error) {
    console.error('Ошибка отправки отзыва:', error);
    if (error.response?.status === 422) {
      const detail = error.response.data?.detail;
      if (Array.isArray(detail)) {
        errorMessage.value = detail.map(err => err.msg).join(', ');
      } else if (typeof detail === 'object') {
        errorMessage.value = Object.values(detail).join(', ');
      } else {
        errorMessage.value = detail || 'Некорректные данные отзыва. Проверьте оценку (1-5) и текст отзыва.';
      }
    } else if (error.response?.status === 400) {
      errorMessage.value = error.response.data?.detail || 'Не удалось отправить отзыв. Возможно, вы уже оставляли отзыв или не являетесь покупателем.';
    } else {
      errorMessage.value = error.response.data?.detail || 'Не удалось отправить отзыв. Попробуйте позже.';
    }
  } finally {
    isSubmittingReview.value = false;
  }
}

const showEditReviewDialog = ref(false);
const editReviewText = ref('');
const editReviewRating = ref(0);
const isUpdatingReview = ref(false);

function editReview() {
  if (!review.value) return;
  editReviewText.value = review.value.review_text;
  editReviewRating.value = review.value.rating;
  showEditReviewDialog.value = true;
}

function formatDate(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
}

async function updateReview() {
  if (isUpdatingReview.value || !editReviewText.value.trim() || !editReviewRating.value || !review.value) return;
  
  const rating = Number(editReviewRating.value);
  if (rating < 1 || rating > 5) {
    errorMessage.value = 'Оценка должна быть от 1 до 5';
    return;
  }

  isUpdatingReview.value = true;
  try {
    const response = await api.put(`/reviews/${review.value.uuid}`, {
      review_text: editReviewText.value.trim(),
      rating: rating
    });
    
    review.value = response.data;
    showEditReviewDialog.value = false;
    
    // Отправляем системное сообщение об обновлении отзыва
    if (websocket.value?.readyState === WebSocket.OPEN) {
      const messageData = { 
        message_text: 'Отзыв был обновлен.',
        is_system: true,
        review: response.data // Добавляем обновленные данные отзыва
      };
      websocket.value.send(JSON.stringify(messageData));
    } else {
      // Если WebSocket закрыт, пробуем переподключиться
      const { carUuid, otherUserUuid } = route.params;
      if (carUuid && otherUserUuid) {
        await connectWebSocket(carUuid, otherUserUuid);
      }
    }
  } catch (error) {
    console.error('Ошибка обновления отзыва:', error);
    errorMessage.value = error.response?.data?.detail || 'Не удалось обновить отзыв';
  } finally {
    isUpdatingReview.value = false;
  }
}

// Обработка входящих WebSocket сообщений
function handleWebSocketMessage(event) {
  try {
    const data = JSON.parse(event.data);
    
    // Если сообщение содержит данные отзыва, обновляем локальный отзыв
    if (data.review) {
      review.value = data.review;
      hasReview.value = true;
    }
    
    // Добавляем сообщение в список
    messages.value.push(data);
    
    // Прокручиваем к последнему сообщению
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    });
  } catch (error) {
    console.error('Ошибка обработки WebSocket сообщения:', error);
  }
}

onUnmounted(() => {
  if (websocket.value) {
    websocket.value.close();
  }
});
</script>