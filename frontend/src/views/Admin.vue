<template>
    <v-container>
        <v-tabs>
            <v-tab to="/admin/full-statistic">
                <p>Watch statistic</p>
            </v-tab>
            <v-tab to="/admin/quiz-maker">
                <p>Create quiz</p>
            </v-tab>
        </v-tabs>
        <v-container>
            <router-view></router-view>
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
}
</script>
<style scoped>
</style>