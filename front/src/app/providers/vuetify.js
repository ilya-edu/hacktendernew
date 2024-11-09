import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          danger: "#a30404",
          success: "#5fb729",
          primary: "#523ae5",
          "primary-lighter": "#6f3cd6",
          secondary: "#5b4a9a",
          "text-lght": "#757070",
        },
      },
    },
  },
});

export { vuetify };
