<template>
    <vue-element-loading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component />

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
import { defineComponent, ref } from 'vue';
import { common_headers, common_requests } from "../components/common_func_component.js";
import header_component from "../components/header_component.vue";
import VueElementLoading from "vue-element-loading";
import { useRouter } from 'vue-router';


export default defineComponent({
    components: {
        VueElementLoading, header_component,
    },
    setup() {
        const loading = ref(false);

        const router = useRouter();

        const created = async () => {
            var code = (new URL(document.location)).searchParams.get("code");
            if (!code) {
                loading.value = false;
                return null;
            }

            loading.value = true;

            var url = new URL(document.location);
            var state = url.searchParams.get("state");
            if (state != sessionStorage.getItem("state")) {
                sessionStorage.clear();
                throw Error("Not Same State");
            }
            history.replaceState("", "", url.pathname);
            var api_url = `${process.env.VUE_APP_API_BASE}/login`;

            var res = await common_requests(
                api_url,
                "POST",
                common_headers(),
                { authorization_code: code, redirect_uri: process.env.VUE_APP_REDIRECT_URI }
            );

            sessionStorage.setItem("token", res.id_token);
            sessionStorage.setItem("user_id", res.user_id);

            router.push('/tasks');
        }

        const google_signin = async () => {
            console.log("google_signin");

            var state = Math.random().toString(36).slice(-8);
            sessionStorage.setItem("state", state);
            var params = new URLSearchParams({
                state: state,
                response_type: "code",
                prompt: "select_account",
                scope: "email",
                client_id: process.env.VUE_APP_CLIENT_ID,
                redirect_uri: process.env.VUE_APP_REDIRECT_URI,
            });
            location.href = process.env.VUE_APP_GOOGLE_AUTH + "?" + params;
        }

        created();
        return {
            loading, created, google_signin, 
        }
    },
})
</script>
