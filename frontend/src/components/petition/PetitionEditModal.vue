<template>
  <b-modal
    id="petition-edit-modal"
    title="RFA Edit Modal"
    centered
    hide-footer
    size="lg"
    @hidden="reset"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
  >
    <template #modal-title> <h2 class="m-0">Edit Complaint</h2> </template>
    <validation-observer ref="petitionEditFormValidation">
      <b-form @submit.prevent>
        <b-row>
          <b-col md="6">
            <b-form-group label-for="title">
              <template #label>
                Title
                <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Title"
                :rules="{ required, regex: /^[A-Z0-9\s]*$/i }"
              >
                <b-form-input
                  id="title"
                  v-model="title"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Title"
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label-for="subject">
              <template #label>
                Subject
                <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Subject"
                :rules="{ required, regex: /^[A-Z0-9\s]*$/i }"
              >
                <b-form-input
                  id="subject"
                  v-model="subject"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Subject"
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="12">
            <b-form-group label="Documents" label-for="documents">
              <b-form-file
                id="documents"
                placeholder="Choose a file or drop it here..."
                drop-placeholder="Drop file here..."
                multiple
                :accept="acceptedFiles.join(', ')"
                @change="upload"
                :file-name-formatter="formatFilesName"
              />
              <small class="text-danger" v-if="documentError === 1"
                >Max {{ maxFilesCount }} files are allowed</small
              >
              <small class="text-danger" v-if="documentError === 2">
                Each file size should be less than {{ maxFileSize }} MB
              </small>
              <small class="text-danger" v-if="documentError === 3">
                Supported File Types are {{ acceptedFiles.join(", ") }}
              </small>
              <div class="d-flex flex-wrap">
                <b-badge
                  pill
                  variant="primary"
                  v-for="(file, index) in prevDocuments"
                  :key="`prevFile-${index}`"
                  class="mr-50 mt-50 cursor-pointer"
                  @click="openFile(file.path)"
                >
                  {{ file.file_data.name }}
                </b-badge>
                <b-badge
                  pill
                  variant="primary"
                  v-for="(file, index) in files"
                  :key="`file-${index}`"
                  class="mr-50 mt-50"
                >
                  {{ file.name }}
                  <feather-icon
                    size="24"
                    icon="XIcon"
                    class="cursor-pointer"
                    @click="removeFile(index)"
                  />
                </b-badge>
              </div>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="12">
            <b-form-group>
              <template #label>
                Content
                <span class="text-danger">*</span>
              </template>
              <quill-editor v-model="content" :options="option" />
            </b-form-group>
          </b-col>
        </b-row>
        <b-form-group class="mt-1 text-right">
          <b-button
            type="submit"
            variant="info"
            pill
            class="mr-1"
            @click="validationForm"
          >
            Update
          </b-button>
          <b-button
            type="reset"
            variant="outline-secondary"
            @click="reset"
            pill
          >
            Reset
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
      title: "",
      subject: "",
      content: "",
      draft: true,
      documentError: 0,
      maxFilesCount: 15,
      maxFileSize: 5,
      files: [],
      prevDocuments: [],
      option: {
        theme: "snow",
        modules: {
          toolbar: [
            [{ header: [1, 2, 3, 4, 5, 6, false] }],

            ["bold", "italic", "underline", "strike"], // toggled buttons

            [{ list: "ordered" }, { list: "bullet" }],
            [{ align: [] }],
            [{ script: "sub" }, { script: "super" }], // superscript/subscript
            [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
            [{ direction: "rtl" }], // text direction

            [{ color: [] }, { background: [] }], // dropdown with defaults from theme
            [{ font: [] }],
          ],
        },
      },
      acceptedFiles: [".jpg", ".png", ".gif", ".pdf", ".docx"],
    };
  },
  mounted() {
    if (this.petition) {
      this.title = this.petition.title;
      this.subject = this.petition.subject;
      this.content = this.petition.content;
      this.draft = this.petition.draft;

      this.prevDocuments = this.petition.documents;
    }
  },
  methods: {
    ...mapActions({
      updatePetition: "appData/updatePetition",
    }),
    async upload(event) {
      this.documentError = 0;

      const files = event.target.files;
      if (files.length > this.maxFilesCount) {
        this.documentError = 1;
        return;
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const ext = file.name.slice(
          ((file.name.lastIndexOf(".") - 1) >>> 0) + 1
        );
        if (file.size > this.maxFileSize * 100 * 1024) {
          this.documentError = 2;
          return;
        }
        if (!this.acceptedFiles.includes(ext)) {
          this.documentError = 3;
          return;
        }
      }

      for (let i = 0; i < files.length; i++) {
        this.files.push(files[0]);
      }
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    openFile(path) {
      window.open(path, "_blank");
    },
    formatFilesName(files) {
      return this.files.length === 1
        ? this.files[0].name
        : `${this.files.length} files selected`;
    },
    async validationForm() {
      const success = await this.$refs.petitionEditFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async submit() {
      try {
        let formData = new FormData();

        for (var i = 0; i < this.files.length; i++) {
          let file = this.files[i];

          formData.append("files[" + i + "]", file);
        }

        const data = {
          title: this.title,
          subject: this.subject,
          content: this.content,
          draft: this.draft,
          history: [],
          currently_marked: [],
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
          this.reset();
          this.$nextTick(() => {
            this.$bvModal.hide("petition-edit-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    reset() {
      this.title = "";
      this.subject = "";
      this.files = [];
      this.content = "";
      this.selectedMarkType = false;
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