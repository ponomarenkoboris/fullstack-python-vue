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

                    <!-- TODO styles and complete multiple answer logic -->

                    <v-radio-group v-model="questionObj.multiple">
                        <v-radio label="Один ответ" :value="false"></v-radio>
                        <v-radio label="Несколько ответов" :value="true"></v-radio>
                    </v-radio-group>

                    <!-- If one answer -->
                    <v-container v-if="!questionObj.multiple">
                        <v-radio-group v-model="questionObj.answer">
                            <v-container v-for="variant in questionObj.variants" class="d-flex align-center justify-space-between">
                                <div class="mr-6">
                                    <v-radio :label="variant.answer"></v-radio>
                                </div>
                                <div width="500">
                                    <v-text-field v-model="variant.answer"></v-text-field>
                                </div>
                            </v-container>
                        </v-radio-group>
                        <v-btn @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, answer: '' })">Добавить вариант овтета</v-btn>
                    </v-container>

                    <!-- If multiple answer options -->
                    <v-container v-else>
                        <v-container v-for="variant in questionObj.variants" :key="variant.id" class="d-flex align-center">
                            <v-checkbox :label="variant.answer"></v-checkbox>
                            <v-text-field v-model="variant.answer"></v-text-field>
                        </v-container>
                        <v-btn @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, answer: '' })">Добавить вариант ответа</v-btn>
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
import { axios } from 'axios'
import { SERVER_URL, endpoints } from "../utils";

export default {
    name: 'QuizMaker',
    data: () => ({
        rules: [
            value => !!value || 'Обязательное поле',
            value => (value && value.length >= 5) || 'Минимальное колличество букв: 5'
        ],
        questionsCount: 0,
        quiz: {
            name: '',
            description: '',
            questions: []
        },
        checkboxValue: '',
    }),
    methods: {
        addQuestion() {
            this.questionsCount++
            this.quiz.questions.push({
                id: this.questionsCount,
                question: '',
                multiple: false,
                variants: [],
                answer: null
            })
        },
        saveQuiz() {
            Object.keys(this.quiz).forEach(key => {
                console.log('this.quiz[key]', this.quiz[key]);
            })
        },
        publishQuiz() {
            this.saveQuiz()
            // axios.post(SERVER_URL + endpoints.createQuiz, {
            //     // TODO add logic
            // })
            console.log('publishing quiz...');
        }
    }
}
</script>