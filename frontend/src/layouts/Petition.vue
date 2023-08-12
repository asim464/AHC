<template>
  <div>
    <div class="text-right mb-1">
      <b-button
        variant="primary"
        pill
        @click="createPetition"
        v-if="hasPermission('petition_create')"
      >
        <feather-icon icon="PlusIcon" class="mr-50" />
        <span class="align-middle">Create</span>
      </b-button>
    </div>
    <b-card>
      <b-row class="mb-1" align-v="center">
        <b-col md="5">
          <b-row no-gutters>
            <b-col cols="3">
              <VueSelectPaginated
                name="Prefix"
                label="name"
                :prevSelected="prefix"
                :getListMethod="getPrefixes"
                @setMethod="(value) => (prefix = value)"
              />
            </b-col>
            <b-col cols="9">
              <b-form-group label="Army No" label-for="armyNo">
                <b-input-group>
                  <template #prepend> </template>
                </b-input-group>
                <b-form-input
                  id="armyNo"
                  v-model="armyNo"
                  placeholder="Army No"
                />
              </b-form-group>
            </b-col>
          </b-row>
        </b-col>
        <b-col md="5">
          <b-form-group label="CNIC" label-for="cnic">
            <b-form-input id="cnic" v-model="cnic" placeholder="CNIC" />
          </b-form-group>
        </b-col>
        <b-col md="2">
          <b-button variant="primary" pill @click="search">
            <feather-icon icon="SearchIcon" class="mr-50" />
            <span class="align-middle">Search</span>
          </b-button>
        </b-col>
      </b-row>
      <b-table
        responsive="sm"
        :fields="fields"
        :items="petitions"
        details-td-class="m-0 p-0"
        small
        v-if="hasPermission('petition_read')"
        :per-page="0"
        :tbody-tr-class="rowClass"
      >
        <template #cell(category)="row">
          {{ categoryName(row.item.category) }}
        </template>
        <template #cell(rank_type)="row">
          {{ typeName(row.item.rank_type) }}
        </template>
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
            variant="info"
            pill
            size="sm"
            class="mr-50"
            @click="editPetition(row.item)"
            v-if="
              hasPermission('petition_update') &&
              row.item.status !== petitionStatus.CLOSED
            "
          >
            Edit
          </b-button>
          <b-button
            variant="success"
            pill
            class="mr-50"
            size="sm"
            @click="detailPetition(row.item)"
            v-if="hasPermission('petition_read') && !row.item.draft"
          >
            Detail
          </b-button>
          <b-button
            variant="danger"
            pill
            size="sm"
            @click="closePetition(row.item)"
            v-if="
              hasPermission('petition_close') &&
              !row.item.draft &&
              row.item.status !== petitionStatus.CLOSED
            "
          >
            Close
          </b-button>
        </template>
      </b-table>
      <template class="pagination">
        <b-pagination
          size="md"
          :total-rows="totalItems"
          v-model="currentPage"
          :per-page="perPage"
        ></b-pagination>
      </template>
      <div :class="'flexContainer' + ' m-1 p-1'">
        <div
          v-for="(val, index) in categoryColors"
          :key="index"
          :class="'flexContainer mr-2'"
        >
          <div :class="'mr-1'">Category {{ index }}</div>
          <div :class="val + ' ' + 'bullet bulle-sm'"></div>
        </div>
      </div>
    </b-card>
    <petition-create-modal
      @modalClosed="onModalClosed"
      :key="`create-${petitionCreateModalCount}`"
    />
    <petition-edit-modal
      :petition="petition"
      @modalClosed="onModalClosed"
      :key="`edit-${petitionEditModalCount}`"
    />
    <petition-draft-modal
      :petition="petition"
      @modalClosed="onModalClosed"
      :key="`draft-${petitionDraftModalCount}`"
    />
    <petition-detail-modal
      :petition="petition"
      @modalClosed="onModalClosed"
      :key="`detail-${petitionDetailModalCount}`"
    />
    <petition-close-modal
      :petition="petition"
      @modalClosed="onModalClosed"
      :key="`closed-${petitionCloseModalCount}`"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
// import PetitionCreateModal from "@/components/petition/PetitionCreateModal.vue";
// import PetitionEditModal from "@/components/petition/PetitionEditModal.vue";
// import PetitionDraftModal from "@/components/petition/PetitionDraftModal.vue";
// import PetitionDetailModal from "@/components/petition/PetitionDetailModal.vue";
// import PetitionCloseModal from "@/components/petition/PetitionCloseModal.vue";
import VueSelectPaginated from "@/components/ui/VueSelectPaginated.vue";
import util from "@/util.js";

export default {
  components: {
    PetitionCreateModal,
    PetitionEditModal,
    PetitionDraftModal,
    PetitionDetailModal,
    PetitionCloseModal,
    VueSelectPaginated,
  },
  mixins: [util],
  data() {
    return {
      fields: [
        { key: "case_no", label: "Case No" },
        { key: "title", label: "Title" },
        { key: "subject", label: "Subject" },
        { key: "category", label: "Category" },
        { key: "type_data.name", label: "Type" },
        { key: "rank_type", label: "Rank Type" },
        { key: "priority_data.name", label: "Priority" },
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
      petitionCreateModalCount: 0,
      petitionEditModalCount: 0,
      petitionDraftModalCount: 0,
      petitionDetailModalCount: 0,
      petitionCloseModalCount: 0,
      prefix: null,
      armyNo: "",
      cnic: "",
    };
  },
  async mounted() {
    try {
      await this.fetchPaginatedData();
    } catch (error) {
      this.displayError(error);
    }
  },
  methods: {
    ...mapActions({
      getPetitions: "appData/getPetitions",
      getPrefixes: "appData/getPrefixes",
    }),
    async search() {
      await this.fetchPaginatedData();
    },
    async fetchPaginatedData() {
      try {
        const res = await this.getPetitions({
          pageNumber: this.currentPage,
          created_by: this.getLoggedInUser.id,
          army_prefix: this.prefix ? this.prefix.id : null,
          army_no: this.armyNo,
          cnic: this.cnic,
        });
        this.petitions = res.data.results;
        this.totalItems = res.data.count;
        this.perPage = res.data.per_page;
      } catch (error) {
        this.displayError(error);
      }
    },
    createPetition() {
      this.petitionCreateModalCount += 1;
      this.$nextTick(() => {
        this.$bvModal.show("petition-create-modal");
      });
    },
    editPetition(petition) {
      this.petition = petition;
      if (this.petition.draft) {
        this.petitionDraftModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("petition-draft-modal");
        });
      } else {
        this.petitionEditModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("petition-edit-modal");
        });
      }
    },
    detailPetition(petition) {
      this.petition = petition;
      this.petitionDetailModalCount += 1;
      this.$nextTick(() => {
        this.$bvModal.show("petition-detail-modal");
      });
    },
    closePetition(petition) {
      this.petition = petition;
      this.petitionCloseModalCount += 1;
      this.$nextTick(() => {
        this.$bvModal.show("petition-close-modal");
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
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
}

.blinking {
  animation: blink 1s linear infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

.flexContainer {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
}
</style>
