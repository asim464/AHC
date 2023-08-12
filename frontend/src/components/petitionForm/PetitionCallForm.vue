<template>
  <div>
    <div ref="calls" class="repeater-form">
      <div v-for="(item, index) in calls" :id="item.id" :key="index" ref="row">
        <b-row>
          <b-col md="10">
            <b-form-group label-for="comment">
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
                  v-model="item.comment"
                  placeholder="Comment"
                  rows="4"
                  class="char-textarea"
                  :state="
                    errors.length > 0
                      ? false
                      : null ||
                        (item.comment.length > 0 &&
                          item.comment.length <= maxCommentCount)
                  "
                  :class="
                    item.comment.length === 0 ||
                    item.comment.length >= maxCommentCount
                      ? 'text-danger'
                      : ''
                  "
                  no-resize
                  :disabled="petition && !item.delete"
                />
                <small class="text-danger">{{ errors[0] }}</small>
                <small
                  class="textarea-counter-value float-right"
                  :class="
                    item.comment.length >= maxCommentCount ? 'bg-danger' : ''
                  "
                >
                  <span class="char-count">{{ item.comment.length }}</span>
                  /
                  {{ maxCommentCount }}
                </small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col lg="2" md="2" class="mb-50">
            <b-button
              variant="outline-danger"
              size="sm"
              class="mt-0 mt-md-2"
              @click="removeItem(index, 5)"
              v-if="
                petition &&
                petition.status !== petitionStatus.CLOSED &&
                item.delete
              "
            >
              <feather-icon icon="XIcon" class="mr-25" />
              <span>Delete</span>
            </b-button>
          </b-col>
        </b-row>
      </div>
    </div>
    <b-button
      variant="primary"
      size="sm"
      @click="repeateAgain(5)"
      v-if="petition && petition.status !== petitionStatus.CLOSED"
    >
      <feather-icon icon="PlusIcon" class="mr-25" />
      <span>Add New</span>
    </b-button>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { required } from "@validations";
import { quillEditor } from "vue-quill-editor";
import VueSelectPaginated from "@/components/ui/VueSelectPaginated.vue";
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import draggable from "vuedraggable";
import util from "@/util.js";
import { heightTransition } from "@core/mixins/ui/transition";

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
  mixins: [util, heightTransition],
  data() {
    return {
      required,
      calls: [],
      nextTodoCallId: 2,
      maxCommentCount: 400,
    };
  },
  mounted() {
    if (this.petition) {
      this.calls = this.petition.calls.map((call) => {
        return {
          ...call,
          delete: false,
        };
      });

      if (this.calls.length > 0) {
        this.nextTodoCallId = this.calls[this.calls.length - 1].id;
      }
    }
  },
  created() {
    window.addEventListener("resize", this.initTrHeight);
  },
  destroyed() {
    window.removeEventListener("resize", this.initTrHeight);
  },
  methods: {
    repeateAgain() {
      this.calls.push({
        id: (this.nextTodoCallId += this.nextTodoCallId),
        comment: "",
        delete: true,
      });
    },
    removeItem(index, type) {
      this.calls.splice(index, 1);
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
  },
};
</script>

<style>
.vSelectStyle .vs__deselect {
  fill: #fff !important;
}

.repeater-form {
  overflow: hidden;
  transition: 0.35s height;
}
</style>
