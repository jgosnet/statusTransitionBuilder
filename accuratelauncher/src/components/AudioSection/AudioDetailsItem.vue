<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ audioItem.name }}
    v-icon.ml-3(@click="deleteAudioItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="9").py-1
        v-text-field(v-model="audioItem.name" hide-details
          label="Track name" density="compact" )
      v-col(cols="1")
      v-col(cols="2").py-1.my-0
        v-checkbox(label="Enabled ?" hide-details
          v-model="audioItem.enabled"
          :color="audioItem.enabled ? 'green' : 'red'"
          density="compact" )
    v-row.px-3.py-1.my-0
      v-col(:cols="labelSize").py-1.my-0
        v-text-field(v-model="audioItem.label" hide-details
          label="Audio label"
          density="compact" )
      v-col(:cols="checkboxcols").py-1.my-0
        v-checkbox(:label="checkboxName" hide-details
          v-model="audioItem.includeAssetName"
          density="compact" )
      v-col(v-show="audioItem.includeAssetName" cols="5").py-1.my-0
        v-text-field(v-model="audioItem.assetName" hide-details
          label="Asset Name"
          density="compact" )
    v-row.px-3.py-1.my-0
      v-col(:cols="audioItem.includeLanguage ? 1 : 12").py-1
        v-checkbox(v-model="audioItem.includeLanguage" hide-details
          :label="audioItem.includeLanguage ? '': 'Specify Language ?'" density="compact" )
      v-col(v-show="audioItem.includeLanguage" cols="11").py-1
        v-text-field(v-model="audioItem.language" hide-details
          label="Language" density="compact" )

</template>

<script>
export default {
  name: "AudioDetailsItem",
  props:["audioItem"],
  data(){
    return {
    }
  },
    computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    labelSize(){
      if (this.audioItem.includeAssetName === false){
        return 10
      } else{
        return 6
      }
    },
    checkboxName(){
      if (this.audioItem.includeAssetName === false){
        return "Asset?"
      } else {
        return ""
      }
    },
    checkboxcols() {
      if (this.audioItem.includeAssetName === false) {
        return 2
      } else {
        return 1
      }
    },
  },
  methods: {
    deleteAudioItem(){
        console.log(`deleting audio item:`)
        console.log(this.audioItem)
      this.$store.dispatch("audioDetails/deleteItem", this.audioItem)
      }
  }
}
</script>

<style scoped>
.dashed-border{
 border-style: dashed;
  background-color: whitesmoke;
}
</style>