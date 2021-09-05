<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
            <template v-slot:activator="{ on, attrs }">
                <v-btn class="mb-6" v-bind="attrs" v-on="on">Пройти опрос</v-btn>
            </template>
            <v-card>
                <v-toolbar dark color="primary" class="mb-6">
                    <v-btn icon dark @click="dialog = false">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ quiz.name }}</v-toolbar-title>
                    <v-spacer></v-spacer>
                </v-toolbar>
                <v-pagination
                    class="mb-7"
                    v-model="paginationController"
                    :length="quiz.questions.length"
                ></v-pagination>
                <v-card-title
                    class="d-flex justify-center"
                >Вопрос: {{ quiz.questions[paginationController - 1].question }}</v-card-title>
                <div
                    v-if="quiz.questions[paginationController - 1].question_photo"
                    class="d-flex justify-center"
                >
                    <img
                        :src="quiz.questions[paginationController - 1].question_photo"
                        :alt="quiz.questions[paginationController - 1].question"
                        width="auto"
                        height="250px"
                    />
                </div>
                <!-- If question haven`t got multiple answer -->
                >
                <div
                    v-if="!quiz.questions[paginationController - 1].multiple"
                    class="d-flex justify-center"
                >
                    <v-radio-group v-model="quiz.questions[paginationController - 1].answer">
                        <v-radio
                            v-for="variant in quiz.questions[paginationController - 1].variants"
                            :key="variant.id"
                            :label="variant.variant"
                            :value="variant.variant"
                        ></v-radio>
                    </v-radio-group>
                </div>
                <!-- If question got multiple answers -->
                <div v-else class="d-flex justify-center">
                    <div>
                        <v-checkbox
                            v-for="variant in quiz.questions[paginationController - 1].variants"
                            :key="variant.id"
                            :label="variant.variant"
                            :input-value="quiz.questions[paginationController - 1].variants.find(val => val === variant.variant)"
                            @click="toggleMultipleAnswer(variant.variant)"
                        ></v-checkbox>
                    </div>
                </div>

                <div class="d-flex justify-center">
                    <v-btn
                        @click="submitAnswers"
                        class="green lighten-1 white--text"
                    >Завершить опрос и отправить ответы</v-btn>
                </div>
            </v-card>
            <v-snackbar v-model="snackbar">
                {{ errorText }}
                <template v-slot:action="{ attrs }">
                    <v-btn color="pink" text v-bind="attrs" @click="removeAlert">Close</v-btn>
                </template>
            </v-snackbar>
        </v-dialog>
    </v-row>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'
import alertMixin from "../mixins/alert";
// TODO add styles

export default {
    props: ['quiz'],
    mixins: [alertMixin],
    data: () => ({
        dialog: false,
        paginationController: 1,
    }),
    watch: {
        dialog(_, oldDialogStatus) {
            if (!oldDialogStatus) {
                this.$props.quiz.questions.forEach(question => { question.multiple ? question.answer = [] : question.answer = '' })
                this.paginationController = 1
            }
        }
    },
    methods: {
        toggleMultipleAnswer(variantValue) {
            const existPosition = this.$props.quiz.questions[this.paginationController - 1].answer.indexOf(variantValue)
            if (existPosition < 0) {
                const elIndex = this.$props.quiz.questions[this.paginationController - 1].answer.length
                this.$set(this.$props.quiz.questions[this.paginationController - 1].answer, elIndex, variantValue)
            } else {
                this.$props.quiz.questions[this.paginationController - 1].answer.splice(existPosition, 1)
            }
        },
        async submitAnswers() {
            const castAnswerToString = question => {
                if (question.multiple && question.answer.length) {
                    return question.answer.length === 1 ?
                        question.answer[0] :
                        question.answer.reduce((prev, curr) => `${prev},${curr}`)
                } else if (question.multiple) {
                    return ''
                } else if (typeof question.answer === 'undefined') {
                    return ''
                } else {
                    return question.answer
                }
            }

            const answers = this.$props.quiz.questions.map(question => ({
                questionId: question.id,
                answer: castAnswerToString(question)
            }))
            const userAnswer = {
                quizId: this.$props.quiz.id,
                answers
            }

            try {
                const refresh = await axios.post(SERVER_URL + endpoints.refresh, { email: localStorage.getItem('worker_email') }, { withCredentials: true })
                if (refresh.status !== 200) throw new Error({ message: 'Not authorized' })
                const response = await axios.post(SERVER_URL + endpoints.userGrading, userAnswer, { withCredentials: true })
                if (response.status === 201) {
                    this.dialog = false
                    this.$emit('updatePollsList')
                }
            } catch (e) {
                console.error(e)
                this.raiseAlert('Неудалось отправить ответы. Попробуйте позже.')
            }
        },
    }
}
</script>