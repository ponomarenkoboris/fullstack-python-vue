<template>
    <v-container class="m-4">
        <v-card class="mb-6">
            <v-card-title>
                <h1>Quiz</h1>
            </v-card-title>
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
        </v-card>
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
    methods: {
        async getQuizList() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.quizList)
                this.quizList =  response.data
                this.quizList.forEach(quiz => {
                    quiz.questions.forEach(question => { if (question.multiple) question.answer = [] })
                })
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