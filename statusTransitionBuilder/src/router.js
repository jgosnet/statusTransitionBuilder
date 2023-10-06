import {createRouter, createWebHistory} from "vue-router";
import MainPage from "@/components/MainPage";

export const routes = [
  {
    path: '/',
    component: MainPage,
  },
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

