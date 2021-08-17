<template>
    <v-container>
        <v-data-table
            :headers="headers"
            :items="desserts"
            :items-per-page="10"
            class="elevation-1"
        ></v-data-table>
    </v-container>
</template>
<script>
export default {
    name: 'Statistic',
    data: () => ({
        headers: [
            {
                text: 'Email пользователя',
                align: 'start',
                sortable: false,
                value: 'email',
            },
            { text: 'Имя', value: 'name' },
            { text: 'Фамилия', value: 'surname' },
            { text: 'Название опроса', value: 'quiz_name' },
            { text: 'Бал пользователя', value: 'user_grade' },
            { text: 'Максимальный бал', value: 'max_grade' },
        ],
        desserts: [
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
            {
                email: 'boris@mail.com',
                name: 'Boris',
                surname: 'Ponomarenko',
                quiz_name: 'HR опрос',
                user_grade: 4.0,
                max_grade: 10,
            },
        ],
    }),
    computed: {
        statisticList() {
            return this.$store.state.statisticList
        }
    }
}
</script>