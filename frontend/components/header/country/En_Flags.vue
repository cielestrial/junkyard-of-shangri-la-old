<script setup lang="ts">
import { countryCodesT } from "./countryData";

import AU from "./flags/AU.vue";
import CA from "./flags/CA.vue";
import EU from "./flags/EU.vue";
import GB from "./flags/GB.vue";
import US from "./flags/US.vue";

defineProps<{
  country: countryCodesT;
  size: string;
}>();
</script>

<template>
  <AU v-if="country === 'AU'" :size="size" />
  <CA v-else-if="country === 'CA'" :size="size" />
  <EU v-else-if="country === 'EU'" :size="size" />
  <GB v-else-if="country === 'GB'" :size="size" />
  <US v-else-if="country === 'US'" :size="size" />
</template>
