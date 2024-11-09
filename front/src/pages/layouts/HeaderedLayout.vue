<template>
  <div class="layout">
    <div class="header-wrapper">
      <div class="header-wrapper__logos d-none d-sm-flex">
        <img
          :src="infoLogo"
          class="ml-4"
          style="width: calc(144px * 0.7 * 1, 375); height: calc(65px * 0.7)"
        />
        <img
          :src="mskLogo"
          class="mx-8 mt-1"
          style="width: calc(187px * 0.7 * 1, 375); height: calc(75px * 0.7)"
        />
        <img
          :src="portalLogo"
          style="width: calc(242px * 0.7 * 1, 375); height: calc(66px * 0.7)"
        />
      </div>
      <div></div>

      <div class="d-flex align-center">
        <span style="font-size: 16px">
          <b>
            <template v-if="userStore.user.username === 'provider'">
              Поставщик
            </template>
            <template v-if="userStore.user.username === 'manager'"> Менеджер </template>
          </b>
        </span>
        <AvatarComponent class="ml-4" size="50px"></AvatarComponent>
        <v-btn
          color="red-darken-4"
          @click="logout()"
          icon="mdi-logout"
          class="mx-2 pa-2"
          size="medium"
          variant="text"
        ></v-btn>
      </div>
    </div>
    <div class="layout__view-wrapper">
      <RouterView />
    </div>
  </div>
</template>
<script setup lang="ts">
import { AvatarComponent } from "@/components";
import infoLogo from "assets/info-logo.svg";
import mskLogo from "assets/msk-logo.svg";
import portalLogo from "assets/portal-logo.svg";
import { useUserStore } from "@/stores";
import { router } from "@/app/providers";

const userStore = useUserStore();

function logout() {
  userStore.user = {};
  router.push({ name: "Login" });
}
</script>
<style lang="scss" scoped>
.layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: $bg-primary;
  font-family: "Montserrat";
  align-items: center;
  min-height: 100vh;
  &__view-wrapper {
    flex-grow: 1;
    width: 100vw;
  }
}

.header-wrapper {
  padding: 8px 0 8px 8px;
  transition: all 0.5s ease;
  width: 100%;
  background-color: white;
  box-shadow: 0 -12px 20px black;
  display: flex;
  align-items: center;
  justify-content: space-between;
  &__logos {
    display: flex;
    align-items: center;
  }
}
</style>
