import api from "./api"; // your axios instance

export const fetchAllJDs = () => {
  return api.get("/jd/all");
};
