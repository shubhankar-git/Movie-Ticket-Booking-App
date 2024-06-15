import { createRouter, createWebHistory } from "vue-router";
import index from "./components/index";
import login from "./components/login";
import register from "./components/register";
import PromoteToAdmin from "./components/PromoteToAdmin.vue";
import AdminPage from "./components/AdminPage.vue";
import TheatreList from "./components/TheatreList.vue";
import showpage from "./components/showpage.vue";
import UserDashboard from "./components/UserDashboard.vue";
import booking from "./components/booking.vue";
import booked from "./components/booked.vue";
import ExportCSV from "./components/ExportCSV.vue";
import showManagement from "./components/showManagement.vue";
const routes = [
  {
    path: "/",
    name: "index",
    component: index,
  },
  {
    path: "/login",
    name: "login",
    component: login,
  },
  {
    path: "/register",
    name: "register",
    component: register,
  },

  {
    path: "/PromoteToAdmin",
    name: "PromoteToAdmin",
    component: PromoteToAdmin,
  },
  {
    path: "/AdminPage",
    name: "AdminPage",
    component: AdminPage,
  },
  {
    path: "/theatres",
    name: "TheatreList",
    component: TheatreList,
  },
  {
    path: "/showpage/:theatreid",
    name: "showpage",
    component: showpage,
    props: true,
  },
  {
    path: "/UserDashboard",
    name: "UserDashboard",
    component: UserDashboard,
  },
  {
    path: "/booking/:showId",
    name: "booking",
    component: booking,
    props: true
  },
  {
    path: "/booked",
    name: "booked",
    component: booked,
  },
  {
    path: "/ExportCSV",
    name: "ExportCSV",
    component: ExportCSV,
  },
  {
    path: "/showManagement",
    name: "showManagement",
    component:showManagement,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
