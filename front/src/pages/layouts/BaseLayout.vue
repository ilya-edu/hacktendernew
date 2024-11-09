<template>
  <div class="layout-base">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<style lang="scss" scoped>
.layout-base {
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: $bg-primary;
  font-family: "Montserrat";
  align-items: center;
  min-height: 100vh;
}
</style>
