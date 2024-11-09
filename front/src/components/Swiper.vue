<template>
  <div class="swipe-card-container">
    <div class="swipe-card-container__card" v-if="nextCard">
      <div class="swipe-card-container__card__row">
        <h3>{{ nextCard.search }}</h3>
      </div>
      <div class="swipe-card-container__card__row" v-if="nextCard.category">
        <span :class="{ decor: keys.has('category') }"
          ><b>Категория: </b>{{ nextCard.category }}</span
        >
        <v-btn
          @click="appendKey('category')"
          class="swipe-card-container__card__row__btn"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__row" v-if="nextCard.vendor">
        <span :class="{ decor: keys.has('vendor') }"
          ><b>Производитель: </b>{{ nextCard.vendor }}</span
        >
        <v-btn
          class="swipe-card-container__card__row__btn"
          @click="appendKey('vendor')"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__row" v-if="nextCard.model">
        <span :class="{ decor: keys.has('model') }"
          ><b>Модель: </b>{{ nextCard.model }}</span
        >
        <v-btn
          class="swipe-card-container__card__row__btn"
          @click="appendKey('model')"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__scroll">
        <div
          class="swipe-card-container__card__row"
          v-for="i in nextCard.props"
        >
          <span :class="{ decor: keys.has(i.name) }"
            ><b>{{ i.name }}: </b>{{ i.value }}</span
          >
          <div class="d-flex">
            <v-tooltip text="Значение этого показателя было отредактировано пользователем" v-if="i.changed">
              <template v-slot:activator="{ props }">
                <v-icon
                  v-bind="props"
                  class="mr-2"
                  icon="mdi-alert"
                  color="warning"
                ></v-icon>
              </template>
            </v-tooltip>
            <v-btn
              @click="appendKey(i.name)"
              style="padding: 2px; margin-right: -6px"
              variant="text"
              size="medium"
              icon="mdi-close"
              color="red"
            ></v-btn>
          </div>
        </div>
      </div>
    </div>
    <div
      ref="card"
      @swiped="handleSwipe"
      v-swipe
      class="swipe-card-container__card"
      v-if="currentCard"
    >
      <div class="swipe-card-container__card__row">
        <h3>{{ currentCard.search }}</h3>
      </div>
      <div class="swipe-card-container__card__row" v-if="currentCard.category">
        <span :class="{ decor: keys.has('category') }"
          ><b>Категория: </b>{{ currentCard.category }}</span
        >
        <v-btn
          @click="appendKey('category')"
          class="swipe-card-container__card__row__btn"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__row" v-if="currentCard.vendor">
        <span :class="{ decor: keys.has('vendor') }"
          ><b>Производитель: </b>{{ currentCard.vendor }}</span
        >
        <v-btn
          class="swipe-card-container__card__row__btn"
          @click="appendKey('vendor')"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__row" v-if="currentCard.model">
        <span :class="{ decor: keys.has('model') }"
          ><b>Модель: </b>{{ currentCard.model }}</span
        >
        <v-btn
          class="swipe-card-container__card__row__btn"
          @click="appendKey('model')"
          variant="text"
          size="medium"
          icon="mdi-close"
          color="red"
        ></v-btn>
      </div>
      <div class="swipe-card-container__card__scroll">
        <div
          class="swipe-card-container__card__row"
          v-for="i in currentCard.props"
        >
          <span :class="{ decor: keys.has(i.name) }"
            ><b>{{ i.name }}: </b>{{ i.value }}</span
          >
          <div class="d-flex">
            <v-tooltip text="Значение этого показателя было отредактировано пользователем" v-if="i.changed">
              <template v-slot:activator="{ props }">
                <v-icon
                  v-bind="props"
                  class="mr-2"
                  icon="mdi-alert"
                  color="warning"
                ></v-icon>
              </template>
            </v-tooltip>
            <v-btn
              @click="appendKey(i.name)"
              style="padding: 2px; margin-right: -6px"
              variant="text"
              size="medium"
              icon="mdi-close"
              color="red"
            ></v-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useSessionStore } from "@/stores/SessionStore";
import { computed, ref } from "vue";

const card = ref();

const keys = ref(new Set());

const currentCard = computed(() => {
  return cards.value.at(-1);
});
const nextCard = computed(() => {
  if (cards.value.at(-2)) return cards.value.at(-2);
  return false;
});

function appendKey(key) {
  if (keys.value.has(key)) {
    keys.value.delete(key);
  } else {
    keys.value.add(key);
  }
}

const sessionStore = useSessionStore();

const cards = ref(sessionStore.tabs);

function handleSwipe(arg) {
  if (arg.detail === "left") {
    card.value.style.left = "-100vw";
    setTimeout(() => {
      card.value.style.left = "0";
      card.value.style.transition = undefined;
      keys.value.clear();
      cards.value.pop();
    }, 200);
  }
  if (arg.detail === "right") {
    card.value.style.left = "100vw";
    setTimeout(() => {
      card.value.style.left = "0";
      card.value.style.transition = undefined;
      keys.value.clear();
      cards.value.pop();
    }, 200);
  }
}
</script>
<style scoped lang="scss">
.decor {
  text-decoration: line-through $primary-lighter;
}
.swipe-card-container {
  background-color: white;
  box-shadow: 0 0 6px -3px black;
  border-radius: 12px;
  margin-top: 24px;
  width: 440px;
  max-width: 90vw;
  height: calc(100vh - 120px);
  position: relative;
  & * {
    user-select: none;
  }
  &__card {
    transition: opacity 1s ease;
    box-shadow: 0 0 6px -4px black;
    border-radius: 12px;
    position: absolute;
    background-color: white;
    display: flex;
    flex-direction: column;
    padding: 16px 24px;
    width: 100%;
    height: 100%;
    & h3 {
      font-size: 22px;
    }

    &__scroll {
      border-top: 1px solid $bg-grey-light;
      padding-top: 12px;
      flex-grow: 1;
      overflow-y: scroll;
      overflow-x: hidden;
      padding-right: 4px;
    }
  }
}
.swipe-card-container__card__row {
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  &__btn {
    padding: 3px;
    margin-right: 4px;
  }
}
</style>
