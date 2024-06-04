import axios from "axios";

const backend = axios.create({
  baseURL: "http://localhost:3001",
});

export default backend;