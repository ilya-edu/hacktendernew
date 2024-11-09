import { coreHttpClient } from "@/api/clients"

class AutofillController {
  static API_ENDPOINT = "api/login";

  static async autofill() {
    const response = await coreHttpClient()
      .post(this.API_ENDPOINT)
      .catch((err) => {
        return err;
      });
    return response;
  }
}

export { AutofillController };
