import { authHttpClient } from "../clients";

class CategorieController {
  static API_ENDPOINT = "https://zakupki-api.kovalev.team/categories";

  static async getCategorieById(id) {
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT+'/'+id+'.json')
      .catch((err) => {
        return err;
      });
    return resp.data;
  }
  static async findCategoriesByStr(str) {
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT+'.json', {params:{q:str}})
      .catch((err) => {
        return err;
      });
    return resp.data;
  }
}

export { CategorieController };
