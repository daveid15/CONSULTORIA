import {boolean, number, object, string} from "yup";
import {formValidation, validation} from "./utils";
import {format} from "rutcl";

const dataTab = new bootstrap.Tab(document.querySelector("#onBoardingTab #data-tab"))
const recommendationsTab = new bootstrap.Tab(document.querySelector("#onBoardingTab #recommendations-tab"))
const documentsTab = new bootstrap.Tab(document.querySelector("#onBoardingTab #documents-tab"))

let schema = object().shape({
    name: string().required(),
    lastName: string().required(),
    rut: string().rut().required(),
    email: string().email().required(),
    phone: string().required().matches(/^[+0-9]{8,12}$/),
    specialty: string().notOneOf(["-1"]),
    subSpecialty: string().notOneOf(["-1"]),
    title: string().required(),
    institution: string().required(),
    mention: string().required(),
    year: number().max(new Date().getFullYear(), "Año invalido").min(1900, "Año invalido"),
    registerCode: string().required(),
    companyName: string(),
    position: string(),
    contactName: string(),
    contactPosition: string(),
    contactEmail: string().email(),
    contactPhone: string().matches(/^[+0-9]{8,12}$/, {excludeEmptyString: true}),
    presentation: string().required(),
    curriculum: string().required(),
    professionalCertificate: string().required(),
    identityCard: string().required(),
    judicialRecord: string().required(),
    avatar: string().required(),
    termsAndConditions: boolean().oneOf([true], "Los términos y condiciones deben ser aceptados para continuar"),
})

 let validationLimit = {
     dataContinue: 12,
     recommendationsContinue: 18,
     DocumentsContinue: 25
}


const validationCallback = {
    dataContinue: () => {
        recommendationsTab.show()
    },
    recommendationsContinue: () => {
        documentsTab.show()
    },
    documentsContinue: (evt) => {
        evt.currentTarget.submit()
    }
}

const form = document.querySelector("#onBoardingForm")

form.addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden']), textarea:not([type='hidden']), select")
    inputs = Array.from(inputs).slice(0, validationLimit[evt.submitter.id])
    if (formValidation(schema, inputs)) {
        validationCallback[evt.submitter.id](evt)
    }
})

const inputs = document.querySelector("#onBoardingForm").querySelectorAll("input:not([type='hidden']), textarea:not([type='hidden']), select")

inputs.forEach(input => {
    input.addEventListener("input", evt => {
        if (evt.target.id === "rut")
            evt.target.value = format(evt.target.value, {dots: false})
        if (evt.target.type === "file")
            evt.path[1].querySelector(".file-name").innerHTML = evt.target.files[0].name ?? ""
        validation(schema, evt)
    })
    input.addEventListener("blur", evt => {
        if (evt.target.id === "rut")
            evt.target.value = format(evt.target.value, {dots: false})
        validation(schema, evt)
    })
})

const recommendationsBack = document.querySelector("#recommendationsBack")
const documentsBack = document.querySelector("#documentsBack")

recommendationsBack.addEventListener("click", () => {
    dataTab.show()
})

documentsBack.addEventListener("click", () => {
    recommendationsTab.show()
})