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

                    <!-- TODO styles and complete multiple answer logic changing on single answer question -->

                    <v-radio-group v-model="questionObj.multiple">
                        <v-radio label="Один ответ" :value="false"></v-radio>
                        <v-radio label="Несколько ответов" :value="true"></v-radio>
                    </v-radio-group>

                    <!-- If one answer -->
                    <v-container v-if="!questionObj.multiple">
                        <v-radio-group v-model="questionObj.answer">
                            <v-container v-for="variant in questionObj.variants" class="d-flex align-center">
                                <div class="mr-6">
                                    <v-radio
                                        v-model="variant.variant"
                                        :disabled="!variant.variant.trim()"
                                    ></v-radio>
                                </div>
                                <div width="500">
                                    <v-text-field v-model="variant.variant"></v-text-field>
                                </div>
                            </v-container>
                        </v-radio-group>
                    </v-container>

                    <!-- If multiple answer options -->
                    <v-container v-else>
                        <v-container v-for="variant in questionObj.variants" :key="variant.id" class="d-flex align-center">
                            <v-checkbox
                                v-model="questionObj.answer"
                                :value="variant"
                            ></v-checkbox>
                            <v-text-field v-model="variant.variant"></v-text-field>
                        </v-container>
                        <h1>{{ questionObj.answer }}</h1>
                    </v-container>
                    <v-btn @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, variant: '' })">Добавить вариант ответа</v-btn>
                </div>
            </form>
            <v-btn @click="addQuestion">Добавить вопрос</v-btn>
        </v-container>
        <v-divider class="mb-6 mt-6"></v-divider>
        <v-container class="d-flex justify-center">
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
                answer: []
            })
        },
        publishQuiz() {
            const quiz = JSON.parse(JSON.stringify(this.quiz))
            console.log(quiz)
            // axios.post(SERVER_URL + endpoints.createQuiz, {
            //     // TODO add logic
            // })
            console.log('publishing quiz...');
        }
    }
}
</script>