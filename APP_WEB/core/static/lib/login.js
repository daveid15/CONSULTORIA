import {object, string} from "yup";
import {formValidation, validation} from "./utils";
import {format} from "rutcl";

const schema = object().shape({
    rut: string().rut().required(),
    password: string().required(),
})


const schemaRestore = object().shape({
    email: string().email().required(),
})








document.querySelector("#loginForm")?.addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden'])")
    if (formValidation(schema, inputs))
        evt.currentTarget.submit()
})

document.querySelector("#loginForm")
    ?.querySelectorAll("input:not([type='hidden'])")
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

document.querySelector("#resetPasswordForm")?.addEventListener("submit", evt => {
    evt.preventDefault()
    let inputs = evt.target.querySelectorAll("input:not([type='hidden'])")
    if (formValidation(schemaRestore, inputs))
        evt.currentTarget.submit()
})


document.querySelector("#resetPasswordForm")
    ?.querySelectorAll("input:not([type='hidden'])")
    .forEach(input => {
        input.addEventListener("input", evt => {
            if (evt.target.id === "rut" || evt.target.id === "pymeRut")
                evt.target.value = format(evt.target.value, {dots: false})
            validation(schemaRestore, evt)
        })
        input.addEventListener("blur", evt => {
            if (evt.target.id === "rut" || evt.target.id === "pymeRut")
                evt.target.value = format(evt.target.value, {dots: false})
            validation(schemaRestore, evt)
        })
    })
