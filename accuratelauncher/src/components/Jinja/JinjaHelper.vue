<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-title(@click="isExpanded = !isExpanded")
    span Jinja Syntax examples
    v-icon.float-right(:icon="expansionIcon" size="large")
  v-card-text(v-show="isExpanded" ).float-left
    v-code
      | {{jinjaExample1}}
</template>

<script>
export default {
  name: "JinjaHelper",
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
  },
  data: function(){
    return {
      isExpanded: false,
      jinjaExample1: "{{ DYNAMIC_PRESET_DATA[\" \"] | default(\"\") }}"
    }
  }
}
</script>

<style scoped>

</style>