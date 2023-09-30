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
            v-card(elevation="2" density="compact" variant="outlined" ).my-1.py-0
              v-card-text.ma-0.pa-1
                v-icon.handle.float-left fa-solid fa-bars
                | --{{element.index}}--
                //v-icon(@click="removeItem(element)") fa-solid fa-xmark

    v-row.px-3.py-1
      v-col(cols="12")
        v-icon.float-right(@click="item.isExpanded = !item.isExpanded" color="green" ) fa-solid fa-check
</template>

<script>
import draggable from 'vuedraggable';

export default {
  name: "FormsViewItem",
  components: {
    draggable
  },
  props: ['item'],
  data(){
    return {
        propertiesIndex: 0,
    }
  },
  computed: {
  },
  methods: {
    addProperty(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.properties.push({
        "index": this.propertiesIndex,
      });
      this.propertiesIndex += 1;
    },
    deleteItem(){
      console.log(`deleting manual marker:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteForm", this.item)
    }
  }
}
</script>

<style scoped>

</style>