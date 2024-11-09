<template>
  <img
    :src="props.src"
    :class="{ 'avatar-img': true, 'avatar-rounded': props.rounded }"
  />
</template>
<script setup lang="ts">
import { computed } from "vue";
import defaultAvatar from "assets/avatar-default.svg";

const props = withDefaults(
  defineProps<{
    src?: string;
    rounded?: boolean;
    size?: string;
  }>(),
  { src: defaultAvatar, rounded: false, size: "100%" }
);
const size = computed(() => {
  return props.size;
});
</script>
<style lang="scss" scoped>
.avatar-img {
  border-radius: 9px;
  background-color: $bg-secondary;
  width: v-bind(size);
  height: v-bind(size);
}

.avatar-rounded {
  border-radius: 100%;
}
</style>
