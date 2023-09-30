<template lang="pug">
fieldset.dashed-border.pa-1
  //| {{item}}
  legend.left-align.pl-2
    | {{ item.key }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div(v-show="!item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="12")
        | source: {{item.source}} - display name: {{item.displayName}}
        v-icon.float-right(@click="item.isExpanded = !item.isExpanded" color="blue" ) fa-solid fa-pen-to-square
  div(v-show="item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="6").py-1
        v-text-field(v-model="item.key" hide-details
          label="Key" density="compact" )
      v-col(cols="6").py-1
        v-text-field(v-model="item.displayName" hide-details
          label="Display Name" density="compact" )
    v-row.px-3.py-1
      v-col(cols="12").py-1.my-0
        v-select(v-model="item.source" hide-details
          :items="possibleMetadataSources"
          label="Source"
          density="compact")
    v-row.px-3.py-1
      v-col(cols="6").py-1
        v-select(v-model="item.displayType" hide-details clearable=""
        :items="possibleDisplayTypes"
          label="Display Type" density="compact" )
      v-col(cols="6").py-1
        v-select(v-model="item.storedType" hide-details clearable=""
        :items="possibleStoredTypes"
          label="Stored Type" density="compact" )
    v-row.px-3.py-1(v-show="item.source === 'metadata'")
      v-col(cols="item.autoPopulate ? 12 : 1").py-1
        v-checkbox(:label="autoPopulateName"
          v-model="item.autoPopulate"
          density="compact" hide-details)
      v-col(v-show="item.autoPopulate === true" cols="11").py-1
        v-text-field(v-model="item.jmespath" hide-details
          label="Jmespath" density="compact" )
    v-row.px-3.py-1
      v-col(cols="12")
        v-icon.float-right(@click="item.isExpanded = !item.isExpanded" color="green" ) fa-solid fa-check

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "MetadataFieldsItem",
  props:["item"],
  data(){
    return {
      isExpanded: true,
    }
  },
  methods: {
    deleteItem(){
      console.log(`deleting metadata item:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteMetadataField", this.item)
    }
  },
  computed: {
    ...mapGetters('woPreset', ['possibleMetadataSources', 'possibleDisplayTypes', 'possibleStoredTypes']),
    autoPopulateName(){
      if (this.item.autoPopulate === true){
        return ""
      } else {
        return "Auto populate ?"
      }
    },
  }
}
</script>

<style scoped>
fieldset{
background-color: whitesmoke;
}

</style>