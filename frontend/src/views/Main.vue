<template>
    <v-container class="d-flex justify-space-around">
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Login as user
            </v-card-title>
            <v-card-subtitle class="d-flex justify-center align-center pt-6">
                <v-icon x-large>
                    {{ userIcon }}
                </v-icon>
            </v-card-subtitle>
            <v-card-subtitle class="d-flex justify-center">
                Log in as a user to pass the prepared quiz
            </v-card-subtitle>
            <v-card-actions>
                <Login usage="user"/>
            </v-card-actions>
        </v-card>
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Login as manager
            </v-card-title>
            <v-card-subtitle class="d-flex justify-center align-center pt-6">
                <v-icon x-large>
                    {{ adminIcon }}
                </v-icon>
            </v-card-subtitle>
            <v-card-subtitle class="d-flex justify-center">
                Log in as admin to create quiz
            </v-card-subtitle>
            <v-card-actions>
                <Login usage="admin"/>
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