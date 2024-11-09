import { authHttpClient } from "../clients";

class PropsController {
  static API_ENDPOINT = "https://zakupki-api.kovalev.team/properties.json";

  static async getProps(q, ids) {
    const tmp = ids.join(',')
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT, {params:{q:q, category_ids: tmp}})
      .catch((err) => {
        return err;
      });
    return resp.data.slice(0, 20);
  }
}

export { PropsController };
