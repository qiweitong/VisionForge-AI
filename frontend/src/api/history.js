import request from"@/api/request"

export function getHistory(){

    return request({

        url:"/history",

        method:"get"

    })

}