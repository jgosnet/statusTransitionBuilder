<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-title(@click="isExpanded = !isExpanded")
    span Import existing configuration
    v-icon.float-right(:icon="expansionIcon" size="large")
  v-card-text.w-100(v-show="isExpanded" ).float-left
    code-mirror.w-100.CodeMirror(v-model="importValue"
      basic :lang="lang"
      )
    v-btn.float-left import
</template>

<script>
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
      importValue: "{}",
    }
  },
}
</script>

<style scoped>

</style>