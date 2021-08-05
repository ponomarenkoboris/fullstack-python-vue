<template>
    <v-container class="m-4">
        <v-container class="d-flex justify-space-between px-10">
            <h1>Quiz</h1>
            <div class="user__info">
                <p>Name: <strong>{{ name }}</strong></p>
                <p>Surname: <strong>{{ surname }}</strong></p>
                <p>email: <strong>{{ email }}</strong></p>
            </div>
        </v-container>
        <div class="d-flex justify-center" v-if="!quizList.length">
            <v-progress-circular
                :size="70"
                :width="7"
                color="primary"
                indeterminate
            ></v-progress-circular>
        </div>
        <v-expansion-panels focusable>
            <v-expansion-panel :class="idx !== quizList.length - 1 && 'mb-2'" v-for="(quiz, idx) in quizList" :key="quiz.id" :disabled="quiz.done">
                <v-expansion-panel-header class="d-flex justify-space-between">
                    <div max-width="300px">
                        {{ quiz.name }}
                    </div>
                    <div max-width="300px">
                        {{ quiz.complite }}
                    </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <div class="mb-6">
                        {{ quiz.decription }}
                    </div>
                    <ActiveQuiz :quiz="quiz" :index="idx"/>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
import ActiveQuiz from '../components/ActiveQuiz.vue'
export default {
    name: 'QuizPanel',
    components: {
        ActiveQuiz
    },
    data: () => ({
        quizList: []
    }),
    computed: {
        name() { return localStorage.getItem('user_name') },
        surname() { return localStorage.getItem('user_surname') },
        email() { return localStorage.getItem('user_email') }
    },
    methods: {
        async getQuizList() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.quizList)
                this.quizList =  response.data
            } catch (error) {
                console.error(error)
            }
        },
    },
    mounted(){
        this.getQuizList()
    }
}
</script>
<style scoped>
 .user__info > p {
     margin: 0
 }
</style>