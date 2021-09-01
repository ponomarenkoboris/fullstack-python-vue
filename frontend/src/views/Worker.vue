<template>
    <v-container class="m-4">
        <v-container class="d-flex justify-space-between px-10">
            <div class="user__info d-flex">
                <p>
                    <strong>Имя:</strong>
                    {{ name }} &nbsp;
                </p>
                <p>
                    <strong>Фамилия:</strong>
                    {{ surname }} &nbsp;
                </p>
                <p>
                    <strong>email:</strong>
                    {{ email }}
                </p>
            </div>
            <v-btn class="red lighten-2" @click="logout">
                <span class="white--text">Logout</span>
                <v-icon class="white--text">{{ logoutIcon }}</v-icon>
            </v-btn>
        </v-container>
        <v-snackbar v-model="snackbar">
            {{ errorText }}
            <template v-slot:action="{ attrs }">
                <v-btn color="pink" text v-bind="attrs" @click="removeAlert">Close</v-btn>
            </template>
        </v-snackbar>
        <v-chip-group class="mb-1">
            <v-chip
                label
                link
                outlined
                color="green"
                @click="() => layoutSwitcher = true"
            >Актуальные опросы</v-chip>
            <v-chip label link outlined @click="() => layoutSwitcher = false">Пройденные опросы</v-chip>
        </v-chip-group>
        <div v-if="layoutSwitcher">
            <div class="d-flex justify-center" v-if="!requestStatus">
                <v-progress-circular :size="70" :width="7" color="primary" indeterminate></v-progress-circular>
            </div>
            <h1 v-if="requestStatus && !quizList.length">Пока нет новых опросов</h1>
            <v-expansion-panels focusable v-else>
                <v-expansion-panel
                    :class="idx !== quizList.length - 1 && 'mb-2'"
                    v-for="(quiz, idx) in quizList"
                    :key="quiz.id"
                    :disabled="quiz.done"
                >
                    <v-expansion-panel-header class="d-flex justify-space-between">
                        <div max-width="300px">{{ quiz.quiz_name }}</div>
                        <div max-width="300px">{{ quiz.complete }}</div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <div class="mb-6">{{ quiz.description }}</div>
                        <ActiveQuiz :quiz="quiz" :index="idx" @updatePollsList="getQuizList" />
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>
        <div v-else>
            <v-data-table
                :headers="headers"
                :items="donePolls"
                :items-per-page="10"
                class="elevation-1"
            ></v-data-table>
        </div>
    </v-container>
</template>
<script>

import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
import ActiveQuiz from '../components/ActiveQuiz.vue'
import alertMixin from "../mixins/alert";
import logoutMixin from "../mixins/logoutMixin";

export default {
    name: 'QuizPanel',
    components: {
        ActiveQuiz
    },
    mixins: [alertMixin, logoutMixin],
    data: () => ({
        quizList: [],
        donePolls: [],
        requestStatus: false,
        layoutSwitcher: true,
        headers: [
            { text: 'Название опроса', value: 'quiz_name' },
            { text: 'Моя оценка', value: 'user_grade' },
            { text: 'Максимальный балл', value: 'max_grade' }
        ],
    }),
    computed: {
        name: () => localStorage.getItem('worker_name'),
        surname: () => localStorage.getItem('worker_surname'),
        email: () => localStorage.getItem('worker_email')
    },
    methods: {
        async getQuizList() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.quizList, { withCredentials: true })
                if (response.status === 200) {
                    const { done_quiz_list: donePolls, quiz_list: quizList } = response.data
                    this.quizList = quizList
                    this.donePolls = donePolls
                }
                this.requestStatus = true
            } catch (error) {
                console.error(error)
                this.raiseAlert('Неудалось выполнить загрузку данных. Повторите позже.')
                this.requestStatus = true
            }
        },
    },
    mounted() {
        this.getQuizList()
    }
}
</script>
<style scoped>
.user__info > p {
    margin: 0;
}
</style>