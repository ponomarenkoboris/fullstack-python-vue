<template>
    <v-container>
        <v-dialog
            v-model="dialogGroup"
            persistent
            max-width="600px"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    color="primary"
                    dark
                    v-bind="attrs"
                    v-on="on"
                >
                    <v-icon>{{ addIcon }}</v-icon>
                    Создание новой группы вопросов
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="text-h5">Создание группы вопросов</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-text-field
                            label="Введите навзание новой группы"
                            required
                            v-model="enteredGroupName"
                        ></v-text-field>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="dialogGroup = false"
                    >
                        Закрыть
                    </v-btn>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="createNewGroup"
                    >
                        Создать
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-container>
            <!-- START Dialog for creating question -->
            <div class="d-flex justify-end">
                <v-row justify="center">
                    <v-dialog
                        v-model="dialogQuestion"
                        persistent
                        max-width="600px"
                    >
                        <v-card>
                            <v-card-title>
                                <span class="text-h5">Создание вопроса</span>
                            </v-card-title>
                            <v-card-text>
                                <v-container>
                                    <v-text-field
                                        label="Вопрос"
                                        v-model="question.question"
                                    ></v-text-field>
                                    <v-file-input
                                        label="Изображение к вопросу (опционально)"
                                        filled
                                        prepend-icon="mdi-camera"
                                        @change="changeQuestionPhoto($event)"
                                        accept="image/*"
                                    ></v-file-input>
                                    <div class="d-flex justify-center">
                                        <v-radio-group
                                            v-model="question.multiple"
                                            row
                                            @change="() => question.multiple ? question.answer = [] : question.answer = ''"
                                        >
                                            <v-radio label="Один ответ" :value="false"></v-radio>
                                            <v-radio label="Несколько ответов" :value="true"></v-radio>
                                        </v-radio-group>
                                    </div>
                                    <v-container v-if="!question.multiple" class="d-flex justify-center">
                                        <v-radio-group
                                            v-model="question.answer"
                                            :rules="[() => !!question.answer.length || 'Необходимо отметить правильный вариант ответа']"
                                        >
                                            <v-container v-for="variant in question.variants" :key="variant.id" class="d-flex align-center">
                                                <div class="mr-6">
                                                    <v-radio
                                                        v-model="variant.variant"
                                                        :disabled="!variant.variant.trim()"
                                                    ></v-radio>
                                                </div>
                                                <div width="500">
                                                    <v-text-field v-model="variant.variant" :rules="questionRules"></v-text-field>
                                                </div>
                                            </v-container>
                                        </v-radio-group>
                                    </v-container>
                                    <v-container v-else>
                                        <v-container v-for="variant in question.variants" :key="variant.id" class="d-flex justify-center">
                                            <v-checkbox
                                                v-model="question.answer"
                                                :value="variant"
                                                :disabled="!variant.variant.trim()"
                                                :rules="[() => !!question.answer.length || 'Необходимо отметить правильный вариант ответа']"
                                            ></v-checkbox>
                                            <div width="500px">
                                                <v-text-field v-model="variant.variant" :rules="questionRules"></v-text-field>
                                            </div>
                                        </v-container>
                                    </v-container>
                                    <div class="d-flex justify-center">
                                        <v-btn
                                            @click="() => question.variants.push({ id: question.variants.length + 1, variant: '' })"
                                        >Добавить вариант ответа</v-btn>
                                    </div>
                                </v-container>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    color="blue darken-1"
                                    text
                                    @click="dialogQuestion = false"
                                >
                                    Отмена
                                </v-btn>
                                <v-btn
                                    color="blue darken-1"
                                    text
                                    @click="createNewQuestion()"
                                >
                                    Сохранить вопрос
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-row>
            </div>
            <!-- END Dialog for creating question -->
            <v-expansion-panels focusable>
                <v-expansion-panel v-for="(group, index) in groups" :key="group.id">
                    <v-expansion-panel-header>
                        <p>{{ group.group_name }}</p>
                        <div class="d-flex justify-end">
                            <v-btn @click="() => { dialogQuestion = true; groupIndex = index; groupName = group.group_name}">
                                <v-icon>{{ addIcon }}</v-icon>
                                Добавить вопрос
                            </v-btn>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <div v-for="(question, idx) in group.questions" :key="question.id"  class="mt-2">
                            <div>
                                <p>Вопрос: {{ question.question }}</p>
                                <div v-if="question.question_photo" class="d-flex align-center mb-2">
                                    <p class="mr-5">Фотография к вопросу: </p>
                                    <img height="100px" :src="question.question_photo" alt="Фотография к вопросу">
                                </div>
                            </div>
                            <p>Варианты ответа: {{ question.variants.reduce((prev, curr) => (typeof prev === 'string' ? prev : prev.variant) + ', ' + curr.variant) }}</p>
                            <p>Правильный ответ: {{ question.answer }}</p>
                            <hr v-if="idx !== group.questions.length - 1">
                        </div>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-container>
        <v-snackbar v-model="snackbar">
            {{ errorText }}
            <template v-slot:action="{ attrs }">
                <v-btn
                    color="pink"
                    text
                    v-bind="attrs"
                    @click="removeAlert"
                >
                    Close
                </v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script>
