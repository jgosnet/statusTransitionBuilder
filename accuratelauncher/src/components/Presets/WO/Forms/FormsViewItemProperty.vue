<template lang="pug">
v-card(elevation="2" density="compact" variant="outlined" ).my-1.py-0
  v-card-text.ma-0.pa-1
    v-icon.handle.float-left fa-solid fa-bars
    div(v-if="!itemProperty.isExpanded" )
      v-row.px-3.py-1
        v-col(cols="12")
          | ({{itemProperty.fieldType}})
          b.pl-2  {{itemProperty.associatedMetadata}}
          v-icon.float-right(@click="itemProperty.isExpanded = !itemProperty.isExpanded" color="blue" ) fa-solid fa-pen-to-square
    div(v-else)
      v-row.px-3.py-1
        v-col(cols="8").py-1

          v-select(v-model="itemProperty.associatedMetadata" hide-details clearable
                      :items="availableMdFields"
                      label="Metadata"
                      density="compact")
        v-col(cols="4").py-1
          v-icon.float-right.pt-6.pl-6(@click="deleteProperty" color="red" ) fa-solid fa-trash-can
          v-checkbox(label="Required ?" hide-details
              v-model="itemProperty.isRequired"
              density="compact" )

      div(v-show="itemProperty.associatedMetadata")
        v-row.px-3.py-1
          v-col(cols="6").py-1
            v-select(v-model="itemProperty.fieldType" hide-details
                      :items="possibleFieldTypes"
                      label="Field Type"
                      density="compact")
          v-col(cols="6").py-1
            v-select(v-show="itemProperty.fieldType != 'boolean'"
                v-model="itemProperty.displayType" hide-details
                      :items="displayType"
                      label="Display Type" clearable
                      density="compact")
        v-row.px-3.py-1(v-show="isEnumPossible")
          v-col(:cols="itemProperty.hasEnum ? '1': '12'").py-1
            v-checkbox(:label="!itemProperty.hasEnum ? 'Enum list ?': ''" hide-details
              v-model="itemProperty.hasEnum"
              density="compact" )
          v-col(v-show="itemProperty.hasEnum" cols="11").py-1
            v-row.px-3.py-1
              draggable(v-model="itemProperty.enumList"
                handle=".handle"
                :group="itemProperty.index"
                @start="drag=true"
                @end="drag=false"
                item-key="index").w-100

                template(#item="{element}")
                  v-card.mb-2.py-0(elevation="6" )
                    v-card-text.ma-0.pa-1
                      v-row.px-3.py-1
                        v-col(cols="1")
                          v-icon.handle.float-left fa-solid fa-bars

                        v-col(cols="10")
                          v-text-field(v-model="element.name" hide-details
                                label="" density="compact" )

                        v-col(cols="1")
                          v-icon.handle.float-right(color="red" @click="deleteEnumOption(element)") fa-solid fa-trash-can


            v-row.px-3.py-1
              v-btn(@click="addEnum(itemProperty)") add enum

      v-row.px-3.py-1
        v-col(cols="12")
          v-icon.float-right(@click="itemProperty.isExpanded = !itemProperty.isExpanded" color="green" ) fa-solid fa-check

</template>

<script>
import {mapGetters} from "vuex";
import draggable from "vuedraggable";


export default {
  name: "FormsViewItemProperty",
  props: ['itemProperty', 'availableMdFields'],
  components:{
    draggable
  },
  data(){
    return {
      possibleFieldTypes: ['string', 'array', 'boolean'],
      displayType: ['radiobutton', 'checkbox', 'boolean', 'date'],
      enumIndex: 0,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['editableMetadataFieldLabels']),
    // availableMetadataFields(){
    //   let mdFields = this.$store.getters['woPreset/editableMetadataFieldLabels'];
    //   mdFields = mdFields.filter(obj => obj.)
    // },
    isEnumPossible(){
      if (this.itemProperty.displayType === 'radiobutton' ||
        this.itemProperty.displayType === 'checkbox' ||
        !this.itemProperty.displayType){
        return true
      }
      return false
    }
  },
  methods: {
    deleteProperty(){
      this.$emit('deleteProperty', this.itemProperty.index)
    },
    addEnum(propertyObject){
      propertyObject.enumList.push({
        index: this.enumIndex,
        name: ''
      });
      this.enumIndex += 1;
    },
    deleteEnumOption(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.itemProperty.enumList = this.itemProperty.enumList.filter(obj => obj.index != element.index);
    }
  }

}
</script>

<style scoped>

</style>