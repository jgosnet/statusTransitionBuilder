<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ displayName }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="12").py-1
        v-text-field(v-model="item.name" hide-details
          label="Token name" density="compact" )

    v-row.px-3.py-1.my-0
      v-col(:cols="labelSize").py-1.my-0
        v-text-field(v-model="item.label" hide-details
          label="Tbmd label"
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
      return `<${this.item.name}>`
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
    deleteItem(){
        console.log(`deleting tbmd item:`)
        console.log(this.item)
      this.$store.dispatch("tbmdDetails/deleteItem", this.item)
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