<template lang="pug">
fieldset.pa-1
  legend.left-align.pl-2.font-weight-bold
    span Video details
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    v-row
      v-col(:cols="labelSize")
        v-text-field(v-model="videoLabel"
          label="Video label" )
      v-col(:cols="checkboxcols")
        v-checkbox(:label="checkboxName" v-model="includeAssetName")
      v-col(v-show="includeAssetName" cols="5")
        v-text-field(v-model="videoAssetName"
          label="Asset Name" )
      v-col(cols="1")


</template>

<script>


export default {
  name: "VideoDetails",
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    labelSize(){
      if (this.includeAssetName === false){
        return 10
      } else{
        return 6
      }
    },
    checkboxName(){
      if (this.includeAssetName === false){
        return "Asset?"
      } else {
        return ""
      }
    },
    checkboxcols() {
      if (this.includeAssetName === false) {
        return 2
      } else {
        return 1
      }
    },
    videoAssetName: {
      get() {
        return this.$store.getters["videoDetails/videoAssetName"]
      },
      set(value) {
        this.$store.dispatch('videoDetails/updateVideoAssetName', value)
      }
    },
    includeAssetName: {
      get() {
        return this.$store.getters["videoDetails/includeAssetName"]
      },
      set(value) {
        this.$store.dispatch('videoDetails/updateIncludeAssetName', value)
      }
    },
    videoLabel: {
      get() {
        return this.$store.getters["videoDetails/videoLabel"]
      },
      set(value) {
        this.$store.dispatch('videoDetails/updateVideoLabel', value)
      }
    },
  },
  data: function(){
    return {
      isExpanded: true,
    }
  }

}
</script>

<style scoped>

</style>