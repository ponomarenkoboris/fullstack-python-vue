<template>
    <v-form
        ref="form"
        v-model="validForm"
        lazy-validation
    >
        <v-container>
            <v-text-field label="Название опроса" :rules="rules" v-model="quiz.name"></v-text-field>
            <v-text-field label="Описание опроса" :rules="rules" v-model="quiz.description"></v-text-field>
            <v-divider class="mb-6 mt-6"></v-divider>
            <v-container>
                <h1>Колличество вопросов: {{ quiz.questions.length }}</h1>
                <div v-for="questionObj in quiz.questions" :key="questionObj.id">
                    <v-divider v-if="questionObj.id !== 1" class="mb-6 mt-6"></v-divider>
                    <div class="d-flex">
                        <v-text-field v-model="questionObj.question" :rules="questionRules" label="Вопрос:"></v-text-field>
                        <v-hover>
                            <v-icon
                                @click="removeQuestion(questionObj.id)"
                            >{{ trashIcon }}</v-icon>
                        </v-hover>
                    </div>

                    <v-file-input
                        label="Изображение к вопросу (опционально)"
                        filled
                        prepend-icon="mdi-camera"
                        @change="changeQuestionPhoto(questionObj.id, $event)"
                        accept="image/*"
                    ></v-file-input>

                    <div class="d-flex justify-center mb-6">
                        <img
                            v-if="questionObj.question_photo"
                            :src="questionObj.question_photo"
                            alt="Фотограффия к вопросу"
                            width="auto"
                            height="200px"
                        >
                    </div>

                    <div class="d-flex justify-center">
                        <v-radio-group
                            v-model="questionObj.multiple"
                            row
                            @change="() => questionObj.multiple ? questionObj.answer = [] : questionObj.answer = ''"
                        >
                            <v-radio label="Один ответ" :value="false"></v-radio>
                            <v-radio label="Несколько ответов" :value="true"></v-radio>
                        </v-radio-group>
                    </div>

                    <!-- If one answer -->
                    <v-container v-if="!questionObj.multiple" class="d-flex justify-center">
                        <v-radio-group
                            v-model="questionObj.answer"
                            :rules="[() => !!questionObj.answer.length || 'Необходимо отметить правильный вариант ответа']"
                        >
                            <v-container v-for="variant in questionObj.variants" :key="variant.id" class="d-flex align-center">
                                <div class="mr-6">
                                    <v-radio
                                        v-model="variant.variant"
                                        :disabled="!variant.variant.trim()"
                                    ></v-radio>
                                </div>
                                <div width="500">
                                    <v-text-field v-model="variant.variant" :rules="questionRules"></v-text-field>
                                </div>
                                <v-hover>
                                    <v-icon
                                        @click="removeVariant(questionObj.id, variant.id)"
                                    >{{ removeVariantIcon }}</v-icon>
                                </v-hover>
                            </v-container>
                        </v-radio-group>
                    </v-container>

                    <!-- If multiple answer -->
                    <!-- TODO stile for checkbox validation -->
                    <v-container v-else>
                        <v-container v-for="variant in questionObj.variants" :key="variant.id" class="d-flex justify-center">
                            <v-checkbox
                                v-model="questionObj.answer"
                                :value="variant"
                                :disabled="!variant.variant.trim()"
                                :rules="[() => !!questionObj.answer.length || 'Необходимо отметить правильный вариант ответа']"
                            ></v-checkbox>
                            <div width="500px">
                                <v-text-field v-model="variant.variant" :rules="questionRules"></v-text-field>
                            </div>
                            <v-hover>
                                <v-icon
                                    @click="removeVariant(questionObj.id, variant.id)"
                                >{{ removeVariantIcon }}</v-icon>
                            </v-hover>
                        </v-container>
                    </v-container>
                    <div class="d-flex justify-center">
                        <v-btn
                            @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, variant: '' })"
                        >Добавить вариант ответа</v-btn>
                    </div>
                </div>
                <v-row justify="space-between" align="center" class="mt-3">
                    <v-btn @click="addNewQuestion(true)">Добавить вопрос</v-btn>

                    <!-- START Dialog for adding created question -->
                    <v-dialog
                        v-model="dialog"
                        scrollable
                        max-width="300px"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                color="primary"
                                dark
                                v-bind="attrs"
                                v-on="on"
                            >
                                Добавить существующий вопрос
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title>Выберите вопрос</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text style="height: 300px;" class="d-flex justify-center">
                                <v-progress-circular
                                    v-if="!allCreatedQuestions.length"
                                    :size="70"
                                    :width="7"
                                    color="primary"
                                    indeterminate
                                    class="mt-3"
                                ></v-progress-circular>
                                <v-radio-group
                                    v-model="selectedQuestion"
                                    column
                                >
                                    <v-radio
                                        v-for="question in allCreatedQuestions"
                                        :key="question.id"
                                        :value="question.id"
                                        :label="question.question"
                                    >
                                    </v-radio>
                                </v-radio-group>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-btn
                                    color="blue darken-1"
                                    text
                                    @click="dialog = false"
                                >
                                    Закрыть
                                </v-btn>
                                <v-btn
                                    color="blue darken-1"
                                    text
                                    @click="addNewQuestion(true)"
                                >
                                    Добавить
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <!-- END Dialog for adding created question -->
                </v-row>

            </v-container>
            <v-divider class="mb-6 mt-6"></v-divider>
            <v-container class="d-flex justify-center">
                <v-btn @click="publishQuiz" color="light-green accent-2">Опубликовать</v-btn>
            </v-container>
        </v-container>
    </v-form>
