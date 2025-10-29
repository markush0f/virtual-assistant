import { contextBridge } from "electron";

contextBridge.exposeInMainWorld("api", {
  // Here we will later expose functions that talk to Python
});