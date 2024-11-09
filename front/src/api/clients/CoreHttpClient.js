import axios from "axios";

const coreHttpClient = () => {
  const baseUrl = "https://rutube-api.kovalev.team/api/videos/";

  return axios.create({
    baseURL: baseUrl,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export { coreHttpClient };
