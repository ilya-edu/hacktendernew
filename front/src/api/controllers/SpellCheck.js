import axios from "axios";

export async function spellcheck(txt) {
  const resp = await axios.request({
    method: "GET",
    url: `https://speller.yandex.net/services/spellservice.json/checkText?text=${txt}&lang=ru&options=0&format=plain`,
  })
  return resp.data;
}
