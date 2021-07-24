<template>
    <v-container>
        <v-text-field label="Название опроса" :rules="rules" v-model="quiz.name"></v-text-field>
        <v-text-field label="Описание опроса" :rules="rules" v-model="quiz.description"></v-text-field>
        <v-divider class="mb-6 mt-6"></v-divider>
        <v-container>
            <h1>Вопросы</h1>
            <form>
                <div v-for="questionObj in quiz.questions" :key="questionObj.id">
                    <v-divider v-if="questionObj.id !== 1" class="mb-6 mt-6"></v-divider>
                    <v-text-field v-model="questionObj.question" label="Вопрос:"></v-text-field>
                    
                    <!-- RADIO TODO Buttons -->

                    <v-radio-group v-model="questionObj.multiple">
                        <v-radio label="Один ответ" :value="false"></v-radio>
                        <v-radio label="Несколько ответов" :value="true"></v-radio>
                    </v-radio-group>

                    <!-- If one answer -->
                    <v-container v-if="!questionObj.multiple">
                        <v-text-field v-model="questionObj.answer" label="Ответ:"></v-text-field>
                    </v-container>

                    <!-- If multiple answer options -->
                    <!-- TODO стилизовать унпуты -->
                    <v-container v-else>
                        <v-container v-for="variant in questionObj.variants" :key="variant.id">
                            <v-checkbox :label="variant.answer"></v-checkbox>
                            <v-text-field v-model="variant.answer"></v-text-field>
                        </v-container>
                        <v-btn @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, answer: '' })">Добавить вариант</v-btn>
                    </v-container>
                </div>
            </form>
            <v-btn @click="addQuestion">Добавить вопрос</v-btn>
        </v-container>
        <v-divider class="mb-6 mt-6"></v-divider>
        <v-container class="d-flex justify-center">
            <v-btn @click="saveQuiz" class="mr-6">Сохранить</v-btn>
            <v-btn @click="publishQuiz" color="light-green accent-2">Опубликовать</v-btn>
        </v-container>
    </v-container>
</template>
<script>
export default {
    name: 'QuizMaker',
    data: () => ({
        rules: [
            value => !!value || 'Обязательное поле',
            value => (value && value.length >= 5) || 'Минимальное колличество букв: 5'
        ],
        questionsConut: 0,
        quiz: {
            name: '',
            description: '',
            questions: []
        },
        checkboxValue: '',
    }),
    methods: {
        addQuestion() {
            this.questionsConut++
            this.quiz.questions.push({ 
                id: this.questionsConut, 
                question: '', 
                multiple: false,
                variants: [],
                answer: null 
            })
        },
        append(e) {
            this.checkboxValue = e
        },
        saveQuiz() {
            Object.keys(this.quiz).forEach(key => {
                console.log(this.quiz[key]);
            })
        },
        publishQuiz() {
            this.saveQuiz()
            console.log('publishing quiz...');
        }
    }
}
</script>