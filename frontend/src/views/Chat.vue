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
          <div class="flex items-center gap-2 p-1 px-4 bg-base-200 rounded-t-box">
            <router-link :to="{ name: 'ChatList' }" class="btn btn-lg btn-primary h-8 w-8">
              ←
            </router-link>

            <div class="avatar-group items-center -space-x-6">
              <div class="avatar">
                <div class="w-14 h-12">
                  <img :src="car.image_url || '/uploads/no_car_image.png'" alt="Автомобиль">
                </div>
              </div>
              <div class="avatar w-10 h-10">
                <div>
                  <img :src="otherUser.avatar_url || '/uploads/user_example.webp'" alt="Пользователь">
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
          </div>

          <div v-if="errorMessage" class="alert alert-error mx-4 mb-4">
            {{ errorMessage }}
          </div>
          <!-- Контейнер сообщений -->
          <div class="flex-1 overflow-y-scroll mx-4 mb-2 min-h-0 flex flex-col">
            <div class="chat"
              :class="{ 'chat-start': message.sender_uuid !== userUuid, 'chat-end': message.sender_uuid === userUuid }"
              v-for="message in messages" :key="message.uuid">
              <div class="chat-bubble" :class="{ 'chat-bubble-primary': message.sender_uuid === userUuid }">
                <p>{{ message.message_text }}</p>
                <span class="text-xs text-gray-500">{{ new Date(message.sent_at).toLocaleString() }}</span>
              </div>
            </div>
          </div>
          <!-- Поле ввода -->
          <div class="form-control mx-4 mb-2">
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const userUuid = computed(() => String(authStore.user?.uuid));
const messages = ref([]);
const newMessage = ref('');
const websocket = ref(null);
const errorMessage = ref('');
const car = ref(null);
const otherUser = ref(null);

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
  } catch (error) {
    console.error('Ошибка загрузки данных чата:', error);
    errorMessage.value = 'Не удалось загрузить данные чата';
  }
}

// Загрузка сообщений
async function loadMessages(carUuid, otherUserUuid) {
  if (!userUuid.value) {
    router.push('/login');
    return;
  }
  if (!isValidUUID(carUuid) || !isValidUUID(otherUserUuid)) {
    errorMessage.value = 'Некорректные параметры чата';
    return;
  }
  try {
    const response = await api.get(`/messages/chat/${carUuid}/${otherUserUuid}`);
    messages.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки сообщений:', error);
    errorMessage.value = 'Ошибка загрузки сообщений';
  }
}

// Подключение WebSocket
async function connectWebSocket(carUuid, otherUserUuid) {
  if (!userUuid.value) {
    router.push('/login');
    return;
  }
  if (!isValidUUID(carUuid) || !isValidUUID(otherUserUuid)) {
    errorMessage.value = 'Некорректные параметры чата';
    return;
  }
  if (websocket.value) {
    websocket.value.close();
    websocket.value = null;
  }
  const wsUrl = `ws://192.168.0.101:8000/api/messages/ws/${userUuid.value}/${carUuid}/${otherUserUuid}`;
  websocket.value = new WebSocket(wsUrl);

  websocket.value.onopen = () => {
    console.log('WebSocket подключен');
  };
  websocket.value.onmessage = (event) => {
    const message = JSON.parse(event.data);
    messages.value.push(message);
  };
  websocket.value.onerror = (error) => {
    console.error('Ошибка WebSocket:', error);
    errorMessage.value = 'Ошибка подключения к чату';
  };
  websocket.value.onclose = (event) => {
    console.log('WebSocket закрыт:', event.code, event.reason);
    if (event.code === 1008) {
      errorMessage.value = 'Ошибка авторизации';
    }
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

function isValidUUID(str) {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return typeof str === 'string' && uuidRegex.test(str);
}

onMounted(async () => {
  const { carUuid, otherUserUuid } = route.params;
  if (carUuid && otherUserUuid) {
    await Promise.all([
      loadMessages(carUuid, otherUserUuid),
      loadChatData(carUuid, otherUserUuid),
      connectWebSocket(carUuid, otherUserUuid),
    ]);
  }
});

onUnmounted(() => {
  if (websocket.value) {
    websocket.value.close();
  }
});
</script>