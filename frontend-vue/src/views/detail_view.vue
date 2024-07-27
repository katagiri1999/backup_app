<template>
    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component />

    <quill-editor v-model:value="text" :options="editorOption" />

    <div class="detail_btn">
        <button @click="save()" type="button" class="btn btn btn-outline-secondary">Save</button>
        <button @click="back()" type="button" class="btn btn btn-outline-secondary">Back</button>
    </div>
</template>

<style>
.ql-snow {
    margin: 0.5%;
}

.detail_btn {
    margin-top: 3%;

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
import { quillEditor } from 'vue3-quill';


export default defineComponent({
    components: {
       quillEditor, VueElementLoading, header_component
    },
    setup() {
        const loading = ref(false);
        const task_id = ref((new URL(document.location)).searchParams.get("task_id"));
        const team_id = ref((new URL(document.location)).searchParams.get("team_id"));
        const text = ref("");
        const editorOption = ref({
            modules: {
                toolbar: [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ list: 'ordered' }, { list: 'bullet' }, { list: 'check' }],
                    [{ indent: '-1' }, { indent: '+1' }],
                    [{ size: ['small', false, 'large', 'huge'] }],
                    [{ color: [] }, { background: [] }],
                    [{ align: [] }],
                    ['link'],
                    ['clean'],
                ]
            },
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
            loading, task_id, team_id, text, editorOption, created, save, back
        }
    },
})
</script>
