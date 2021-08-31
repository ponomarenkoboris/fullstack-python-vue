import { mdiExitToApp } from "@mdi/js";
import axios from "axios";
import { endpoints, SERVER_URL, getCSRFTokenHeader } from "../utils";

const logoutMixin = {
    data: () => ({
        logoutIcon: mdiExitToApp,
    }),
    methods: {
        async logout() {
            try {
                const config = { withCredentials: true, headers: getCSRFTokenHeader() }
                const response = await axios.post(SERVER_URL + endpoints.logout, {}, config)
                if (response.status === 200) {
                    localStorage.clear()
                    this.$router.replace('/')
                }
            } catch (e) {
                this.raiseAlert('Неудалось выполнить выход. Попробуйте позже.')
            }
        }
    }
}
export default logoutMixin