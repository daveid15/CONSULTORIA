import {setServicesElements} from "./utils";

window.addEventListener("load", () => {
    const id = parseInt(new URL(window.location.href).pathname.match(/\d+/gm)[0]);
    setServicesElements(id);
})