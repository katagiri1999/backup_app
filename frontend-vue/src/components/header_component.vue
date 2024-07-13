<template>
    <header class="header_header">
        <h1>Back-app</h1>

        <template v-if="after_login">
            <router-link to="/tasks" exact-active-class="active">Tasks</router-link>
        </template>

    </header>
</template>

<style>
.header_header {
    background-color: #373535;
    color: white;
    padding: 20px;
    text-align: center;

    h1 {
        border-bottom: double 3px white;
    }

    h5 {
        padding-top: 1%;
    }

    a {
        color: gray;
    }

    .active {
        color: white;
    }
}
</style>

<script>
export default {
    props: {
        msg: String,
        after_login: Boolean,
    }
}

</script>
