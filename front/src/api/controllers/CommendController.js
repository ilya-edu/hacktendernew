import { authHttpClient } from "../clients";

class CommendController {
  static API_ENDPOINT = "https://zakupki-api.kovalev.team/products/search.json";

  static async getCommends(q) {
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT, {params:{q:q}})
      .catch((err) => {
        return err;
      });
    return resp.data;
  }
}

export { CommendController };
