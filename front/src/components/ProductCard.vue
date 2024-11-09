<template>
  <div class="product-card elevation-1">
    <div class="d-flex align-center mb-4">
      <v-text-field
        label="Название продукта"
        rounded
        class="product-card__search mr-2"
        color="red-lighten-1"
        :hint="searchMetrics"
        variant="outlined"
        persistent-hint
        prepend-inner-icon="mdi-magnify"
        v-model="search"
        @update:model-value="searchHandle"
      />
      <v-btn
        variant="text"
        :icon="locked ? 'mdi-lock-outline' : 'mdi-lock-open-variant-outline'"
        @click="locked = !locked"
      />
    </div>
    <div @click="search = formattedSearch; prompt=undefined" v-if="prompt" class="prompt">
      Возможно вы имели ввиду: {{ formattedSearch }}?
    </div>
    <ProductCardMainInfo
      :locked="locked"
      :search="search"
      @category-set="setCategory"
      ref="mainData"
    />
    <v-virtual-scroll
      class="product-card__scroll-wrapper"
      :items="productProps"
    >
      <template v-slot:default="{ item, index }">
        <ProductProp @changed="changes[index] = true" v-bind="item" v-model="propsModels[index]" />
      </template>
    </v-virtual-scroll>
    <div
      class="d-flex justify-between mt-4"
      style="justify-content: space-between"
    >
      <v-btn
        class="text-none text-subtitle-2"
        variant="flat"
        elevation="0"
        color="blue-darken-3"
        no-caps
        @click="SessionStore.pushTab({
          search:search,
          category:mainData.category,
          model:mainData.model,
          vendor:mainData.manufacturer,
          props:mappedProps
        })"
      >
        Отправить на проверку
      </v-btn>
      <v-btn
        class="text-none text-subtitle-2"
        variant="flat"
        elevation="0"
        color="blue-darken-3"
        no-caps
        @click="handlePropsEdit()"
      >
        Заполнить данные
      </v-btn>
    </div>
    <div class="product-card__mini-cards" v-show="commendProducts.length">
      <ProductCardMini
        @clicked="handleSelectMainInfo"
        v-for="product in commendProducts"
        :key="product.id"
        class="mb-4"
        v-bind="product"
      />
    </div>
  </div>
</template>
<script setup>
import ProductCardMini from "./ProductCardMini.vue";
import ProductProp from "./ProductProp.vue";
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { CommendController } from "../api/controllers/CommendController";
import { CategorieController } from "@/api/controllers/CategorieController";
import ProductCardMainInfo from "./ProductCardMainInfo.vue";
import { ProductsController } from "@/api/controllers/ProductsController";
import { PropsController } from "@/api/controllers/PropertiesController";
import { GenerateController } from "@/api/controllers/GenerateController";
import { useSessionStore } from "@/stores/SessionStore";
import { spellcheck } from "@/api/controllers/SpellCheck";


const prop = ref()
const SessionStore = useSessionStore()
const search = ref("");
const lastSearch = ref(0);
const searchMetrics = computed(() => {
  if (commendsLoading.value) return "-";
  if (lastSearch.value)
    return `Время ответа: ${lastSearch.value}мс, найдено СТЕ: ${commendProducts.length}`;
  return "";
});
const mainData = ref();

const commendProducts = ref([]);
const commendsLoading = ref(false);
const locked = ref(false);

const category = ref();
const category2 = ref()
const categories = ref([]);

async function setCategory(v) {
  category.value = v;
}

const mappedProps = computed(()=>{
  return productProps.value.map((v, i)=>({...v, value: propsModels.value[i], changed: changes.value[i]}))
})

async function handleSelectMainInfo(data) {
  category2.value = data.category
  mainData.value.setMainData(data.model,data.vendor,data.category.name);
}

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

function blur() {
  event.preventDefault();
  if (event.keyCode === 13) {
    document.activeElement.blur();
  }
}
async function setCommends() {
  if (!search.value || locked.value) return;
  commendsLoading.value = true;
  const resp = await CommendController.getCommends(search.value);
  commendsLoading.value = false;
  commendProducts.value = resp;
}

const formattedSearch = computed(()=>{
  let str = search.value
  prompt.value.forEach((v)=>{
    str = str.slice(0, v.pos) + v.s[0] + str.slice(v.pos+v.len)
  })
  return str
})

const searchHandle = async (v) => {
  debounceCommends(v)
  const resp = await spellcheck(v)
  prompt.value = resp
  if(!prompt.value.length){
    prompt.value = undefined
  }
}

const debounceCommends = debounce(setCommends, 700);

onMounted(() => {
  document.addEventListener("keyup", blur);
});
onBeforeUnmount(() => {
  document.removeEventListener("keyup", blur);
});

const productProps = ref([]);
const propsModels = ref([]);
const propsChanges = ref([])
const changes = computed({
  get(){
    if(!propsChanges.value.length){
      propsChanges.value = productProps.value.map(()=>false)
    }
    return propsChanges.value
  },
  set(v){
    propsChanges.value = v
  }
})

async function handlePropsEdit() {
  for (let i = 0; i < productProps.value.length; i++) {
    propsModels.value[i] = await GenerateController.getGenerate(
      productProps.value[i],
      search.value
    );
    changes.value[i] = false
  }
}

watch([category, category2], async ([v1, v3]) => {
  if ((v1 || v3) && search.value && !locked.value) {
    if(v3){
      productProps.value = await PropsController.getProps(search.value, [v3.id]);
    }
    if(v1){
      productProps.value = await PropsController.getProps(search.value, [v1.id]);
    }
    propsModels.value = productProps.value.map(() => "");
  }
});

const prompt = ref('')
</script>
<style scoped lang="scss">
@media screen and (max-width: 992px) {
  .product-card {
    min-width: 90vw !important;
  }
}
.prompt{
  margin-bottom: 4px;
  color: rgb(40, 40, 190);
  cursor: pointer;
}
.product-card {
  position: relative;
  background-color: white;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: 24px 32px;
  border-radius: 16px;
  width: 34vw;
  height: 80vh;
  &__search {
    max-height: 56px;
    & :deep(.v-field--active i) {
      transition: none !important;
      color: red !important;
    }
    & :deep(i) {
      color: rgb(78, 78, 78);
    }
    &:hover :deep(i) {
      color: black;
      transition: all 1s ease;
    }
    & :deep(.v-messages__message) {
      color: red;
    }
  }
  &__mini-cards {
    position: absolute;
    top: 0;
    left: calc(100% + 24px);
    max-width: 340px;
    width: calc(33vw - 48px);
    max-height: 100%;
    padding-right: 12px;
    overflow-y: scroll;
  }
  &__scroll-wrapper {
    padding-right: 12px;
    flex-grow: 1;
  }
}
</style>
