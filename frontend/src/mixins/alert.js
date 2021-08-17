const alertMixin = {
    data: () => ({
        snackbar: false,
        errorText: ''
    }),
    methods: {
        raiseAlert(text) {
            this.errorText = text
            this.snackbar = true
        },
        removeAlert() {
            this.errorText = ''
            this.snackbar = false
        }
    }
}

export default alertMixin