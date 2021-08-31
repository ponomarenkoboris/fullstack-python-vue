export const SERVER_URL = window.location.hostname !== 'quiz-client-vue.herokuapp.com' ?
    'http://127.0.0.1:8000/api.quiz/'
    : 'https://quiz-backend-server.herokuapp.com/api.quiz/'

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

const csrfTokenHeader = () => {
    let csrftoken = null

    return () => {
        if (document.cookie && document.cookie !== '' && !csrftoken) {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                    csrftoken = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                    break;
                }
            }
        }

        return { 'X-CSRFToken': csrftoken }
    }
}

export const getCSRFTokenHeader = csrfTokenHeader()