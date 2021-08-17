<template>
    <v-row justify="center">
        <v-btn id="btn_login" @click="dialog = true" color="primary">
            <span id="login">Войти как {{ usage === 'worker' ? 'пользователь' : 'менеджер' }}</span>
        </v-btn>
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Вход в систему</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field label="Электронная почта*" required v-model="email"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field label="Пароль*" type="password" required v-model="password"></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                <small>*обязательные поля</small>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" id="closeModal" text @click="closeModal">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="login">Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="snackbar">
            {{ errorText }}
            <template v-slot:action="{ attrs }">
                <v-btn
                    color="pink"
                    text
                    v-bind="attrs"
                    @click="removeAlert"
                >
                    Close
                </v-btn>
            </template>
        </v-snackbar>
    </v-row>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
import alertMixin from "../mixins/alert";

export default {
    name: 'Login',
    mixins: [alertMixin],
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
            const authStatus = this.$props.usage === 'user' ? 'worker' : 'manager'
            const requestConfig = {
                email: this.email,
                password: this.password,
                auth_status: authStatus
            }
            try {
                const response = await axios.post(SERVER_URL + endpoints.login, requestConfig)
                if (response.status === 200) {
                    localStorage.setItem(`${authStatus}_email`, response.data['email'])
                    localStorage.setItem(`${authStatus}_name`, response.data['name'])
                    localStorage.setItem(`${authStatus}_surname`, response.data['surname'])
                    this.$router.push(`/${authStatus}`)
                }
                this.dialog = false
            } catch (e)  {
                this.raiseAlert('Неудалось выполнить вход в систему. Попробуйте позже.')
            }
        }
    },
}
</script>