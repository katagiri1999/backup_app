<script>
export default {
    methods: {
        common_headers() {
            return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": sessionStorage.getItem("token"),
            }
        },
        async common_requests(url, method, headers, params = {}) {
            var request_log = { request: { url: url, method: method, headers: headers, params: params } };
            console.log(request_log);

            if (method == "GET" || method == "DELETE") {
                var detail = {
                    method: method,
                    headers: headers,
                };
                url = url + "?" + new URLSearchParams(params)
            } else {
                detail = {
                    method: method,
                    headers: headers,
                    body: JSON.stringify(params),
                };
            }

            var res = await fetch(
                url,
                detail
            );

            var body = await res.json();

            if (res.status != 200) {
                console.log("invalid response");
                console.log(body);
                if (res.status == 401) {
                    alert("Session expired. Please login again");
                } else {
                    alert("Unexpected error. Please login again");
                }
                sessionStorage.clear();
                this.$router.push("/");
                throw Error("invalid response");
            }

            console.log({ response: body });
            return body;
        },
        update_session_expiration() {
            let now = new Date();
            now.setMinutes(now.getMinutes() + 30);
            let now_string = `${now.getFullYear()}/${("0" + (now.getMonth() + 1)).slice(-2)}/${("0" + now.getDate()).slice(-2)} ${("0" + now.getHours()).slice(-2)}:${("0" + now.getMinutes()).slice(-2)}`;
            return now_string;
        }
    }
}
</script>
