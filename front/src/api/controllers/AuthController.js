import { authHttpClient } from "@/api/clients"

class AuthController {
  static API_ENDPOINT = "api/login";

  static async logIn(login, pass) {
    const postData = new URLSearchParams({
      username: login,
      password: pass,
    });
    const response = await authHttpClient()
      .post(this.API_ENDPOINT, postData)
      .catch((err) => {
        return err;
      });
    return response;
  }
}

export { AuthController };
