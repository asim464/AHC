smallsmall
<template>
  <b-modal
    id="petition-draft-modal"
    title="RFA Drfat Modal"
    centered
    hide-footer
    size="xl"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
  >
    <template #modal-title> <h2 class="m-0">Edit RFA</h2> </template>
    <b-form @submit.prevent>
      <vue-perfect-scrollbar
        :settings="perfectScrollbarSettings"
        class="modal-size"
      >
        <b-tabs content-class="py-1" fill>
          <b-tab no-body>
            <template #title>
              <feather-icon
                icon="HomeIcon"
                :class="homeFormState ? 'text-danger' : ''"
              />
              <span :class="homeFormState ? 'text-danger' : ''">Home</span>
            </template>
            <validation-observer ref="petitionDraftHomeFormValidation">
              <PetitionHomeForm
                :petition="petition"
                ref="homeForm"
                :mode="modes.CREATE"
              />
            </validation-observer>
          </b-tab>
          <b-tab no-body>
            <template #title>
              <feather-icon
                icon="FileIcon"
                :class="detailFormState ? 'text-danger' : ''"
              />
              <span :class="detailFormState ? 'text-danger' : ''">Detail</span>
            </template>
            <validation-observer ref="petitionDraftDetailFormValidation">
              <PetitionDetailForm
                :petition="petition"
                ref="detailForm"
                :mode="modes.CREATE"
              />
            </validation-observer>
          </b-tab>
        </b-tabs>
      </vue-perfect-scrollbar>

      <b-form-group class="mt-1 text-right">
        <b-button
          type="submit"
          variant="primary"
          pill
          class="mr-1"
          @click="validationForm"
        >
          Update & Mark
        </b-button>
        <b-button
          type="submit"
          variant="info"
          pill
          class="mr-1"
          @click="saveDraft"
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
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    VuePerfectScrollbar,
    PetitionHomeForm,
    PetitionDetailForm,
  },
  props: {
    petition: Object,
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
      draft: false,
      homeFormState: false,
      detailFormState: false,
    };
  },
  mounted() {
    if (this.petition) {
      this.draft = this.petition.draft;
    }
  },
  methods: {
    ...mapActions({
      updatePetition: "appData/updatePetition",
    }),
    async saveDraft() {
      this.draft = true;
      const homeForm = this.$refs.homeForm.$data;
      const detailForm = this.$refs.detailForm.$data;
      try {
        const users = homeForm.markedUserList.map((user) => {
          return user.id;
        });

        const benefits = detailForm.benefitPlots.map((benefit) => {
          return {
            address: benefit.address ? benefit.address : null,
            status: benefit.status ? benefit.status : null,
          };
        });
        const feedbacks = detailForm.feedbacks.map((feedback) => {
          return {
            habitual: feedback.habitual ? feedback.habitual : null,
            assessment: feedback.assessment ? feedback.assessment : null,
          };
        });
        const family = detailForm.family.map((fam) => {
          return {
            name: fam.name ? fam.name : null,
            job: fam.job ? fam.job : null,
            age: fam.age ? fam.age : null,
            education: fam.education ? fam.education : null,
            is_married: fam.isMarried,
            is_alive: fam.isAlive,
            miscellaneous: fam.miscellaneous ? fam.miscellaneous : null,
            employment: fam.employment ? fam.employment : null,
            financial_status: fam.financialStatus ? fam.financialStatus : null,
            relation: fam.relation ? fam.relation.value : null,
          };
        });
        const property = detailForm.property.map((prop) => {
          return {
            address: prop.address ? prop.address : null,
            type: prop.type ? prop.type.value : null,
          };
        });
        const detail = {
          army_prefix: detailForm.prefix ? detailForm.prefix.id : null,
          army_no: detailForm.armyNo ? detailForm.armyNo : null,
          rank: detailForm.rank ? detailForm.rank.id : null,
          type: detailForm.type ? detailForm.type.id : null,
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
          date_of_retirement: detailForm.dateOfRetirement
            ? detailForm.dateOfRetirement
            : null,
          cause_of_retirement: detailForm.causeOfRetirement
            ? detailForm.causeOfRetirement
            : null,
          permanent_address: detailForm.permanent ? detailForm.permanent : null,
          temporary_address: detailForm.temporary ? detailForm.temporary : null,
          commutation: detailForm.commutation ? detailForm.commutation : null,
          pension: detailForm.pension ? detailForm.pension : null,
          financial_assistance_from_army: detailForm.financialAssistanceFromArmy
            ? detailForm.financialAssistanceFromArmy
            : null,
          ancestral_house: detailForm.ancestralHouse
            ? detailForm.ancestralHouse
            : null,
          ancestral_land: detailForm.ancestralLand
            ? detailForm.ancestralLand
            : null,
          current_source_of_income: detailForm.currentSourceOfIncome
            ? detailForm.currentSourceOfIncome
            : null,
          assessment: detailForm.assessment ? detailForm.assessment : null,
          recommendation: detailForm.recommendation
            ? detailForm.recommendation
            : null,
          staff_comment: detailForm.staffComment
            ? detailForm.staffComment
            : null,
          updated_by: this.getLoggedInUser.id,
          benefits: benefits,
          feedbacks: feedbacks,
          family: family,
          property: property,
        };

        const history = [];
        if (homeForm.comment) {
          for (let i = 0; i < users.length; i++) {
            const user = users[i];
            history.push({
              comment: homeForm.comment,
              marked_from: this.getLoggedInUser.id,
              marked_to: user,
            });
          }
        }

        let formData = new FormData();

        for (var i = 0; i < homeForm.files.length; i++) {
          let file = homeForm.files[i];

          formData.append("files[" + i + "]", file);
        }

        const data = {
          title: homeForm.title ? homeForm.title : null,
          subject: homeForm.subject ? homeForm.subject : null,
          content: homeForm.content ? homeForm.content : null,
          draft: this.draft,
          history: history,
          detail: detail,
          initial_comment: homeForm.category
            ? homeForm.category.name === "Cat 2"
              ? homeForm.initialComment
              : null
            : null,
          currently_marked: users,
          type: homeForm.type ? homeForm.type.id : null,
          priority: homeForm.priority ? homeForm.priority.id : null,
          category: homeForm.category ? homeForm.category.id : null,
          created_by: this.getLoggedInUser.id,
          updated_by: this.getLoggedInUser.id,
        };

        formData.append("data", JSON.stringify(data));

        const res = await this.updatePetition({
          payload: formData,
          pk: this.petition.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("petition-draft-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    async validationForm() {
      let success = await this.$refs.petitionDraftHomeFormValidation.validate();
      if (success) {
        this.homeFormState = false;
        success = await this.$refs.petitionDraftDetailFormValidation.validate();
        if (success) {
          this.detailFormState = false;
          await this.submit();
        } else {
          this.detailFormState = true;
        }
      } else {
        this.homeFormState = true;
      }
    },
    async submit() {
      this.draft = false;

      const homeForm = this.$refs.homeForm.$data;
      const detailForm = this.$refs.detailForm.$data;
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

        if (
          homeForm.dateOfCommission > homeForm.dateOfRetirement &&
          homeForm.dateOfRetirement != ""
        ) {
          this.displayError(
            `Date of Commission can not be greater than Date of Retirement`
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
          type: detailForm.type.id,
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

        let formData = new FormData();

        for (var i = 0; i < homeForm.files.length; i++) {
          let file = homeForm.files[i];

          formData.append("files[" + i + "]", file);
        }

        const data = {
          title: homeForm.title,
          subject: homeForm.subject,
          content: homeForm.content,
          draft: this.draft,
          history: history,
          detail: detail,
          initial_comment: homeForm.category
            ? homeForm.category.name === "Cat 2"
              ? homeForm.initialComment
              : null
            : null,
          currently_marked: users,
          type: homeForm.type.id,
          priority: homeForm.priority.id,
          category: homeForm.category.id,
          created_by: this.getLoggedInUser.id,
          updated_by: this.getLoggedInUser.id,
        };

        formData.append("data", JSON.stringify(data));

        const res = await this.updatePetition({
          payload: formData,
          pk: this.petition.id,
        });
        if (res.status === 200) {
          this.$swal({
            title: "RFA updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("petition-draft-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        console.log(error);
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
  height: 65vh;
}
</style>
