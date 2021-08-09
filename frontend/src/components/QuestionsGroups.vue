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
                            v-model="enteredName"
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
                        Сохранить
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-container>
            <v-expansion-panels focusable>
                <v-expansion-panel v-for="(group, idx) in groups" :key="idx">
                    <v-expansion-panel-header>
                        <p>{{ group.name }}</p>
                        <div class="d-flex justify-end">
                            <v-row justify="center">
                                <v-dialog
                                    v-model="dialogQuestion"
                                    persistent
                                    max-width="600px"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn
                                            v-bind="attrs"
                                            v-on="on"
                                        >
                                            <v-icon>{{ addIcon }}</v-icon>
                                            Добавить вопрос
                                        </v-btn>
                                    </template>
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
                                                @click="createNewQuestion(group.id)"
                                            >
                                                Сохранить вопрос
                                            </v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </v-row>
                        </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <div v-for="(question, idx) in group.questions" :key="idx">
                            <p>Вопрос: {{ question.question }}</p>
                            <p>Варианты ответа: </p>
                            <p>Правильный ответ: {{ question.answer }}</p>
                        </div>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-container>
    </v-container>
</template>

<script>
import { mdiPlus } from '@mdi/js';
export default {
    name: "QuestionsGroups",
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
        enteredName: ''
    }),
    methods: {
        createNewGroup() {
            const newGroup = { id: this.groups.length + 1, name: this.enteredName, questions: [] }
            this.groups.push(newGroup)
            this.enteredName = ''
            this.dialogGroup = false
        },
        createNewQuestion(groupId) {
            this.groups.forEach(group => {
                if (group.id === groupId) {
                    group.questions.push(JSON.parse(JSON.stringify(this.question)))
                    this.question.question = ''
                    this.question.multiple = false
                    this.question.variants = []
                    this.question.answer = ''
                    this.question.question_photo = ''
                }
            })
            this.dialogQuestion = false
        },
        changeQuestionPhoto(event) {
            const reader = new FileReader()

            reader.onload = ev => {
                this.question.question_photo = ev.currentTarget.result
            }

            reader.readAsDataURL(event)
        }
    }
}
</script>