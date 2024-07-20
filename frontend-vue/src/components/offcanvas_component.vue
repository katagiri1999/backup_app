<template>

    <VueElementLoading :active="loading" spinner="bar-fade-scale" is-full-screen />

    <svg xmlns="http://www.w3.org/2000/svg" data-bs-toggle="offcanvas" href="#offcanvasID" role="button"
        aria-controls="offcanvasID" width="32" height="32" fill="currentColor" class="bi bi-list left"
        viewBox="0 0 16 16">
        <path fill-rule="evenodd"
            d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5" />
    </svg>

    <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasID" aria-labelledby="offcanvasExampleLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasExampleLabel">Teams</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <span class="mid">Select Team</span>
            <multiselect
                v-model="team"
                :options="teams"
                :placeholder="now_team_name"
                :allow-empty="false"
                :show-labels="false"
                :custom-label="custom_label"
                @close="close"
            />

            <span class="mid">Add Team</span>
            <div class="mb-3">
                <input class="form-control" placeholder="Team Name" v-model="new_team_name">
            </div>
            <button @click="new_team()" type="button" class="btn btn btn-outline-secondary">Add Team</button>

            <span class="mid">Delete This Team</span>
            <button @click="delete_team()" type="button" class="btn btn-outline-danger">Delete Team</button>

        </div>
    </div>

</template>

<style>
.left {
    float: left;
}

.mid {
    margin-top: 10%;
    display: flex;
}
</style>

<script>
import common_func_component from "../components/common_func_component.vue";
import VueElementLoading from "vue-element-loading";
import Multiselect from 'vue-multiselect';
import "vue-multiselect/dist/vue-multiselect.css";


export default {
    mixins: [common_func_component],
    props: {
        teams: Array,
    },
    components: {
        VueElementLoading, Multiselect,
    },
    data() {
        return {
            loading: false,
            team: "",
            new_team_name: "",
        }
    },
    computed: {
        now_team_name() {
            var ret = "";
            var query_team_id = (new URL(document.location)).searchParams.get("team_id");
            if (!query_team_id) {
                ret = sessionStorage.getItem("user_id");
            }

            for (let team of this.teams) {
                if (team.team_id == query_team_id) {
                    ret = team.team_name;
                }
            }

            return ret;
        }
    },
    methods: {
        custom_label(team) {
            return team.team_name;
        },
        close() {
            if (this.team) {
                console.log(`switch to ${this.team.team_id}`);
                history.replaceState("", "", `${new URL(document.location).pathname}?team_id=${this.team.team_id}`);
                location.reload();
            }
        },
        async new_team() {

            if (!this.new_team_name) {
                alert("Can not empty");
                throw Error("Can not empty");
            }
            this.loading = true;
            await this.common_requests(
                `${process.env.VUE_APP_API_BASE}/teams`,
                "POST",
                this.common_headers(),
                { team_name: this.new_team_name }
            );

            this.$emit('get_teams');
            this.loading = false;
        },
        async delete_team() {
            if (this.now_team_name == sessionStorage.getItem("user_id")) {
                alert("Can not delete this team");
                throw Error("Can not delete this team");
            }

            var result = confirm("Are you sure you want to delete this Team?");
            console.log(result);
            if (!result) {
                return null;
            }

            this.loading = true;
            await this.common_requests(
                `${process.env.VUE_APP_API_BASE}/teams`,
                "DELETE",
                this.common_headers(),
            );

            this.$emit('get_teams');
            history.replaceState("", "", `${new URL(document.location).pathname}`);
            location.reload();
        },
    }
}

</script>
