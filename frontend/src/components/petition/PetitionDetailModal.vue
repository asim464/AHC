smallsmall
<template>
  <b-modal
    id="petition-detail-modal"
    title="RFA Detail Modal"
    centered
    hide-footer
    size="xl"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
  >
    <template #modal-title> <h2 class="m-0">Detail RFA</h2> </template>
    <b-form @submit.prevent>
      <b-tabs content-class="py-1" fill v-model="tabIndex">
        <b-tab no-body>
          <template #title>
            <feather-icon
              icon="HomeIcon"
              :class="homeFormState ? 'text-danger' : ''"
            />
            <span :class="homeFormState ? 'text-danger' : ''">Home</span>
          </template>
          <vue-perfect-scrollbar
            :settings="perfectScrollbarSettings"
            class="modal-size"
          >
            <validation-observer ref="petitionDetailHomeFormValidation">
              <PetitionHomeForm
                :petition="petition"
                :mode="modes.EDIT"
                ref="homeForm"
              />
            </validation-observer>
          </vue-perfect-scrollbar>
        </b-tab>
        <b-tab no-body>
          <template #title>
            <feather-icon
              icon="FileIcon"
              :class="detailFormState ? 'text-danger' : ''"
            />
            <span :class="detailFormState ? 'text-danger' : ''">Detail</span>
          </template>
          <vue-perfect-scrollbar
            :settings="perfectScrollbarSettings"
            class="modal-size"
          >
            <validation-observer ref="petitionDetailFormValidation">
              <PetitionDetailForm
                :petition="petition"
                ref="detailForm"
                :mode="modes.EDIT"
              />
            </validation-observer>
          </vue-perfect-scrollbar>
        </b-tab>
        <b-tab no-body>
          <template #title>
            <feather-icon
              icon="PhoneCallIcon"
              :class="callFormState ? 'text-danger' : ''"
            />
            <span :class="callFormState ? 'text-danger' : ''">Call</span>
          </template>
          <vue-perfect-scrollbar
            :settings="perfectScrollbarSettings"
            class="modal-size"
          >
            <validation-observer ref="petitionDetailCallFormValidation">
              <PetitionCallForm
                :petition="petition"
                ref="callForm"
                :mode="modes.EDIT"
              />
            </validation-observer>
          </vue-perfect-scrollbar>
        </b-tab>
        <b-tab no-body>
          <template #title>
            <feather-icon icon="FileIcon" />
            <span>History</span>
          </template>
          <div class="modal-size">
            <PetitionHistoryForm :petition="petition" :mode="modes.EDIT" />
          </div>
        </b-tab>
      </b-tabs>

      <b-form-group
        class="mt-1 text-right"
        v-if="petition !== null && petition.status !== petitionStatus.CLOSED"
      >
        <b-button
          type="submit"
          variant="primary"
          pill
          class="mr-1"
          @click="setRetain"
          v-if="showRetain && tabIndex === 0"
        >
          Retain & Mark
        </b-button>
        <b-button
          type="submit"
          variant="primary"
          pill
          class="mr-1"
          @click="validationHomeForm"
          v-if="tabIndex === 0"
        >
          Mark
        </b-button>
        <b-button
          type="submit"
          variant="info"
          pill
          class="mr-1"
          @click="validationDetailForm"
          v-if="tabIndex === 1"
        >
          Update
        </b-button>
        <b-button
          type="submit"
          variant="info"
          pill
          class="mr-1"
          @click="validationCallForm"
          v-if="tabIndex === 2"
        >
          Update
        </b-button>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import PetitionHomeForm from "@/components/petitionForm/PetitionHomeForm.vue";
