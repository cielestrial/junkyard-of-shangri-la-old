<script setup lang="ts">
  import { theme } from '~/pages/index.vue';
  import MyAnimations from '../effects/MyAnimations.vue';

  const { colorScheme } = inject('theme') as theme;

  const skipLinksRef = ref<HTMLDivElement | null>(null);
  const focused = ref(false);

  onMounted(() => {
    if (skipLinksRef.value !== null) skipLinksRef.value.focus();
  });

  function focusSearchBar(event: MouseEvent) {
    const searchBar = document.getElementById('searchBar');
    searchBar?.scrollIntoView(true);
    searchBar?.focus();
    event.preventDefault();
  }

  const skipLinks =
    'absolute rounded top-3 left-4 opacity-0 cursor-default z-0 ' +
    'focus-visible:z-20 focus-visible:opacity-100 focus-visible:cursor-pointer ';
  const skipLink = 'p-2 rounded underline shadow ' + colorScheme;
</script>

<template>
  <div ref="skipLinksRef">
    <a
      href="#main"
      :class="skipLinks"
      @focus="focused = true"
      @blur="focused = false"
      @click="focusSearchBar">
      <MyAnimations name="slide">
        <p v-if="focused" :class="skipLink">Skip to main content</p>
      </MyAnimations>
    </a>
  </div>
</template>
