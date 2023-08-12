<template>
    <div>
      <div class="text-right mb-1">
        <b-button
          variant="primary"
          pill
          @click="createComplaintType"
          v-if="hasPermission('complaint_type_create')"
        >
          <feather-icon icon="PlusIcon" class="mr-50" />
          <span class="align-middle">Create</span>
        </b-button>
      </div>
      <b-card>
        <b-table
          responsive="sm"
          :fields="fields"
          :items="petitionTypes"
          details-td-class="m-0 p-0"
          small
          v-if="hasPermission('complaint_type_read')"
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
              v-if="hasPermission('complaint_type_update')"
            >
              Edit
            </b-button>
            <b-button
              variant="danger"
              pill
              size="sm"
              @click="removeComplaintType(row.item)"
              v-if="hasPermission('complaint_type_delete')"
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
      <complaint-type-create-modal
        @modalClosed="onModalClosed"
        :key="`create-${ComplaintTypeCreateModal}`"
      />
      <complaint-type-edit-modal
        :petitionType="petitionType"
        @modalClosed="onModalClosed"
        :key="`edit-${ComplaintTypeEditModal}`"
      />
    </div>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import ComplaintTypeCreateModal from "@/components/subCategory/SubCategoryCreateModal.vue";
  import ComplaintTypeEditModal from "@/components/subCategory/SubCategoryEditModal.vue";
  import util from "@/util.js";
  
  export default {
    components: {
        ComplaintTypeCreateModal,
        ComplaintTypeEditModal,
    },
    data() {
      return {
        fields: [
          { key: "id", label: "Id" },
          { key: "name", label: "Sub Category" },
          { key: "created_at", label: "Created At" },
          { key: "created_by_data", label: "Created By" },
          { key: "updated_by_data", label: "Updated By" },
          { key: "manage", label: "Manage" },
        ],
        currentPage: 1,
        perPage: 0,
        totalItems: 0,
        petitionTypes: [],
        ComplaintType: null,
        CompalintCreateModalCount: 0,
        CompalintTypeEditModalCount: 0,
      };
    },
    mixins: [util],
    async mounted() {
      await this.fetchPaginatedData();
    },
    methods: {
      ...mapActions({
        getPetitionTypes: "appData/getComplaintTypes",
        deletePetitionType: "appData/deletePetitionType",
      }),
      async fetchPaginatedData() {
        try {
          const res = await this.getPetitionTypes({
            pageNumber: this.currentPage,
          });
          this.petitionTypes = res.data.results;
          this.totalItems = res.data.count;
          this.perPage = res.data.per_page;
        } catch (error) {
          this.displayError(error);
        }
      },
      createComplaintType() {
        this.petitionTypeCreateModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("complaint-type-create-modal");
        });
      },
      editPetitionType(petitionType) {
        this.petitionType = petitionType;
        this.petitionTypeEditModalCount += 1;
        this.$nextTick(() => {
          this.$bvModal.show("complaint-type-edit-modal");
        });
      },
      async removePetitionType(petitionType) {
        this.petitionType = petitionType;
        try {
          const res = await this.deleteComplaintType({
            pk: this.complaintType.id,
          });
          if (res.status === 204) {
            this.$swal({
              title: "RFA Type deleted successfully",
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
  