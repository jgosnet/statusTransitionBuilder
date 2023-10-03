<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ item.name }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div(v-show="!item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="12")
        b {{item.properties.length}} propertie(s)
        v-icon.ml-3.float-right(@click="item.isExpanded = !item.isExpanded" color="blue" ) fa-solid fa-pen-to-square


  div(v-show="item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="12").py-1
        v-text-field(v-model="item.name" hide-details
          label="Name (unique)" density="compact" )

    v-row.px-3.py-1
      v-col(cols="1").py-1.my-0
        v-btn(size="small" @click="addProperty")
          v-icon fa-solid fa-plus
      v-col(cols="11").py-1.my-0
        span(v-show="!item.properties.length" ) No properties.
        draggable(v-model="item.properties"
          handle=".handle"
          :group="item.index"
          @start="drag=true"
          @end="drag=false"
          item-key="index")
          template(#item="{element}")
            FormsViewItemProperty(@deleteProperty='deleteProperty'
                :itemProperty="element"
                :availableMdFields="availableMetadataFields")


    v-row.px-3.py-1
      v-col(cols="12")
        v-icon.float-right(@click="item.isExpanded = !item.isExpanded" color="green" ) fa-solid fa-check
</template>

<script>
import draggable from 'vuedraggable';
import FormsViewItemProperty from "@/components/Presets/WO/Forms/FormsViewItemProperty";

export default {
  name: "FormsViewItem",
  components: {
    FormsViewItemProperty,
    draggable
  },
  props: ['item'],
  data(){
    return {
        propertiesIndex: 0,
    }
  },
  computed: {
    availableMetadataFields(){
      let mdFields = this.$store.getters['woPreset/editableMetadataFieldLabels'];
      console.log(mdFields)
      let availableFieldLabels = []

      mdFields.forEach(name => {
        console.log(`name: ${name}`)
        const propertyWithLabel = this.item.properties.filter(elt => elt.associatedMetadata == name)
        console.log(propertyWithLabel)
        if (!propertyWithLabel.length){
          availableFieldLabels.push(name)
        }
      })

      return availableFieldLabels
    },
  },
  methods: {
    addProperty(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.properties.push({
        index: this.propertiesIndex,
        isExpanded: true,
        associatedMetadata: null,
        fieldType: 'string',
        isRequired: false,
        enumList: [],
        hasEnum: false,
      });
      this.propertiesIndex += 1;
    },
    deleteItem(){
      console.log(`deleting manual marker:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteForm", this.item)
    },
    deleteProperty(propertyIndex){
      console.log(`deleting property: ${propertyIndex}`);
      // eslint-disable-next-line vue/no-mutating-props
      this.item.properties = this.item.properties.filter((obj) => obj.index != propertyIndex);
    }
  }
}
</script>

<style scoped>

</style>