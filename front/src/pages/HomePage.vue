<template>
  <div class="home-page">
    <img
      :src="ml1"
      class="home-page__ml1 home-page__ml"
    />
    <img
      :src="ml2"
      class="home-page__ml2 home-page__ml"
    />
    <img
      :src="ml3"
      class="home-page__ml3 home-page__ml"
    />
    <img
      :src="ml4"
      class="home-page__ml4 home-page__ml"
    />
    <img
      :src="ml5"
      class="home-page__ml5 home-page__ml"
    />
    <ProductCard v-if="userStore.user.username === 'provider'" class="mt-10" />
    <Swiper v-if="userStore.user.username === 'manager'" />
  </div>
</template>
<script setup>
import ProductCard from "@/components/ProductCard.vue";
import Swiper from "@/components/Swiper.vue";
import { useUserStore } from "@/stores";
import ml1 from "assets/ml1.svg";
import ml2 from "assets/ml2.svg";
import ml3 from "assets/ml3.svg";
import ml4 from "assets/ml4.svg";
import ml5 from "assets/ml5.svg";

const userStore = useUserStore()

</script>
<style scoped lang="scss">
@media screen and (max-width: 992px) {
  .product-card__search {
    width:90vw !important;
  }
}
.home-page {
  position: relative;
  display: flex;
  justify-content: center;
  &__ml{
    position: absolute;
    width: 256px;
    height: 256px;
    max-width: 14vw;
    max-height: 14vw;
    user-select: none;
  }
  &__ml1 {
    left:5vw;
    width: 312px;
    height: 312px;
    top:15vh;
  }
  &__ml3 {
    transform: rotate(20deg);
    left: 24vw;
    width: 174px;
    height: 174px;
    top: 46vh;
  }
  &__ml2 {
    right:8vw;
    width: 182px;
    height: 182px;
    top:38vh;
  }
  &__ml4 {
    transform: rotate(90deg);
    right: 17vw;
    width: 152px;
    height: 152px;
    top: 5vh;
  }
  &__ml5 {
    transform: rotate(-10deg);
    right:30vw;
    top: calc(100vh - 360px);
  }
}
</style>
