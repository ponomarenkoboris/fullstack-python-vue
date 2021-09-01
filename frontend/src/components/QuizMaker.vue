<template>
    <v-form ref="form" v-model="validForm" lazy-validation>
        <v-container>
            <v-text-field label="Название опроса" :rules="rules" v-model="quiz.quiz_name"></v-text-field>
            <v-text-field label="Описание опроса" :rules="rules" v-model="quiz.description"></v-text-field>
            <v-divider class="mb-6 mt-6"></v-divider>
            <v-container>
                <div class="d-flex justify-space-between">
                    <h1>Колличество вопросов: {{ quiz.questions.length }}</h1>
                    <h2>Максимальный балл за прохождение опроса: {{ quiz_max_grade }}</h2>
                </div>
                <div v-for="questionObj in quiz.questions" :key="questionObj.id">
                    <v-divider v-if="questionObj.id !== 1" class="mb-6 mt-6"></v-divider>
                    <div class="d-flex">
                        <v-text-field
                            v-model="questionObj.question"
                            :rules="questionRules"
                            label="Вопрос:"
                        ></v-text-field>
                        <v-hover>
                            <v-icon @click="removeQuestion(questionObj.id)">{{ trashIcon }}</v-icon>
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
                        />
                    </div>

                    <div class="d-flex justify-center mb-3">
                        <v-radio-group
                            v-model="questionObj.multiple"
                            row
                            @change="() => questionObj.multiple ? questionObj.answer = [] : questionObj.answer = ''"
                        >
                            <v-radio label="Один ответ" :value="false"></v-radio>
                            <v-radio label="Несколько ответов" :value="true"></v-radio>
                        </v-radio-group>
                    </div>
                    <div class="d-flex justify-center">
                        <v-btn
                            @click="() => questionObj.variants.push({ id: questionObj.variants.length + 1, variant: '', score: 0 })"
                        >
                            <v-icon class="mr-3">{{ addVariantIcon }}</v-icon>Добавить вариант ответа
                        </v-btn>
                    </div>
                    <!-- If one answer -->
                    <v-container v-if="!questionObj.multiple" class="d-flex justify-center">
                        <v-radio-group
                            v-model="questionObj.answer"
                            :rules="[() => !!questionObj.answer.length || 'Необходимо отметить правильный вариант ответа']"
                        >
                            <v-row
                                v-for="variant in questionObj.variants"
                                :key="variant.id"
                                class="d-flex align-center"
                            >
                                <div class="mr-6">
                                    <v-radio
                                        v-model="variant.variant"
                                        :disabled="!variant.variant.trim()"
                                    ></v-radio>
                                </div>
                                <div style="width: 500px; margin-right: 10px;">
                                    <v-text-field
                                        style="width: 500px;"
                                        v-model="variant.variant"
                                        :rules="questionRules"
                                        label="Вариант ответа"
                                    ></v-text-field>
                                </div>
                                <div style="width: 500px;">
                                    <v-text-field
                                        type="number"
                                        v-model.number="variant.score"
                                        :rules="inputNumberRules"
                                        outlined
                                        label="Балл за выбранный вариант"
                                    ></v-text-field>
                                </div>
                                <v-hover>
                                    <v-icon
                                        @click="removeVariant(questionObj.id, variant.id)"
                                    >{{ removeVariantIcon }}</v-icon>
                                </v-hover>
                            </v-row>
                        </v-radio-group>
                    </v-container>

                    <!-- If multiple answer -->
                    <!-- TODO stile for checkbox validation -->
                    <v-container v-else>
                        <v-row
                            v-for="variant in questionObj.variants"
                            :key="variant.id"
                            class="d-flex justify-center align-center mt-3"
                        >
                            <v-checkbox
                                v-model="questionObj.answer"
                                :value="variant"
                                :disabled="!variant.variant.trim()"
                                :rules="[() => !!questionObj.answer.length || 'Необходимо отметить правильный вариант ответа']"
                            ></v-checkbox>
                            <div style="width: 500px; margin-right: 10px;">
                                <v-text-field
                                    style="width: 500px;"
                                    v-model="variant.variant"
                                    :rules="questionRules"
                                    label="Вариант ответа"
                                ></v-text-field>
                            </div>
                            <div style="width: 500px;">
                                <v-text-field
                                    type="number"
                                    v-model.number="variant.score"
                                    :rules="inputNumberRules"
                                    outlined
                                    label="Балл за выбранный вариант"
                                ></v-text-field>
                            </div>
                            <v-hover>
                                <v-icon
                                    @click="removeVariant(questionObj.id, variant.id)"
                                >{{ removeVariantIcon }}</v-icon>
                            </v-hover>
                        </v-row>
                    </v-container>
                </div>
                <v-row justify="space-between" align="center" class="mt-3">
                    <v-btn @click="appendQuestion()">
                        <v-icon class="mr-3">{{ addQuestionIcon }}</v-icon>Добавить вопрос
                    </v-btn>

                    <!-- START Dialog for adding created question -->
                    <v-dialog v-model="dialog" scrollable max-width="300px">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn color="primary" dark v-bind="attrs" v-on="on">
                                <v-icon class="mr-3">{{ addQuestionFromGroupIcon }}</v-icon>Добавить вопрос из группы
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title>Выберите вопрос</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text style="height: 300px;" class="d-flex justify-center">
                                <v-progress-circular
                                    v-if="!questionGroups.length"
                                    :size="70"
                                    :width="7"
                                    color="primary"
                                    indeterminate
                                    class="mt-3"
                                ></v-progress-circular>
                                <v-radio-group v-model="selectedQuestion" column>
                                    <v-container v-for="group in questionGroups" :key="group.id">
                                        <h4>{{ group.group_name }}</h4>
                                        <v-radio
                                            v-for="question in group.questions"
                                            :key="question.id"
                                            :value="question.id"
                                            :label="question.question"
                                        ></v-radio>
                                    </v-container>
                                </v-radio-group>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-btn color="blue darken-1" text @click="dialog = false">Закрыть</v-btn>
                                <v-btn
                                    color="blue darken-1"
                                    text
                                    @click="appendQuestion(true)"
                                >Добавить</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <!-- END Dialog for adding created question -->
                </v-row>
            </v-container>
            <v-divider class="mb-6 mt-6"></v-divider>
            <!-- Calendar -->
            <v-container class="d-flex flex-column align-center">
                <v-sheet
                    class="rounded-lg pa-4 mb-2 d-flex flex-column align-center"
                    elevation="5"
                    width="520"
                >
                    <strong>Выбирете день, когда опрос будет доступен для прохождения</strong>
                    <v-date-picker class="mt-2" locale="ru-RU" v-model="publishDate" full-width />
                </v-sheet>
            </v-container>
            <!-- end calendar -->
            <v-container class="d-flex justify-center">
                <v-btn
                    @click="publishQuiz"
                    :disabled="!quiz.questions.length"
                    color="light-green accent-2"
                >
                    <v-icon class="mr-2">{{ publishQuizIcon }}</v-icon>Опубликовать опрос
                </v-btn>
            </v-container>
        </v-container>
    </v-form>
