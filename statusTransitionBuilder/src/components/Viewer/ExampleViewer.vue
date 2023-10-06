<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-title(@click="isExpanded = !isExpanded")
    span Usage
    v-icon.float-right(:icon="expansionIcon" size="large")
  v-card-text(v-show="isExpanded" ).float-left
    v-code
      | {{exampleCode}}
</template>

<script>
export default {
  name: "ExampleViewer",
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
      exampleCode: "status_helper = test"
    }
  }
}
</script>

<style scoped>

</style>