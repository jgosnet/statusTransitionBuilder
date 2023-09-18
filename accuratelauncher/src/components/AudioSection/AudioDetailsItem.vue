<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2 Audio1-8
  div()
    v-row
      v-col(cols="12")
        | {{ audioItem }}
      v-text-field(label="name" v-model="audioItem.name" )
</template>

<script>
export default {
  name: "AudioDetailsItem",
  props:["audioItem"],
  data: function (){
    return {
    }
  }
}
</script>

<style scoped>
.dashed-border{
 border-style: dashed;
  background-color: whitesmoke;
}
</style>