</template>
<script>
import {
    mdiDelete,
    mdiClose,
    mdiPencilPlus,
    mdiPlusBoxMultiple,
    mdiCloudCheck,
    mdiConnection
} from '@mdi/js';
import axios from 'axios'
import { SERVER_URL, endpoints, getCSRFTokenHeader } from "../utils";
import alertMixin from "../mixins/alert";
export default {
    name: 'QuizMaker',
    mixins: [alertMixin],
    computed: {
        quiz_max_grade() {
            let max_grade = 0
            this.quiz.questions.forEach(question => {
                if (question.multiple) {
                    const answer = question.answer.map(item => item.variant).join(',')
                    max_grade += question.variants.reduce((prev, curr) => answer.indexOf(curr.variant) > -1 ? prev += curr.score : prev, 0)
                }
                max_grade += question.variants.reduce((prev, curr) => {
                    return question.answer.indexOf(curr.variant) > -1 ? prev += curr.score : prev
                }, 0)
            })
            return max_grade
        }
    },
    data: () => ({
        validForm: true,
        dialog: false,
        selectedQuestion: '',
        questionGroups: [],
        publishDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        rules: [
            value => !!value || 'Обязательное поле',
            value => (value && value.length >= 5) || 'Минимальное колличество букв: 5'
        ],
        questionRules: [
            value => !!value.trim() || 'Обязательное поле'
        ],
        inputNumberRules: [
            value => value.toString().length >= 0 || 'Необходимо ввести число'
        ],
        quiz: {
            quiz_name: '',
            description: '',
            questions: []
        },
        checkboxValue: '',
        trashIcon: mdiDelete,
        removeVariantIcon: mdiClose,
        addVariantIcon: mdiPencilPlus,
        addQuestionIcon: mdiPlusBoxMultiple,
        publishQuizIcon: mdiCloudCheck,
        addQuestionFromGroupIcon: mdiConnection
    }),
    watch: {
        dialog(_, oldDialogValue) {
            !oldDialogValue ? this.fetchQuestionGroups() : this.questionGroups = []
        },
    },
    methods: {
        appendQuestion(fetchedQuestion = false) {
            if (fetchedQuestion) {
                let question = {}
                this.questionGroups.forEach(group => {
                    const specificQuestion = group.questions.find(question => question.id === +this.selectedQuestion)
                    if (specificQuestion) question = { ...specificQuestion, id: this.quiz.questions.length, question_group: null }
                })
                if (question.multiple) {
                    question.answer = question.answer.split(',').map(answer => {
                        return question.variants.find(variant => variant.variant === answer)
                    })
                }
                this.quiz.questions.push(question)
                this.dialog = false
            } else {
                this.quiz.questions.push({
                    id: this.quiz.questions.length,
                    question: '',
                    multiple: false,
                    variants: [],
                    answer: []
                })
            }
        },
        async fetchQuestionGroups() {
            try {
                const refresh = await axios.post(SERVER_URL + endpoints.refresh, { email: localStorage.getItem('manager_email') }, { withCredentials: true })
                if (refresh.status !== 200) throw new Error({ message: 'Not authorized' })
                const response = await axios.get(SERVER_URL + endpoints.questionsGroup, { withCredentials: true })
                this.questionGroups = response.data
            } catch (e) {
                this.raiseAlert('Неудалось соединиться с сервером.')
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
            if (!isValid || !this.quiz.questions.length) return
            const notReactiveQuiz = JSON.parse(JSON.stringify(this.quiz))
            notReactiveQuiz.quiz_max_grade = this.quiz_max_grade
            notReactiveQuiz.questions.forEach(question => {
                if (question.multiple && question.answer.length) {
                    question.answer = question.answer.length === 1 ?
                        question.answer[0].variant :
                        question.answer.map(answer => answer.variant).join(',')
                } else if (question.multiple) {
                    question.answer = ''
                } else if (typeof question.answer === 'undefined') {
                    question.answer = ''
                }
                question.question_max_grade = question.variants.reduce((prev, curr) => {
                    if (question.multiple) {
                        return question.answer.indexOf(curr.variant) > -1 ? prev += curr.score : prev
                    }
                    return prev >= curr.score ? prev : curr.score
                }, 0)
            })
            notReactiveQuiz['publish_date'] = Math.floor(new Date(new Date(this.publishDate).getTime() - 10800000) / 1000)
            try {
                const refresh = await axios.post(SERVER_URL + endpoints.refresh, { email: localStorage.getItem('manager_email') }, { withCredentials: true })
                if (refresh.status !== 200) throw new Error({ message: 'Not authorized' })
                const response = await axios.post(SERVER_URL + endpoints.quizList, {
                    ...notReactiveQuiz
                }, { withCredentials: true })
                if (response.status === 200) {
                    this.quiz = {
                        quiz_name: '',
                        description: '',
                        questions: []
                    }
                    this.publishDate = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
                }
            } catch (e) {
                console.error(e)
                this.raiseAlert("Невозмодно отправить запрос на сервер. Повторите позже.")
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