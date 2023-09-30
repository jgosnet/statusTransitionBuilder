<template lang="pug">
fieldset.dashed-border.pa-1.mb-4
  legend.left-align.pl-2
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div(v-show="!item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="12")
        b {{item.title}}
        v-icon.ml-3.float-right(@click="item.isExpanded = !item.isExpanded" color="blue" ) fa-solid fa-pen-to-square
        div.ml-3.box(:style="{ backgroundColor: item.hoverColor}")
        div.ml-3.box(:style="{ backgroundColor: item.backgroundColor}")

  div(v-show="item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="6").py-1
        v-text-field(v-model="item.track" hide-details
          label="Track (unique, lower case, no spaces)" density="compact" )
      v-col(cols="6").py-1
        v-text-field(v-model="item.title" hide-details
          label="Display Name" density="compact" )

    v-row.px-3.py-1
      v-col(cols="4").py-1.my-0
        v-text-field(v-model="item.backgroundColor" hide-details
          label="Background color" density="compact" )
      v-col(cols="2").py-1.my-0
        color-picker.ml-5(v-model:pureColor="item.backgroundColor" format="hex6")
      v-col(cols="4").py-1.my-0
        v-text-field(v-model="item.hoverColor" hide-details
          label="Hover color" density="compact" )
      v-col(cols="2").py-1.my-0
        color-picker.round-border(v-model:pureColor="item.hoverColor" format="hex6")
    v-row.px-3.py-1
      v-col(cols="10").py-1.my-0
        v-select(v-model="item.associatedForm" hide-details clearable
          :items="formsNames"
          label="Form (optional)" density="compact" )
      v-col(cols="2")
        v-icon.float-right(@click="item.isExpanded = !item.isExpanded" color="green" ) fa-solid fa-check
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "ManualMarkerItem",
  props: ['item'],
  data(){
    return {

    }
  },
  computed: {
    ...mapGetters('woPreset', ["formsNames"])
  },
  methods: {
    deleteItem(){
      console.log(`deleting manual marker:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteManualMarker", this.item)
    }
  }
}
</script>

<style scoped>
.box{
  float: right;
    width: 20px;
  height: 20px;
  border: 1px solid rgba(0, 0, 0, .2);
  display: inline-block;
  /*width: 10px;*/
  /*height: 10px;*/
}

.vc-color-wrap.transparent {
  border-radius: 10px !important;
}
.current-color{
  border-radius: 10px !important;
}
</style>