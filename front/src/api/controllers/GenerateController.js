import axios from "axios";

class GenerateController {
  static API_ENDPOINT = "https://37a8-94-177-230-82.ngrok-free.app/generate_characteristics";

  static async getGenerate(prop, name) {
    const resp = await axios({
      method: 'post',
      url: this.API_ENDPOINT,
      headers: {
        "ngrok-skip-browser-warning": true
      }, 
      data:{ properties:[prop], name: name}
    });
    return resp.data[0].value;
  }
}

export { GenerateController };
