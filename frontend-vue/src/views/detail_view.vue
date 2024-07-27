<template>
    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component msg="Login" />

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
import header_component from "..//components/header_component.vue";
import common_func_component from "../components/common_func_component.vue";
import VueElementLoading from "vue-element-loading";
import { quillEditor } from 'vue3-quill';

export default {
    mixins: [common_func_component],
    components: {
        quillEditor, VueElementLoading, header_component
    },
    data() {
        return {
            loading: false,
            task_id: (new URL(document.location)).searchParams.get("task_id"),
            team_id: (new URL(document.location)).searchParams.get("team_id"),
            text: "",
            editorOption: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote', 'code-block'],
                        [{ list: 'ordered' }, { list: 'bullet' },  { list: 'check' }],
                        [{ indent: '-1' }, { indent: '+1' }],
                        [{ size: ['small', false, 'large', 'huge'] }],
                        [{ color: [] }, { background: [] }],
                        [{ align: [] }],
                        ['link'],
                        ['clean'],
                    ]
                },
            },
        }
    },
    methods: {
        async save() {
            this.loading = true;

            var res = await this.common_requests(
                `${process.env.VUE_APP_API_BASE}/tasks?task_id=${this.task_id}`,
                "PUT",
                this.common_headers(),
                { detail: this.text }
            );
            console.log(res);

            this.loading = false;
        },
        async back() {
            this.loading = true;
            location.href = `../tasks?team_id=${this.team_id}`;
        },
    },
    async created() {
        this.loading = true;

        var res = await this.common_requests(
            `${process.env.VUE_APP_API_BASE}/tasks`,
            "GET",
            this.common_headers(),
            { task_id: this.task_id }
        );
        this.text = res.contents[0].detail;

        this.loading = false;
    }
}
</script>
