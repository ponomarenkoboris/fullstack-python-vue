import { mdiExitToApp } from "@mdi/js";
import axios from "axios";
import { endpoints, SERVER_URL } from "../utils";

const logoutMixin = {
    data: () => ({
        logoutIcon: mdiExitToApp,
    }),
    methods: {
        async logout() {
            try {
                const response = await axios.post(SERVER_URL + endpoints.logout, {}, { withCredentials: true })
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