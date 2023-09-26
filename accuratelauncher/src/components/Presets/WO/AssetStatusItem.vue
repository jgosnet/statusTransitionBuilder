<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ item.key }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="12").py-1
        v-text-field(v-model="item.key" hide-details
          label="Status Name" density="compact" )

    v-row.px-3.py-1.my-0
      v-col(cols="12").py-1.my-0
        v-select(v-model="item.color" hide-details
          :items="possibleStatusColors"
          label="Color"
          density="compact"
          :class="statusColor")

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "AssetStatusItem",
  props:["item"],
  methods: {
    deleteItem(){
      console.log(`deleting asset status item:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteOutputStatus", this.item)
    }
  },
  computed: {
    ...mapGetters('woPreset', ['possibleStatusColors']),
    statusColor(){
      console.log(this.item.color)
      // eslint-disable-next-line no-undef
      switch(this.item.color) {
        case "var(--AP-SUCCESS)":
          return "green"
        case "var(--AP-ERROR)":
          return "red"
        case "var(--AP-FOREGROUND-2)":
          return "blue"
      }
      return ""
    },
  }
}
</script>

<style scoped>
.red{
  background-color: indianred;
}

.green{
  background-color: lightgreen;
}

.blue{
  background-color: lightskyblue;
}
</style>