<template lang="pug">
v-card(color="transparent" elevation="0" ).h-100
  SnackBarPopup
  v-layout
    v-app-bar(color="surface-variant" prominent density="compact" )
      v-menu(transition="slide-y-transition")
        template(v-slot:activator="{ props }")
          v-btn(v-bind="props" icon="fas fa-bars")
        v-list(density="compact" nav)
          v-list-item(v-for='item in menuItems'
            :key='item.title'
            :to='item.path'
            :prepend-icon="item.icon"
            exact-active-class='grey' large)
            v-list-item-title.item-title {{item.title}}

      v-toolbar-title
        v-icon fa-brands fa-youtube
        span.pl-3 Accurate launcher
        //v-spacer
      i.pr-4 updated on: 9/29/2023
    //v-navigation-drawer(permanent :width="190")
    //  v-list(density="compact" nav)
    //      v-list-item(v-for='item in menuItems'
    //        :key='item.title'
    //        :to='item.path'
    //        :prepend-icon="item.icon"
    //        exact-active-class='grey' large)
    //        v-list-item-title.item-title {{item.title}}
  router-view(v-slot="{ Component }")
    transition(name="fade" mode="out-in" )
      keep-alive
        Component(:is="Component")


</template>

<script>
/* eslint-disable */
import './assets/main.css'
import SnackBarPopup from "@/components/utils/SnackBarPopup";
import {mapGetters} from "vuex";
import DpdBuilderPage from "@/components/DpdBuilderPage"

export default {
  name: 'App',
  components: {
    SnackBarPopup,
    DpdBuilderPage
  },
  data() {
    return {
      menuItems: [
        {title: 'Home', path: '/', icon: 'fa-solid fa-house'},
        {title: 'Prerequisites', path: '/prerequisites', icon: 'fa-solid fa-list-check'},
        {title: 'Dynamic Preset Data', path: '/dpd', icon: 'fa-solid fa-indent'},
        {title: 'Accurate launcher', path: '/launcher', icon: 'fa-solid fa-bolt'},
        {title: 'Accurate WO', path: '/preset', icon: 'fa-solid fa-user-check'},
        {title: 'Check Results', path: '/results', icon: 'fa-solid fa-clipboard-check'},
      ]
    }
  },
    computed: {
    },
  methods: {
    openSnackbar(){
      this.snackbar = true
    },

  },
  mounted() {
    console.log('loading!')
    // this.$store.dispatch('configuration/loadConfiguration');
  }
}
</script>

<style>
html, body{
  height: 100%;
}
/*.vue-codemirror{*/
/*   background-color: white !important;*/
/*  padding-top: 0px !important;*/
/*  }*/

.cm-editor{
  min-height: 300px !important;
  max-height: 720px !important;
}

.left-align{
  text-align: left;
}

.right-align{
  text-align: right;
}

.no-border{
  border-style: none;
}

body{
/*background: rgb(221,221,235);*/
/*background: linear-gradient(90deg, rgba(221,221,235,1) 0%, rgba(138,138,182,1)  100%);*/
    width: 100%;
    height:100%;
}


body{
        /*background-image: url('/src/assets/background-2462431_1920.jpg') !important;*/
  /*background-repeat: no-repeat;*/
  /*background-attachment: fixed;*/
  /*background-size: 100% 100%;*/
}
#app {
  font-family: Roboto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 45px;
  border-style: none;

}

.default_height {
  padding-top: 0px;
  min-height: 300px;
}

.fade-enter-active {
  transition: all 0.2s ease-out;
}

.fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.fade-enter-from,
.fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

input[type=checkbox]{
     margin: 4px 0 0;
    line-height: normal;
    width: 20px;
    height: 20px;
}

fieldset{
min-height: 20px;
  border-radius: 10px;
}

legend{
  font-size: large;
}

#expand{
  position: absolute;
  float:right;
  right: 20px;
  background-color: white;
  margin-top:-25px;
  margin-right:5px;
}



</style>
