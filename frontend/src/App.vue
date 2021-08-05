<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
    name: 'App',
    mounted() {
        // TODO make auth check if user or admin
        // const jwt = document.cookie.split(';')[0]
        // if (jwt.split('=')[1] && localStorage.getItem('user_email')
        //     && localStorage.getItem('user_name')
        //     && localStorage.getItem('user_surname')) {
        //     this.$router.push('/user')
        //         .catch(() => {})
        // }
    }
};
</script>
