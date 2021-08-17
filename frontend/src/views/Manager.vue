<template>
    <v-container>
        <v-container class="d-flex justify-space-between px-10">
            <v-tabs>
                <v-tab to="/manager/full-statistic/">
                    <p>Просмотр статистики</p>
                </v-tab>
                <v-tab to="/manager/quiz-maker/">
                    <p>Создание опроса</p>
                </v-tab>
                <v-tab to="/manager/questions-groups/">
                    <p>Группы вопросов</p>
                </v-tab>
            </v-tabs>
            <div class="manager__info">
                <p>Имя: <strong>{{ name }}</strong></p>
                <p>Фамилия: <strong>{{ surname }}</strong></p>
                <p>email: <strong>{{ email }}</strong></p>
            </div>
        </v-container>
        <v-container>
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </v-container>
    </v-container>
</template>
<script>
import Statistic from '../components/Statistic.vue'
export default {
    name: 'Admin',
    components: {
        Statistic
    },
    computed: {
        name:() => localStorage.getItem('manager_name'),
        surname:() => localStorage.getItem('manager_surname'),
        email:() => localStorage.getItem('manager_email')
    }
}
</script>
<style scoped>
.manager__info > p {
    margin: 0
}
</style>