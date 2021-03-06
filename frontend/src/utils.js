export const SERVER_URL = window.location.hostname !== 'quiz-client-app.herokuapp.com' ?
    'http://127.0.0.1:8000/api.quiz/'
    : 'https://quiz-server-app.herokuapp.com/api.quiz/'

export const endpoints = {
    quizList: 'quiz-list/',
    userGrading: 'user-grading/',
    questionsList: 'questions-list/',
    questionsGroup: 'questions-group/',
    quizFullStatistic: 'quiz-full-statistic/',
    login: 'login/',
    register: 'register/',
    logout: 'logout/',
    refresh: 'refresh/'
}