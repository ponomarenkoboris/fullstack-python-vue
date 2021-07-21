<template>
    <v-card class="mb-6">
        <v-card-title>
            <h1>Quiz</h1>
        </v-card-title>
        <v-expansion-panels>
            <v-expansion-panel v-for="quiz in quizList" :key="quiz.id">
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
                    <ActiveQuiz :quiz="quiz" />
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-card>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
import ActiveQuiz from './ActiveQuiz.vue'
export default {
    name: 'QuizPanel',
    components: {
        ActiveQuiz
    },
    data: () => ({
        quizList: [
            {
                id: 1,
                name: 'Опрос об условиях работы',
                complite: '5/10',
                decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ea commodo consequat'
            },
            {
                id: 2,
                name: 'Опрос по оборудованию',
                complite: '0/10',
                decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ea commodo consequat'
            },
            {
                id: 3,
                name: 'Самочувствие',
                complite: '6/10',
                decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam'
            }
        ]
    }),
    methods: {
        async getQuizList() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.allQuiz)
                const quizList = await response.data
                this.getQuizList = quizList
            } catch (error) {
                
            }
        },
        async checkTocken(){
            try {
                const response = await axios.get(SERVER_URL + endpoints.checkToken, { withCredentials: true }) // withCredentials: true отпраляет куки
                console.log('response.data', response.data);
            } catch (e) {}
        }
    },
    // mounted() {
    //     this.getQuizList()
    // },
}
</script>