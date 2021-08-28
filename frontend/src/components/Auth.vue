<template>
    <v-row justify="center" style="margin-top: 0;">
        <v-btn
            @click="dialog = true"
            :color="actionType === 'login' ? 'green white--text' : 'primary'"
        >
            {{ actionType === 'login' ? 'Войти' : 'Зарегистрироваться' }}
        </v-btn>
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="text-h5">{{ actionType === 'login' ? 'Вход в систему' : 'Регистрация' }}</span>
                </v-card-title>
                <v-card-text>
                    <v-form v-model="isValid" ref="form">
                        <v-container>
                            <v-row v-if="actionType === 'registration'">
                                <v-col cols="12">
                                    <v-text-field label="Имя*" required v-model="name" :rules="inputFiledRules"></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field label="Фамилия*" required v-model="surname" :rules="inputFiledRules"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field label="Электронная почта*" required v-model="email" :rules="emailInputRules"></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field label="Пароль*" type="password" required v-model="password" :rules="inputFiledRules"></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-form>
                <small>*обязательное поле</small>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="blue darken-1" id="closeModal" text @click="closeModal">Закрыть</v-btn>
                    <v-btn color="blue darken-1" text @click="auth">{{ actionType === 'login' ? 'Войти' : 'Зарегистрироваться' }}</v-btn>
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
// TODO add styles

export default {
    name: 'Login',
    mixins: [alertMixin],
    props: {
        usage: String,
        actionType: String
    },
    data: () => ({
        dialog: false,
        isValid: false,
        email: '',
        password: '',
        name: '',
        surname: '',
        inputFiledRules: [
            value => !!value || 'Обязательное поле',
            value => value.length <= 255 || 'Слишком большое значение для поля'
        ],
        emailInputRules: [
            email => !!email || 'Обязательное поле',
            email => /.+@.+\..+/.test(email) || 'Некорректный e-mail',
            email => email.length <= 255 || 'Слишком большое значение для поля'
        ]
    }),
    methods: {
        closeModal() {
            this.dialog = false
            this.email = ''
            this.password = ''
            this.name = ''
            this.surname = ''
        },
        async auth() {
            if (!this.$refs.form.validate()) return
            const authStatus = this.$props.usage === 'worker' ? 'worker' : 'manager'
            let authData = {}
            if (this.$props.actionType === 'login') {
                authData = {
                    email: this.email,
                    password: this.password,
                    auth_status: authStatus
                }
            } else {
                authData = {
                    email: this.email,
                    password: this.password,
                    name: this.name,
                    surname: this.surname,
                    auth_status: authStatus
                }
            }
            try {
                const apiPath = this.$props.actionType === 'login' ? endpoints.login : endpoints.register
                const response = await axios.post(SERVER_URL + apiPath, authData, { withCredentials: true })
                if (response.status === 200) {
                    localStorage.clear()
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