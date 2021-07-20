<template>
    <v-container m-6 class="d-flex justify-space-around">
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Login as user
            </v-card-title>
            <v-icon x-large>
                mdi-account-circle
            </v-icon>
            <v-card-subtitle class="d-flex justify-center">
                Log in as a user to pass the prepared quiz
            </v-card-subtitle>
            <v-card-actions>
                <Login usage="user"/>
            </v-card-actions>
        </v-card>
        <v-card class="mx-auto my-12 d-flex flex-column justify-center pb-6" width="374">
            <v-card-title class="d-flex justify-center">
                Login as admin
            </v-card-title>
            <v-icon x-large>
                mdi-wrench
            </v-icon>
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

export default {
    name: 'Main',
    components: {
        Login
    },
    computed: {
        userName() { return this.$store.state.email }
    },
    methods: {
    }
}
</script>