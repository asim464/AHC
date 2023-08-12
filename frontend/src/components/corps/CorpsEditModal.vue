<template>
    <b-modal
      id="corps-edit-modal"
      title="Corps Edit Modal"
      centered
      hide-footer
      size="lg"
      @hidden="reset"
      :no-close-on-esc="true"
      :no-close-on-backdrop="true"
    >
      <template #modal-title>
        <h2 class="m-0">Edit Corps </h2>
      </template>
      <validation-observer ref="corpsEditFormValidation">
        <b-form @submit.prevent>
          <b-form-group label-for="type">
            <template #label> Corps <span class="text-danger">*</span> </template>
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
      Corp: Object,
    },
    data() {
      return {
        required,
        type: "",
      };
    },
    async mounted() {
      if (this.Corp) {
        this.type = this.Corp.name;
      }
    },
    methods: {
      ...mapActions({
        updateCorps: "appData/updateCorps",
      }),
      async validationForm() {
        const success =
          await this.$refs.corpsEditFormValidation.validate();
        if (success) {
          await this.submit();
        }
      },
      async submit() {
        try {
          const res = await this.updateCorps({
            payload: {
              name: this.type,
              updated_by: this.getLoggedInUser.id,
            },
            pk: this.Corp.id,
          });
          if (res.status === 200) {
            this.$swal({
              title: "Corps updated successfully",
              icon: "success",
            });
            this.reset();
            this.$nextTick(() => {
              this.$bvModal.hide("corps-edit-modal");
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