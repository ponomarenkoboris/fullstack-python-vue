<template>
    <v-container>
        <v-card>
            <v-card-title>{{ value }}</v-card-title>
            <v-card-actions>
                <v-btn @click="increase">Click on my</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
export default {
    name: 'Main',
    data: () => ({
        value: 1
    }),
    methods: {
        increase() {
            this.value++
            this.$store.commit('changeName', this.value)
            console.log(this.$store.state.name);
        }
    }
}
</script>