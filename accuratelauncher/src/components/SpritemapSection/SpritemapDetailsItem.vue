<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2 {{ displayName }}
  div()
    v-row.px-3.py-1.my-0
      v-col(:cols="labelSize").py-1.my-0
        v-text-field(v-model="item.label" hide-details
          label="label"
          density="compact" )
      v-col(:cols="checkboxcols").py-1.my-0
        v-checkbox(:label="checkboxName" hide-details
          v-model="item.includeAssetName"
          density="compact" )
      v-col(v-show="item.includeAssetName" cols="5").py-1.my-0
        v-text-field(v-model="item.assetName" hide-details
          label="Asset Name"
          density="compact" )


</template>

<script>
export default {
  name: "TbmdDetailsItem",
  props:["item"],
  data(){
    return {
    }
  },
    computed: {
    displayName(){
      if (this.item.name === 'spritemap_image'){
        return 'Image'
      } else if (this.item.name === 'spritemap_manifest'){
        return 'Manifest'
      }
      return 'unknown..'
    },
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    labelSize(){
      if (this.item.includeAssetName === false){
        return 10
      } else{
        return 6
      }
    },
    checkboxName(){
      if (this.item.includeAssetName === false){
        return "Asset?"
      } else {
        return ""
      }
    },
    checkboxcols() {
      if (this.item.includeAssetName === false) {
        return 2
      } else {
        return 1
      }
    },
  },
  methods: {
  }
}
</script>

<style scoped>
.dashed-border{
 border-style: dashed;
  background-color: whitesmoke;
}
</style>