<template>
  <b-modal
    id="petition-close-modal"
    title="RFA Close Modal"
    centered
    hide-footer
    size="lg"
    @hidden="reset"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
  >
    <template #modal-title> <h2 class="m-0">Close RFA</h2> </template>
    <validation-observer ref="petitionCloseFormValidation">
      <b-form @submit.prevent>
        <b-row>
          <b-col md="12">
            <b-form-group label-for="finalComment">
              <template #label>
                Final Comment <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Final Comment"
                rules="required"
              >
                <b-form-textarea
                  id="finalComment"
                  v-model="finalComment"
                  placeholder="Final Comment"
                  rows="4"
                  :state="
                    errors.length > 0
                      ? false
                      : null ||
                        (finalComment.length > 0 &&
                          finalComment.length <= maxCommentCount)
                  "
                  class="char-textarea"
                  :class="
                    finalComment.length === 0 ||
                    finalComment.length >= maxCommentCount
                      ? 'text-danger'
                      : ''
                  "
                  no-resize
                />
                <small class="text-danger">{{ errors[0] }}</small>
                <small
                  class="textarea-counter-value float-right"
                  :class="
                    finalComment.length >= maxCommentCount ? 'bg-danger' : ''
                  "
                >
                  <span class="char-count">{{ finalComment.length }}</span>
                  /
                  {{ maxCommentCount }}
                </small>
              </validation-provider>
            </b-form-group>
          </b-col>
        </b-row>
        <b-form-group class="mt-1 text-right">
          <b-button
            type="submit"
            variant="primary"
            pill
            class="mr-1"
            @click="validationForm"
          >
            Close
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
import { quillEditor } from "vue-quill-editor";
import VueSelectPaginated from "@/components/ui/VueSelectPaginated.vue";
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import draggable from "vuedraggable";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    quillEditor,
    VueSelectPaginated,
    VuePerfectScrollbar,
    draggable,
  },
  props: {
    petition: Object,
  },
  mixins: [util],
  data() {
    return {
      required,
      perfectScrollbarSettings: {
        maxScrollbarLength: 100,
        wheelPropagation: false,
        useBothWheelAxes: false,
        suppressScrollX: true,
      },
      finalComment: "",
      maxCommentCount: 400,
    };
  },
  methods: {
    ...mapActions({
      updatePetition: "appData/updatePetition",
    }),
    async validationForm() {
      const success = await this.$refs.petitionCloseFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async submit() {
      try {
        const res = await this.updatePetition({
          payload: {
            final_comment: this.finalComment,
            status: 2,
            updated_by: this.getLoggedInUser.id,
          },
          pk: this.petition.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA closed successfully",
            icon: "success",
          });
          this.reset();
          this.$nextTick(() => {
            this.$bvModal.hide("petition-close-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    reset() {
      this.finalComment = "";
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
  },
};
</script>

<style lang="scss"  scoped>
@import "@core/scss/vue/libs/quill.scss";

.scroll-area-size {
  height: 30vh;
}
.vSelectStyle .vs__deselect {
  fill: #fff !important;
}
</style>