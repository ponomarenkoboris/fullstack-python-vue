<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark v-bind="attrs" v-on="on">
                    Login as {{ usage }}
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="text-h5">User Profile</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field label="Email*" required v-model="email"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field label="Password*" type="password" required v-model="password"></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                <small>*indicates required field</small>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeModal">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="login">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
export default {
    name: 'Login',
    props: {
        usage: String
    },
    data: () => ({
        dialog: false,
        email: '',
        password: ''
    }),
    methods: {
        closeModal() {
            this.dialog = false
            this.email = ''
            this.password = ''
        },
        async login() {
            const isManager = this.$props.usage === 'user'
            const requestConfig = {
                email: this.email,
                password: this.password,
                is_manager: isManager
            }
            const response = await axios.post(SERVER_URL + endpoints.loginUser, requestConfig)
            if (response.data['jwt']) {
                const userAuthStatus = isManager ? 'manager' : 'user'
                localStorage.setItem(`${userAuthStatus}_email`, response.data['email'])
                localStorage.setItem(`${userAuthStatus}_name`, response.data['name'])
                localStorage.setItem(`${userAuthStatus}_surname`, response.data['surname'])
                document.cookie = `jwt=${response.data['jwt']};`
                this.$router.push(`/${isManager ? 'user' : 'admin'}`)
            }
            this.dialog = false
        }
    },
}
</script>