import { mdiPlus } from '@mdi/js';
import axios from 'axios'
import { SERVER_URL, endpoints } from "../utils";
import alertMixin from "../mixins/alert";

export default {
    name: "QuestionsGroups",
    mixins: [alertMixin],
    data: () => ({
        dialogGroup: false,
        dialogQuestion: false,
        addIcon: mdiPlus,
        questionRules: [
            value => !!value.trim() || 'Обязательное поле'
        ],
        groups: [],
        question: {
            question: '',
            multiple: false,
            variants: [],
            answer: '',
            question_photo: ''
        },
        groupIndex: null,
        groupName: null,
        enteredGroupName: ''
    }),
    watch: {
        dialogQuestion(_, oldDialogQuestion) {
            if (oldDialogQuestion) {
                this.question.question = ''
                this.question.multiple = false
                this.question.variants = []
                this.question.answer = ''
                this.question.question_photo = ''
                this.groupIndex = null
                this.groupName = null
            }
        },
        dialogGroup(_, oldDialogGroup) {
            if (oldDialogGroup) this.enteredGroupName = ''
        }
    },
    methods: {
        async createNewGroup() {
            try {
                const newGroup = { group_name: this.enteredGroupName, questions: [] }
                const response = await axios.post(SERVER_URL + endpoints.questionGroups, newGroup)
                const createdGroup = await response.data
                this.groups.push(createdGroup)
                this.enteredGroupName = ''
                this.dialogGroup = false
            } catch (e) {
                console.error(e)
            }
        },
        async createNewQuestion() {
            const question = JSON.parse(JSON.stringify(this.question))
            if (question.multiple && question.answer.length) {
                question.answer = question.answer.reduce((prev, curr) => prev.variant + ',' + curr.variant)
            } else if (question.multiple) {
                question.answer = ''
            } else if (typeof question.answer === 'undefined') {
                question.answer = ''
            }

            try {
                const response = await axios.put(SERVER_URL + endpoints.questionGroups,{ group_name: this.groupName, questions: [question] })
                const updatedGroup = await response.data
                this.groups.splice(this.groupIndex, 1, updatedGroup)
            } catch (e) {
                console.error(e)
            }
            this.dialogQuestion = false
        },
        async getQuestionGroups() {
            try {
                const response = await axios.get(SERVER_URL + endpoints.questionGroups)
                this.groups = response.data
            } catch (e) {
                console.error(e)
            }
        },
        changeQuestionPhoto(event) {
            const reader = new FileReader()

            reader.onload = ev => {
                console.log(ev.currentTarget.result)
                this.question.question_photo = ev.currentTarget.result
            }

            reader.readAsDataURL(event)
        },
    },
    mounted() {
        this.getQuestionGroups()
    }
}
</script>