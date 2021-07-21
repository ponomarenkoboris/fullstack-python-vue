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
						Вопрос: {{ questionNumber }}/10
					</v-card-title>
					<v-card-actions @click="nextQuestion">
						<v-btn>Next</v-btn>
					</v-card-actions>
				</div>
			</v-card>
		</v-dialog>
	</v-row>
</template>
<script>
export default {
	props: ['quiz'],
	data: () => ({
		dialog: false,
		notifications: false,
		sound: true,
		widgets: false,
		questionNumber: 0
	}),
	methods: {
		nextQuestion() {
			this.questionNumber !== 10 && ++this.questionNumber
		},
		prevQuestion() {
			this.questionNumber !== 0 && --this.questionNumber
		}
	}
}
</script>