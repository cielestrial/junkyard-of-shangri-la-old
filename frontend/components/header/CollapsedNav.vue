<script setup lang="ts">
import { theme } from '~/pages/index.vue';
import MyAnimations from '../effects/MyAnimations.vue';
import MyOverlay from '../effects/MyOverlay.vue';
import { trapFocus } from '../effects/effectUtils';
import BIcons from '../icons/BIcons.vue';
import MySwitch from './MySwitch.vue';
import Country from './country/Country.vue';
import Members from './members/Members.vue';

const { colorScheme } = inject('theme') as theme;

const hamburgerRef = ref<HTMLButtonElement | null>(null);
const modalRef = ref<HTMLDivElement | null>(null);
const opened = ref(false);

const tabList = ref<NodeListOf<Element>>();
const tabLength = ref(-1);
const tabIndex = ref(-1);

watch(modalRef, (newVal) => {
  if (newVal !== null) {
    tabIndex.value = 0;
    tabList.value = newVal.querySelectorAll('button, input, [tabindex = "0"]');
    tabLength.value = tabList.value.length;
    if (tabLength.value > 0)
      (tabList.value[tabIndex.value] as HTMLInputElement).focus();
  }
});

function close() {
  opened.value = false;
  if (hamburgerRef.value !== null) hamburgerRef.value.focus();
}

const _menu =
  'w-fit h-fit z-10 rounded border-2 transition shadow ' + colorScheme;
const menuButton =
  _menu + 'relative mx-5 p-2 active:scale-95 hover:bg-gray-300 ';
const drawer = _menu + 'absolute right-0.5 top-0.5 ';
const exitButton =
  'w-fit h-fit text-red-500 bg-white/90 rounded active:scale-95 ' +
  'shadow dark:shadow-gray-900/50 ' +
  'absolute top-2 right-2';
</script>

<template>
  <div>
    <MyAnimations name="fade">
      <MyOverlay z="z-10" v-if="opened" @click="close" />
    </MyAnimations>

    <button
      aria-label="Menu"
      aria-haspopup="dialog"
      aria-controls="drawer"
      ref="hamburgerRef"
      type="button"
      :class="menuButton"
      @click="
        () => {
          opened = true;
          hamburgerRef?.focus();
        }
      "
    >
      <BIcons class="rounded-full" icon="list" size="1.5rem" />
    </button>

    <MyAnimations name="slide">
      <div
        id="drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Menu"
        ref="modalRef"
        v-if="opened"
        :class="drawer"
        @keydown.esc="
          (event) => {
            opened = false;
            event.stopImmediatePropagation();
          }
        "
        @keydown.tab="
          (event) => {
            tabIndex = trapFocus(event, tabLength, tabIndex);
            (tabList?.[tabIndex] as HTMLInputElement)?.focus();
          }
        "
      >
        <button
          aria-label="Close"
          type="button"
          @click="close"
          :class="exitButton"
        >
          <BIcons icon="x-square-fill" size="1.5rem" />
        </button>
        <div class="flex flex-col gap-y-8 p-8 items-center mt-4 mb-2">
          <Members />
          <MySwitch />
          <Country />
        </div>
      </div>
    </MyAnimations>
  </div>
</template>
