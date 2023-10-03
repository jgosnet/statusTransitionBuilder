<template lang="pug">
fieldset.dashed-border.pa-1.mb-3
  legend.left-align.pl-2.w-100
    | {{ item.name }} {{statusStr}}
    //v-icon.ml-3(@click="deleteItem"
    //  size="x-small" ) fa-solid fa-trash-can
        div(id="expand")
    v-icon(:icon="expansionIcon" @click="isExpanded = !isExpanded")
    div(v-show="isExpanded").mb-3.w-100
      v-row.px-3.py-1
        v-col(cols="12").py-1.my-0
          v-select(v-model="item.form"
            hide-details
              :items="formsNames"
            clearable="true"
              label="Editable Metadata form"
              density="compact")

      v-row.px-3.py-1
        v-col(cols="12").py-1.my-0
          ReadOnlyViewSection(:item="item")

    //v-row.px-3.py-1
    //  v-col(cols="12").py-1.mt-2.dashed-border
    //    v-tabs(v-model="tab" )
    //      v-tab(value="form") Form
    //      v-tab(value="readonly") Read-only fields
    //    v-window(v-model="tab")
    //      v-window-item(value="form" )
    //        //MetadataViewItem(:item="item.form")
    //        | Not available yet.
    //      v-window-item(value="readonly" )


</template>

<script>
import ReadOnlyViewSection from "@/components/Presets/WO/MetadataViews/ReadOnlyViewSection";
import {mapGetters} from "vuex";
export default {
  name: "MetadataViewItem",
  components: {ReadOnlyViewSection},
  props: ["item"],
  data(){
    return {
      tab: "readonly",
      isExpanded: false,
    }
  },
  methods: {

  },
  computed: {
    ...mapGetters('woPreset', ['formsNames']),
    statusStr(){
      if (this.item.readOnlyFields.length > 0){
        return `(${this.item.readOnlyFields.length} items)`
      } else {
        return ''
      }
    },
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    }
  }
}
</script>

<style scoped>
.dashed-border{
  border-style: dashed;
  border-radius: 10px;
  border-width: 1px;
}

v-window{
background-color: whitesmoke;
}
</style>