import { defineStore } from "pinia";
import { AuthController } from "@/api/controllers";

function parseToken(token) {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: {},
  }),
  getters: {
    isSignedIn(state) {
      return (
        !!state.user.accessToken?.length && !!state.user.refreshToken?.length
      );
    },
  },
  actions: {
    async login(login, password) {
      const resp = await AuthController.logIn(login, password);
      if (resp.name !== "AxiosError") {
        const parsedToken = parseToken(resp.data.access_token);
        this.user.username = parsedToken.sub;
        this.user.roles = parsedToken.roles;
        this.user.accessToken = resp.data.access_token;
        this.user.refreshToken = resp.data.refresh_token;
      }
    },
  },
  persist: {
    enabled: true,
  },
});
