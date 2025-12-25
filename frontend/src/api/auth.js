import api from "./api";

export const signupUser = (data) => {
  return api.post("/auth/signup", data);
};

export const loginUser = (data) => {
  return api.post("/auth/login", data);
};
