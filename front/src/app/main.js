import { createApp } from "vue";
import { router, store, vuetify } from "./providers";
import App from "./App.vue";
import swipe from "./directives/swipe";

const app = createApp(App);

app.directive('swipe', swipe)

app.use(store).use(router).use(vuetify).mount("#app");
