import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores"
import { MissingPage } from "@/pages";

const routes = [
  {
    path: "",
    redirect: { name: "Home" },
    component: () => import("@/pages/layouts/BaseLayout.vue"),
    children: [
      {
        name: "Login",
        path: "/login",
        component: () => import("@/pages/LoginPage.vue"),
      },
    ],
  },
  {
    path: "/",
    redirect: { name: "Home" },
    component: () => import("@/pages/layouts/HeaderedLayout.vue"),
    children: [
      {
        name: "Home",
        path: "/home",
        component: () => import("@/pages/HomePage.vue"),
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: MissingPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (!userStore.isSignedIn && to.name !== "Login") {
    next({ name: "Login" })
    return;
  } else {
    next()
  }
});

export { router };
