<template>
    <v-container>
        <v-dialog
            v-model="dialog"
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
                    <v-icon>{{ addGroupIcon }}</v-icon>
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
                        @click="dialog = false"
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
            <p v-for="(name, idx) in groupsNames" :key="idx">{{ name }}</p>
        </v-container>
    </v-container>
</template>

<script>
import { mdiPlus } from '@mdi/js';
export default {
    name: "QuestionsGroups",
    data: () => ({
        dialog: false,
        addGroupIcon: mdiPlus,
        groupsNames: [],
        enteredName: ''
    }),
    methods: {
        createNewGroup() {
            this.groupsNames.push(this.enteredName)
            this.enteredName = '1'
            this.dialog = false
        }
    }
}
</script>

<style scoped>

</style>