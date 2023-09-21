<script setup lang="ts">
import { computed, inject, ref } from "vue";
import MyAnimations from "~/components/MyAnimations.vue";
import Overlay from "~/components/Overlay.vue";
import { theme } from "~/pages/index.vue";
import BIcons from "../../icons/BIcons.vue";
import Flags_EN from "./En_Flags.vue";
import { countryCodes, countryCodesT } from "./countryData";

const { darkTheme, colorScheme } = inject("theme") as theme;

const opened = ref(false);
const options = ref(countryCodes);
const selected = ref<countryCodesT>("CA");

function menuHandler(option: countryCodesT) {
  selected.value = option;
  opened.value = false;
}

const dropdownMenu = "relative w-28 h-fit";

const select = computed(
  () =>
    "w-28 h-10 rounded flex justify-between items-center p-2 border-2 " +
    "shadow-md hover:bg-slate-300 relative z-10 " +
    (opened.value ? "border-b-0 rounded-bl-none rounded-br-none " : "") +
    colorScheme.value
);

const caret = computed(
  () =>
    "my-auto ml-2 transition " +
    (opened.value ? "rotate-180 " : "") +
    (darkTheme.value ? "text-white/90 " : "text-black/90 ")
);

const dropdownList = computed(
  () =>
    "w-28 h-fit mt-10 absolute list-outside list-none shadow-md z-10 " +
    "border-2 border-t-0 rounded-br rounded-bl " +
    colorScheme.value
);

const dropdownItem = computed(
  () =>
    "w-full h-10 flex p-2 border-t-2 hover:bg-slate-300 " +
    (darkTheme.value ? "border-slate-400 " : "border-slate-700 ")
);
</script>

<template>
  <div>
    <MyAnimations name="fade">
      <Overlay z="z-10" v-if="opened" @click="opened = false" />
    </MyAnimations>
    <MyAnimations name="slide">
      <ul v-if="opened" :class="dropdownList">
        <li
          v-for="(option, key) in options"
          :key="key"
          :class="{ active: option === selected }"
        >
          <button
            type="button"
            :class="dropdownItem"
            @click="() => menuHandler(option)"
          >
            <Flags_EN class="mr-2 my-auto" :country="option" size="2.5rem" />
            <span class="my-auto text-left">{{ option }}</span>
          </button>
        </li>
      </ul>
    </MyAnimations>
    <div :class="dropdownMenu">
      <button type="button" :class="select" @click="opened = !opened">
        <div class="flex">
          <Flags_EN class="mr-2 my-auto" :country="selected" size="2rem" />
          <span class="my-auto text-left">{{ selected }}</span>
        </div>
        <BIcons :class="caret" icon="caret-down-fill" size="1rem" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.active {
  background-color: #94a3b8;
  pointer-events: none;
}
</style>
