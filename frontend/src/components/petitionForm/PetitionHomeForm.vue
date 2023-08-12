<template>
  <div>
    <b-row>
      <b-col md="6">
        <b-form-group label="Title" v-if="mode === modes.EDIT">
          <h4 class="mb-0">{{ title }}</h4>
        </b-form-group>
        <b-form-group label-for="title" v-else>
          <template #label> Title <span class="text-danger">*</span> </template>
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
      <b-col md="3">
        <b-form-group
          label="Marking Type"
          label-for="markingType"
          v-slot="{ ariaDescribedby }"
        >
          <b-form-radio-group
            id="markingType"
            v-model="selectedMarkType"
            :aria-describedby="ariaDescribedby"
            @change="onMarkTypeChange"
            :disabled="petition && petition.status === petitionStatus.CLOSED"
          >
            <b-form-radio v-model="selectedMarkType" :value="true">
              Internal
            </b-form-radio>
            <b-form-radio v-model="selectedMarkType" :value="false">
              External
            </b-form-radio>
          </b-form-radio-group>
        </b-form-group>
      </b-col>
      <b-col md="3">
        <VueSelectPaginated
          name="Organization"
          label="name"
          rules="required"
          :disabled="selectedMarkType"
          :prevSelected="selectedOrganization"
          :getMethod="getOrganization"
          :getListMethod="getOrganizations"
          @setMethod="onOrganizationChange"
        />
      </b-col>
    </b-row>
    <b-row class="match-height">
      <b-col md="6">
        <div>
          <b-form-group label="Subject" v-if="mode === modes.EDIT">
            <h4 class="mb-0">{{ subject }}</h4>
          </b-form-group>
          <b-form-group label-for="subject" v-else>
            <template #label>
              Subject <span class="text-danger">*</span>
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
        </div>
        <b-row>
          <b-col md="6">
            <b-form-group label="Type" v-if="mode === modes.EDIT">
              <h4 class="mb-0">
                {{ type ? type.name : "" }}
              </h4>
            </b-form-group>
            <VueSelectPaginated
              name="Type"
              label="name"
              rules="required"
              :prevSelected="type"
              :getListMethod="getPetitionTypes"
              @setMethod="(value) => (type = value)"
              v-else
            />
          </b-col>
          <b-col md="6">
            <b-form-group label="Priority" v-if="mode === modes.EDIT">
              <h4 class="mb-0">
                {{ priority ? priority.name : "" }}
              </h4>
            </b-form-group>
            <VueSelectPaginated
              name="Priority"
              label="name"
              rules="required"
              :prevSelected="priority"
              :getListMethod="getPriorities"
              @setMethod="(value) => (priority = value)"
              v-else
            />
          </b-col>
        </b-row>
        <b-row>
          <b-col md="6">
            <b-form-group label="Category" v-if="mode === modes.EDIT">
              <h4 class="mb-0">
                {{ category ? category.name : "" }}
              </h4>
            </b-form-group>
            <VueSelectPaginated
              name="Category"
              label="name"
              rules="required"
              :prevSelected="category"
              :getListMethod="getCategories"
              @setMethod="(value) => (category = value)"
              v-else
            />
          </b-col>
          <b-col md="6">
            <b-form-group label="Initial Comment" v-if="mode === modes.EDIT">
              <h5 class="mb-0">
                {{ initialComment }}
              </h5>
            </b-form-group>
            <b-form-group v-else label-for="initialComment">
              <template #label>
                Initial Comment
                <span
                  class="text-danger"
                  v-if="category && category.name === 'Cat 2'"
                  >*</span
                >
              </template>
              <validation-provider
                #default="{ errors }"
                name="Initial Comment"
                :rules="{
                  required: category
                    ? category.name === 'Cat 2'
                      ? required
                      : false
                    : false,
                  regex: /^[A-Z0-9.\s]*$/i,
                }"
              >
                <b-form-textarea
                  id="initialComment"
                  v-model="initialComment"
                  placeholder="Initial Comment"
                  rows="2"
                  class="char-textarea"
                  no-resize
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !category ||
                    category.name !== 'Cat 2'
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
                <small
                  class="textarea-counter-value float-right"
                  :class="
                    initialComment.length >= maxCommentCount ? 'bg-danger' : ''
                  "
                >
                  <span class="char-count">{{ initialComment.length }}</span>
                  /
                  {{ maxCommentCount }}
                </small>
              </validation-provider>
            </b-form-group>
          </b-col>
        </b-row>
        <div>
          <b-form-group label="Documents" v-if="mode === modes.EDIT">
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
            </div>
          </b-form-group>
          <b-form-group label-for="documents" v-else>
            <template #label> Documents </template>
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
                v-for="(file, index) in files"
                :key="index"
                class="mr-50 mt-50"
              >
                {{ file.name }}
                <feather-icon
                  size="24"
                  icon="XIcon"
                  class="cursor-pointer"
                  @click="removeFile(index, files)"
                />
              </b-badge>
            </div>
          </b-form-group>
        </div>
        <b-row class="h-100">
          <b-col md="12">
            <b-form-group
              label="Content"
              class="h-100"
              id="quillFormGroup"
              v-if="mode === modes.EDIT"
            >
              <quill-editor
                v-model="content"
                :options="detailOption"
                :disabled="true"
              />
            </b-form-group>
            <b-form-group class="h-100" id="quillFormGroup" v-else>
              <template #label>
                Content <span class="text-danger">*</span>
              </template>
              <quill-editor v-model="content" :options="option" />
            </b-form-group>
          </b-col>
        </b-row>
      </b-col>
      <b-col md="6">
        <b-row>
          <b-col md="6">
            <b-form-group label="Users">
              <vue-perfect-scrollbar
                :settings="perfectScrollbarSettings"
                class="scroll-area-size border border-primary"
              >
                <draggable
                  :list="availableUserList"
                  :move="checkMove"
                  tag="ul"
                  :group="{
                    name: 'users',
                    pull: 'clone',
                    put: true,
                  }"
                  class="list-group list-group-flush cursor-move"
                  :disabled="
                    petition && petition.status === petitionStatus.CLOSED
                  "
                >
                  <b-list-group-item
                    v-for="(listItem, index) in availableUserList"
                    :key="index"
                    tag="li"
                  >
                    <div class="d-flex">
                      <div class="ml-25">
                        <b-card-text class="mb-0 font-weight-bold">
                          {{ listItem.name }}
                        </b-card-text>
                      </div>
                    </div>
                  </b-list-group-item>
                </draggable>
              </vue-perfect-scrollbar>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group>
              <template #label>
                Marked To <span class="text-danger">*</span>
              </template>
              <vue-perfect-scrollbar
                :settings="perfectScrollbarSettings"
                class="scroll-area-size border border-primary"
              >
                <draggable
                  :list="markedUserList"
                  @change="onListChange"
                  tag="ul"
                  group="users"
                  class="list-group list-group-flush cursor-move"
                  :disabled="
                    petition && petition.status === petitionStatus.CLOSED
                  "
                >
                  <b-list-group-item
                    v-for="(listItem, index) in markedUserList"
                    :key="index"
                    tag="li"
                  >
                    <div class="d-flex">
                      <div class="ml-25">
                        <b-card-text class="mb-0 font-weight-bold">
                          {{ listItem.name }}
                        </b-card-text>
                      </div>
                    </div>
                  </b-list-group-item>
                </draggable>
              </vue-perfect-scrollbar>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="12">
            <b-form-group label-for="comment" class="mb-50">
              <template #label>
                Comment <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Comment"
                :rules="{ required, regex: /^[A-Z0-9.\s]*$/i }"
              >
                <b-form-textarea
                  id="comment"
                  v-model="comment"
                  placeholder="Comment"
                  rows="4"
                  :state="
                    errors.length > 0
                      ? false
                      : null ||
                        (comment.length > 0 &&
                          comment.length <= maxCommentCount)
                  "
                  class="char-textarea"
                  :class="
                    comment.length === 0 || comment.length >= maxCommentCount
                      ? 'text-danger'
                      : ''
                  "
                  no-resize
                  :disabled="
                    petition && petition.status === petitionStatus.CLOSED
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
                <small
                  class="textarea-counter-value float-right"
                  :class="comment.length >= maxCommentCount ? 'bg-danger' : ''"
                >
                  <span class="char-count">{{ comment.length }}</span>
                  /
                  {{ maxCommentCount }}
                </small>
              </validation-provider>
            </b-form-group>
            <b-form-group class="mt-0 w-75">
              <b-form-file
                id="mark-documents"
                placeholder="Choose a file or drop it here..."
                drop-placeholder="Drop file here..."
                multiple
                :accept="acceptedFiles.join(', ')"
                @change="uploadMark"
                :file-name-formatter="formatMarkFilesName"
              />
              <small class="text-danger" v-if="markDocumentError === 1"
                >Max {{ maxFilesCount }} files are allowed</small
              >
              <small class="text-danger" v-if="markDocumentError === 2">
                Each file size should be less than {{ maxFileSize }} MB
              </small>
              <small class="text-danger" v-if="markDocumentError === 3">
                Supported File Types are {{ acceptedFiles.join(", ") }}
              </small>
              <div class="d-flex flex-wrap">
                <b-badge
                  pill
                  variant="primary"
                  v-for="(file, index) in markFiles"
                  :key="index"
                  class="mr-50 mt-50"
                >
                  {{ file.name }}
                  <feather-icon
                    size="24"
                    icon="XIcon"
                    class="cursor-pointer"
                    @click="removeFile(index, markFiles)"
                  />
                </b-badge>
              </div>
            </b-form-group>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </div>
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
    mode: {
      type: Number,
      default: 0,
    },
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
      comment: "",
      maxCommentCount: 400,
      selectedMarkType: true,
      selectedOrganization: null,
      availableUserList: [],
      markedUserList: [],
      documentError: 0,
      markDocumentError: 0,
      maxFilesCount: 15,
      maxFileSize: 5,
      files: [],
      markFiles: [],
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
      detailOption: {
        theme: "snow",
        modules: {
          toolbar: false,
        },
      },
      type: null,
      priority: null,
      category: null,
      initialComment: "",
      acceptedFiles: [".jpg", ".jpeg", ".png", ".pdf", ".docx"],
    };
  },
  async mounted() {
    if (this.petition) {
      this.title = this.petition.title;
      this.subject = this.petition.subject;
      this.content = this.petition.content;
      this.initialComment = this.petition.initial_comment
        ? this.petition.initial_comment
        : "";
      this.priority = this.petition.priority;
      this.prevDocuments = this.petition.documents;

      if (this.petition.draft) {
        this.markedUserList = this.petition.currently_marked_data;
        if (this.petition.history.length > 0) {
          this.comment = this.petition.history[0].comment;
        }
      }

      this.type = this.petition.type_data;
      this.priority = this.petition.priority_data;
      this.category = this.petition.category_data;
    }

    if (this.selectedMarkType) {
      try {
        const res = await this.getOrganization({
          pk: this.getLoggedInUser.organization,
        });
        this.selectedOrganization = res.data;
      } catch (error) {
        this.displayError(error);
      }
    }
  },
  methods: {
    ...mapActions({
      getUser: "appData/getUser",
      getUsersUnPaginated: "appData/getUsersUnPaginated",
      getPetitionTypes: "appData/getPetitionTypes",
      getPriorities: "appData/getPriorities",
      getCategories: "appData/getCategories",
      getOrganization: "appData/getOrganization",
      getOrganizations: "appData/getOrganizations",
    }),
    async onMarkTypeChange(markedType) {
      if (markedType) {
        try {
          const res = await this.getOrganization({
            pk: this.getLoggedInUser.organization,
          });
          this.selectedOrganization = res.data;
        } catch (error) {
          this.displayError(error);
        }
      }
    },
    async onOrganizationChange(organization) {
      if (!organization) {
        this.availableUserList = [];
        return;
      }

      try {
        const res = await this.getUsersUnPaginated({
          organization: organization.id,
        });
        this.availableUserList = res.data;
      } catch (error) {
        this.displayError(error);
      }
      this.selectedOrganizationId = null;
    },
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
        this.files.push(files[i]);
      }
    },
    async uploadMark(event) {
      this.markDocumentError = 0;

      const files = event.target.files;
      if (files.length > this.maxFilesCount) {
        this.markDocumentError = 1;
        return;
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const ext = file.name.slice(
          ((file.name.lastIndexOf(".") - 1) >>> 0) + 1
        );
        if (file.size > this.maxFileSize * 100 * 1024) {
          this.markDocumentError = 2;
          return;
        }
        if (!this.acceptedFiles.includes(ext)) {
          this.markDocumentError = 3;
          return;
        }
      }

      for (let i = 0; i < files.length; i++) {
        this.markFiles.push(files[i]);
      }
    },
    formatFilesName(files) {
      return this.files.length === 1
        ? this.files[0].name
        : `${this.files.length} files selected`;
    },
    formatMarkFilesName(files) {
      return this.markFiles.length === 1
        ? this.markFiles[0].name
        : `${this.markFiles.length} markFiles selected`;
    },
    openFile(path) {
      window.open(path, "_blank");
    },
    removeFile(index, files) {
      files.splice(index, 1);
    },
    checkMove(evt) {
      for (let i = 0; i < this.markedUserList.length; i++) {
        const element = this.markedUserList[i];
        if (element.username === evt.draggedContext.element.username) {
          return false;
        }
      }
      return true;
    },
    onListChange({ removed }) {
      if (removed) {
        const users = [];
        let removedFirst = false;

        for (let i = 0; i < this.availableUserList.length; i++) {
          const element = this.availableUserList[i];
          if (element.id === removed.element.id && !removedFirst) {
            removedFirst = true;
          } else {
            users.push(element);
          }
        }

        this.availableUserList = users;
      }
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
  },
};
</script>

<style lang="scss" scoped>
@import "@core/scss/vue/libs/quill.scss";

.scroll-area-size {
  height: 30vh;
}

.scroll-area-size ul {
  height: 100%;
}

.quill-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
}

.quill-editor {
  overflow-y: hidden;
}

.vSelectStyle .vs__deselect {
  fill: #fff !important;
}
</style>
