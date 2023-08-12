import ToastificationContent from "@core/components/toastification/ToastificationContent.vue";

const util = {
  data() {
    return {
      modes: {
        CREATE: 1,
        EDIT: 2,
      },
    };
  },
  methods: {
    displayError(error) {
      const msgs = [];
      if (
        !error.response ||
        error.response.status === 500 ||
        typeof error.response.data === "string"
      ) {
        msgs.push("Error: Server Error");
      } else {
        const data = error.response.data;
        for (let key in data) {
          const element = data[key];
          if (Array.isArray(element)) {
            if (typeof element[0] === "string") {
              if (key !== "msg") {
                msgs.push(`${key}: ${element[0]}`);
              } else {
                msgs.push(`${element[0]}`);
              }
            } else if (typeof element[0] === "object") {
              for (const key in element[0]) {
                if (key !== "msg") {
                  msgs.push(`${key}: ${element[0][key][0]}`);
                } else {
                  msgs.push(`${element[0][key][0]}`);
                }
              }
            }
          } else if (typeof element === "object") {
            for (const key in element) {
              if (key !== "msg") {
                msgs.push(`${key}: ${element[key][0]}`);
              } else {
                msgs.push(`${element[key][0]}`);
              }
            }
          } else {
            if (element !== "Invalid page.") {
              msgs.push(element);
            }
          }
        }
      }

      for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i];
        this.$toast(
          {
            component: ToastificationContent,
            props: {
              title: "Error",
              icon: "BellIcon",
              text: msg,
              variant: "danger",
            },
          },
          {
            timeout: 2000,
            position: "top-center",
          }
        );
      }
    },
  },
};

export default util;
