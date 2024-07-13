<template>
    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />

    <!--ボタン -->
    <svg @click="logout" xmlns="http://www.w3.org/2000/svg" height="32" width="32" viewBox="0 0 24 24" fill="currentColor">
        <path d="M0 0h24v24H0z" fill="none" />
        <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z" />
    </svg>
</template>

<script>
import VueElementLoading from "vue-element-loading";

export default {
    components: {
        VueElementLoading
    },
    data() {
        return {
            loading: false,
        }
    },
    methods: {
        async logout() {
            function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)) }

            this.loading = true;
            await sleep(2000);
            sessionStorage.clear();
            this.loading = false;
            this.$router.push("/");
        }
    }
}
</script>
