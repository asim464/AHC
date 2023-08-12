<template>
    <div>
      <div class="text-right mb-1">
        <b-button
          variant="primary"
          pill
          @click="createMartialStatus"
          v-if="hasPermission('martial_status_create')"
        >
          <feather-icon icon="PlusIcon" class="mr-50" />
          <span class="align-middle">Create</span>
        </b-button>
      </div>
      <b-card>
        <b-table
          responsive="sm"
          :fields="fields"
          :items="martialStatuses"
          details-td-class="m-0 p-0"
          small
          v-if="hasPermission('martial_status_read')"
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
              @click="editMartialStatus(row.item)"
              v-if="hasPermission('martial_status_update')"
            >
              Edit
            </b-button>
            <b-button
              variant="danger"
              pill
              size="sm"
              @click="removeMartialStatus(row.item)"
              v-if="hasPermission('martial_status_delete')"
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
      <martial-status-create-modal
        @modalClosed="onModalClosed"
        :key="`create-${MartialStatusCreateModal}`"
      />
      <martial-status-edit-modal
        :MartialStatus="MartialStatus"
        @modalClosed="onModalClosed"
        :key="`edit-${MartialStatusEditModal}`"
      />
    </div>
  </template>

  <script>
  import { mapActions, mapGetters } from "vuex";
  import MartialStatusCreateModal from "@/components/martialStatus/MartialStatusCreateModal.vue";
  import MartialStatusEditModal from "@/components/martialStatus/MartialStatusEditModal.vue";
  import util from "@/util.js";

  export default {
    components: {
        MartialStatusCreateModal,
        MartialStatusEditModal,
    },
    data() {
      return {
        fields: [
          { key: "id", label: "Id" },
          { key: "name", label: "Martial Status" },
          { key: "created_at", label: "Created At" },
          { key: "created_by_data", label: "Created By" },
          { key: "updated_by_data", label: "Updated By" },
          { key: "manage", label: "Manage" },
        ],
        currentPage: 1,
        perPage: 0,
        totalItems: 0,
        martialStatuses: [],
        MartialStatus: null,
        MartialStatusCreateModalCount: 0,
        MartialStatusEditModalCount: 0,
      };
    },
    mixins: [util],
    async mounted() {
      await this.fetchPaginatedData();
    },
    methods: {
      ...mapActions({
        getMartialStatuses: "appData/getMartialStatuses",
        deleteMartialStatus: "appData/deleteMartialStatus",
      }),
      async fetchPaginatedData() {
        try {
          const res = await this.getMartialStatuses({
            pageNumber: this.currentPage,
          });
          this.martialStatuses = res.data.results;
          this.totalItems = res.data.count;
          this.perPage = res.data.per_page;
        } catch (error) {
          this.displayError(error);
        }
      },
      createMartialStatus() {
        this.MartialStatusCreateModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("martial-status-create-modal");
        });
      },
      editMartialStatus(MartialStatus) {
        this.MartialStatus = MartialStatus;
        this.MartialStatusEditModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("martial-status-edit-modal");
        });
      },
      async removeMartialStatus(MartialStatus) {
        this.MartialStatus = MartialStatus;
        try {
          const res = await this.deleteMartialStatus({
            pk: this.MartialStatus.id,
          });
          if (res.status === 204) {
            this.$swal({
              title: "Martial Status deleted successfully",
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
