<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-title(@click="isExpanded = !isExpanded")
    span Import existing configuration
    v-icon.float-right(:icon="expansionIcon" size="large")
  v-card-text.w-100(v-show="isExpanded" ).float-left
    v-textarea(v-model="importValue") test
    v-btn.float-left(@click="importConfiguration") import
</template>

<script>
import {python} from "@codemirror/lang-python";

export default {
  name: "ImporterPage",

  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
  },
  data(){
    return {
      isExpanded: false,
      importValue: "",
      lang: python(),
      linter: null,
    }
  },
  methods: {
    importConfiguration(){
      this.$store.dispatch('status/importConfig', this.importValue);
    }
  },
}
</script>

<style scoped>

</style>