<template>
  <div class="product-prop">
    <v-text-field
      :label="name"
      rounded
      @update:model-value="emit('changed')"
      v-model="model"
      class="product-card__search"
      color="blue-darken-3"
      variant="underlined"
    />
  </div>
</template>
<script setup>
import { computed } from "vue";

const emit = defineEmits(["update:modelValue", "changed"]);

const model = computed({
  get() {
    if(!props.modelValue) return props.defaultValue;
    return props.modelValue;
  },
  set(v) {
    emit("update:modelValue", v);
  },
});

const props = defineProps({
  type: String, //number || string
  name: String,
  modelValue: String,
});
</script>
<style scoped lang="scss">
.product-prop{
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 8px;
}
</style>
