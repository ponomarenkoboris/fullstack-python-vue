<template>
    <v-container>
        <v-container>
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
            <v-container class="d-flex justify-space-between">
                <div class="manager__info d-flex flex-column">
                    <p>Имя: <strong>{{ name }}</strong>&nbsp;</p>
                    <p>Фамилия: <strong>{{ surname }}</strong>&nbsp;</p>
                    <p>email: <strong>{{ email }}</strong>&nbsp;</p>
                </div>
                <v-btn
                    class="red lighten-2"
                    @click="logout"
                >
                    <span class="white--text">Logout</span>
                    <v-icon class="white--text">
                        {{ logoutIcon }}
                    </v-icon>
                </v-btn>
            </v-container>
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
import logoutMixin from "../mixins/logoutMixin";

export default {
    name: 'Admin',
    components: {
        Statistic
    },
    mixins: [logoutMixin],
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