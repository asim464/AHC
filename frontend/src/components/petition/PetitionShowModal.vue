<template>
  <div>
    <b-modal
      id="petition-show-modal"
      title="RFA show Modal"
      centered
      hide-footer
      size="lg"
      :no-close-on-esc="true"
      :no-close-on-backdrop="true"
    >
      <template #modal-title> <h2 class="m-0">RFA</h2> </template>
      <b-table
        responsive="sm"
        :fields="fields"
        :items="petitions"
        details-td-class="m-0 p-0"
        small
        v-if="hasPermission('petition_read')"
        :per-page="0"
        :tbody-tr-class="rowClass"
        class="modal-size"
      >
        <template #cell(draft)="row">
          {{ row.item.draft ? "Yes" : "No" }}
        </template>
        <template #cell(created_by_data)="row">
          {{
            row.item.created_by_data ? row.item.created_by_data.username : ""
          }}
        </template>
        <template #cell(updated_by_data)="row">
          {{
            row.item.updated_by_data ? row.item.updated_by_data.username : ""
          }}
        </template>
        <template #cell(manage)="row">
          <b-button
            variant="success"
            pill
            size="sm"
            @click="detailPetition(row.item)"
            v-if="hasPermission('petition_read') && !row.item.draft"
          >
            Detail
          </b-button>
        </template>
      </b-table>
      <b-pagination
        size="md"
        :total-rows="totalItems"
        v-model="currentPage"
        :per-page="perPage"
      ></b-pagination>
    </b-modal>
    <petition-detail-modal
      :petition="petition"
      @modalClosed="onModalClosed"
      :key="`detail-${petitionDetailModalCount}`"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import PetitionDetailModal from "@/components/petition/PetitionDetailModal.vue";
import util from "@/util.js";

export default {
  mixins: [util],
  props: {
    filter: Object,
  },
  components: {
    PetitionDetailModal,
  },
  data() {
    return {
      fields: [
        { key: "title", label: "Title" },
        { key: "subject", label: "Subject" },
        { key: "draft", label: "Draft" },
        { key: "created_at", label: "Created At" },
        { key: "created_by_data", label: "Created By" },
        { key: "updated_at", label: "Updated At" },
        { key: "updated_by_data", label: "Updated By" },
        { key: "manage", label: "Manage" },
      ],
      currentPage: 1,
      perPage: 0,
      totalItems: 0,
      petitions: [],
      petition: null,
      petitionDetailModalCount: 0,
    };
  },
  async mounted() {
    await this.fetchPaginatedData();
  },
  methods: {
    ...mapActions({
      getPetitions: "appData/getPetitions",
    }),
    async fetchPaginatedData() {
      try {
        const res = await this.getPetitions({
          pageNumber: this.currentPage,
          organization: this.getLoggedInUser.organization,
          ...this.filter,
        });
        this.petitions = res.data.results;
        this.totalItems = res.data.count;
        this.perPage = res.data.per_page;
      } catch (error) {
        this.displayError(error);
      }
    },
    detailPetition(petition) {
      this.petition = petition;
      this.petitionDetailModalCount += 1;
      this.$nextTick(() => {
        this.$bvModal.show("petition-detail-modal");
      });
    },
    async onModalClosed() {
      await this.fetchPaginatedData();
    },
  },
  computed: {
    ...mapGetters({
      hasPermission: "appData/hasPermission",
      getLoggedInUser: "appData/getLoggedInUser",
    }),
  },
  watch: {
    currentPage: async function (val) {
      await this.fetchPaginatedData();
    },
  },
};
</script>

<style>
.modal-size {
  height: 65vh;
}
</style>
