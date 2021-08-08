<!-- TODO add styles -->
<template>
	<v-row justify="center">
		<v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
			<template v-slot:activator="{ on, attrs }">
				<v-btn class="mb-6" v-bind="attrs" v-on="on">Start quiz</v-btn>
			</template>
			<v-card>
				<v-toolbar dark	color="primary" class="mb-6">
					<v-btn icon dark @click="dialog = false">
						<v-icon>mdi-close</v-icon>
					</v-btn>
					<v-toolbar-title>{{ quiz.name }}</v-toolbar-title>
					<v-spacer></v-spacer>
				</v-toolbar>
                <v-pagination class="mb-7" v-model="paginationController" :length="quiz.questions.length"></v-pagination>
				<v-card-title class="d-flex justify-center">
					Вопрос: {{ quiz.questions[paginationController - 1].question }}
				</v-card-title>
                <div
                    v-if="quiz.questions[paginationController - 1].question_photo"
                    class="d-flex justify-center"
                >
                    <img
                        :src="quiz.questions[paginationController - 1].question_photo"
                        :alt="quiz.questions[paginationController - 1].question"
                        width="auto"
                        height="250px"
                    >
                </div>
                <div v-if="!quiz.questions[paginationController - 1].multiple" class="d-flex justify-center">
                    <v-radio-group v-model="quiz.questions[paginationController - 1].answer">
                        <v-radio
                            v-for="variant in quiz.questions[paginationController - 1].variants"
                            :key="variant.id"
                            :label="variant.variant"
                            :value="variant.variant"
                        ></v-radio>
                    </v-radio-group>
                </div>
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
                    <v-btn @click="submitAnswers" class="green lighten-1 white--text">Завершить опрос и отправить ответы</v-btn>
                </div>
			</v-card>
		</v-dialog>
	</v-row>
</template>
<script>
import axios from 'axios'
import { SERVER_URL, endpoints } from '../utils'

export default {
	props: ['quiz'],
	data: () => ({
		dialog: false,
		paginationController: 1,
	}),
    watch: {
	    dialog(_, oldDialogStatus) {
	        if (oldDialogStatus) this.$props.quiz.questions.forEach(question => { if (question.answer) delete question.answer})
            if (!oldDialogStatus) {
                this.$props.quiz.questions.forEach(question => { question.multiple ? question.answer = [] : question.answer = ''})
                this.paginationController = 1
            }
        }
    },
	methods: {
        toggleMultipleAnswer(variantValue) {
            const existPosition = this.$props.quiz.questions[this.paginationController - 1].answer.indexOf(variantValue)
            if (existPosition < 0) {
                const elIndex = this.$props.quiz.questions[this.paginationController - 1].answer.length
                this.$set(this.$props.quiz.questions[this.paginationController - 1].answer, elIndex,variantValue)
            } else {
                this.$props.quiz.questions[this.paginationController - 1].answer.splice(existPosition, 1)
            }
        },
        async submitAnswers() {
            const castAnswerToString = question => {
                if (question.multiple && question.answer.length) {
                    return question.answer.reduce((prev, curr) => prev + ',' + curr)
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
                email: localStorage.getItem('user_email'),
                answers
            }

            console.log(userAnswer)
            // TODO make request
            // const response = await axios.post(SERVER_URL + endpoints.submitAnswers)
        },
    }
}
</script>