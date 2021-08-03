<!-- TODO add styles -->
<template>
	<v-row justify="center">
		<v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
			<template v-slot:activator="{ on, attrs }">
				<v-btn class="mb-6" v-bind="attrs" v-on="on">Start quiz</v-btn>
			</template>
			<v-card>
				<v-toolbar dark	color="primary">
					<v-btn icon dark @click="dialog = false">
						<v-icon>mdi-close</v-icon>
					</v-btn>
					<v-toolbar-title>{{ quiz.name }}</v-toolbar-title>
					<v-spacer></v-spacer>
				</v-toolbar>
                <v-pagination v-model="paginationController" :length="quiz.questions.length"></v-pagination>
				<div class="d-flex align-center justify-center">
					<v-card-title>
						Вопрос: {{ paginationController - 1 + 1 }}/{{ quiz.questions.length }}
					</v-card-title>
				</div>
				<v-card-text>
					Вопрос: {{ quiz.questions[paginationController - 1].question }}
				</v-card-text>
				<div v-if="!quiz.questions[paginationController - 1].multiple">
					<v-radio-group v-model="quiz.questions[paginationController - 1].answer">
                        <v-radio
                            v-for="variant in quiz.questions[paginationController - 1].variants"
                            :key="variant.id"
                            :label="variant.variant"
                            :value="variant.variant"
                        ></v-radio>
                    </v-radio-group>
                    <h1>{{ quiz.questions[paginationController - 1].answer }}</h1>
				</div>
				<div v-else>
					<v-checkbox 
						v-for="variant in quiz.questions[paginationController - 1].variants"
						:key="variant.id"
						:label="variant.variant"
                        :input-value="quiz.questions[paginationController - 1].answer.find(val => val === variant.variant)"
						@click="toggleMultipleAnswer(variant.variant)"
					></v-checkbox>
				</div>
                <v-btn @click="submitAnswers">Завершить опрос и отправиьт ответы</v-btn>
			</v-card>
		</v-dialog>
	</v-row>
</template>
<script>
export default {
	props: ['quiz'],
	data: () => ({
		dialog: false,
		paginationController: 1
	}),
	methods: {
        toggleMultipleAnswer(variantValue) {
            const existPosition = this.$props.quiz.questions[this.paginationController - 1].answer.indexOf(variantValue)
            if (existPosition < 0) {
                const elIndex = this.$props.quiz.questions[this.paginationController - 1].answer.length
                this.$set(this.$props.quiz.questions[this.paginationController - 1].answer, elIndex,variantValue)
            } else {
                this.$props.quiz.questions[this.paginationController - 1].answer.splice(existPosition, 1)
            }
            console.log(this.$props.quiz.questions[this.paginationController - 1].answer)
        },
        submitAnswers() {
            const answers = this.$props.quiz.questions.map(question => ({
                questionId: question.id,
                // TODO add validation (if question.answer is empty array)
                answer: question.multiple ? question.answer.reduce((prev, curr) => prev + ',' + curr) : question.answer
            }))
            const userAnswer = {
                quizId: this.$props.quiz.id,
                username: 'boris', // TODO add user username
                answers
            }
            console.log(userAnswer)
        },
    }
}
</script>