import axios from "axios";

const api = axios.create({

    baseURL: "http://127.0.0.1:8000"

});

export async function predictImage(file){

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(

        "/predict",

        formData,

        {

            headers:{

                "Content-Type":"multipart/form-data"

            }

        }

    );

    return response.data;
}