export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn;
  },

  loggedInUser(state) {
    return state.auth.user;
  }
};

export const state = () => ({
  busy: false,
  loggedIn: false,
  strategy: "local",
  user: false
});
