<template>
  <div>
    <v-autocomplete
      label="Категория"
      class="mb-4"
      :custom-filter="() => true"
      color="blue-darken-3"
      variant="underlined"
      v-model="category"
      @update:search="debounceCategories"
      @update:model-value="emitCategory"
      :items="formattedCategories"
    />
    <v-autocomplete
      label="Модель"
      class="mb-4"
      :custom-filter="() => true"
      color="blue-darken-3"
      variant="underlined"
      v-model="model"
      @update:search="debounceModels"
      :items="models"
    />
    <v-autocomplete
      label="Производитель"
      class="mb-4"
      :custom-filter="() => true"
      color="blue-darken-3"
      variant="underlined"
      v-model="manufacturer"
      @update:search="debounceVendors"
      :items="manufacturers"
    />
  </div>
</template>
<script setup>
import { ref, computed } from "vue";
import { CategorieController } from "@/api/controllers/CategorieController";
import { ProductsController } from "@/api/controllers/ProductsController";

const category = ref();
const categories = ref([]);

const model = ref();
const models = ref([]);

const manufacturer = ref();
const manufacturers = ref([]);

const props = defineProps({
  search: String,
  locked: Boolean
})

function debounce(func, ms) {
  let timeout;
  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, arguments), ms);
  };
}

const formattedCategories = computed(() => {
  return categories.value.map((c) => c.name);
});

const emit = defineEmits(['categorySet'])

function emitCategory(e){ 
  emit('categorySet',categories.value.find((v)=>v.name === e))
}

async function setCategories(str) {
  if (str.length) {
    categories.value = await CategorieController.findCategoriesByStr(str);
  }
}
const debounceCategories = debounce(setCategories, 700);

async function setModels(str) {
  if (!props.search || props.locked) return;
  const resp = await ProductsController.getModels(str);
  models.value = resp;
}
const debounceModels = debounce(setModels, 700);

async function setVendors(str) {
  if (!props.search || props.locked) return;
  const resp = await ProductsController.getVendors(str);
  manufacturers.value = resp;
}
const debounceVendors = debounce(setVendors, 700);

function setMainData(model_, vendor_, category_){
  model.value = model_;
  manufacturer.value = vendor_;
  category.value = category_
  emitCategory(category_)
}

defineExpose({setMainData, manufacturer, model, category})
</script>
