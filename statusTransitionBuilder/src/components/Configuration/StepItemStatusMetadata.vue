<template lang="pug">
v-col(cols="1").py-1.my-0
  v-btn(size="small" @click="addMetadata()")
    v-icon fa-solid fa-plus
v-col(cols="11").py-1.my-0
  span(v-show="!item.includeMetadata.length" ) No Metadata.

  draggable(v-model="item.includeMetadata"
          handle=".handle1"
          :group="item.index"
          @start="drag=true"
          @end="drag=false"
          item-key="index").w-100

    template(#item="{element}")
      v-card.mb-2.py-0(elevation="6" )
        v-card-text.ma-0.pa-1
          v-row.px-3.pt-1
            v-col(cols="1")
              v-icon.handle1.float-left fa-solid fa-bars
            v-col(cols="4")
              v-text-field(v-model="element.name" hide-details
                            label="Name" density="compact" )
            v-col(cols="6")
              v-combobox(v-model="element.jmespath" hide-details
                            label="Jmespath (ex: `asset_details.content_type`)" density="compact" :items="possibleMetadataJmespath")
            v-col(cols="1")
              v-icon.handle.float-right(color="red" @click="deleteMetadata(element)" size="x-large" ) fa-solid fa-xmark

</template>

<script>
import draggable from "vuedraggable";
import {mapGetters} from "vuex";


export default {
  name: "StepItemStatusMetadata",
  components: {
    draggable
  },
  computed: {
    ...mapGetters('status', ['possibleMetadataJmespath']),
  },
  props: ['item'],
  methods: {
    addMetadata(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.includeMetadata.push({
        index: this.item.metadataIndex,
        name: '',
        jmespath: ''
      });
      // eslint-disable-next-line vue/no-mutating-props
      this.item.metadataIndex += 1;
    },
    deleteMetadata(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.includeMetadata = this.item.includeMetadata.filter(obj => obj.index !== element.index);
    }
  }
}
</script>

<style scoped>

</style>