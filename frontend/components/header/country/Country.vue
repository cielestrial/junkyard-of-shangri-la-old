<script setup lang="ts">
import { ref, computed, inject } from "vue";
import Overlay from "../../Overlay.vue";
import Flags_EN from "./En_Flags.vue";
import BIcons from "../../icons/BIcons.vue";
import { theme } from "~/pages/index.vue";
import MyAnimations from "../../MyAnimations.vue";

const { darkTheme, colorScheme } = inject("theme") as theme;

interface all_countries {
  AU: "Australia";
  BE: "Belgium";
  CA: "Canada";
  DK: "Denmark";
  EU: "Europe";
  FR: "France";
  GB: "United Kingdom";
  IE: "Ireland";
  JP: "Japan";
  LT: "Lithuania";
  PL: "Poland";
  RO: "Romania";
  SE: "Sweden";
  US: "United States";
  ZA: "South Africa";
}
const en_countries = Object.freeze({
  AU: "Australia",
  CA: "Canada",
  EU: "Europe",
  GB: "United Kingdom",
  US: "United States",
});
type countriesT = typeof en_countries;
// type countryNames = countriesT[keyof countriesT];
export type countryCodesT = keyof countriesT;
const countryCodes = Object.keys(en_countries) as Array<countryCodesT>;

const opened = ref(false);
const options = ref(countryCodes);
const selected = ref<countryCodesT>("CA");

function menuHandler(option: countryCodesT) {
  selected.value = option;
  opened.value = false;
}

const dropdownMenu = "relative w-28 cursor-pointer ";

const select = computed(
  () =>
    "rounded flex flex-row justify-between items-center p-2 border-2 " +
    "drop-shadow hover:bg-slate-300 text " +
    colorScheme.value +
    (opened.value ? "border-b-0 rounded-bl-none rounded-br-none " : " ")
);

const caret = computed(
  () =>
    "transition transform-gpu origin-center ml-2 " +
    (opened.value ? "rotate-180 " : "")
);

const dropdownList = computed(
  () =>
    "w-28 cursor-pointer absolute mt-[2.63rem] list-outside list-none " +
    "drop-shadow-2xl transition transform-gpu border-2 " +
    "border-t-0 rounded-br rounded-bl " +
    colorScheme.value
);

const dropdownItem = computed(
  () =>
    "flex flex-row p-2 text border-t-2 hover:bg-slate-300 " +
    (darkTheme.value ? "border-slate-400 " : "border-slate-700 ")
);
</script>

<template>
  <div>
    <Overlay v-if="opened" @click="opened = false" />
    <MyAnimations name="slide">
      <ul v-if="opened" :class="dropdownList">
        <li
          v-for="(option, key) in options"
          :key="key"
          :class="{ active: option === selected }"
          @click="() => menuHandler(option)"
        >
          <button type="button" :class="dropdownItem">
            <Flags_EN class="mr-2" :country="option" size="1.5rem" />
            {{ option }}
          </button>
        </li>
      </ul>
    </MyAnimations>

    <div :class="dropdownMenu">
      <button type="button" :class="select" @click="opened = !opened">
        <div class="flex flex-row">
          <Flags_EN class="mr-2" :country="selected" size="1.5rem" />
          <span class="selected">{{ selected }}</span>
        </div>
        <BIcons :class="caret" icon="caret-down-fill" size="1rem" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.active {
  background-color: gray !important;
  cursor: default !important;
  pointer-events: none !important;
}
</style>
