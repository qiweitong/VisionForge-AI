import request from "./request";

export function getModelList() {
    return request({
        url: "/model/list",
        method: "get"
    });
}

export function getCurrentModel() {
    return request({
        url: "/model/current",
        method: "get"
    });
}

export function selectModel(modelName) {
    return request({
        url: "/model/select",
        method: "post",
        data: { name: modelName }
    });
}

export function reloadYolo() {
    return request({
        url: "/model/reload_yolo",
        method: "post"
    });
}
