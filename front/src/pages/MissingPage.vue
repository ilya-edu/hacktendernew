<template>
  <div class="missing-page-wrapper">
    <img :src="imgNotFound" />
    <v-btn text="Назад" type="filled" @click="router.go(-1)"></v-btn>
  </div>
</template>
<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();
</script>
<style lang="scss" scoped>
.missing-page-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-top: 5%;
  align-items: center;
}
</style>
