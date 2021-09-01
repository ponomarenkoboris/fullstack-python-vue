<template>
    <v-container>
        <v-data-table
            :headers="headers"
            :items="statistic"
            :items-per-page="10"
            class="elevation-1"
            :loading="loadingData"
            loading-text="Loading... Please wait"
            @click:row="seeMoreInfo($event)"
        ></v-data-table>

        <v-dialog
            transition="dialog-bottom-transition"
            max-width="600"
            :value="fullStatisticController"
        >
            <v-card>
                <v-toolbar color="light-green lighten-2 black--text" height="100px" dark>
                    <v-container>
                        <p style="margin: 0">Опрос: {{ fullStatisticData.quiz_name }}</p>
                        <p
                            style="margin: 0"
                        >Пользователь: {{ fullStatisticData.user_name }} {{ fullStatisticData.user_surname }}</p>
                        <p style="margin: 0">Email: {{ fullStatisticData.user_email }}</p>
                    </v-container>
                </v-toolbar>
                <v-card-text class="mt-5">
                    <v-sheet
                        rounded
                        v-for="questionStatistic in fullStatisticData.questions_statistic"
                        :key="questionStatistic.id"
                        elevation="8"
                    >
                        <v-container class="mb-2">
                            <div class="d-flex justify-space-between">
                                <div>Вопрос: {{ questionStatistic.question_name }}</div>
                                <div>Оценка: {{ questionStatistic.user_grade }}/{{ questionStatistic.question_max_grade }}</div>
                            </div>
                            <div>
                                <div>Ответ пользователя: {{ questionStatistic.user_answer }}</div>
                                <div>Правлильный ответ: {{ questionStatistic.correct_answer }}</div>
                            </div>
                        </v-container>
                    </v-sheet>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn @click="closeDialog" text>Закрыть</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-snackbar v-model="snackbar">
            {{ errorText }}
            <template v-slot:action="{ attrs }">
                <v-btn color="pink" text v-bind="attrs" @click="removeAlert">Close</v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>
<script>
import alertMixin from "../mixins/alert";
import axios from 'axios'
import { SERVER_URL, endpoints } from "../utils";

export default {
    name: 'Statistic',
    mixins: [alertMixin],
    data: () => ({
        headers: [
            {
                text: 'Email пользователя',
                align: 'start',
                sortable: false,
                value: 'user_email',
            },
            { text: 'Имя', value: 'user_name' },
            { text: 'Фамилия', value: 'user_surname' },
            { text: 'Название опроса', value: 'quiz_name' },
            { text: 'Бал пользователя', value: 'user_grade' },
            { text: 'Максимальный бал', value: 'quiz_max_grade' },
            { text: 'Дата завершение опроса', value: 'completion_date' }
        ],
        statistic: [],
        loadingData: true,
        fullStatisticController: false,
        fullStatisticData: {}
    }),
    methods: {
        async getStatistic() {
            try {
                const refresh = await axios.post(SERVER_URL + endpoints.refresh, { email: localStorage.getItem('manager_email') }, { withCredentials: true })
                if (refresh.status !== 200) throw new Error({ message: 'Not authorized' })
                const response = await axios.get(SERVER_URL + endpoints.quizFullStatistic, { withCredentials: true })
                if (response.status === 200) {
                    const validStatistic = response.data.map(quizStatistic => {
                        const { completion_date } = quizStatistic
                        const date = new Date(completion_date * 1000 + 10800000)
                        return {
                            ...quizStatistic,
                            completion_date: `${date.getDate() + '.' + (date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1) + '.' + date.getFullYear()},
                                ${date.getHours() + ':' + (date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes())}`
                        }
                    })
                    this.statistic = validStatistic
                    this.loadingData = false
                }
            } catch (e) {
                console.error(e.message)
                this.raiseAlert('Неудалось получить данные статистики. Повторите позже.')
                this.loadingData = false
            }
        },
        seeMoreInfo(event) {
            this.fullStatisticData = event
            this.fullStatisticController = true
        },
        closeDialog() {
            this.fullStatisticData = {}
            this.fullStatisticController = false
        }
    },
    mounted() {
        this.getStatistic()
    }
}
</script>