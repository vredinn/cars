<template>
    <div class="container mx-auto pt-0 flex">
        <div class="flex w-full h-full">
            <div class="p-4 flex flex-col h-full min-h-0 w-full">
                <h2 class="text-xl font-bold mb-4">Чаты</h2>
                <div v-if="isLoading" class="flex justify-center my-8">
                    <span class="loading loading-spinner loading-lg"></span>
                </div>
                <div v-else-if="errorMessage" class="alert alert-error">
                    {{ errorMessage }}
                </div>
                <div v-else-if="chats.length === 0" class="alert alert-info justify-center">
                    У вас пока нет чатов
                </div>
                <div v-else class="flex-1 overflow-y-auto space-y-2">
                    <router-link v-for="chat in chats" :key="chat.uuid"
                        :to="{ name: 'Chat', params: { carUuid: chat.car_uuid, otherUserUuid: chat.other_user_uuid } }"
                        class="block p-2 bg-base-200 rounded-box hover:bg-base-300 transition text-wrap">
                        <div class="flex gap-2 items-center">
                            <div class="avatar-group items-center -space-x-6">
                                <div class="avatar">
                                    <div class="w-14 h-12">
                                        <img :src="chat.car_image_url || '/uploads/no_car_image.png'" alt="Автомобиль">
                                    </div>
                                </div>
                                <div class="avatar">
                                    <div class="w-12 h-12 rounded-full">
                                        <img 
                                            :src="chat.other_user_avatar_url || '/uploads/user_example.webp'" 
                                            alt="avatar" 
                                            class="w-full h-full object-cover"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div class="flex-1 w-full min-w-0">
                                <div class="flex flex-col">
                                    <p class="font-bold truncate mb-0"
                                        :title="chat.car_brand_name + ' ' + chat.car_model_name">
                                        {{ chat.car_brand_name }} {{ chat.car_model_name }}
                                    </p>
                                    <p class="truncate" :title="chat.other_user_name">
                                        {{ chat.other_user_name }}
                                    </p>
                                </div>
                                <p class="text-sm truncate" :title="chat.message_text">
                                    {{ chat.sender_name.length > 10 ? chat.sender_name.slice(0, 10) +
                                        '.' : chat.sender_name }}: {{ chat.message_text }}
                                </p>

                                <p class="text-xs">
                                    {{ new Date(chat.sent_at).toLocaleString(undefined, {
                                        year: 'numeric',
                                        month: '2-digit',
                                        day: '2-digit',
                                        hour: '2-digit',
                                        minute: '2-digit',
                                        hour12: false
                                    }) }}
                                </p>
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const userUuid = computed(() => String(authStore.user?.uuid));
const chats = ref([]);
const errorMessage = ref('');
const isLoading = ref(false);

async function loadChats() {
    if (!userUuid.value) {
        router.push('/login');
        return;
    }
    isLoading.value = true;
    try {
        const response = await api.get(`/messages/user/${userUuid.value}`);
        chats.value = await Promise.all(response.data.map(async (chat) => {
            let carData = { brand_name: 'Неизвестно', model_name: '', image_url: null };
            try {
                const carResponse = await api.get(`/cars/${chat.car_uuid}`);
                carData = carResponse.data;
                carData.image_url = carData.images?.length > 0 ? carData.images[0].image_url : null;
            } catch (error) {
                console.error(`Ошибка загрузки автомобиля ${chat.car_uuid}:`, error);
            }
            const otherUserUuid = chat.sender_uuid === userUuid.value ? chat.receiver_uuid : chat.sender_uuid;
            chat.sender_name = chat.sender_uuid === userUuid.value ? 'Вы' : chat.sender.name;
            let userData = { name: 'Неизвестно', avatar_url: null };
            try {
                const userResponse = await api.get(`/users/${otherUserUuid}`);
                userData = userResponse.data;
            } catch (error) {
                console.error(`Ошибка загрузки пользователя ${otherUserUuid}:`, error);
            }
            return {
                uuid: chat.uuid,
                car_uuid: chat.car_uuid,
                car_brand_name: carData.brand_name,
                car_model_name: carData.model_name,
                car_image_url: carData.image_url,
                other_user_uuid: otherUserUuid,
                other_user_name: userData.name,
                other_user_avatar_url: userData.avatar_url,
                message_text: chat.message_text,
                sent_at: chat.sent_at,
                sender_name: chat.sender_name,
            };
        }));
        chats.value.sort((a, b) => new Date(b.sent_at) - new Date(a.sent_at));
    } catch (error) {
        console.error('Ошибка загрузки чатов:', error);
        errorMessage.value = 'Ошибка загрузки чатов';
    } finally {
        isLoading.value = false;
    }
}

onMounted(async () => {
    await loadChats();
});
</script>