<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ item.key }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div().mb-3
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
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "MetadataFieldsItem",
  props:["item"],
  methods: {
    deleteItem(){
      console.log(`deleting metadata item:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteMetadataField", this.item)
    }
  },
  computed: {
    ...mapGetters('woPreset', ['possibleMetadataSources', 'possibleDisplayTypes', 'possibleStoredTypes'])
  }
}
</script>

<style scoped>

</style>