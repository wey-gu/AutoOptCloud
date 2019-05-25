const DEBUG = false;
let backendURL = "http://localhost:5000";
if (!DEBUG) {
  backendURL = "https://cloud-opt.siwei.info:5000";
}

export default {
  backendURL: backendURL
};
