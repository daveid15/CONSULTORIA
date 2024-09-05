import {boolean, object, string, date} from "yup";
import {formValidation, validation} from "./utils";
import {format} from "rutcl";

const personalDataTab = new bootstrap.Tab(document.querySelector("#pymeTab #personalData-tab"))
const pymeDataTab = new bootstrap.Tab(document.querySelector("#pymeTab #pymeData-tab"))

let schema = object().shape({
    email: string().email().required(),
    phone: string().required().matches(/^[+0-9]{8,12}$/),
    name: string().required(),
    lastName: string().required(),
    rut: string().rut().required(),
    address: string().required(),
    birthday: date(),
    profession: string(),
    pymeName: string().required(),
    pymeRut: string().rut().required(),
    pymeAddress: string().required(),
    pymeActivity: string().required(),
    pymeEmail: string().email().required(),
    pymePhone: string().required().matches(/^[+0-9]{8,12}$/),
    pymeWebPage: string(),
    legalRepresentative: boolean().oneOf([true, false], "Elija una opción"),
    termsAndConditions: boolean().oneOf([true], "Los términos y condiciones deben ser aceptados para continuar"),
})

const validationLimit = {
    personalDataContinue: 8,
    pymeDataContinue: 17
}

const validationCallback = {
    personalDataContinue: () => {
        pymeDataTab.show();
    },
    pymeDataContinue: (evt) => {
        evt.currentTarget.submit()
    }
}

document.querySelector("#pymeForm").addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden'])")
    inputs = Array.from(inputs).slice(0, validationLimit[evt.submitter.id])
    if (formValidation(schema, inputs))
        validationCallback[evt.submitter.id](evt)
})

document.querySelector("#pymeForm")
    .querySelectorAll("input:not([type='hidden'])")
    .forEach(input => {
        input.addEventListener("input", evt => {
            if (evt.target.id === "rut" || evt.target.id === "pymeRut")
                evt.target.value = format(evt.target.value, {dots: false})
            validation(schema, evt)
        })
        input.addEventListener("blur", evt => {
            if (evt.target.id === "rut" || evt.target.id === "pymeRut")
                evt.target.value = format(evt.target.value, {dots: false})
            validation(schema, evt)
        })
    })

document.querySelector("#pymeDataBack").addEventListener("click", () => {
    personalDataTab.show();
})