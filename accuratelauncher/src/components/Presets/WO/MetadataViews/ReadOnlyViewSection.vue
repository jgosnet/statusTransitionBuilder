<template lang="pug">
div().mb-3
  v-row.px-3.py-3
    v-col(cols="8").py-1.mt-2.right-separator
      //h3(v-if="this.item.readOnlyFields.length == 0" ) drag and drop here
      h3() Read-only fields
      | drag and drop here
      draggable(v-model="item.readOnlyFields"
          :group="item.name"
          @start="drag=true"
          @end="drag=false"
          item-key="id")

        template(#item="{element}")
          v-card(elevation="2" density="compact" variant="outlined" ).my-1.py-0
            v-card-text.ma-0.pa-1
              | {{element.key}}
              v-icon(@click="removeItem(element)") fa-solid fa-xmark
            //v-card-text
            //  | {{element}}

    v-col(cols="4").py-1.mt-2.left-separator
      h3 Available fields
      draggable(v-model="availableMetadataFields"
          :group="item.name"
          @start="drag=true"
          @end="drag=false"
          item-key="id")
        template(#item="{element}")
          v-card(elevation="2" density="compact" variant="outlined" ).my-1.py-0
            v-card-text.ma-0.pa-1
              v-tooltip(:text='element.source + ": " + element.key + " [" + element.label + "]"' location="top")
                template(v-slot:activator="{ props }")
                  span(v-bind="props") {{element.key}}



</template>

<script>
import draggable from 'vuedraggable';

export default {
  name: "ReadOnlyViewSection",
  components: {draggable},
  props: ["item"],
  data(){
    return {
      tab: "",
    }
  },
  methods: {
    removeItem(mdItem){
      console.log(mdItem)
      // eslint-disable-next-line vue/no-mutating-props
      this.item.readOnlyFields = this.item.readOnlyFields.filter(el => el.index != mdItem.index);
    },
  },
  computed: {
    availableMetadataFields: {
      get() {
        let mdList = []
        const formattedMd = this.$store.getters['woPreset/metadataFields']
        for (const itemIndex in formattedMd){
          const mdItem = formattedMd[itemIndex];
          if(this.item.readOnlyFields.some(fieldItem => fieldItem.index === mdItem.index)){
            console.log("do nothing")
          } else{
            mdList.push(mdItem)
          }
        }
        return mdList
      },
      set(value) {
        this.$store.commit('updateList', value)
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

.small-font{
  font-size: small;
  font-weight: bold;
}

.left-separator{
  border-left: solid;
    border-width: 1px;
}

.right-separator{
  border-right: solid;
  border-width: 1px;
}
</style>