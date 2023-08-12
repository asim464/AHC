<template>
    <div>
      <div class="text-right mb-1">
        <b-button
          variant="primary"
          pill
          @click="createCorps"
          v-if="hasPermission('corps_create')"
        >
          <feather-icon icon="PlusIcon" class="mr-50" />
          <span class="align-middle">Create</span>
        </b-button>
      </div>
      <b-card>
        <b-table
          responsive="sm"
          :fields="fields"
          :items="Corps"
          details-td-class="m-0 p-0"
          small
          v-if="hasPermission('corps_read')"
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
              @click="editCorps(row.item)"
              v-if="hasPermission('corps_update')"
            >
              Edit
            </b-button>
            <b-button
              variant="danger"
              pill
              size="sm"
              @click="removeCorps(row.item)"
              v-if="hasPermission('corps_delete')"
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
      <corps-create-modal
        @modalClosed="onModalClosed"
        :key="`create-${CorpsCreateModal}`"
      />
      <corps-edit-modal
        :Corp="Corp"
        @modalClosed="onModalClosed"
        :key="`edit-${CorpsEditModal}`"
      />
    </div>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import CorpsCreateModal from "@/components/corps/CorpsCreateModal.vue";
  import CorpsEditModal from "@/components/corps/CorpsEditModal.vue";
  import util from "@/util.js";
  
  export default {
    components: {
        CorpsCreateModal,
        CorpsEditModal,
    },
    data() {
      return {
        fields: [
          { key: "id", label: "Id" },
          { key: "name", label: "Corps" },
          { key: "created_at", label: "Created At" },
          { key: "created_by_data", label: "Created By" },
          { key: "updated_by_data", label: "Updated By" },
          { key: "manage", label: "Manage" },
        ],
        currentPage: 1,
        perPage: 0,
        totalItems: 0,
        Corps: [],
        Corp: null,
        CorpsCreateModalCount: 0,
        CorpsEditModalCount: 0,
      };
    },
    mixins: [util],
    async mounted() {
      await this.fetchPaginatedData();
    },
    methods: {
      ...mapActions({
        getCorps: "appData/getCorps",
        deleteCorps: "appData/deleteCorps",
      }),
      async fetchPaginatedData() {
        try {
          const res = await this.getCorps({
            pageNumber: this.currentPage,
          });
          this.Corps = res.data.results;
          this.totalItems = res.data.count;
          this.perPage = res.data.per_page;
        } catch (error) {
          this.displayError(error);
        }
      },
      createCorps() {
        this.CorpsCreateModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("Corps-create-modal");
        });
      },
      editCorps(Corp) {
        this.Corp = Corp;
        this.CorpsEditModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("corps-edit-modal");
        });
      },
      async removeCorps(Corp) {
        this.Corp = Corp;
        try {
          const res = await this.deleteCorps({
            pk: this.Corp.id,
          });
          if (res.status === 204) {
            this.$swal({
              title: "Corps deleted successfully",
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
  