<template>
  <b-modal
    id="edit-user-modal"
    centered
    size="lg"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
    dialog-class="my-dialog-class"
  >
    <template #modal-title> <h2 class="m-0">Edit User</h2> </template>
    <validation-observer ref="editUserFormValidation">
      <b-form @submit.prevent>
        <b-form-row>
          <b-col>
            <VueSelectPaginated
              name="Role"
              label="name"
              :prevSelected="role"
              :getListMethod="getRoles"
              @setMethod="
                (value) => {
                  role = value;
                }
              "
            />
          </b-col>
        </b-form-row>
      </b-form>
    </validation-observer>
    <template #modal-footer>
      <b-form-group class="text-right">
        <b-button type="submit" variant="info" pill @click="validationForm">
          Update
        </b-button>
      </b-form-group>
    </template>
  </b-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import VueSelectPaginated from "@/components/ui/VueSelectPaginated.vue";
import { required } from "@validations";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    VueSelectPaginated,
  },
  props: {
    user: Object,
  },
  mixins: [util],
  data() {
    return {
      required,
      role: null,
    };
  },
  async mounted() {
    if (this.user) {
      this.role = this.user.role_data;
    }
  },
  methods: {
    ...mapActions({
      createUser: "appData/createUser",
      getRoles: "appData/getRoles",
    }),
    async validationForm() {
      const success = await this.$refs.editUserFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async submit() {
      try {
        const res = await this.createUser({
          id: this.user.id,
          username: this.user.username,
          name: this.user.name,
          profile_status: this.user.profile_status,
          telephone: this.user.telephone,
          rank_name: this.user.rank_name,
          service_name: this.user.service_name,
          rank_order: this.user.rank_order,
          rank_id: this.user.rank_id,
          appointment_id: this.user.appointment_id,
          appointment_name: this.user.appointment_name,
          appointment_order: this.user.appointment_order,
          executive_order: this.user.executive_order,
          appointment_type: this.user.appointment_type,
          data_center_id: this.user.data_center_id,
          organization: this.user.organization,
          role: this.role ? this.role.id : null,
          created_by: this.getLoggedInUser.id,
          updated_by: this.getLoggedInUser.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "User updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("edit-user-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
  },
};
</script>

<style></style>
