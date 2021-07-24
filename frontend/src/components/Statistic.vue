<template>
    <v-container>
        <h1>Statistic components</h1>
        <div v-for="(statistic, idx) of statisticList" :key="idx">
            <p>{{ statistic }}</p>
        </div>
    </v-container>
</template>
<script>
export default {
    name: 'Statistic',
    computed: {
        statisticList() {
            return this.$store.state.statisticList
        }
    }
}
</script>