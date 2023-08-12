<template>
  <div>
    <div>
      <b-row>
        <b-col md="3">
          <b-form-group label="Type" v-if="mode === modes.EDIT">
            <h4 class="mb-0">{{ type ? type.name : "" }}</h4>
          </b-form-group>
          <VueSelectPaginated
            name="Type"
            label="name"
            rules="required"
            :prevSelected="type"
            :getListMethod="getPetitionDetailTypes"
            @setMethod="(value) => (type = value)"
            v-else
          />
        </b-col>
      </b-row>
      <h4 class="font-weight-bolder">Complaint Detail</h4>
      <b-row>
        <b-col md="3">
          <b-row no-gutters>
            <b-col cols="4">
              <!-- <VueSelectPaginated
                name="Prefix"
                label="name"
                :prevSelected="prefix"
                :getListMethod="getPrefixes"
                @setMethod="(value) => (prefix = value)"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              /> -->
            </b-col>
            <b-col cols="8">
              <b-form-group>
                <template label-for="Army No">
                  Army No <span class="text-danger"></span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Army No"
                  rules="integer"
                >
                  <b-form-input
                    id="armyNo"
                    v-model="armyNo"
                    :state="errors.length > 0 ? false : null"
                    placeholder="Army No"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                </validation-provider>
              </b-form-group>
            </b-col>
          </b-row>
        </b-col>
        <b-col md="3">
          <VueSelectPaginated
            name="Rank"
            label="name"
            :prevSelected="rank"
            :getListMethod="getRankTypes"
            @setMethod="(value) => (rank = value)"
            :disabled="
              (petition && petition.status === petitionStatus.CLOSED) ||
              !type ||
              type.name === detailTypes.CIVILIAN ||
              type.name === detailTypes.ANONYMOUS
            "
          />
        </b-col>
        <b-col md="3">
          <b-form-group label-for="name">
            <template #label> Name <span class="text-danger"></span> </template>
            <validation-provider
              #default="{ errors }"
              name="Name"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="name"
                v-model="name"
                :state="errors.length > 0 ? false : null"
                placeholder="Name"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="3">
          <b-form-group label-for="course">
            <template #label>
              Course <span class="text-danger"></span>
            </template>
            <validation-provider
              #default="{ errors }"
              name="Course"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="course"
                v-model="course"
                :state="errors.length > 0 ? false : null"
                placeholder="Course"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="3">
          <b-form-group label-for="parentUnit">
            <template #label>
              Parent Unit <span class="text-danger"></span>
            </template>
            <validation-provider
              #default="{ errors }"
              name="Parent Unit"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="parentUnit"
                v-model="parentUnit"
                :state="errors.length > 0 ? false : null"
                placeholder="Parent Unit"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="3">
          <b-form-group label-for="unitComd">
            <template #label>
              Unit Comd <span class="text-danger"></span>
            </template>
            <validation-provider
              #default="{ errors }"
              name="Unit Comd"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="unitComd"
                v-model="unitComd"
                :state="errors.length > 0 ? false : null"
                placeholder="Unit Comd"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="3">
          <b-form-group label-for="contactNo">
            <template #label>
              Contact No <span class="text-danger"></span>
            </template>
            <validation-provider
              #default="{ errors }"
              name="Contact No"
              rules="integer|length:11"
            >
              <b-form-input
                id="contactNo"
                v-model="contactNo"
                :state="errors.length > 0 ? false : null"
                placeholder="Contact No"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="3">
          <b-form-group label-for="cnic">
            <template #label> CNIC <span class="text-danger"></span> </template>
            <validation-provider
              #default="{ errors }"
              name="CNIC"
              rules="integer|length:13"
            >
              <b-form-input
                id="cnic"
                v-model="cnic"
                :state="errors.length > 0 ? false : null"
                placeholder="CNIC"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="3">
          <b-form-group label-for="isAlive">
            <template #label>
              Is Alive <span class="text-danger"></span>
            </template>
            <b-form-radio-group
              id="isAlive"
              v-model="isAlive"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.ANONYMOUS
              "
            >
              <b-form-radio v-model="isAlive" :value="true">
                Alive
              </b-form-radio>
              <b-form-radio v-model="isAlive" :value="false">
                Deceased
              </b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
        <b-col md="3">
          <validation-provider #default="{ errors }" name="Date of Commission">
            <b-form-group
              label-for="dateOfCommission"
              :state="errors.length > 0 ? false : null"
            >
              <template #label>
                Date of Commission <span class="text-danger"></span>
              </template>
              <b-form-datepicker
                id="dateOfCommission"
                v-model="dateOfCommission"
                :max="new Date()"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </b-form-group>
          </validation-provider>
        </b-col>
        <b-col md="3">
          <b-form-group
            label="Date of Retirement (SOS)"
            label-for="dateOfRetirement"
          >
            <b-form-datepicker
              id="dateOfRetirement"
              v-model="dateOfRetirement"
              class="mb-2"
              :max="new Date()"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            />
          </b-form-group> </b-col
        ><b-col md="3">
          <b-form-group
            label="Cause of Retirement"
            label-for="causeOfRetirement"
          >
            <validation-provider
              #default="{ errors }"
              name="Cause of Retirement"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="causeOfRetirement"
                v-model="causeOfRetirement"
                placeholder="Cause of Retirement"
                :state="errors.length > 0 ? false : null"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="3">
          <VueSelectPaginated
            name="Status"
            label="name"
            :prevSelected="status"
            :getListMethod="getPetitionDetailStatuses"
            @setMethod="(value) => (status = value)"
            :disabled="
              (petition && petition.status === petitionStatus.CLOSED) ||
              !type ||
              type.name === detailTypes.CIVILIAN ||
              type.name === detailTypes.ANONYMOUS
            "
          />
        </b-col>
      </b-row>
      <h5 class="font-weight-bolder">Address</h5>
      <b-row>
        <b-col md="6">
          <b-form-group label="Permanent" label-for="permanent">
            <validation-provider
              #default="{ errors }"
              name="Permanent"
              :rules="{ regex: /^[A-Z0-9.,/#-\s]*$/i }"
            >
              <b-form-input
                id="permanent"
                v-model="permanent"
                placeholder="Permanent"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="6">
          <b-form-group label="Temporary" label-for="temporary">
            <validation-provider
              #default="{ errors }"
              name="Temporary"
              :rules="{ regex: /^[A-Z0-9.,/#-\s]*$/i }"
            >
              <b-form-input
                id="temporary"
                v-model="temporary"
                placeholder="Temporary"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
    </div>
    <div class="mb-1">
      <h4 class="font-weight-bolder">Details of Assets</h4>
      <h5 class="font-weight-bolder">Svc / Appt Benefit Plots</h5>
      <div ref="benefitPlots" class="repeater-form">
        <b-row
          v-for="(item, index) in benefitPlots"
          :id="item.id"
          :key="index"
          ref="benefitPlotsRow"
        >
          <b-col md="5">
            <b-form-group label-for="address">
              <template #label>
                Address <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Address"
                :rules="{ required, regex: /^[A-Z0-9.,/#-\s]*$/i }"
              >
                <b-form-input
                  id="address"
                  type="text"
                  v-model="item.address"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Address"
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !type ||
                    type.name === detailTypes.CIVILIAN ||
                    type.name === detailTypes.ANONYMOUS
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col md="5">
            <b-form-group label-for="status">
              <template #label>
                Status <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Status"
                rules="required|alpha"
              >
                <b-form-input
                  id="status"
                  type="text"
                  v-model="item.status"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Status"
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !type ||
                    type.name === detailTypes.CIVILIAN ||
                    type.name === detailTypes.ANONYMOUS
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col lg="2" md="2" class="mb-50">
            <b-button
              variant="outline-danger"
              class="mt-0 mt-md-2"
              size="sm"
              @click="removeItem(index, 1)"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            >
              <feather-icon icon="XIcon" class="mr-25" />
              <span>Delete</span>
            </b-button>
          </b-col>
        </b-row>
      </div>
      <b-button
        variant="primary"
        size="sm"
        @click="repeateAgain(1)"
        :disabled="
          (petition && petition.status === petitionStatus.CLOSED) ||
          !type ||
          type.name === detailTypes.CIVILIAN ||
          type.name === detailTypes.ANONYMOUS
        "
      >
        <feather-icon icon="PlusIcon" class="mr-25" />
        <span>Add New</span>
      </b-button>
      <b-row class="mt-50">
        <b-col md="4">
          <b-form-group label="Commutation" label-for="commutation">
            <validation-provider
              #default="{ errors }"
              name="Commutation"
              rules="integer"
            >
              <b-form-input
                id="commutation"
                type="text"
                v-model="commutation"
                placeholder="Commutation"
                :state="errors.length > 0 ? false : null"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group label="Pension" label-for="pension">
            <validation-provider
              #default="{ errors }"
              name="Pension"
              rules="integer"
            >
              <b-form-input
                id="pension"
                type="text"
                v-model="pension"
                placeholder="Pension"
                :state="errors.length > 0 ? false : null"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group
            label="Financial Assistance From Army"
            label-for="financialAssistanceFromArmy"
          >
            <validation-provider
              #default="{ errors }"
              name="Financial Assistance From Army"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="financialAssistanceFromArmy"
                type="text"
                v-model="financialAssistanceFromArmy"
                placeholder="Financial Assistance From Army"
                :state="errors.length > 0 ? false : null"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="4">
          <b-form-group label="Ancestral House" label-for="ancestralHouse">
            <validation-provider
              #default="{ errors }"
              name="Ancestral House"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="ancestralHouse"
                type="text"
                v-model="ancestralHouse"
                placeholder="Ancestral House"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group label="Ancestral Land" label-for="ancestralLand">
            <validation-provider
              #default="{ errors }"
              name="Ancestral Land"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="ancestralLand"
                type="text"
                v-model="ancestralLand"
                placeholder="Ancestral Land"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group
            label="Current Source Of Income"
            label-for="currentSourceOfIncome"
          >
            <validation-provider
              #default="{ errors }"
              name="Current Source Of Income"
              :rules="{ regex: /^[A-Z\s]*$/i }"
            >
              <b-form-input
                id="currentSourceOfIncome"
                type="text"
                v-model="currentSourceOfIncome"
                placeholder="Current Source Of Income"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
                "
              />
              <small class="text-danger">{{ errors[0] }}</small>
            </validation-provider>
          </b-form-group>
        </b-col>
      </b-row>
      <h5 class="font-weight-bolder">Feedback from Unit Offrs</h5>
      <div ref="feedbacks" class="repeater-form">
        <b-row
          v-for="(item, index) in feedbacks"
          :id="item.id"
          :key="index"
          ref="feedbacksRow"
        >
          <b-col md="5">
            <b-form-group label-for="habitual">
              <template #label>
                Habitual / Non Habitual
                <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Habitual / Non Habitual"
                :rules="{ required, regex: /^[A-Z\s]*$/i }"
              >
                <b-form-input
                  id="habitual"
                  type="text"
                  v-model="item.habitual"
                  placeholder="Habitual / Non Habitual"
                  :state="errors.length > 0 ? false : null"
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !type ||
                    type.name === detailTypes.CIVILIAN ||
                    type.name === detailTypes.ANONYMOUS
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col md="5">
            <b-form-group label-for="assessment">
              <template #label>
                Assessment
                <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Assessment"
                :rules="{ required, regex: /^[A-Z\s]*$/i }"
              >
                <b-form-input
                  id="assessment"
                  type="text"
                  v-model="item.assessment"
                  placeholder="Assessment"
                  :state="errors.length > 0 ? false : null"
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !type ||
                    type.name === detailTypes.CIVILIAN ||
                    type.name === detailTypes.ANONYMOUS
                  "
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col lg="2" md="2" class="mb-50">
            <b-button
              variant="outline-danger"
              size="sm"
              class="mt-0 mt-md-2"
              @click="removeItem(index, 2)"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            >
              <feather-icon icon="XIcon" class="mr-25" />
              <span>Delete</span>
            </b-button>
          </b-col>
        </b-row>
      </div>
      <b-button
        variant="primary"
        size="sm"
        @click="repeateAgain(2)"
        :disabled="
          (petition && petition.status === petitionStatus.CLOSED) ||
          !type ||
          type.name === detailTypes.CIVILIAN ||
          type.name === detailTypes.ANONYMOUS
        "
      >
        <feather-icon icon="PlusIcon" class="mr-25" />
        <span>Add New</span>
      </b-button>
    </div>
    <div class="mb-1">
      <h4 class="font-weight-bolder">Family Details</h4>
      <div ref="family" class="repeater-form">
        <div
          v-for="(item, index) in family"
          :id="item.id"
          :key="index"
          ref="familyRow"
        >
          <b-row>
            <b-col md="4">
              <b-form-group label="Name" label-for="name">
                <template #label>
                  Name
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Name"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="name"
                    type="text"
                    v-model="item.name"
                    placeholder="Name"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group label-for="job">
                <template #label>
                  Job
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Job"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="job"
                    type="text"
                    v-model="item.job"
                    placeholder="Job"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <validation-provider
                #default="{ errors }"
                name="Relation"
                rules="required"
              >
                <b-form-group
                  label-for="relation"
                  :state="errors.length > 0 ? false : null"
                >
                  <template #label>
                    Relation
                    <span class="text-danger">*</span>
                  </template>
                  <v-select
                    id="relation"
                    v-model="item.relation"
                    :options="familyRelations"
                    placeholder="Relation"
                    label="text"
                    class="v-style-chooser"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <b-form-invalid-feedback
                    :state="errors.length > 0 ? false : null"
                  >
                    {{ errors[0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </validation-provider>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="4">
              <b-form-group label-for="education">
                <template #label>
                  Education
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Education"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="education"
                    type="text"
                    v-model="item.education"
                    placeholder="Education"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group label-for="age">
                <template #label>
                  Age
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Age"
                  rules="required|integer"
                >
                  <b-form-input
                    id="age"
                    type="text"
                    v-model="item.age"
                    placeholder="Age"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="2">
              <b-form-group label="Married / Single">
                <template #label>
                  Married / Single
                  <span class="text-danger">*</span>
                </template>
                <b-form-radio-group v-model="item.isMarried">
                  <b-form-radio :value="true"> Married </b-form-radio>
                  <b-form-radio :value="false"> Single </b-form-radio>
                </b-form-radio-group>
              </b-form-group>
            </b-col>
            <b-col md="2">
              <b-form-group label="Alive / Deceased">
                <template #label>
                  Alive / Deceased
                  <span class="text-danger">*</span>
                </template>
                <b-form-radio-group
                  v-model="item.isAlive"
                  :disabled="
                    (petition && petition.status === petitionStatus.CLOSED) ||
                    !type ||
                    type.name === detailTypes.CIVILIAN ||
                    type.name === detailTypes.ANONYMOUS
                  "
                >
                  <b-form-radio v-model="item.isAlive" :value="true">
                    Alive
                  </b-form-radio>
                  <b-form-radio v-model="item.isAlive" :value="false">
                    Deceased
                  </b-form-radio>
                </b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="4">
              <b-form-group label-for="employment">
                <template #label>
                  Employment
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Employment"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="employment"
                    type="text"
                    v-model="item.employment"
                    placeholder="Employment"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group label-for="miscellaneous">
                <template #label>
                  Miscellaneous
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Miscellaneous"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="miscellaneous"
                    type="text"
                    v-model="item.miscellaneous"
                    placeholder="Miscellaneous"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group label-for="financialStatus">
                <template #label>
                  Financial Status
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Financial Status"
                  :rules="{ required, regex: /^[A-Z\s]*$/i }"
                >
                  <b-form-input
                    id="financialStatus"
                    type="text"
                    v-model="item.financialStatus"
                    placeholder="Financial Status"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="10"></b-col>
            <b-col lg="2" md="2" class="mb-50">
              <b-button
                variant="outline-danger"
                size="sm"
                class="mt-0 mt-md-2"
                @click="removeItem(index, 3)"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
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
        @click="repeateAgain(3)"
        :disabled="
          (petition && petition.status === petitionStatus.CLOSED) ||
          !type ||
          type.name === detailTypes.CIVILIAN ||
          type.name === detailTypes.ANONYMOUS
        "
      >
        <feather-icon icon="PlusIcon" class="mr-25" />
        <span>Add New</span>
      </b-button>
    </div>
    <div class="mb-1">
      <h4 class="font-weight-bolder">Property Held</h4>
      <div ref="property" class="repeater-form">
        <div
          v-for="(item, index) in property"
          :id="item.id"
          :key="index"
          ref="propertyRow"
        >
          <b-row>
            <b-col md="5">
              <b-form-group label-for="address">
                <template #label>
                  Address
                  <span class="text-danger">*</span>
                </template>
                <validation-provider
                  #default="{ errors }"
                  name="Address"
                  :rules="{ required, regex: /^[A-Z0-9.,/#-\s]*$/i }"
                >
                  <b-form-input
                    id="address"
                    type="text"
                    v-model="item.address"
                    placeholder="Address"
                    :state="errors.length > 0 ? false : null"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>
            </b-col>
            <b-col md="5">
              <validation-provider
                #default="{ errors }"
                name="Type"
                rules="required"
              >
                <b-form-group
                  label-for="type"
                  :state="errors.length > 0 ? false : null"
                >
                  <template #label>
                    Type
                    <span class="text-danger">*</span>
                  </template>
                  <v-select
                    id="type"
                    v-model="item.type"
                    :options="propertyTypes"
                    placeholder="Type"
                    label="text"
                    class="style-chooser"
                    :disabled="
                      (petition && petition.status === petitionStatus.CLOSED) ||
                      !type ||
                      type.name === detailTypes.CIVILIAN ||
                      type.name === detailTypes.ANONYMOUS
                    "
                  />
                  <b-form-invalid-feedback
                    :state="errors.length > 0 ? false : null"
                  >
                    {{ errors[0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </validation-provider>
            </b-col>
            <b-col lg="2" md="2" class="mb-50">
              <b-button
                variant="outline-danger"
                size="sm"
                class="mt-0 mt-md-2"
                @click="removeItem(index, 4)"
                :disabled="
                  (petition && petition.status === petitionStatus.CLOSED) ||
                  !type ||
                  type.name === detailTypes.CIVILIAN ||
                  type.name === detailTypes.ANONYMOUS
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
        @click="repeateAgain(4)"
        :disabled="
          (petition && petition.status === petitionStatus.CLOSED) ||
          !type ||
          type.name === detailTypes.CIVILIAN ||
          type.name === detailTypes.ANONYMOUS
        "
      >
        <feather-icon icon="PlusIcon" class="mr-25" />
        <span>Add New</span>
      </b-button>
    </div>
    <b-row>
      <b-col md="4">
        <b-form-group label="Assessment" label-for="assessment">
          <validation-provider
            #default="{ errors }"
            name="Assessment"
            :rules="{ regex: /^[A-Z\s]*$/i }"
          >
            <b-form-input
              id="assessment"
              type="text"
              v-model="assessment"
              placeholder="Assessment"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            />
            <small class="text-danger">{{ errors[0] }}</small>
          </validation-provider>
        </b-form-group>
      </b-col>
      <b-col md="4">
        <b-form-group label="Recommendation" label-for="recommendation">
          <validation-provider
            #default="{ errors }"
            name="Recommendation"
            :rules="{ regex: /^[A-Z\s]*$/i }"
          >
            <b-form-input
              id="recommendation"
              type="text"
              v-model="recommendation"
              placeholder="Recommendation"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            />
            <small class="text-danger">{{ errors[0] }}</small>
          </validation-provider>
        </b-form-group>
      </b-col>
      <b-col md="4">
        <b-form-group label="Staff Comment" label-for="staffComment">
          <validation-provider
            #default="{ errors }"
            name="Staff Comment"
            :rules="{ regex: /^[A-Z\s]*$/i }"
          >
            <b-form-input
              id="staffComment"
              type="text"
              v-model="staffComment"
              placeholder="Staff Comment"
              :disabled="
                (petition && petition.status === petitionStatus.CLOSED) ||
                !type ||
                type.name === detailTypes.CIVILIAN ||
                type.name === detailTypes.ANONYMOUS
              "
            />
            <small class="text-danger">{{ errors[0] }}</small>
          </validation-provider>
        </b-form-group>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
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
      armyNo: "",
      name: "",
      course: "",
      parentUnit: "",
      unitComd: "",
      contactNo: "",
      cnic: "",
      isAlive: true,
      dateOfCommission: "",
      dateOfCommission: "",
      dateOfRetirement: "",
      causeOfRetirement: "",
      permanent: "",
      temporary: "",
      benefitPlots: [],
      nextTodoBenefitPlotsId: 2,
      feedbacks: [],
      nextTodoFeedbacksId: 2,
      family: [],
      nextTodoFamilyId: 2,
      property: [],
      nextTodoPropertyId: 2,
      commutation: "",
      pension: "",
      financialAssistanceFromArmy: "",
      ancestralHouse: "",
      ancestralLand: "",
      currentSourceOfIncome: "",
      assessment: "",
      recommendation: "",
      staffComment: "",
      rank: null,
      prefix: null,
      type: null,
      status: null,
    };
  },
  async mounted() {
    if (this.petition) {
      const detail = this.petition.detail;

      this.armyNo = detail.army_no;
      this.name = detail.name;
      this.course = detail.course;
      this.parentUnit = detail.parent_unit;
      this.unitComd = detail.unit_comd;
      this.contactNo = detail.contact_no;
      this.cnic = detail.cnic;
      this.isAlive = detail.is_alive;
      this.dateOfCommission = detail.date_of_commission;
      this.dateOfRetirement = detail.date_of_retirement;
      this.causeOfRetirement = detail.cause_of_retirement;
      this.permanent = detail.permanent_address;
      this.temporary = detail.temporary_address;
      this.commutation = detail.commutation;
      this.pension = detail.pension;
      this.financialAssistanceFromArmy = detail.financial_assistance_from_army;
      this.ancestralHouse = detail.ancestral_house;
      this.ancestralLand = detail.ancestral_land;
      this.currentSourceOfIncome = detail.current_source_of_income;
      this.assessment = detail.assessment;
      this.recommendation = detail.recommendation;
      this.staffComment = detail.staff_comment;

      this.benefitPlots = detail.benefits.map((benefit) => {
        return benefit;
      });
      this.feedbacks = detail.feedbacks.map((feedback) => {
        return feedback;
      });
      this.family = detail.family.map((fam) => {
        return {
          id: fam.id,
          name: fam.name,
          job: fam.job,
          age: fam.age,
          education: fam.education,
          isMarried: fam.is_married,
          isAlive: fam.is_alive,
          miscellaneous: fam.miscellaneous,
          employment: fam.employment,
          financialStatus: fam.financial_status,
          relation: {
            value: fam.relation,
            text: fam.relation,
          },
        };
      });
      this.property = detail.property.map((prop) => {
        return {
          id: prop.id,
          address: prop.address,
          type: {
            value: prop.type,
            text: prop.type,
          },
        };
      });

      if (this.benefitPlots.length > 0) {
        this.nextTodoBenefitPlotsId =
          this.benefitPlots[this.benefitPlots.length - 1].id;
      }

      if (this.feedbacks.length > 0) {
        this.nextTodoFeedbacksId = this.feedbacks[this.feedbacks.length - 1].id;
      }

      if (this.family.length > 0) {
        this.nextTodoFamilyId = this.family[this.family.length - 1].id;
      }

      if (this.property.length > 0) {
        this.nextTodoPropertyId = this.property[this.property.length - 1].id;
      }

      this.type = this.petition.detail.type_data;
      this.prefix = this.petition.detail.prefix_data;
      this.rank = this.petition.detail.rank_type_data;
      this.status = this.petition.detail.status_data;
    }
  },
  created() {
    window.addEventListener("resize", this.initTrHeight);
  },
  destroyed() {
    window.removeEventListener("resize", this.initTrHeight);
  },
  methods: {
    ...mapActions({
      getRankTypes: "appData/getRankTypes",
      getPrefixes: "appData/getPrefixes",
      getPetitionDetailTypes: "appData/getPetitionDetailTypes",
      getPetitionDetailStatuses: "appData/getPetitionDetailStatuses",
    }),
    repeateAgain(type) {
      if (type === 1) {
        this.benefitPlots.push({
          id: (this.nextTodoBenefitPlotsId += this.nextTodoBenefitPlotsId),
        });
      } else if (type === 2) {
        this.feedbacks.push({
          id: (this.nextTodoFeedbacksId += this.nextTodoFeedbacksId),
        });
      } else if (type === 3) {
        this.family.push({
          id: (this.nextTodoFamilyId += this.nextTodoFamilyId),
          isMarried: false,
          isAlive: true,
        });
      } else if (type === 4) {
        this.property.push({
          id: (this.nextTodoPropertyId += this.nextTodoPropertyId),
        });
      }
    },
    removeItem(index, type) {
      if (type === 1) {
        this.benefitPlots.splice(index, 1);
      } else if (type === 2) {
        this.feedbacks.splice(index, 1);
      } else if (type === 3) {
        this.family.splice(index, 1);
      } else if (type === 4) {
        this.property.splice(index, 1);
      }
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
