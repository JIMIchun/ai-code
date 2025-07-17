import { createStore } from 'vuex';

export default createStore({
  state: {
    userInfo: {},
    selectPatientId: '',
    selectPatientInfo: {},
    patientsList: [],
    accountList: [],
    sessionList: [],
    selectSessionId: null,
    casesTimeline: [],
  },
  mutations: {
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo;
    },
    SET_SELECT_PATIENT_ID(state, selectPatientId) {
      state.selectPatientId = selectPatientId;
    },
    SET_SELECT_PATIENT_INFO(state, selectPatientInfo) {
      state.selectPatientInfo = selectPatientInfo;
    },
    SET_PATIENTS_LIST(state, patientsList) {
      state.patientsList = patientsList;
    },
    SET_ACCOUNT_LIST(state, accountList) {
      state.accountList = accountList;
    },
    SET_SESSION_LIST(state, sessionList) {
      state.sessionList = sessionList;
    },
    SET_SELECT_SESSION_ID(state, selectSessionId) {
      state.selectSessionId = selectSessionId;
    },
    SET_CASES_TIMELINE(state, casesTimeline) {
      state.casesTimeline = casesTimeline;
    },
  },
  actions: {
    async getUserInfo({ commit, rootState }) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await rootState.proxy.$axios.get('/user_info');
        commit('SET_USER_INFO', response.data);
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    async queryPatientsByUserId({ commit, rootState }) {
      const response = await rootState.proxy.$axios.get('/get_patients_by_user');
      commit('SET_PATIENTS_LIST', response.data);
    },
    async queryAllPatientData({ commit, rootState }) {
      const response = await rootState.proxy.$axios.get('/patients');
      commit('SET_ACCOUNT_LIST', response.data);
      commit('SET_SELECT_PATIENT_ID', response.data[0].patient_id);
    },
    async querysessionList({ commit, rootState, state }, isInit = true) {
      const patientId = state.selectPatientId;
      const response = await rootState.proxy.$axios.get(`/get_sessions/${patientId}`);
      if (response.status === 200) {
        commit('SET_SESSION_LIST', response.data);
        if (isInit) {
          commit('SET_SELECT_SESSION_ID', response.data[0].session_id);
        }
      }
    },
    async queryPatientTimeline({ commit, rootState, state }) {
      const patientId = state.selectPatientId;
      const response = await rootState.proxy.$axios.get(`/cases_by_patient/${patientId}`);
      commit('SET_CASES_TIMELINE', response.data);
    },
  },
  getters: {
    userInfo: state => state.userInfo,
    selectPatientId: state => state.selectPatientId,
    selectPatientInfo: state => state.selectPatientInfo,
    patientsList: state => state.patientsList,
    accountList: state => state.accountList,
    sessionList: state => state.sessionList,
    selectSessionId: state => state.selectSessionId,
    casesTimeline: state => state.casesTimeline,
  },
});
