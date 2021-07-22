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
					<v-toolbar-items>
						<v-btn dark	text @click="dialog = false">Save</v-btn>
					</v-toolbar-items>
				</v-toolbar>
				<div class="d-flex align-center justify-center">
					<v-card-actions @click="prevQuestion">
						<v-btn>Previous</v-btn>
					</v-card-actions>
					<v-card-title>
						Вопрос: {{ questionNumber + 1 }}/{{ quiz.questions.length }}
					</v-card-title>
					<v-card-actions @click="nextQuestion">
						<v-btn>Next</v-btn>
					</v-card-actions>
				</div>
				<v-card-text>
					Вопрос: {{ quiz.questions[questionNumber].question }}
				</v-card-text>
				<div v-if="!quiz.questions[questionNumber].variants">
					<v-textarea 
						outlined 
						name="input-7-4" 
						label="Outlined textarea" 
						v-model="textAnswer"
					></v-textarea>
					<v-btn @click="submitTextFieldAnswer">Submit</v-btn>
				</div>
				<div v-else>
					<v-checkbox 
						v-for="question in quiz.questions[questionNumber].variants" 
						:key="question.id"
						v-model="chooseAnswer" 
						:label="question.answer" 
						:value="question.answer"
					></v-checkbox>
					<v-btn @click="submitChooseAnswer">Submit</v-btn>
				</div>
			</v-card>
		</v-dialog>
	</v-row>
</template>
<script>
export default {
	props: ['quiz', 'index'],
	data: () => ({
		dialog: false,
		questionNumber: 0,
		textAnswer: '',
		chooseAnswer: []
	}),
	methods: {
		nextQuestion() {
			this.questionNumber !== 10 && ++this.questionNumber
		},
		prevQuestion() {
			this.questionNumber !== 0 && --this.questionNumber
		},
		submitTextFieldAnswer() {
			const question = this.$props.quiz.questions[this.questionNumber]
			this.$store.commit('writeAnswer', { quizIndex: this.$props.index, question, answer: this.textAnswer })
			this.textAnswer = ''
			this.questionNumber !== 10 && ++this.questionNumber
		},
		submitChooseAnswer() {
			const answer = [...this.chooseAnswer]
			const question = this.$props.quiz.questions[this.questionNumber]
			this.$store.commit('writeAnswer', { quizIndex: this.$props.index, question, answer })
			this.chooseAnswer.length = 0
			this.questionNumber !== 10 && ++this.questionNumber
		}
	}
}
</script>