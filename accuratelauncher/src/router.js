import {createRouter, createWebHistory} from "vue-router";
import DpdBuilderPage from "@/components/DpdBuilderPage";
import PresetBuilderPage from "@/components/PresetBuilderPage";
import TheHome from "@/components/TheHome";
import LauncherPreset from "@/components/LauncherPreset";
import PrerequisitesPage from "@/components/PrerequisitesPage";

export const routes = [
  {
    path: '/',
    component: TheHome,
  },
  {
    path: '/prerequisites',
    component: PrerequisitesPage,
  },
  {
    path: '/dpd',
    component: DpdBuilderPage,
  },
  {
    path: '/launcher',
    component: LauncherPreset,
  },
  {
    path: '/preset',
    component: PresetBuilderPage,
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(function(to, from, next){
  let possiblePaths = routes.map(obj => obj.path)
  // console.log(possiblePaths)

  if (possiblePaths.includes(to.path)){
      next()
    }
    else {
      next('/')
    }

  }
);

