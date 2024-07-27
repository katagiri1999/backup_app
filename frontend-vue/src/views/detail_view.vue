<template>
    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component />

    <mavon-editor
        language="en"
        :toolbars="markdownOption"
        v-model="text"
        @save="save()"
    />

    <div class="detail_btn">
        <button @click="save()" type="button" class="btn btn btn-outline-secondary">Save</button>
        <button @click="back()" type="button" class="btn btn btn-outline-secondary">Back to List</button>
    </div>
</template>

<style>
.detail_btn {
    margin-top: 3%;
    margin-bottom: 3%;

    button {
        margin-left: 1%;
    }
}

@media screen and (max-width: 768px) {}
</style>

<script>
import { defineComponent, ref } from 'vue';
import { common_headers, common_requests } from "../components/common_func_component.js";
import header_component from "../components/header_component.vue";
import VueElementLoading from "vue-element-loading";


export default defineComponent({
    components: {
        VueElementLoading, header_component
    },
    setup() {
        const loading = ref(false);
        const task_id = ref((new URL(document.location)).searchParams.get("task_id"));
        const team_id = ref((new URL(document.location)).searchParams.get("team_id"));
        const text = ref("");
        const markdownOption = ref({
            bold: true,
            italic: true,
            header: true,
            underline: true,
            strikethrough: true,
            mark: true,
            superscript: true,
            subscript: true,
            quote: true,
            ol: true,
            ul: true,
            link: true,
            code: true,
            table: true,
            fullscreen: true,
            subfield: true,
            preview: true,
            help: true,
        });

        const created = async () => {
            loading.value = true;

            var res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/tasks`,
                "GET",
                common_headers(),
                { task_id: task_id.value }
            );
            text.value = res.contents[0].detail;

            loading.value = false;
        }

        const save = async () => {
            loading.value = true;

            var res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/tasks?task_id=${task_id.value}`,
                "PUT",
                common_headers(),
                { detail: text.value }
            );
            console.log(res);

            loading.value = false;
        }

        const back = async () => {
            loading.value = true;
            location.href = `../tasks?team_id=${team_id.value}`;
        }

        created();
        return {
            loading, task_id, team_id, text, markdownOption, created, save, back
        }
    },
})
</script>
