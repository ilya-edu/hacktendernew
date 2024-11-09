import { authHttpClient } from "../clients";

class ProductsController {
  static API_ENDPOINT = "https://zakupki-api.kovalev.team/products/";

  static async getModels(str) {
    if(!str) return []
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT+'models.json',{params:{q:str}})
      .catch((err) => {
        return err;
      });
    return resp.data;
  }
  static async getVendors(str) {
    if(!str) return []
    const resp = await authHttpClient()
      .get(this.API_ENDPOINT+'vendors.json',{params:{q:str}})
      .catch((err) => {
        return err;
      });
    return resp.data;
  }
}

export { ProductsController };
