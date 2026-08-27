import request from "./request"

export function getStatistics(){

    return request({

        url:"/statistics",

        method:"get"

    })

}