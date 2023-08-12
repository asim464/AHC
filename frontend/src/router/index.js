import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/auth/Login.vue"),
      meta: {
        layout: "full",
      },
    },
    {
      path: "/user",
      name: "User",
      component: () => import("@/views/user/User.vue"),
      meta: {
        pageTitle: "User",
        breadcrumb: [
          {
            text: "User",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "show_user",
      },
    },
    {
      path: "/addcomplaints",
      name: "addcomplaints",
      component: () => import("@/views/petition/Petition.vue"),
      meta: {
        pageTitle: "Complaint Management ",
        breadcrumb: [
          {
            text: "Complaint",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/complaints",
      name: "complaints",
      component: () => import("@/views/complainantType/ComplaintType.vue"),
      meta: {
        pageTitle: "Complainant Type",
        breadcrumb: [
          {
            text: "Complainant Type",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "complaint_type_show",
      },
    },
    {
      path: "/role",
      name: "Role",
      component: () => import("@/views/role/Role.vue"),
      meta: {
        pageTitle: "Role",
        breadcrumb: [
          {
            text: "Role",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "show_role",
      },
    },
    {
      path: "/organization",
      name: "Organization",
      component: () => import("@/views/organization/Organization.vue"),
      meta: {
        pageTitle: "Organization",
        breadcrumb: [
          {
            text: "Organization",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "show_organization",
      },
    },
    {
      path: "/CallerType",
      name: "CallerType",
      component: () => import("@/views/callerType/CallerType.vue"),
      meta: {
        pageTitle: "Caller Type",
        breadcrumb: [
          {
            text: "Caller Type",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/Category",
      name: "Category",
      component: () => import("@/views/category/Category.vue"),
      meta: {
        pageTitle: "Category",
        breadcrumb: [
          {
            text: "Category",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "category_show",
      },
    },
    {
      path: "/SubCategory",
      name: "SubCategory",
      component: () => import("@/views/subcategory/SubCategory.vue"),
      meta: {
        pageTitle: "Sub Category",
        breadcrumb: [
          {
            text: "Sub Category",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/City",
      name: "City",
      component: () => import("@/views/city/City.vue"),
      meta: {
        pageTitle: "City",
        breadcrumb: [
          {
            text: "City",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "city_show",
      },
    },
    {
      path: "/Corps",
      name: "Corps",
      component: () => import("@/views/corps/Corps.vue"),
      meta: {
        pageTitle: "Corps",
        breadcrumb: [
          {
            text: "Corps",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "corps_show",
      },
    },
    {
      path: "/Ranks",
      name: "Ranks",
      component: () => import("@/views/ranks/Ranks.vue"),
      meta: {
        pageTitle: "Ranks",
        breadcrumb: [
          {
            text: "Ranks",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/MartialStatus",
      name: "MartialStatus",
      component: () => import("@/views/martialStatus/MartialStatus.vue"),
      meta: {
        pageTitle: "Martial Status",
        breadcrumb: [
          {
            text: "Martial Status",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "martial_status_show",
      },
    },
    {
      path: "/RelationType",
      name: "RelationType",
      component: () => import("@/views/relationType/RelationType.vue"),
      meta: {
        pageTitle: "Relation Type",
        breadcrumb: [
          {
            text: "Relation Type",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/RequestSource",
      name: "RequestSource",
      component: () => import("@/views/requestSource/RequestSource.vue"),
      meta: {
        pageTitle: "Request Source",
        breadcrumb: [
          {
            text: "Request Source",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "/ServingStatus",
      name: "ServingStatus",
      component: () => import("@/views/servingStatus/ServingStatus.vue"),
      meta: {
        pageTitle: "Serving Status",
        breadcrumb: [
          {
            text: "Serving Status",
            active: true,
          },
        ],
        requiresAuth: true,
        permission: "serving_status_show",
      },
    },
    {
      path: "/Type",
      name: "Type",
      component: () => import("@/views/Type/Type.vue"),
      meta: {
        pageTitle: "Type",
        breadcrumb: [
          {
            text: "Type",
            active: true,
          },
        ],
        requiresAuth: true,
        // permission: "complaint_type_show",
      },
    },
    {
      path: "*",
      redirect: "/login",
    },
  ],
});

// ? For splash screen
// Remove afterEach hook if you are not using splash screen
router.afterEach(() => {
  // Remove initial loading
  const appLoading = document.getElementById("loading-bg");
  if (appLoading) {
    appLoading.style.display = "none";
  }
});

export default router;
