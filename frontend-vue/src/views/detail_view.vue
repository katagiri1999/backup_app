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
        <svg @click="save()" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
            <path d="M11 2H9v3h2z"/>
            <path d="M1.5 0h11.586a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 14.5v-13A1.5 1.5 0 0 1 1.5 0M1 1.5v13a.5.5 0 0 0 .5.5H2v-4.5A1.5 1.5 0 0 1 3.5 9h9a1.5 1.5 0 0 1 1.5 1.5V15h.5a.5.5 0 0 0 .5-.5V2.914a.5.5 0 0 0-.146-.353l-1.415-1.415A.5.5 0 0 0 13.086 1H13v4.5A1.5 1.5 0 0 1 11.5 7h-7A1.5 1.5 0 0 1 3 5.5V1H1.5a.5.5 0 0 0-.5.5m3 4a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5V1H4zM3 15h10v-4.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5z"/>
        </svg>
        <svg @click="back()" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-return-left" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M14.5 1.5a.5.5 0 0 1 .5.5v4.8a2.5 2.5 0 0 1-2.5 2.5H2.707l3.347 3.346a.5.5 0 0 1-.708.708l-4.2-4.2a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 8.3H12.5A1.5 1.5 0 0 0 14 6.8V2a.5.5 0 0 1 .5-.5"/>
        </svg>
    </div>
</template>

<style>
.detail_btn {
    margin-top: 3%;
    margin-bottom: 3%;

    svg {
        margin-right: 3%;
    }

    svg:hover {
        fill: #939090;
        cursor: pointer;
        padding: 1px;
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
            var params = new URLSearchParams({
                team_id: team_id.value
            });
            location.href = "../tasks" + "?" + params;
        }

        created();
        return {
            loading, task_id, team_id, text, markdownOption, created, save, back
        }
    },
})
</script>
