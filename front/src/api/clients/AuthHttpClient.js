import axios from "axios";

const authHttpClient = () => {
  const baseUrl = "https://jwt-api.kovalev.team/";

  return axios.create({
    baseURL: baseUrl,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export { authHttpClient };
