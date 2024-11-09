<template>
  <div class="product-card-mini">
    <div
      v-ripple="{ class: `text-blue-darken-3` }"
      class="product-card-mini__title"
      @click="opened = !opened"
    >
      <div class="d-flex justify-between align-center">
        <h3>{{ props.name }}</h3>
        <v-icon
          icon="mdi-chevron-up"
          :style="{transform:opened?'rotate(180deg)':'',transition:'transform 0.7s ease'}"
          class="ml-3"
          color="blue-darken-3"
          size="large"
        />
      </div>
      <div class="mb-3">
        <span><b>Категория:</b> {{ props.category.name }}</span>
      </div>
    </div>

    <div
      class="product-card-mini__body"
      :class="{
        'product-card-mini__body-opened': opened,
        'product-card-mini__body-closed': !opened,
      }"
    >
      <div>
        <v-img class="mt-2" :src="props.image" />

        <div class="mb-3">
          <span><b>Модель:</b> {{ props.model }}</span>
        </div>
        <div>
          <span><b>Производитель:</b> {{ props.vendor }}</span>
        </div>
        <div class="d-flex justify-center mt-4">
          <v-btn
            class="text-none text-subtitle-2"
            variant="flat"
            elevation="0"
            color="blue-darken-3"
            no-caps
            @click="emit('clicked', {model, vendor, category})"
            >Использовать как шаблон</v-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";

const emit = defineEmits(['clicked'])
const opened = ref(false);
const props = defineProps({
  name: String,
  image: String,
  category: Object,
  model: String,
  vendor: String,
});
</script>
<style scoped lang="scss">
.product-card-mini {
  background-color: white;

  border-radius: 12px;
  & span {
    font-size: 12px;
    line-height: 12px;
  }
  &__title {
    padding: 16px 24px;
    border-radius: 12px 12px 0 0;
    cursor: pointer;
    &:hover {
      background-color: $secondary-hover;
    }
    & h3 {
      font-size: 16px;
    }
  }
  &__body {
    display: grid;
    grid-template-rows: 1fr;
    transition: grid-template-rows 0.7s ease;
    & > div {
      transition: all 0.7s ease;
      overflow: hidden;
      padding: 0 24px 16px 24px;
    }
  }
  &__body-closed {
    grid-template-rows: 0fr;
    margin-bottom: 0px;
    & > div {
      padding: 0;
    }
  }
}
</style>
