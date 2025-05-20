// stores/filters.js
import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import api from '@/api'

export const useFiltersStore = defineStore('filters', () => {
    // Справочные данные
    const brands = ref([])
    const models = ref([])
    const carConditions = ref([])
    const steeringSides = ref([])
    const bodyTypes = ref([])
    const transmissions = ref([])
    const fuelTypes = ref([])
    const driveTypes = ref([])

    // Флаги загрузки (по желанию)
    const loading = ref(false)
    const error = ref(null)

    async function loadAll() {
        try {
            loading.value = true
            error.value = null

            const [brandsRes, modelsRes] = await Promise.all([
                api.get('/brands/'),
                api.get('/models/')
            ])

            brands.value = brandsRes.data
            models.value = modelsRes.data

            const enumsPromises = {
                carConditions: api.get('/enums/car-conditions').then(r => r.data),
                steeringSides: api.get('/enums/steering-sides').then(r => r.data),
                bodyTypes: api.get('/enums/body-types').then(r => r.data),
                transmissions: api.get('/enums/transmissions').then(r => r.data),
                fuelTypes: api.get('/enums/fuel-types').then(r => r.data),
                driveTypes: api.get('/enums/drive-types').then(r => r.data)
            }

            const results = await Promise.all(Object.values(enumsPromises))
                ;[
                    carConditions.value,
                    steeringSides.value,
                    bodyTypes.value,
                    transmissions.value,
                    fuelTypes.value,
                    driveTypes.value
                ] = results
        } catch (e) {
            error.value = e
            console.error('Ошибка загрузки фильтров:', e)
        } finally {
            loading.value = false
        }
    }

    return {
        brands,
        models,
        carConditions,
        steeringSides,
        bodyTypes,
        transmissions,
        fuelTypes,
        driveTypes,
        loading,
        error,
        loadAll
    }
})
