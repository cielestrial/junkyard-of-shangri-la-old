<script setup lang="ts">
  import { inject, onMounted, ref } from 'vue-demi';
  import MyAnimations from '../effects/MyAnimations.vue';
  import type { theme } from '~/pages/index.vue';

  type landmarks = ['Main', 'Footer'];
  const props = defineProps<{ to: landmarks[number] }>();

  const { colorScheme } = inject('theme') as theme;

  const skipLinksRef = ref<HTMLDivElement | null>(null);
  const focused = ref(false);

  onMounted(() => {
    if (skipLinksRef.value !== null && props.to === 'Main')
      skipLinksRef.value.focus();
  });

  function focusElement(event: MouseEvent, id: string) {
    const element = document.getElementById(id);
    element?.scrollIntoView(true);
    element?.focus();
    event.preventDefault();
  }

  const skipLinks =
    'absolute rounded top-3 left-4 opacity-0 cursor-default z-0 shadow active:scale-95 ' +
    'focus-visible:z-20 focus-visible:opacity-100 focus-visible:cursor-pointer ' +
    colorScheme;
  const skipLink = 'p-2 rounded underline transition hover:animate-pulse ';
</script>

<template>
  <div :id="`skipTo${to}`" ref="skipLinksRef">
    <a
      v-if="to === 'Main'"
      href="#main"
      :class="skipLinks"
      :aria-labelledby="`${to}Text`"
      @focus="focused = true"
      @blur="focused = false"
      @click="(event) => focusElement(event, 'searchBar')"
    >
      <MyAnimations name="slide-down">
        <p v-show="focused" :id="`${to}Text`" :class="skipLink">
          Skip to main content
        </p>
      </MyAnimations>
    </a>
    <a
      v-else
      href="#footer"
      :class="skipLinks"
      :aria-labelledby="`${to}Text`"
      @focus="focused = true"
      @blur="focused = false"
      @click="(event) => focusElement(event, 'contactButton')"
    >
      <MyAnimations name="slide-down">
        <p v-show="focused" :id="`${to}Text`" :class="skipLink">
          Skip to end of content
        </p>
      </MyAnimations>
    </a>
  </div>
</template>
