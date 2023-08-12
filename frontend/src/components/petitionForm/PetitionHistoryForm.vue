<template>
  <b-row>
    <b-col md="12">
      <b-form-group label="History">
        <vue-perfect-scrollbar
          :settings="perfectScrollbarSettings"
          class="scroll-area-size-history border border-primary"
          v-if="petition"
        >
          <b-list-group-item
            v-for="(listItem, index) in historyAndCalls"
            :key="index"
            tag="li"
          >
            <div class="d-flex">
              <div class="ml-25">
                <div v-if="listItem.type === 'History'">
                  <b-card-text class="mb-0 font-weight-bold">
                    From: {{ listItem.marked_from_data.name }}
                  </b-card-text>
                  <b-card-text class="mb-0 font-weight-bold">
                    To: {{ listItem.marked_to_data.name }}
                  </b-card-text>
                  <b-card-text class="mb-0 font-weight-bold">
                    Time: {{ listItem.marked_at }}
                  </b-card-text>
                  <b-card-text class="mb-0 font-weight-bold">
                    Type: {{ listItem.type }}
                    <feather-icon
                      icon="FileIcon"
                      size="20"
                      class="text-primary"
                    />
                  </b-card-text>
                  <b-card-text
                    class="mb-0 font-weight-bold"
                    v-if="
                      listItem.marked_from === getLoggedInUser.id ||
                      listItem.marked_to === getLoggedInUser.id
                    "
                  >
                    Comment: {{ listItem.comment }}
                  </b-card-text>
                </div>
                <div v-if="listItem.type === 'Call'">
                  <b-card-text class="mb-0 font-weight-bold">
                    From: {{ listItem.call_from_data.name }}
                  </b-card-text>
                  <b-card-text class="mb-0 font-weight-bold">
                    Time: {{ listItem.call_at }}
                  </b-card-text>
                  <b-card-text class="mb-0 font-weight-bold">
                    Type: {{ listItem.type }}
                    <feather-icon
                      icon="PhoneCallIcon"
                      size="20"
                      class="text-primary"
                    />
                  </b-card-text>
                  <b-card-text
                    class="mb-0 font-weight-bold"
                    v-if="listItem.call_from === getLoggedInUser.id"
                  >
                    Comment: {{ listItem.comment }}
                  </b-card-text>
                </div>
              </div>
            </div>
          </b-list-group-item>
        </vue-perfect-scrollbar>
      </b-form-group>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from "vuex";
import VuePerfectScrollbar from "vue-perfect-scrollbar";

export default {
  components: {
    VuePerfectScrollbar,
  },
  props: {
    petition: Object,
    mode: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      perfectScrollbarSettings: {
        maxScrollbarLength: 100,
        wheelPropagation: false,
        useBothWheelAxes: false,
        suppressScrollX: true,
      },
    };
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
    historyAndCalls() {
      const arr = [];
      for (let i = 0; i < this.petition.history.length; i++) {
        const element = this.petition.history[i];
        arr.push({
          ...element,
          type: "History",
          time: element.marked_at,
        });
      }
      for (let i = 0; i < this.petition.calls.length; i++) {
        const element = this.petition.calls[i];
        arr.push({
          ...element,
          type: "Call",
          time: element.call_at,
        });
      }
      return arr.sort(function (a, b) {
        return new Date(a.time) - new Date(b.time);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@core/scss/vue/libs/quill.scss";

.scroll-area-size-history {
  height: 60vh;
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
