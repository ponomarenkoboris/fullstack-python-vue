<template>
    <v-container class="d-flex justify-space-around flex-column">
        <v-sheet class="pa-5 d-flex justify-center">
            <v-switch
                v-model="loginSwitch"
                inset
                :label="`Войти как ${ authAs }`"
            ></v-switch>
        </v-sheet>
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Войти как {{ authAs }}
            </v-card-title>
            <v-card-subtitle class="d-flex justify-center align-center pt-6">
                <v-icon x-large>
                    {{ userIcon }}
                </v-icon>
            </v-card-subtitle>
            <v-card-subtitle class="d-flex justify-center">
                Войти как {{ loginSwitch ? 'сотрудник, чтобы пройти опросы' : 'менеджер, чтобы созавать опросы' }}
            </v-card-subtitle>
            <v-card-actions class="d-flex align-center justify-space-around">
                <Auth :usage="loginSwitch ? 'worker' : 'manager'" actionType="login"/>
                <Auth :usage="loginSwitch ? 'worker' : 'manager'" actionType="registration"/>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import Auth from '../components/Auth.vue'
import { mdiAccount , mdiAccountLock } from '@mdi/js';

export default {
    name: 'Main',
    components: {
        Auth
    },
    computed: {
        authAs() {
            return this.loginSwitch ? 'сотрудник' : 'менеджер'
        }
    },
    data: () => ({
        userIcon: mdiAccount,
        adminIcon: mdiAccountLock,
        loginSwitch: true
    })
}
</script>