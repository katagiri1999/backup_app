<template>

    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />

    <svg xmlns="http://www.w3.org/2000/svg" data-bs-toggle="offcanvas" href="#offcanvasID" role="button" aria-controls="offcanvasID" width="32" height="32" fill="currentColor" class="bi bi-list left" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5" />
    </svg>

    <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasID" aria-labelledby="offcanvasExampleLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasExampleLabel">Teams</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" id="close_off"></button>
        </div>
        <div class="offcanvas-body">
            <span class="select_team">Select Team</span>
            <multiselect
                v-model="team"
                :options="teams"
                :placeholder="now_team_name"
                :allow-empty="false"
                :show-labels="false"
                :custom-label="custom_label"
                @close="switch_team()"
            />

            <span class="add_team">Add New Team</span>
            <div class="mb-3">
                <input class="form-control" placeholder="Team Name" v-model="new_team_name">
            </div>
            <button @click="new_team()" type="button" class="btn btn btn-outline-secondary">Add Team</button>

            <span class="del_team">Delete This Team</span>
            <button @click="delete_team()" type="button" class="btn btn-outline-danger">Delete Team</button>

        </div>
    </div>

</template>

<style>
.left {
    float: left;
}

.add_team {
    margin-top: 50%;
    display: flex;
}

.del_team,
.select_team {
    margin-top: 5%;
    display: flex;
}

@media screen and (max-width: 768px) {
    .offcanvas {
        --bs-offcanvas-width: 80%;
    }
}
</style>

<script>
import { computed, defineComponent, ref } from 'vue';
import { common_headers, common_requests } from "./common_func_component.js";
import VueElementLoading from "vue-element-loading";
import Multiselect from 'vue-multiselect';
import "vue-multiselect/dist/vue-multiselect.css";


export default defineComponent({
    props: { teams: Array },
    components: {
        VueElementLoading, Multiselect,
    },
    setup(props) {
        const loading = ref(false);
        const team = ref("");
        const new_team_name = ref("");

        const now_team_name = computed(() => {
            var ret = "";
            var query_team_id = (new URL(document.location)).searchParams.get("team_id");
            if (!query_team_id) {
                ret = sessionStorage.getItem("user_id");
            }

            for (let team of props.teams) {
                if (team.team_id == query_team_id) {
                    ret = team.team_name;
                }
            }

            return ret;
        })

        const custom_label = (team) => {
            return team.team_name;
        }

        const close_offcanvas = async () => {
            document.getElementById('close_off').click();
        }

        const switch_team = async () => {
            if (team.value) {
                await close_offcanvas();
                loading.value = true;

                var params = new URLSearchParams({
                    team_id: team.value.team_id
                });
                location.href = "./tasks" + "?" + params;
            }
        }

        const new_team = async () => {

            if (!new_team_name.value) {
                alert("Can not empty");
                throw Error("Can not empty");
            }

            await close_offcanvas();
            loading.value = true;

            var res = await common_requests(
                `${process.env.VUE_APP_API_BASE}/teams`,
                "POST",
                common_headers(),
                { team_name: new_team_name.value },
            );
            var new_team_id = res.team_id;

            loading.value = true;
            var params = new URLSearchParams({
                team_id: new_team_id,
            });
            location.href = "./tasks" + "?" + params;
        }

        const delete_team = async () => {
            if (now_team_name.value == sessionStorage.getItem("user_id")) {
                alert("Can not delete this team");
                throw Error("Can not delete this team");
            }

            if (sessionStorage.getItem("role") != "admin") {
                alert("Can not delete this team");
                throw Error("Can not delete this team");
            }

            var result = confirm("Are you sure you want to delete this Team?");
            if (!result) {
                return null;
            }

            await close_offcanvas();
            loading.value = true;
            await common_requests(
                `${process.env.VUE_APP_API_BASE}/teams`,
                "DELETE",
                common_headers(),
            );

            loading.value = true;
            location.href = `./tasks`;
        }

        return {
            loading, team, new_team_name, now_team_name, custom_label, close_offcanvas, switch_team, new_team, delete_team, 
        }
    },
})
</script>
