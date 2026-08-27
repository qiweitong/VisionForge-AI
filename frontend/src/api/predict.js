import request from "./request";

export function predictImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request({
    url: "/predict",
    method: "post",
    data: formData
  });
}