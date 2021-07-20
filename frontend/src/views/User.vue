<template>
    <v-container>
        <h1>This is user panel</h1>
        <Quiz />
        <FullStatistic />
        <ActiveQuiz />
    </v-container>
</template>
<script>
import Quiz from '../components/Quiz.vue'
import FullStatistic from '../components/FullStatistic.vue'
import ActiveQuiz from '../components/ActiveQuiz.vue'
export default {
    name: 'User',
    components: {
        Quiz,
        FullStatistic,
        ActiveQuiz
    }
}
</script>