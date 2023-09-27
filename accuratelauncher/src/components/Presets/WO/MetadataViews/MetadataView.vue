<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Metadata View
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1

  div(v-show="isExpanded" )
    v-row
      v-col(cols="12")
        MetadataViewItem.noborder(v-for='item in metadataViewAsset'
            :key='item.name'
            :item="item" )

</template>

<script>
import {mapGetters} from "vuex";
import MetadataViewItem from "@/components/Presets/WO/MetadataViews/MetadataViewItem";

export default {
  name: "MetadataView",
  components: {MetadataViewItem},
  data(){
    return {
      tab: "asset",
      isExpanded: true,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['metadataViewAsset']),
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
legend{
  font-size: large;
}
.noborder{
  border-style: none;
}
</style>