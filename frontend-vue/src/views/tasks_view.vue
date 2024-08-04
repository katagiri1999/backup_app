<template>

    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />
    <header_component />

    <!-- メニューボタン -->
    <div class="menu_btn">
        <setting_component />
        <svg @click="open_modal('post')" data-bs-toggle="modal" data-bs-target="#modal1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-plus-square" viewBox="0 0 16 16">
            <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z" />
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4" />
        </svg>
        <reload_component />
        <logout_component />
        <teams_component :teams="teams" />
    </div>

    <Vue3EasyDataTable :headers="table_headers" :items="table_items" :rows-per-page="10" :table-height="420" theme-color="gray" buttons-pagination :body-item-class-name="bodyItemClassNameFunction" :header-item-class-name="headerItemClassNameFunction">
        <template #item-detail="item">
            <svg @click="to_detail(item)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5"/>
                <path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0z"/>
            </svg>
        </template>
        <template #item-operation="item">
            <svg @click="open_modal('put', item)" data-bs-toggle="modal" data-bs-target="#modal1" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
            </svg>
            <svg @click="open_modal('delete', item)" data-bs-toggle="modal" data-bs-target="#modal1" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5" />
            </svg>
        </template>
    </Vue3EasyDataTable>

    <!-- コンテンツ用モーダル -->
    <div class="modal" id="modal1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5> {{ modal_title }} </h5>
                    <button class="btn-close" data-bs-dismiss="modal" id="modal_close1"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="modal_value.task" id="modal_task">
                        <label>Task:</label>
                    </div>
                    <br>
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="modal_value.user" id="modal_user">
                        <label>User:</label>
                    </div>
                    <br>
                    <div class="form-floating">
                        <select class="form-select form-select-sm" v-model="modal_value.status" id="modal_status">
                            <option value="Untouched">Untouched</option>
                            <option value="Processing">Processing</option>
                            <option value="Finished">Finished</option>
                        </select>
                        <label>Status:</label>
                    </div>
                    <br>
                    <div class="form-floating">
                        <input type="date" class="form-control" v-model="modal_value.limit" id="modal_limit">
                        <label>Limit:</label>
                    </div>
                    <div class="error">
                        <template v-if="modal_error">
                            <div class="alert alert-danger">
                                <b>⚠{{ modal_error }}</b>
                            </div>
                        </template>
                    </div>
                    <svg @click="call_contents_api" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                        <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05" />
                    </svg>
                </div>
            </div>
        </div>
    </div>

</template>

<style>
.menu_btn {
    text-align: right;
    margin-top: 1%;
    margin-right: 1%;

    svg {
        margin-left: 0.5%;
        margin-right: 0.5%;
    }
}

svg:hover {
    fill: #939090;
    cursor: pointer;
    padding: 1px;
}

.vue3-easy-data-table {
    margin: 1%;
    padding: 1%;

    .task_id_column {
        display: none;
    }

    .vue3-easy-data-table__header th {
        background-color: #ededed;
    }

    .bi-trash3 {
        margin-left: 10%;
    }
}

.error {
    margin-top: 3%;
    margin-bottom: 3%;
}

@media screen and (max-width: 768px) {
    .modal-dialog {
        margin-top: 30%;
    }

    .menu_btn {
        svg {
            margin-left: 1%;
            margin-right: 1%;
        }
    }

    .vue3-easy-data-table {
        .bi-trash3 {
            margin-left: 20%;
        }
    }
}
</style>

<script>
import { defineComponent, ref } from 'vue';
import { common_headers, common_requests } from "../components/common_func_component.js";
import header_component from "../components/header_component.vue";
import setting_component from "../components/setting_component.vue";
import reload_component from "../components/reload_component.vue";
import logout_component from "../components/logout_component.vue";
import teams_component from "../components/teams_component.vue";
import VueElementLoading from "vue-element-loading";
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';


const MODAL_TITLE_POST = "Register Task";
const MODAL_TITLE_PUT = "Update Task";
const MODAL_TITLE_DELETE = "Delete Task";

const bodyItemClassNameFunction = (column) => {
    if (column === 'task_id') return 'task_id_column';
    return '';
};

const headerItemClassNameFunction = (header) => {
    if (header.value === 'task_id') return 'task_id_column';
    return '';
};

