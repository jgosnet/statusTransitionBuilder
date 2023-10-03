<template lang="pug">
v-container(fluid)

  v-row
    v-col(cols="12").py-0.pl-0


  v-row
    v-col(cols="8").py-0.pl-0
      v-card.w-100
        v-card-text
          v-tabs(v-model="selectedTab" selected-class="selected-tab").my-0.py-0
            v-tab(value="__pl_accurate") __pl_accurate
            v-tab(value="__pl_files" ) __pl_files
            v-tab(value="__pl_technical" ) __pl_technical
            v-tab(value="__pl_logging" ) __pl_logging

          v-window.left-align(v-model="selectedTab")
            PLCode(item="__pl_accurate")
            PLCode(item="__pl_files")
            PLCode(item="__pl_logging")
            PLCode(item="__pl_technical")

    v-col(cols="4").py-0.pl-0
      v-card.float-right
        v-card-text(style="text-align:left")
          span The following files need to be imported in rally as presets with the following filename import
          v-img.mt-5.float-right(:src="filenameImage" max-width="500px" )
</template>

<script>
import PLCode from "@/components/Prerequisites/PLCode";

export default {
  name: "PrerequisitesPage",
  components: {PLCode},
  data(){
    return {
      selectedTab: '__pl_',
      filenameImage: require('@/assets/images/preset_filename.png'),
    }
  },
  computed:{
  }
}
</script>

<style scoped>

</style>