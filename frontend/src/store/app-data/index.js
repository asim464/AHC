import axiosIns from "@/libs/axios";

export default {
  namespaced: true,
  state: {
    isLoggedIn: false,
    user: null,
    navMenuItems: [],
  },
  getters: {
    getLoggedInUser: (state) => {
      return state.user;
    },
    hasPermission: (state) => (name) => {
      if (state.user) {
        return state.user.permissions.hasOwnProperty(name);
      }
      return false;
    },
    hasRole: (state) => (name) => {
      if (state.user.role_data.code_name === name) {
        return true;
      }
      return false;
    },
    isLoggedIn: (state) => state.isLoggedIn,
    getNavMenuItems: (state) => state.navMenuItems,
  },
  mutations: {
    login(state, data) {
      state.isLoggedIn = true;
      state.user = data.user;
    },
    logout(state) {
      state.isLoggedIn = false;
      state.user = null;
    },
    setNavMenuItems(state) {
      state.navMenuItems = [];

      if (state.user.permissions.hasOwnProperty("dashboard_show")) {
        state.navMenuItems.push({
          title: "Dashboard",
          route: "Dashboard",
          icon: "HomeIcon",
        });
      }

      if (state.user.permissions.hasOwnProperty("show_user")) {
        state.navMenuItems.push({
          title: "User",
          icon: "UserIcon",
          route: "User",
        });
      }

      if (state.user.permissions.hasOwnProperty("show_role")) {
        state.navMenuItems.push({
          title: "Role",
          icon: "UsersIcon",
          route: "Role",
        });
      }

      if (state.user.permissions.hasOwnProperty("show_organization")) {
        state.navMenuItems.push({
          title: "Organization",
          icon: "BoxIcon",
          route: "Organization",
        });
      }

      // if (state.user.permissions.hasOwnProperty("petition_show")) {
        state.navMenuItems.push({
          title: "Manage Complaints",
          icon: "FileIcon",
          route: "addcomplaints",
        });
      // }

      if (state.user.permissions.hasOwnProperty("marked_petition_show")) {
        state.navMenuItems.push({
          title: "Marked RFA",
          icon: "FileIcon",
          route: "MarkedPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("all_petition_show")) {
        state.navMenuItems.push({
          title: "All RFA",
          icon: "FileIcon",
          route: "AllPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("approve_can")) {
        state.navMenuItems.push({
          title: "Outstanding RFA",
          icon: "FileIcon",
          route: "ApprovePetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("approve_can")) {
        state.navMenuItems.push({
          title: "Approved RFA",
          icon: "FileIcon",
          route: "ApprovedPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("petition_link_show")) {
        state.navMenuItems.push({
          title: "Link RFA",
          icon: "FileIcon",
          route: "LinkPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("approve_link_can")) {
        state.navMenuItems.push({
          title: "Approve Link RFA",
          icon: "FileIcon",
          route: "ApproveLinkPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("approve_link_can")) {
        state.navMenuItems.push({
          title: "Approved Link RFA",
          icon: "FileIcon",
          route: "ApprovedLinkPetition",
        });
      }

      if (state.user.permissions.hasOwnProperty("suggestion_show")) {
        state.navMenuItems.push({
          title: "Suggestion",
          icon: "FileIcon",
          route: "Suggestion",
        });
      }

      if (state.user.permissions.hasOwnProperty("document_show")) {
        state.navMenuItems.push({
          title: "Document",
          icon: "FileIcon",
          route: "Document",
        });
      }

      if (state.user.permissions.hasOwnProperty("petition_can_search")) {
        state.navMenuItems.push({
          title: "RFA Search",
          icon: "FileIcon",
          route: "SearchPetition",
        });
      }

      const reportsMenuItem = {
        title: "Reports",
        icon: "ToolIcon",
        children: [],
      };

      if (
        state.user.permissions.hasOwnProperty("daily_report_show") ||
        state.user.permissions.hasOwnProperty("overall_report_show")
      ) {
        state.navMenuItems.push(reportsMenuItem);
      }

      if (state.user.permissions.hasOwnProperty("daily_report_show")) {
        reportsMenuItem.children.push({
          title: "Daily",
          route: "Daily",
        });
      }
      if (state.user.permissions.hasOwnProperty("overall_report_show")) {
        reportsMenuItem.children.push({
          title: "Overall",
          route: "Overall",
        });
      }

      const lookUpMenuItem = {
        title: "Lookup Tables",
        icon: "ToolIcon",
        children: [],
      };

      // if (
      //   state.user.permissions.hasOwnProperty("complaint_type_show") ||
      //   state.user.permissions.hasOwnProperty("rank_type_show") ||
      //   state.user.permissions.hasOwnProperty("prefix_show") ||
      //   state.user.permissions.hasOwnProperty("priority_show") ||
      //   state.user.permissions.hasOwnProperty("category_show") ||
      //   state.user.permissions.hasOwnProperty("petition_detail_type_show")
      // )
       {
        state.navMenuItems.push(lookUpMenuItem);
      }

      if (state.user.permissions.hasOwnProperty("complaint_type_show")) {
        lookUpMenuItem.children.push({
          title: "Complainant Type",
          route: "complaints",
        });
      }
      // if (state.user.permissions.hasOwnProperty("petition_detail_type_show")) {
        lookUpMenuItem.children.push({
          title: "Caller Type",
          route: "CallerType",
        });
      // }
      // if (state.user.permissions.hasOwnProperty("category_show")) {
        lookUpMenuItem.children.push({
          title: "Type",
          route: "Type",
        });
      // }
      // if (state.user.permissions.hasOwnProperty("rank_type_show")) {
        lookUpMenuItem.children.push({
          title: "Ranks",
          route: "Ranks",
        });
      // }
      if (state.user.permissions.hasOwnProperty("corps_show")) {
        lookUpMenuItem.children.push({
          title: "Corps",
          route: "Corps",
        });
      }
      if (state.user.permissions.hasOwnProperty("city_show")) {
        lookUpMenuItem.children.push({
          title: "City",
          route: "City",
        });
      }
      if (state.user.permissions.hasOwnProperty("martial_status_show")) {
        lookUpMenuItem.children.push({
          title: "Martial Status",
          route: "MartialStatus",
        });
      }

      if (state.user.permissions.hasOwnProperty("category_show")) {
        lookUpMenuItem.children.push({
          title: "Category",
          route: "Category",
        });
      }
      // if (state.user.permissions.hasOwnProperty("category_show")) {
        lookUpMenuItem.children.push({
          title: "Sub Category",
          route: "SubCategory",
        });
      // }
      // if (state.user.permissions.hasOwnProperty("category_show")) {
        lookUpMenuItem.children.push({
          title: "Request Source",
          route: "RequestSource",
        });
      // }
      // if (state.user.permissions.hasOwnProperty("category_show")) {
        lookUpMenuItem.children.push({
          title: "Relation Type",
          route: "RelationType",
        });
      // }
      if (state.user.permissions.hasOwnProperty("serving_status_show")) {
        lookUpMenuItem.children.push({
          title: "Serving Status",
          route: "ServingStatus",
        });
      }

    },
  },
  actions: {
    async login({ commit }, payload) {
      const res = await axiosIns.post("login", payload);
      if (res.status === 200) {
        commit("login", res.data);
        commit("setNavMenuItems");
      }
      return res;
    },
    async logout({ commit }) {
      const res = await axiosIns.post("logout");
      if (res.status === 204) {
        commit("logout");
      }
      return res;
    },
    async getCurrentUser({ commit }) {
      const res = await axiosIns.get("current");
      if (res.status === 200) {
        commit("login", res.data);
        commit("setNavMenuItems");
      }
    },
    async getLoggedInUser({ commit }) {
      const res = await axiosIns.get("logged-in-user");
      return res;
    },
    async getRoles({ commit }, { pageNumber, name }) {
      let url = `roles/?page=${pageNumber}`;
      if (name) {
        url += `&name=${name}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getRole({ commit }, { pk }) {
      const res = await axiosIns.get(`roles/${pk}/`);
      return res;
    },
    async createRole({ commit }, payload) {
      const res = await axiosIns.post("roles/", payload);
      return res;
    },
    async updateRole({ commit }, { payload, pk }) {
      const res = await axiosIns.put(`roles/${pk}/`, payload);
      return res;
    },
    async deleteRole({ commit }, { pk }) {
      const res = await axiosIns.delete(`roles/${pk}/`);
      return res;
    },
    async getPermissions({ commit }) {
      const res = await axiosIns.get("permissions");
      return res;
    },
    async getUser({ commit }, { pk }) {
      const res = await axiosIns.get(`account/users/${pk}/`);
      return res;
    },
    async getUsers({ commit }, { pageNumber, name, username, organization }) {
      let url = `account/users/?page=${pageNumber}`;
      if (name) {
        url += `&name=${name}`;
      }
      if (username) {
        url += `&username=${username}`;
      }
      if (organization) {
        url += `&organization=${organization}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getUsersUnPaginated({ commit }, { organization }) {
      let url = `account/users-unpaginated/`;
      if (organization) {
        url += `?organization=${organization}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async createUser({ commit }, payload) {
      const res = await axiosIns.post("users-create-update", payload);
      return res;
    },
    async getOrganization({ commit }, { pk }) {
      const res = await axiosIns.get(`account/organizations/${pk}/`);
      return res;
    },
    async getOrganizations({ commit }, { pageNumber, name, parent }) {
      let url = `account/organizations/?page=${pageNumber}`;
      if (name) {
        url += `&name=${name}`;
      }
      if (parent) {
        url += `&parent=${parent}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    /*
    async getPetitions(
      { commit },
      {
        pageNumber,
        created_by,
        currently_marked,
        organization,
        army_prefix,
        army_no,
        cnic,
        status,
        not_status,
        created_at,
        exceed_by_10_days,
        detail_type,
        rank_type,
        is_serving,
        category,
        exceed_by_24_hrs,
        delayed_by_24_hrs,
        approved_by,
        created_by_organization,
        case_no,
        title,
        mobile_number,
        draft,
        pend_marked,
        is_delete,
        from_date,
        to_date,
        final_approval,
        after_approval_24_hrs,
        not_final_approval,
        marked_by_organization,
        not_organization,
        last_30_days,
        my_organization,
      }
    ) {
      let url = `petitions/?page=${pageNumber}`;
      if (created_by) {
        url += `&created_by=${created_by}`;
      }
      if (currently_marked) {
        url += `&currently_marked=${currently_marked}`;
      }
      if (organization) {
        url += `&organization=${organization}`;
      }
      if (army_prefix && army_no) {
        url += `&army_prefix=${army_prefix}&army_no=${army_no}`;
      }
      if (cnic) {
        url += `&cnic=${cnic}`;
      }
      if (case_no) {
        url += `&case_no=${case_no}`;
      }
      if (title) {
        url += `&title=${title}`;
      }
      if (mobile_number) {
        url += `&mobile_number=${mobile_number}`;
      }
      if (status) {
        url += `&status=${status}`;
      }
      if (not_status) {
        url += `&not_status=${not_status}`;
      }
      if (created_at) {
        url += `&created_at=${created_at}`;
      }
      if (exceed_by_10_days) {
        url += `&exceed_by_10_days=${exceed_by_10_days}`;
      }
      if (exceed_by_24_hrs) {
        url += `&exceed_by_24_hrs=${exceed_by_24_hrs}`;
      }
      if (delayed_by_24_hrs) {
        url += `&delayed_by_24_hrs=${delayed_by_24_hrs}`;
      }
      if (detail_type) {
        url += `&detail_type=${detail_type}`;
      }
      if (rank_type) {
        url += `&rank_type=${rank_type}`;
      }
      if (is_serving !== undefined) {
        url += `&is_serving=${is_serving}`;
      }
      if (category) {
        url += `&category=${category}`;
      }
      if (approved_by) {
        url += `&approved_by=${approved_by}`;
      }
      if (created_by_organization) {
        url += `&created_by_organization=${created_by_organization}`;
      }
      if (draft !== null && draft !== undefined) {
        url += `&draft=${draft}`;
      }
      if (pend_marked) {
        url += `&pend_marked=${pend_marked}`;
      }
      if (is_delete !== null && is_delete !== undefined) {
        url += `&is_delete=${is_delete}`;
      }
      if (from_date) {
        url += `&from_date=${from_date}`;
      }
      if (to_date) {
        url += `&to_date=${to_date}`;
      }
      if (final_approval) {
        url += `&final_approval=${final_approval}`;
      }
      if (after_approval_24_hrs) {
        url += `&after_approval_24_hrs=${after_approval_24_hrs}`;
      }
      if (not_final_approval !== null && not_final_approval !== undefined) {
        url += `&not_final_approval=${not_final_approval}`;
      }
      if (marked_by_organization) {
        url += `&marked_by_organization=${marked_by_organization}`;
      }
      if (not_organization) {
        url += `&not_organization=${not_organization}`;
      }
      if (last_30_days) {
        url += `&last_30_days=${last_30_days}`;
      }
      if (my_organization) {
        url += `&my_organization=${my_organization}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async createPetition({ commit }, payload) {
      const res = await axiosIns.post("petitions/", payload);
      return res;
    },
    async getPetition({ commit }, { pk }) {
      const res = await axiosIns.get(`petitions/${pk}/`);
      return res;
    },
    async updatePetition({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`petitions/${pk}/`, payload);
      return res;
    },
    async deletePetition({ commit }, { pk }) {
      const res = await axiosIns.delete(`petitions/${pk}/`);
      return res;
    },
    async updatePetitionDetail({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`petition-detail/${pk}/`, payload);
      return res;
    },
    async approvePetition({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`petition-approves/${pk}/`, payload);
      return res;
    },
    async getDailyReport({ commit }, { date, organization }) {
      const res = await axiosIns.get(`daily-report`, {
        params: { date: date, organization: organization },
      });
      return res;
    },
    async getOverallReport({ commit }, { from_date, to_date, organization }) {
      const res = await axiosIns.get(`overall-report`, {
        params: {
          from_date: from_date,
          to_date: to_date,
          organization: organization,
        },
      });
      return res;
    },
    async getPerformanceData({ commit }) {
      const res = await axiosIns.get(`performance-data`);
      return res;
    },
    async getStatisticsData({ commit }) {
      const res = await axiosIns.get(`statistics-data`);
      return res;
    },
    async getUserData({ commit }) {
      const res = await axiosIns.get(`user-data`);
      return res;
    },
    async getNoOfRFAPlot({ commit }, { start_date, end_date }) {
      const res = await axiosIns.get(`no-of-rfa-plot`, {
        params: { start_date: start_date, end_date: end_date },
      });
      return res;
    },
    async getDirRFAByDtePlot({ commit }, { date }) {
      const res = await axiosIns.get(`dir-rfa-by-dte-plot`, {
        params: { date: date },
      });
      return res;
    },
    async getOverallRFACatPlot({ commit }) {
      const res = await axiosIns.get(`overall-rfa-by-cat-plot`);
      return res;
    },
    async getOverallRFACatStatusPlot({ commit }) {
      const res = await axiosIns.get(`overall-rfa-by-cat-status-plot`);
      return res;
    },
    async getOverallRFATypeStatusPlot({ commit }) {
      const res = await axiosIns.get(`overall-rfa-by-type-status-plot`);
      return res;
    },
    async getRFACatPlot({ commit }, { isToday }) {
      const res = await axiosIns.get(`rfa-by-cat`, {
        params: { isToday: isToday },
      });
      return res;
    },
    async getRFATypePlot({ commit }, { isToday }) {
      const res = await axiosIns.get(`rfa-by-type`, {
        params: { isToday: isToday },
      });
      return res;
    },
    async createSuggestion({ commit }, payload) {
      const res = await axiosIns.post("suggestions/", payload);
      return res;
    },
    async getSuggestions({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`suggestions/?page=${pageNumber}`);
      return res;
    },
    async deleteSuggestion({ commit }, { pk }) {
      const res = await axiosIns.delete(`suggestions/${pk}/`);
      return res;
    },
    async updateSuggestion({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`suggestions/${pk}/`, payload);
      return res;
    },
    */
    async createComplaintType({ commit }, payload) {
      const res = await axiosIns.post("complainant-types/", payload);
      return res;
    },
    async getComplaintTypes({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`complainant-types/?page=${pageNumber}`);
      return res;
    },
    async getComplaintType({ commit }, { pk }) {
      const res = await axiosIns.get(`complainant-types/${pk}/`);
      return res;
    },
    async deleteComplaintType({ commit }, { pk }) {
      const res = await axiosIns.delete(`complainant-types/${pk}/`); 
      return res;
    },
    async updateComplaintType({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`complainant-types/${pk}/`, payload);
      return res;
    },
    async createMartialStatus({ commit }, payload) {
      const res = await axiosIns.post("martial-statuses/", payload);
      return res;
    },
    async getMartialStatuses({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`martial-statuses/?page=${pageNumber}`);
      return res;
    },
    async getMartialStatus({ commit }, { pk }) {
      const res = await axiosIns.get(`martial-statuses/${pk}/`);
      return res;
    },
    async deleteMartialStatus({ commit }, { pk }) {
      const res = await axiosIns.delete(`martial-statuses/${pk}/`);
      return res;
    },
    async updateMartialStatus({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`martial-statuses/${pk}/`, payload);
      return res;
    },
    async createCorps({ commit }, payload) {
      const res = await axiosIns.post("corps/", payload);
      return res;
    },
    async getCorps({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`corps/?page=${pageNumber}`);
      return res;
    },
    async getCorp({ commit }, { pk }) {
      const res = await axiosIns.get(`corps/${pk}/`);
      return res;
    },
    async deleteCorps({ commit }, { pk }) {
      const res = await axiosIns.delete(`corps/${pk}/`);
      return res;
    },
    async updateCorps({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`corps/${pk}/`, payload);
      return res;
    },
    async createServing({ commit }, payload) {
      const res = await axiosIns.post("serving-statuses/", payload);
      return res;
    },
    async getServings({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`serving-statuses/?page=${pageNumber}`);
      return res;
    },
    async getServing({ commit }, { pk }) {
      const res = await axiosIns.get(`serving-statuses/${pk}/`);
      return res;
    },
    async deleteServing({ commit }, { pk }) {
      const res = await axiosIns.delete(`serving-statuses/${pk}/`);
      return res;
    },
    async updateServing({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`serving-statuses/${pk}/`, payload);
      return res;
    },
    async createCity({ commit }, payload) {
      const res = await axiosIns.post("cities/", payload);
      return res;
    },
    async getCity({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`cities/?page=${pageNumber}`);
      return res;
    },
    async getCities({ commit }, { pk }) {
      const res = await axiosIns.get(`cities/${pk}/`);
      return res;
    },
    async deleteCity({ commit }, { pk }) {
      const res = await axiosIns.delete(`cities/${pk}/`);
      return res;
    },
    async updateCity({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`cities/${pk}/`, payload);
      return res;
    },
    async createCategory({ commit }, payload) {
      const res = await axiosIns.post("categories/", payload);
      return res;
    },
    async getCategory({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`categories/?page=${pageNumber}`);
      return res;
    },
    async getCategories({ commit }, { pk }) {
      const res = await axiosIns.get(`categories/${pk}/`);
      return res;
    },
    async deleteCategory({ commit }, { pk }) {
      const res = await axiosIns.delete(`categories/${pk}/`);
      return res;
    },
    async updateCategory({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`categories/${pk}/`, payload);
      return res;
    },
    /*
    async createPetitionDetailType({ commit }, payload) {
      const res = await axiosIns.post("petition-detail-types/", payload);
      return res;
    },
    async getPetitionDetailTypes({ commit }, { pageNumber }) {
      const res = await axiosIns.get(
        `petition-detail-types/?page=${pageNumber}`
      );
      return res;
    },
    async getPetitionDetailType({ commit }, { pk }) {
      const res = await axiosIns.get(`petition-detail-types/${pk}/`);
      return res;
    },
    async deletePetitionDetailType({ commit }, { pk }) {
      const res = await axiosIns.delete(`petition-detail-types/${pk}/`);
      return res;
    },
    async updatePetitionDetailType({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`petition-detail-types/${pk}/`, payload);
      return res;
    },
    async createPetitionDetailStatus({ commit }, payload) {
      const res = await axiosIns.post("petition-detail-statuses/", payload);
      return res;
    },
    async getPetitionDetailStatuses({ commit }, { pageNumber }) {
      const res = await axiosIns.get(
        `petition-detail-statuses/?page=${pageNumber}`
      );
      return res;
    },
    async getPetitionDetailStatus({ commit }, { pk }) {
      const res = await axiosIns.get(`petition-detail-statuses/${pk}/`);
      return res;
    },
    async deletePetitionDetailStatus({ commit }, { pk }) {
      const res = await axiosIns.delete(`petition-detail-statuses/${pk}/`);
      return res;
    },
    async updatePetitionDetailStatus({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(
        `petition-detail-statuses/${pk}/`,
        payload
      );
      return res;
    },
    async createRankType({ commit }, payload) {
      const res = await axiosIns.post("rank-types/", payload);
      return res;
    },
    async getRankTypes({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`rank-types/?page=${pageNumber}`);
      return res;
    },
    async getRankType({ commit }, { pk }) {
      const res = await axiosIns.get(`rank-types/${pk}/`);
      return res;
    },
    async deleteRankType({ commit }, { pk }) {
      const res = await axiosIns.delete(`rank-types/${pk}/`);
      return res;
    },
    async updateRankType({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`rank-types/${pk}/`, payload);
      return res;
    },
    async createPrefix({ commit }, payload) {
      const res = await axiosIns.post("prefixes/", payload);
      return res;
    },
    async getPrefixes({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`prefixes/?page=${pageNumber}`);
      return res;
    },
    async getPrefix({ commit }, { pk }) {
      const res = await axiosIns.get(`prefixes/${pk}/`);
      return res;
    },
    async deletePrefix({ commit }, { pk }) {
      const res = await axiosIns.delete(`prefixes/${pk}/`);
      return res;
    },
    async updatePrefix({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`prefixes/${pk}/`, payload);
      return res;
    },
    async createPriority({ commit }, payload) {
      const res = await axiosIns.post("priorities/", payload);
      return res;
    },
    async getPriorities({ commit }, { pageNumber }) {
      const res = await axiosIns.get(`priorities/?page=${pageNumber}`);
      return res;
    },
    async getPriority({ commit }, { pk }) {
      const res = await axiosIns.get(`priorities/${pk}/`);
      return res;
    },
    async deletePriority({ commit }, { pk }) {
      const res = await axiosIns.delete(`priorities/${pk}/`);
      return res;
    },
    async updatePriority({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`priorities/${pk}/`, payload);
      return res;
    },
    async createCategory({ commit }, payload) {
      const res = await axiosIns.post("categories/", payload);
      return res;
    },
    async getCategories({ commit }, { pageNumber, is_active }) {
      let url = `categories/?page=${pageNumber}`;
      if (is_active !== undefined && is_active !== null) {
        url += `&is_active=${is_active}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getCategory({ commit }, { pk }) {
      const res = await axiosIns.get(`categories/${pk}/`);
      return res;
    },
    async deleteCategory({ commit }, { pk }) {
      const res = await axiosIns.delete(`categories/${pk}/`);
      return res;
    },
    async updateCategory({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`categories/${pk}/`, payload);
      return res;
    },
    async createDocument({ commit }, payload) {
      const res = await axiosIns.post("upload-document", payload);
      return res;
    },
    async getDocuments({ commit }, { pageNumber, name, created_by }) {
      let url = `documents/?page=${pageNumber}`;
      if (name) {
        url += `&name=${name}`;
      }
      if (created_by) {
        url += `&created_by=${created_by}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async createPetitionLink({ commit }, payload) {
      const res = await axiosIns.post("petition-links/", payload);
      return res;
    },
    async getPetitionLinks(
      { commit },
      { pageNumber, created_by_organization, approved_by, created_by }
    ) {
      let url = `petition-links/?page=${pageNumber}`;
      if (created_by_organization) {
        url += `&created_by_organization=${created_by_organization}`;
      }
      if (approved_by) {
        url += `&approved_by=${approved_by}`;
      }
      if (created_by) {
        url += `&created_by=${created_by}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getPetitionLink({ commit }, { pk }) {
      const res = await axiosIns.get(`petition-links/${pk}/`);
      return res;
    },
    async deletePetitionLink({ commit }, { pk }) {
      const res = await axiosIns.delete(`petition-links/${pk}/`);
      return res;
    },
    async updatePetitionLink({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`petition-links/${pk}/`, payload);
      return res;
    },
    async approvePetitionLink({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(
        `petition-link-approves/${pk}/`,
        payload
      );
      return res;
    },
    async getOrganizationChildren(
      { commit },
      { pageNumber, parent_name, child_name, level, parent }
    ) {
      let url = `account/hierarchies/?page=${pageNumber}`;
      if (parent_name) {
        url += `&parent_name=${parent_name}`;
      }
      if (child_name) {
        url += `&child_name=${child_name}`;
      }
      if (level) {
        url += `&level=${level}`;
      }
      if (parent) {
        url += `&parent=${parent}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async updatePetitionFinalApproval({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(
        `petition-final-approval/${pk}/`,
        payload
      );
      return res;
    },*/

  },
};
