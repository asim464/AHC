<template>
    <div>
      <div class="text-right mb-1">
        <b-button
          variant="primary"
          pill
          @click="createCity"
          v-if="hasPermission('city_create')"
        >
          <feather-icon icon="PlusIcon" class="mr-50" />
          <span class="align-middle">Create</span>
        </b-button>
      </div>
      <b-card>
        <b-table
          responsive="sm"
          :fields="fields"
          :items="cities"
          details-td-class="m-0 p-0"
          small
          v-if="hasPermission('city_read')"
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
              v-if="hasPermission('city_update')"
            >
              Edit
            </b-button>
            <b-button
              variant="danger"
              pill
              size="sm"
              @click="removeCity(row.item)"
              v-if="hasPermission('city_delete')"
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
      <city-create-modal
        @modalClosed="onModalClosed"
        :key="`create-${CityCreateModal}`"
      />
      <city-edit-modal
        :city="city"
        @modalClosed="onModalClosed"
        :key="`edit-${CityEditModal}`"
      />
    </div>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import CityCreateModal from "@/components/city/CityCreateModal.vue";
  import CityEditModal from "@/components/city/CityEditModal.vue";
  import util from "@/util.js";
  
  export default {
    components: {
      CityCreateModal,
      CityEditModal,
    },
    data() {
      return {
        fields: [
          { key: "id", label: "Id" },
          { key: "name", label: "City" },
          { key: "created_at", label: "Created At" },
          { key: "created_by_data", label: "Created By" },
          { key: "updated_by_data", label: "Updated By" },
          { key: "manage", label: "Manage" },
        ],
        currentPage: 1,
        perPage: 0,
        totalItems: 0,
        cities: [],
        city: null,
        cityCreateModal: 0,
        cityEditModal: 0,
      };
    },
    mixins: [util],
    async mounted() {
      await this.fetchPaginatedData();
    },
    methods: {
      ...mapActions({
        getCity: "appData/getCity",
        deleteCity: "appData/deleteCity",
      }),
      async fetchPaginatedData() {
        try {
          const res = await this.getCity({
            pageNumber: this.currentPage,
          });
          this.cities = res.data.results;
          this.totalItems = res.data.count;
          this.perPage = res.data.per_page;
        } catch (error) {
          this.displayError(error);
        }
      },
      createCity() {
        this.cityCreateModal += 1;
        this.$nextTick(() => {
        this.$bvModal.show("city-create-modal");
        });
      },
      editPetitionType(city) {
        this.city = city;
        this.cityEditModal += 1;
        this.$nextTick(() => {
          this.$bvModal.show("city-edit-modal");
        });
      },
      async removeCity(city) {
        this.city = city;
        try {
          const res = await this.deleteCity({
            pk: this.city.id,
          });
          if (res.status === 204) {
            this.$swal({
              title: "City deleted successfully",
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
  