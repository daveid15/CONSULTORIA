import {object, string} from "yup";
import {formValidation, inputListener} from "./utils";

const schema = object().shape({
    name: string().required(),
    lastName: string().required(),
    rut: string().rut().required(),
    email: string().email().required(),
    phone: string().required().matches(/^[+0-9]{8,12}$/),
    pymeName: string(),
    pymeRut: string().rut().notRequired(),
    pymeAddress: string(),
    pymeActivity: string(),
})

document.querySelector("#pymeAccountForm").addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden'])")
    if (formValidation(schema, inputs))
        evt.currentTarget.submit()
})

document.querySelector("#pymeAccountForm")
    .querySelectorAll("input:not([type='hidden'])")
    .forEach(input => {
        inputListener(input, schema)
    })