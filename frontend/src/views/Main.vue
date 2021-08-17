<template>
    <v-container class="d-flex justify-space-around">
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Войти как сотрудник
            </v-card-title>
            <v-card-subtitle class="d-flex justify-center align-center pt-6">
                <v-icon x-large>
                    {{ userIcon }}
                </v-icon>
            </v-card-subtitle>
            <v-card-subtitle class="d-flex justify-center">
                Войдите как сотрудник, чтобы пройти опросы
            </v-card-subtitle>
            <v-card-actions>
                <Login usage="worker"/>
            </v-card-actions>
        </v-card>
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Войти как менеджер
            </v-card-title>
            <v-card-subtitle class="d-flex justify-center align-center pt-6">
                <v-icon x-large>
                    {{ adminIcon }}
                </v-icon>
            </v-card-subtitle>
            <v-card-subtitle class="d-flex justify-center">
                Войдите как менеджер для того, чтобы создать новый опрос
            </v-card-subtitle>
            <v-card-actions>
                <Login usage="manager"/>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import Login from '../components/Login.vue'
import { mdiAccount , mdiAccountLock } from '@mdi/js';

export default {
    name: 'Main',
    components: {
        Login
    },
    data: () => ({
        userIcon: mdiAccount,
        adminIcon: mdiAccountLock
    })
}
</script>