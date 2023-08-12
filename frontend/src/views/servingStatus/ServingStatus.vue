<template>
    <div>
      <div class="text-right mb-1">
        <b-button
          variant="primary"
          pill
          @click="createServingStatus"
          v-if="hasPermission('serving_status_create')"
        >
          <feather-icon icon="PlusIcon" class="mr-50" />
          <span class="align-middle">Create</span>
        </b-button>
      </div>
      <b-card>
        <b-table
          responsive="sm"
          :fields="fields"
          :items="servingStatus"
          details-td-class="m-0 p-0"
          small
          v-if="hasPermission('serving_status_read')"
          :per-page="0"
        >
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
              class="mr-1"
              @click="editPetitionType(row.item)"
              v-if="hasPermission('serving_status_update')"
            >
              Edit
            </b-button>
            <b-button
              variant="danger"
              pill
              size="sm"
              @click="removeServingStatus(row.item)"
              v-if="hasPermission('serving_status_delete')"
            >
              Delete
            </b-button>
          </template>
        </b-table>
        <b-pagination
          size="md"
          :total-rows="totalItems"
          v-model="currentPage"
          :per-page="perPage"
        ></b-pagination>
      </b-card>
      <serving-create-modal
        @modalClosed="onModalClosed"
        :key="`create-${ServingCreateModal}`"
      />
      <serving-edit-modal
        :serving="serving"
        @modalClosed="onModalClosed"
        :key="`edit-${ServingEditModal}`"
      />
    </div>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import ServingCreateModal from "@/components/servingStatus/ServingStatusCreateModal.vue";
  import ServingEditModal from "@/components/servingStatus/ServingStatusEditModal.vue";
  import util from "@/util.js";
  
  export default {
    components: {
      ServingCreateModal,
      ServingEditModal,
    },
    data() {
      return {
        fields: [
          { key: "id", label: "Id" },
          { key: "name", label: "Serving Status" },
          { key: "created_at", label: "Created At" },
          { key: "created_by_data", label: "Created By" },
          { key: "updated_by_data", label: "Updated By" },
          { key: "manage", label: "Manage" },
        ],
        currentPage: 1,
        perPage: 0,
        totalItems: 0,
        servingStatus: [],
        serving: null,
        ServingStatusCreateModal: 0,
        ServingStatusEditModal: 0,
      };
    },
    mixins: [util],
    async mounted() {
      await this.fetchPaginatedData();
    },
    methods: {
      ...mapActions({
        getServings: "appData/getServings",
        deleteServing: "appData/deleteServing",
      }),
      async fetchPaginatedData() {
        try {
          const res = await this.getServings({
            pageNumber: this.currentPage,
          });
          this.servingStatus = res.data.results;
          this.totalItems = res.data.count;
          this.perPage = res.data.per_page;
        } catch (error) {
          this.displayError(error);
        }
      },
      createServingStatus() {
        this.ServingStatusCreateModal += 1;
        this.$nextTick(() => {
          this.$bvModal.show("serving-create-modal");
        });
      },
      editPetitionType(serving) {
        this.serving = serving;
        this.ServingStatusEditModal += 1;
        this.$nextTick(() => {
          this.$bvModal.show("serving-edit-modal");
        });
      },
      async removeServingStatus(serving) {
        this.serving = serving;
        try {
          const res = await this.deleteServing({
            pk: this.serving.id,
          });
          if (res.status === 204) {
            this.$swal({
              title: "Serving Status deleted successfully",
              icon: "success",
            });
            if (
              (this.totalItems - 1) % this.perPage === 0 &&
              this.currentPage !== 1
            ) {
              this.currentPage -= 1;
            } else {
              await this.fetchPaginatedData();
            }
          }
        } catch (error) {
          this.displayError(error);
        }
      },
      async onModalClosed() {
        await this.fetchPaginatedData();
      },
    },
    computed: {
      ...mapGetters({
        hasPermission: "appData/hasPermission",
      }),
    },
    watch: {
      currentPage: async function (val) {
        await this.fetchPaginatedData();
      },
    },
  };
  </script>
  
  <style></style>
  