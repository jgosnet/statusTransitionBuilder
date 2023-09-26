<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Metadata Fields
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(metadataFields).length === 0" ) No Metadata Fields specified
    v-row
      v-col(cols="12")
        MetadataFieldsItem(v-for='item in metadataFields'
            :key='item.index'
            :item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addItem" elevation="2") Add New Metadata Field
</template>

<script>
import {mapGetters} from "vuex";
import MetadataFieldsItem from "@/components/Presets/WO/MetadataFieldsItem";

export default {
  name: "MetadataFields",
  components: {MetadataFieldsItem},
  data(){
    return {
      isExpanded: true,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['metadataFields']),
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    addItem(){
      this.$store.dispatch("woPreset/addMetadataField")
    }
  }
}
</script>

<style scoped>
fieldset{
  border-style: dashed;
}
</style>