</template>
<script>
import { mdiDelete, mdiClose } from '@mdi/js';
import axios from 'axios'
import { SERVER_URL, endpoints } from "../utils";

export default {
    name: 'QuizMaker',
    data: () => ({
        validForm: true,
        dialog: false,
        selectedQuestion: '',
        allCreatedQuestions: [],
        rules: [
            value => !!value || 'Обязательное поле',
            value => (value && value.length >= 5) || 'Минимальное колличество букв: 5'
        ],
        questionRules: [
            value => !!value.trim() || 'Обязательное поле'
        ],
        questionsCount: 0,
        quiz: {
            name: '',
            description: '',
            questions: []
        },
        checkboxValue: '',
        trashIcon: mdiDelete,
        removeVariantIcon: mdiClose
    }),
    watch: {
        dialog(_, oldDialogValue) {
            !oldDialogValue ? this.addCreatedQuestion() : this.allCreatedQuestions = []
        }
    },
    methods: {
        addNewQuestion(needToAdd = false) {
            if (this.selectedQuestion && needToAdd) {
                const question = this.allCreatedQuestions.find(question => question.id === +this.selectedQuestion)
                if (question.multiple) {
                    question.answer = question.answer.split(',').map(answer => {
                        return question.variants.find(variant => variant.variant === answer)
                    })
                }
                this.quiz.questions.push(question)
                this.dialog = false
            } else if (needToAdd) {
                this.quiz.questions.push({
                    id: this.questionsCount,
                    question: '',
                    multiple: false,
                    variants: [],
                    answer: []
                })
            }
            this.questionsCount++
        },
        async addCreatedQuestion() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.questionsList)
                console.log(response.data)
                this.allCreatedQuestions = [...response.data]
            } catch (e) {
                console.error(e)
            }
        },
        changeQuestionPhoto(questionId, event) {
            const reader = new FileReader()

            reader.onload = ev => {
                this.quiz.questions = this.quiz.questions.map(question => {
                    if (question.id === questionId) question.question_photo = ev.currentTarget.result
                    return question
                })
            }

            reader.readAsDataURL(event)
        },
        async publishQuiz() {
            const isValid = this.$refs.form.validate()
            if (!isValid) return
            const notReactiveQuiz = JSON.parse(JSON.stringify(this.quiz))

            notReactiveQuiz.questions.forEach(question => {
                if (question.multiple && question.answer.length) {
                    question.answer = question.answer.reduce((prev, curr) => prev.variant + ',' + curr.variant)
                } else if (question.multiple) {
                    question.answer = ''
                } else if (typeof question.answer === 'undefined') {
                    question.answer = ''
                }
            })

            try {
                console.log('publishing quiz...', notReactiveQuiz);
                const response = await axios.post(SERVER_URL + endpoints.createQuiz, {
                    ...notReactiveQuiz
                })
                const data = await response.data
                console.log(data)
            } catch (e) {
                console.error(e)
            }
        },
        removeQuestion(questionId) {
            this.quiz.questions = this.quiz.questions.filter(question => question.id !== questionId)
        },
        removeVariant(questionId, variantId) {
            this.quiz.questions.forEach(question => {
                if (question.id === questionId) {
                    question.variants = question.variants.filter(variant => variant.id !== variantId)
                }
            })
        }
    }
}
</script>