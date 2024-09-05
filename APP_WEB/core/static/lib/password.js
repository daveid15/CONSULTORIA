import {object, string, ref} from "yup";
import * as Yup from "yup";
import {formValidation, inputListener} from "./utils";

const schema = object().shape({
    password: string().required(),
    confirmPassword: Yup.string().oneOf([ref("password")],"Contraseña no coincide").required('Required')
})

document.querySelector("#passwordForm").addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden'])")
    if (formValidation(schema, inputs))
        evt.currentTarget.submit()
})

document.querySelector("#passwordForm")
    .querySelectorAll("input:not([type='hidden'])")
    .forEach(input => {
        inputListener(input, schema)
    })
