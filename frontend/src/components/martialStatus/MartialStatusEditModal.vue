<template>
    <b-modal
      id="martial-status-edit-modal"
      title="Martial Status Edit Modal"
      centered
      hide-footer
      size="lg"
      @hidden="reset"
      :no-close-on-esc="true"
      :no-close-on-backdrop="true"
    >
      <template #modal-title>
        <h2 class="m-0">Martial Status Edit</h2>
      </template>
      <validation-observer ref="martialStatusEditFormValidation">
        <b-form @submit.prevent>
          <b-form-group label-for="type">
            <template #label> Martial Status <span class="text-danger">*</span> </template>
            <validation-provider
              #default="{ errors }"
              name="Type"
              rules="required|alpha"
            >
              <b-form-input
                id="type"
                v-model="type"
                :state="errors.length > 0 ? false : null"
                placeholder="Type"
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
          <b-form-group class="mt-2 text-right">
            <b-button
              type="submit"
              variant="info"
              pill
              class="mr-1"
              @click="validationForm"
            >
              Update
            </b-button>
          </b-form-group>
        </b-form>
      </validation-observer>
    </b-modal>
  </template>

  <script>
  import { mapActions, mapGetters } from "vuex";
  import { ValidationProvider, ValidationObserver } from "vee-validate";
  import { required } from "@validations";
  import util from "@/util.js";

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    mixins: [util],
    props: {
      MartialStatus: Object,
    },
    data() {
      return {
        required,
        type: "",
      };
    },
    async mounted() {
      if (this.MartialStatus) {
        this.type = this.MartialStatus.name;
      }
    },
    methods: {
      ...mapActions({
        editMartialStatus: "appData/updateMartialStatus",
      }),
      async validationForm() {
        const success =
          await this.$refs.martialStatusEditFormValidation.validate();
        if (success) {
          await this.submit();
        }
      },
      async submit() {
        try {
          const res = await this.editMartialStatus({
            payload: {
              name: this.type,
              updated_by: this.getLoggedInUser.id,
            },
            pk: this.MartialStatus.id,
          });
          if (res.status === 200) {
            this.$swal({
              title: "Martial Status updated successfully",
              icon: "success",
            });
            this.reset();
            this.$nextTick(() => {
              this.$bvModal.hide("martial-status-edit-modal");
            });
            this.$emit("modalClosed");
          }

        } catch (error) {
          this.displayError(error);
        }
      },
      reset() {
        this.type = "";
      },
    },
    computed: {
      ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
    },
  };
  </script>

  <style>
  </style>
