<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Metadata Fields
    //v-tooltip(text="123" )
    //  template(v-slot:activator="{ props }")
    //    v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
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
        //v-btn(prepend-icon="fa-solid fa-plus"
        //@click="addItem" elevation="2" variant="outlined" ) Add New Metadata Field
        v-dialog.w-50
          template(v-slot:activator="{ props }")
            v-btn(prepend-icon="fa-solid fa-plus" v-bind="props"
               elevation="2" variant="outlined" ) Add New Metadata Field
          template(v-slot:default="{ isActive }")
            v-card(title="New Metadata field")
              v-card-text
                v-row.px-3.py-1
                  v-col(cols="12").py-1.my-0
                    v-select(v-model="source" hide-details
                      :items="possibleMetadataSources"
                      label="Source"
                      density="compact")

                div(v-show="this.source === 'metadata'" )
                  v-row.px-3.py-1
                    v-col(cols="6").py-1
                      v-text-field(v-model="key" hide-details
                        label="Key" density="compact")
                    v-col(cols="6").py-1
                      v-text-field(v-model="label" hide-details
                        label="Display name" density="compact")
                  v-row.px-3.py-1
                    v-col(cols="item.autoPopulate ? 12 : 1").py-1
                      v-checkbox(:label="autoPopulateName"
                        v-model="autoPopulate"
                        density="compact" hide-details)
                    v-col(v-show="autoPopulate === true" cols="11").py-1
                      v-text-field(v-model="jmespath" hide-details
                        label="Jmespath" density="compact" )

                v-row(v-show="this.source === 'properties'" ).px-3.py-1
                  v-col(cols="12").py-1
                    v-select(v-model="propertyKey" hide-details
                      :items="possiblePropertiesNames"
                      label="Key"
                      density="compact")

              v-card-actions
                v-spacer
                v-btn(@click="isActive.value = false") Cancel
                v-btn(@click="isActive.value = false;addItem();" :disabled="!newFormIsValid" ) confirm


</template>

<script>

import {mapGetters} from "vuex";
import MetadataFieldsItem from "@/components/Presets/WO/MetadataFieldsItem";

export default {
  name: "MetadataFields",
  components: {MetadataFieldsItem},
  data(){
    return {
      key: "",
      label: "",
      jmespath: "",
      autoPopulate: false,
      propertyKey: "duration",
      source: "metadata",
      isExpanded: false,
    }
  },
  computed: {
    autoPopulateName(){
      if (this.autoPopulate === true){
        return ""
      } else {
        return "Auto populate ?"
      }
    },
    newFormIsValid(){
      if ((this.source === 'metadata' && this.key)
      || (this.source === 'properties' && this.propertyKey)){
        return true
      }
      return false
    },
    ...mapGetters('woPreset', ['metadataFields', 'possibleMetadataSources',
      'possiblePropertiesNames', "possibleProperties"]),
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
      let payload = {
        source: this.source
      }
      if (this.source === 'metadata'){
        payload['key'] = this.key
        payload['displayName'] = this.label
        payload['jmespath'] = this.jmespath
        payload['autoPopulate'] = this.autoPopulate
      } else if (this.source === 'properties'){
        payload['key'] = this.propertyKey
        // find the existing property
        const item = this.possibleProperties.find((element) => element.key === this.propertyKey);
        payload['displayName'] = item.label
        payload['storedType'] = item.storedType
        payload['displayType'] = item.displayType
      }

      this.$store.dispatch("woPreset/addMetadataField", payload)

      this.autoPopulate = false;
      this.jmespath = "";
      this.key = "";
      this.label = "";
      this.propertyKey = "duration";
      this.source = "metadata";
    }
  }
}
</script>

<style scoped>
fieldset{
  border-style: dashed;
}
legend{
  font-size: large;
}
</style>