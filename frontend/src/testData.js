// Test server data
export const quizList = [
    {
        id: 1,
        name: 'Опрос об условиях работы',
        complite: '5/10',
        done: false,
        decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ea commodo consequat',
        questions: [
            {
                id: 1,
                question: 'fjdfoisi idjsif?',
                multiple: true,
                variants: [
                    {
                        id: 1,
                        answer: 'djifdji'
                    },
                    {
                        id: 2,
                        answer: 'bla bla bla'
                    },
                    {
                        id: 3,
                        answer: 'sulfat'
                    },
                    {
                        id: 4,
                        answer: 'gfjfjfj'
                    }
                ],
                answer: null
            },
            {
                id: 2,
                question: 'lllllllllllllllllllll?',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 3,
                question: 'ddddddddddddddd?',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 4,
                question: 'ccccccccccccccccccc?',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 5,
                question: 'xxxxxxxxxxxxxxxx',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 6,
                question: 'eeeeeeeeeeeeeee',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 7,
                question: 'rrrrrrrrrrrrrrrrrrrrrrr?',
                multiple: true,
                variants: [
                    {
                        id: 1,
                        answer: 'djifdji'
                    },
                    {
                        id: 2,
                        answer: 'bla bla bla'
                    },
                    {
                        id: 3,
                        answer: 'sulfat'
                    },
                    {
                        id: 4,
                        answer: 'gfjfjfj'
                    }
                ]
            },
            {
                id: 8,
                question: 'tttttttttttttttttt?',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 9,
                question: 'jjjjjjjjjjjjjjjjjjjjj?',
                variants: [],
                multiple: false,
                answer: null
            },
            {
                id: 10,
                question: 'last question in quiz?',
                variants: [],
                multiple: false,
                answer: null
            },
        ]
    },
    {
        id: 2,
        name: 'Опрос по оборудованию',
        complite: '0/10',
        done: false,
        decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ea commodo consequat',
        questions: []
    },
    {
        id: 3,
        name: 'Самочувствие',
        complite: '6/10',
        done: true,
        decription: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
        questions: []
    }
]