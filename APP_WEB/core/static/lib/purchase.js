import {boolean, object, string} from "yup";
import {formValidation} from "./utils";

let schema = object().shape({
    description: string().required(),
    name: string().required(),
    lastName: string().required(),
    rut: string().rut().required(),
    email: string().email().required(),
    phone: string().required().matches(/^[+0-9]{8,12}$/),
    pymeName: string(),
    pymeRut: string().rut().notRequired(),
    pymeAddress: string(),
    pymeActivity: string(),
    termsAndConditions: boolean().oneOf([true], "Los términos y condiciones y Políticas de privacidad deben ser aceptados para continuar")
})

document.querySelector("#purchaseForm").addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden']):not([type='radio']), textarea:not([type='hidden'])")
    if (formValidation(schema, inputs))
        evt.currentTarget.submit()
})

document.querySelector("#purchaseForm").addEventListener("submit", evt => {
    evt.preventDefault()
    console.log(evt.target.querySelectorAll("input:not([type='hidden']):not([type='radio']), textarea:not([type='hidden'])"))
})