import PetitionDetailForm from "@/components/petitionForm/PetitionDetailForm.vue";
import PetitionCallForm from "@/components/petitionForm/PetitionCallForm.vue";
import PetitionHistoryForm from "@/components/petitionForm/PetitionHistoryForm.vue";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    VuePerfectScrollbar,
    PetitionHomeForm,
    PetitionDetailForm,
    PetitionCallForm,
    PetitionHistoryForm,
  },
  props: {
    petition: Object,
    showRetain: {
      type: Boolean,
      default: false,
    },
  },
  mixins: [util],
  data() {
    return {
      perfectScrollbarSettings: {
        maxScrollbarLength: 100,
        wheelPropagation: false,
        useBothWheelAxes: false,
        suppressScrollX: true,
      },
      tabIndex: 0,
      homeFormState: false,
      detailFormState: false,
      callFormState: false,
      retain: false,
    };
  },
  methods: {
    ...mapActions({
      updatePetition: "appData/updatePetition",
      updatePetitionDetail: "appData/updatePetitionDetail",
    }),
    async setRetain() {
      this.retain = true;
      await this.validationHomeForm();
    },
    async validationHomeForm() {
      const success =
        await this.$refs.petitionDetailHomeFormValidation.validate();
      if (success) {
        this.homeFormState = false;
        await this.submit();
      } else {
        this.homeFormState = true;
      }
    },
    async validationDetailForm() {
      const success = await this.$refs.petitionDetailFormValidation.validate();
      if (success) {
        this.detailFormState = false;
        await this.updateDetail();
      } else {
        this.detailFormState = true;
      }
    },
    async validationCallForm() {
      const success =
        await this.$refs.petitionDetailCallFormValidation.validate();
      if (success) {
        this.callFormState = false;
        await this.updateCall();
      } else {
        this.callFormState = true;
      }
    },
    async submit() {
      const homeForm = this.$refs.homeForm.$data;

      try {
        const users = homeForm.markedUserList.map((user) => {
          return user.id;
        });

        if (users.length === 0) {
          this.displayError("RFA has to be marked");
          return;
        }

        if (homeForm.comment.length > homeForm.maxCommentCount) {
          this.displayError(
            `Comment Length cannot be greater than ${homeForm.maxCommentCount}`
          );
          return;
        }

        const history = [];
        for (let i = 0; i < users.length; i++) {
          const user = users[i];
          history.push({
            comment: homeForm.comment,
            marked_from: this.getLoggedInUser.id,
            marked_to: user,
          });
        }

        const data = {
          retain: this.showRetain ? this.retain : null,
          history: history,
          currently_marked: users,
          updated_by: this.getLoggedInUser.id,
        };

        const res = await this.updatePetition({
          payload: data,
          pk: this.petition.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA marked successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("petition-detail-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        console.log(error);
        this.displayError(error);
      }
    },
    async updateDetail() {
      const detailForm = this.$refs.detailForm.$data;

      try {
        const benefits = detailForm.benefitPlots.map((benefit) => {
          return {
            address: benefit.address,
            status: benefit.status,
          };
        });
        const feedbacks = detailForm.feedbacks.map((feedback) => {
          return {
            habitual: feedback.habitual,
            assessment: feedback.assessment,
          };
        });
        const family = detailForm.family.map((fam) => {
          return {
            name: fam.name,
            job: fam.job,
            age: fam.age,
            education: fam.education,
            is_married: fam.isMarried,
            is_alive: fam.isAlive,
            miscellaneous: fam.miscellaneous,
            employment: fam.employment,
            financial_status: fam.financialStatus,
            relation: fam.relation.value,
          };
        });
        const property = detailForm.property.map((prop) => {
          return {
            address: prop.address,
            type: prop.type.value,
          };
        });

        const detail = {
          army_prefix: detailForm.prefix ? detailForm.prefix.id : null,
          army_no: detailForm.armyNo ? detailForm.armyNo : null,
          rank: detailForm.rank ? detailForm.rank.id : null,
          status: detailForm.status ? detailForm.status.id : null,
          name: detailForm.name ? detailForm.name : null,
          course: detailForm.course ? detailForm.course : null,
          parent_unit: detailForm.parentUnit ? detailForm.parentUnit : null,
          unit_comd: detailForm.unitComd ? detailForm.unitComd : null,
          contact_no: detailForm.contactNo ? detailForm.contactNo : null,
          cnic: detailForm.cnic ? detailForm.cnic : null,
          is_alive: detailForm.isAlive,
          date_of_commission: detailForm.dateOfCommission
            ? detailForm.dateOfCommission
            : null,
          date_of_retirement:
            detailForm.dateOfRetirement !== ""
              ? detailForm.dateOfRetirement
              : null,
          cause_of_retirement:
            detailForm.causeOfRetirement !== ""
              ? detailForm.causeOfRetirement
              : null,
          permanent_address:
            detailForm.permanent !== "" ? detailForm.permanent : null,
          temporary_address:
            detailForm.temporary !== "" ? detailForm.temporary : null,
          commutation:
            detailForm.commutation !== "" ? detailForm.commutation : null,
          pension: detailForm.pension !== "" ? detailForm.pension : null,
          financial_assistance_from_army:
            detailForm.financialAssistanceFromArmy !== ""
              ? detailForm.financialAssistanceFromArmy
              : null,
          ancestral_house:
            detailForm.ancestralHouse !== "" ? detailForm.ancestralHouse : null,
          ancestral_land:
            detailForm.ancestralLand !== "" ? detailForm.ancestralLand : null,
          current_source_of_income:
            detailForm.currentSourceOfIncome !== ""
              ? detailForm.currentSourceOfIncome
              : null,
          assessment:
            detailForm.assessment !== "" ? detailForm.assessment : null,
          recommendation:
            detailForm.recommendation !== "" ? detailForm.recommendation : null,
          staff_comment:
            detailForm.staffComment !== "" ? detailForm.staffComment : null,
          updated_by: this.getLoggedInUser.id,
          benefits: benefits,
          feedbacks: feedbacks,
          family: family,
          property: property,
        };

        const res = await this.updatePetitionDetail({
          payload: detail,
          pk: this.petition.detail.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA detail updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("petition-detail-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    async updateCall() {
      const callForm = this.$refs.callForm.$data;

      try {
        for (let i = 0; i < callForm.calls.length; i++) {
          const element = callForm.calls[i];
          if (element.comment.length > this.maxCommentCount) {
            this.displayError(
              `Comment Length cannot be greater than ${this.maxCommentCount}`
            );
            return;
          }
        }

        const calls = callForm.calls.map((call) => {
          return {
            comment: call.comment,
            call_from: this.getLoggedInUser.id,
          };
        });

        const res = await this.updatePetition({
          payload: {
            calls: calls,
            updated_by: this.getLoggedInUser.id,
          },
          pk: this.petition.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA calls updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("petition-detail-modal");
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

<style lang="scss" scoped>
.scroll-area-size {
  height: 30vh;
}

.scroll-area-size ul {
  height: 100%;
}

.modal-size {
  height: 55vh;
}
</style>
