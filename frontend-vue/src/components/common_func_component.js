export function common_headers() {
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "authorization": sessionStorage.getItem("token"),
    }
}

export async function common_requests(url, method, headers, params = {}) {
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

        location.href = process.env.VUE_APP_REDIRECT_URI;
        throw Error("invalid response");
    }

    console.log({ response: body });
    return body;
}
