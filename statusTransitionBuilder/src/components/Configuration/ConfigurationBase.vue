<template lang="pug">
v-card.mx-0
  v-card-title Steps
  v-card-text
    StepsView.mb-3

</template>

<script>
import StepsView from "@/components/Configuration/StepsView";
export default {
  name: "ConfigurationBase",
  components: {StepsView}
}
</script>

<style scoped>

</style>