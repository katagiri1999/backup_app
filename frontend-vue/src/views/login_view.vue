<template>
    <vue-element-loading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component msg="Login" />

    <div class="login">
        <img src="@/assets/google_login.svg" class="login-btn" @click="google_signin">
    </div>
</template>

<style>
.login {
    margin: 5%;
    padding: 7%;
    text-align: center;
    border-style: outset;
    border-radius: 1%;
    border-width: 3px;

    .login-btn {
        width: 20%;
        cursor: pointer;
    }

    .login-btn:hover {
        opacity: 0.7;
    }
}

@media screen and (max-width: 768px) {
    .login {
        .login-btn {
            width: 80%;
        }
    }
}
</style>

<script>
import header_component from "..//components/header_component.vue";
import common_func_component from "../components/common_func_component.vue";
import VueElementLoading from "vue-element-loading";

export default {
    mixins: [common_func_component],
    data() {
        return {
            loading: true,
        }
    },
    components: {
        header_component, VueElementLoading
    },
    async created() {
        var code = (new URL(document.location)).searchParams.get("code");
        if (!code) {
            this.loading = false;
            return null;
        }

        this.loading = true;

        var url = new URL(document.location);
        var state = url.searchParams.get("state");
        if (state != sessionStorage.getItem("state")) {
            sessionStorage.clear();
            throw Error("Not Same State");
        }
        history.replaceState("", "", url.pathname);
        var api_url = `${process.env.VUE_APP_API_BASE}/login`;

        var is_local = location.href.includes('localhost') || location.href.includes('127.0.0.1');

        var headers = this.common_headers();
        var res = await this.common_requests(api_url, "POST", headers, { authorization_code: code, local: is_local });

        sessionStorage.setItem("token", res.id_token);
        sessionStorage.setItem("user_id", res.user_id);

        this.loading = false;
        this.$router.push("/tasks");
    },
    methods: {
        async google_signin() {
            console.log("google_signin");

            var state = Math.random().toString(36).slice(-8);
            sessionStorage.setItem("state", state);
            window.location = `${process.env.VUE_APP_GOOGLE_AUTH}&state=${state}`
        },
    }
}
</script>