export default defineComponent({
    components: {
        header_component, VueElementLoading, Vue3EasyDataTable, setting_component, reload_component, logout_component, teams_component
    },
    setup() {
        const self_user_id = ref(sessionStorage.getItem("user_id"));
        const team_id = ref("");
        const loading = ref(false);
        const teams = ref([]);
        const modal_value = ref({
            task_id: "",
            task: "",
            user: "",
            status: "",
            limit: "",
        });
        const modal_title = ref("");
        const modal_error = ref("");
        const table_headers = ref([
            { text: "TASK_ID", value: "task_id" },
            { text: "TASK", value: "task", sortable: true },
            { text: "DETAIL", value: "detail", sortable: true },
            { text: "USER", value: "user_id", sortable: true },
            { text: "STATUS", value: "status", sortable: true },
            { text: "LIMIT", value: "limit", sortable: true },
            { text: "OPERATION", value: "operation" },
        ]);
        const table_items = ref([]);

        const created = async () => {
            var query_team_id = (new URL(document.location)).searchParams.get("team_id");
            loading.value = true;

            await get_teams();

            var self_team_id = "";
            for (let team of teams.value) {
                if (team.team_name == self_user_id.value) {
                    self_team_id = team.team_id;
                }
            }

            if (!self_team_id) {
                var res = await common_requests(
                    `${process.env.VUE_APP_API_BASE}/teams`,
                    "POST",
                    common_headers(),
                    { team_name: self_user_id.value },
                );
                self_team_id = res.team_id;
                teams.value = [res];
            }

            team_id.value = query_team_id ? query_team_id : self_team_id;
            res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/refresh`,
                "POST",
                common_headers(),
                { team_id: team_id.value }
            );

            history.replaceState("", "", `${new URL(document.location).pathname}?team_id=${team_id.value}`);

            sessionStorage.setItem("token", res.id_token);
            sessionStorage.setItem("role", res.role);

            await get_contents();
            loading.value = false;
        }

        const open_modal = async (kind, item = {}) => {
            modal_error.value = "";

            if (kind == "post") {
                modal_title.value = MODAL_TITLE_POST;
                modal_value.value.task = "";
                modal_value.value.user = "";
                modal_value.value.status = "";
                modal_value.value.limit = "";
                document.getElementById("modal_task").disabled = false;
                document.getElementById("modal_user").disabled = false;
                document.getElementById("modal_status").disabled = false;
                document.getElementById("modal_limit").disabled = false;

            } else {
                modal_value.value.task_id = item.task_id;
                modal_value.value.task = item.task;
                modal_value.value.user = item.user_id;
                modal_value.value.status = item.status;
                modal_value.value.limit = item.limit;

                if (kind == "put") {
                    modal_title.value = MODAL_TITLE_PUT;
                    document.getElementById("modal_task").disabled = false;
                    document.getElementById("modal_user").disabled = false;
                    document.getElementById("modal_status").disabled = false;
                    document.getElementById("modal_limit").disabled = false;

                } else if (kind == "delete") {
                    modal_title.value = MODAL_TITLE_DELETE;
                    document.getElementById("modal_task").disabled = true;
                    document.getElementById("modal_user").disabled = true;
                    document.getElementById("modal_status").disabled = true;
                    document.getElementById("modal_limit").disabled = true;
                }
            }
        }

        const get_contents = async () => {
            var res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/tasks`,
                "GET",
                common_headers()
            );

            table_items.value = res.contents;
        }

        const get_teams = async () => {
            var res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/teams`,
                "GET",
                common_headers()
            );

            teams.value = res.contents;
        }

        const call_contents_api = async () => {
            if (!modal_value.value.task || !modal_value.value.user || !modal_value.value.status || !modal_value.value.limit) {
                modal_error.value = "Can not empty";
                throw Error("Can not empty");
            }

            var api_url = `${process.env.VUE_APP_API_BASE}/tasks`;
            var api_method = "";
            var params = {};

            if (modal_title.value == MODAL_TITLE_POST) {
                api_method = "POST";
                params = {
                    task: modal_value.value.task,
                    user_id: modal_value.value.user,
                    status: modal_value.value.status,
                    limit: modal_value.value.limit
                }

            } else if (modal_title.value == MODAL_TITLE_PUT) {
                api_method = "PUT";
                api_url = `${api_url}?task_id=${modal_value.value.task_id}`
                params = {
                    task: modal_value.value.task,
                    user_id: modal_value.value.user,
                    status: modal_value.value.status,
                    limit: modal_value.value.limit
                }

            } else if (modal_title.value == MODAL_TITLE_DELETE) {
                api_method = "DELETE";
                params = {
                    task_id: modal_value.value.task_id,
                }
            }

            loading.value = true;
            document.getElementById('modal_close1').click();
            await common_requests(
                api_url,
                api_method,
                common_headers(),
                params,
            );

            await get_contents();
            loading.value = false;
        }

        const to_detail = async (item) => {
            loading.value = true;
            var params = new URLSearchParams({
                team_id: team_id.value,
                task_id: item.task_id,
            });
            location.href = "./tasks/detail" + "?" + params;
        }

        created();
        return {
            bodyItemClassNameFunction, headerItemClassNameFunction, self_user_id, team_id, loading, teams, modal_value, modal_title, modal_error, table_headers, table_items,
            open_modal, call_contents_api, to_detail,
        }
    },
})
</script>
