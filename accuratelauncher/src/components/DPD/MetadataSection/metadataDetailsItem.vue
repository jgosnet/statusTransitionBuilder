<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ item.keyname }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="12").py-1
        v-text-field(v-model="item.keyname" hide-details
          label="Key" density="compact" )

    v-row.px-3.py-1.my-0
      v-col(cols="12").py-1.my-0
        v-text-field(v-model="item.jmespath" hide-details
          label="Jmespath"
          density="compact" )


</template>

<script>
export default {
  name: "metadataDetailsItem",
  props:["item"],
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
      this.$store.dispatch("metadata/deleteItem", this.item)
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