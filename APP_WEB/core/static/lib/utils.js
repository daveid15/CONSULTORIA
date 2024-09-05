import "regenerator-runtime"

import {addMethod, setLocale, string} from "yup";
import {format, validate} from "rutcl"

/**
 * El siguiente método se utiliza para agregar un nuevo tipo de validación a través de yup
 */
addMethod(string, "rut", function (args) {
    return this.test("test-rut", args, function (value) {
        const {path, createError} = this
        if (value === "")
            return true
        else
            return validate(value) || createError({path, message: args || "Rut Invalido"})
    })
})

setLocale({
    mixed: {
        default: "Campo Requerido",
        required: "Campo Requerido",
        notType: "Campo Requerido",
        notOneOf: "Campo Requerido",
    },
    number: {
        min: 'Debe ser mayor a ${min}',
        max: 'Debe ser menor a ${max}',
        moreThan: 'Debe ser un numero de 9 dígitos.',
        lessThan: 'Debe ser un numero de 9 dígitos.',
    },
    string: {
        max: 'No debe ser mayor a ${max} caracteres.',
        min: 'Debe ser mayor a ${min} caracteres.',
        email: 'Email invalido',
        matches: "Formato invalido"
    },
})

export const validation = (schema, evt) => {
    try {
        evt.target.id === "confirmPassword" || evt.target.id === "password" && evt.target.parentElement.parentElement.querySelector("#confirmPassword") ?
            schema.pick([evt.target.id]).validateSync({
                password: evt.target.parentElement.parentElement.querySelector("#password").value,
                [evt.target.id]: evt.target.type === "checkbox" ? evt.target.checked : evt.target.value
            }) :
            schema.pick([evt.target.id]).validateSync({
                [evt.target.id]: evt.target.type === "checkbox" ? evt.target.checked : evt.target.value
            })
        clearError(evt)
    } catch (err) {
        setError(evt, err)
    }
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

export const formValidation = (schema, inputs,) => {
    let valid = Array(inputs.length).fill(false)
    inputs.forEach((input, index) => {
        try {
            input.id === "confirmPassword" || input.id === "password" && input.parentElement.parentElement.querySelector("#confirmPassword") ?
                schema.pick([input.id]).validateSync({
                    password: input.parentElement.parentElement.querySelector("#password").value,
                    [input.id]: input.type === "checkbox" ? input.checked : input.value
                }) :
                schema.pick([input.id]).validateSync({
                    [input.id]: input.type === "checkbox" ? input.checked : input.value
                })
            valid[index] = true
            clearFormError(input)
        } catch (err) {
            valid[index] = false
            setFormError(input, err)
        }
    })
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    return valid.every(Boolean);
}

export const setError = (evt, err) => {
    evt.path[1].querySelector(".feedback").innerHTML = err.message
    evt.path[1].querySelector(".helper") ? evt.path[1].querySelector(".helper").style.display = "none" : null
}

export const clearError = (evt) => {
    evt.path[1].querySelector(".feedback").innerHTML = ""
    evt.path[1].querySelector(".helper") ? evt.path[1].querySelector(".helper").style.display = "block" : null
}

const setFormError = (input, err) => {
    input.parentElement.querySelector(".feedback").innerHTML = err.message
    input.parentElement.querySelector(".helper") ? input.parentElement.querySelector(".helper").style.display = "none" : null
}

const clearFormError = (input) => {
    input.parentElement.querySelector(".feedback").innerHTML = ""
    input.parentElement.querySelector(".helper") ? input.parentElement.querySelector(".helper").style.display = "block" : null
}

export const inputListener = (input, schema) => {
    input.addEventListener("input", evt => {
        if (evt.target.id === "rut" || evt.target.id === "pymeRut" && evt.target.value !== "-" && evt.target.value !== "")
            evt.target.value = format(evt.target.value, {dots: false})
        validation(schema, evt)
    })
    input.addEventListener("blur", evt => {
        if (evt.target.id === "rut" || evt.target.id === "pymeRut" && evt.target.value !== "-" && evt.target.value !== "")
            evt.target.value = format(evt.target.value, {dots: false})
        validation(schema, evt)
    })
}

// SERVICES

let url = 'http://www.finhelp.cl/rest';

let username = 'rest_2021';
let password = '#1#..jau.X__XHA19';
let encoded = window.btoa(username + ':' + password)
let auth = 'Basic ' + encoded;
let headers = new Headers();

headers.append("Accept", 'application/json');
headers.append("Authorization", auth);
headers.append("Content-Type", "application/json");

let service_count = document.getElementById('service-count');
let servicesDiv = document.getElementById('services');
let spinner = "<div class=\"mx-auto d-flex my-5\">\n" +
    "        <div class=\"spinner-border text-secondary mx-auto\" role=\"status\">\n" +
    "            <span class=\"visually-hidden\">Loading...</span>\n" +
    "        </div>\n" +
    "    </div>";

const formatter = new Intl.NumberFormat('es-CL', {
    style: "currency",
    currency: "CLP"
});

let page = 1;
let services;
let maxPage;

let selectedArea = '';

/**
 *
 * @param text {string}
 * @param id {int}
 * @returns {HTMLDivElement}
 */
export function createItemFilter(text, id) {
    let itemDiv = document.createElement("div");
    itemDiv.classList.add('item');
    itemDiv.setAttribute('id', `${text + '-' + id}`)
    let itemP = document.createElement("p");
    let itemPText = document.createTextNode(text);
    itemP.appendChild(itemPText)
    itemDiv.appendChild(itemP)

    itemDiv.addEventListener('click', async (evt) => {
        let element = evt.target
        page = 1;
        setLoader();
        let itemActive = document.getElementById('filters-menu').querySelector('.active');

        if (itemActive !== null) {
            itemActive.classList.remove('active')
        }
        element.classList.add('active')

        await setServicesElements(id);

    })

    return itemDiv
}

export async function setServicesElements(id) {
    services = await getServices(id);
    service_count.innerText = services.length === 1 ? `${services.length} asesoría` : `${services.length} asesorías`
    setPagination()
    setServiceCards()
}

export async function setAllServicesElements() {
    setLoader()
    services = await getAllServices();
    service_count.innerText = services.length === 1 ? `${services.length} asesoría` : `${services.length} asesorías`
    setPagination()
    setServiceCards()
}

/**
 * Renderiza los botones para cambiar de página si es que existen como mínimo 6 servicios
 */
function setPagination() {
    if (services.length > 6) {
        const pagination = document.querySelector("#service-pagination .pagination.pagination-table")

        maxPage = Math.ceil(services.length / 6)

        pagination.innerHTML =
            '<li class="page-item">\n' +
            '    <button class="page-link" onclick="previousPage()" aria-label="Previous">\n' +
            '        <span aria-hidden="true">&laquo;</span>\n' +
            '    </button>\n' +
            '</li>'

        for (let i = 1; i <= maxPage; i++) {
            if (i === 1)
                pagination.innerHTML += `<li class="page-item active"><button class="page-link">${i}</button></li>`
            else
                pagination.innerHTML += `<li class="page-item"><button class="page-link">${i}</button></li>`
        }

        pagination.innerHTML +=
            '<li class="page-item">\n' +
            '    <button class="page-link" onclick="nextPage()" aria-label="Next">\n' +
            '        <span aria-hidden="true">&raquo;</span>\n' +
            '    </button>\n' +
            '</li>'

        const buttons = document.querySelectorAll(".page-item:not(:first-child):not(:last-child)")

        buttons.forEach(pageItem => {
            pageItem.querySelector("button").addEventListener("click", evt => {
                document.querySelector(".page-item.active").classList.remove("active")
                evt.target.parentElement.classList.add("active")
                page = parseInt(evt.target.innerText)
                setServiceCards()
            })
        })
    } else {
        document.querySelector("#service-pagination .pagination.pagination-table").innerHTML = ""
    }
}

/**
 * Renderiza las cards de servicios de acuerdo al número de página en el que se encuentre
 */
function setServiceCards() {

    let start = (page - 1) * 6
    let end = start + 6

    servicesDiv.innerHTML = null

    services.slice(start, end).map((item, index) => {
        servicesDiv.innerHTML += ` <div class='col'>
        <div class='servicios-card cursor--pointer' data-bs-toggle="modal" data-bs-target=${"#" + item.service_name.replace(/ /g, "_").replace(/([()])/g, "_")}>
            <div class="${'servicios-card-body ' + getColor(index)}">
                <div class='badge-servicio my-2'>
                    <p>${item.area_name || selectedArea}</p>
                </div>
                <p class='body--large bold text-blue'>${item.service_name}</p>
                <p class='body--small text-blue'>${item.service_description}</p>
                <h4 class='h4 medium text-blue mt-auto'>${formatter.format(item.service_value) === '$0' ? 'Cotizar' : item.from ? `Desde ${formatter.format(item.service_value)}` : formatter.format(item.service_value)}</h4>
            </div>
            <div class='servicios-img-container d-none d-lg-flex'>
                <img src=${item.service_image || 'https://picsum.photos/800/800'} alt=""/>
            </div>
        </div>
    </div> 
    
    <div class="modal fade" id=${item.service_name.replace(/ /g, "_").replace(/([()])/g, "_")} tabindex="-1" aria-labelledby=${item.service_name.replace(/ /g, "_").replace(/([()])/g, "_") + "Label"} aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body">
                    <button type="button" class="modal-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    <div class="d-flex flex-column flex-lg-row">
                        <img class="img-fluid modal-image" src=${item.service_image || 'https://picsum.photos/300/400'} alt="service-image">
                        <div class="d-flex flex-column">
                            <h3 class="text-blue my-1--custom">${item.service_name}</h3>
                            <span class="body--small text-gray text-normal">${item.service_description}</span>
                            <span class="body--small text-blue mt-1--custom mb-0-5--custom">¿Cómo es el proceso?</span>
                            <ul class="body--small text-gray text-normal">
                                <li>Compra el servicio de tu interés</li>
                                <li>Crea tu cuenta</li>
                                <li>Paga el servicio seleccionado</li>
                                <li>Un asesor te contactará en el menor tiempo posible</li>
                                <li>Tu servicio será prestado por videoconferencia, sin necesidad de desplazamientos y
                                    reuniones
                                    en
                                    oficinas
                                </li>
                            </ul>
                            <h5 class="text-blue mt-0-5--custom mb-1--custom">${formatter.format(item.service_value) === '$0' ? 'Cotizar' : item.from ? `Desde ${formatter.format(item.service_value)}` : formatter.format(item.service_value)}</h5>
                            <div class="d-flex">
                                <a class="button" href="/purchase/${item.service_id}/">Comenzar asesoría</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`
    })
}

function nextPage() {
    if (page < maxPage) {
        page++;
        const element = document.querySelector(".page-item.active")
        element.classList.remove("active")
        element.nextElementSibling.classList.add("active")
        setServiceCards()
    }
}

function previousPage() {
    if (page > 1) {
        page--;
        const element = document.querySelector(".page-item.active")
        element.classList.remove("active")
        element.previousElementSibling.classList.add("active")
        setServiceCards()
    }
}

export function getLabelAreas() {
    return fetch(`${url}/area_all/`, {
        method: 'GET',
        headers,
        credentials: "omit"
    }).then(res => {
        if (res.status !== 200) {
            throw Error
        }
        return res.json();
    }).then(data => {
        return data.data
    }).catch(() => {
    })
}

function getServices(id) {
    return fetch(`${url}/area_service/`, {
        method: 'POST',
        body: JSON.stringify({
            "area_id": id
        }),
        headers,
        credentials: "omit"
    }).then(res => {
        if (res.status !== 200) {
            throw Error
        }
        return res.json();
    }).then(data => {
        selectedArea = Object.keys(data.data)[0];
        return data.data[Object.keys(data.data)[0]]
    }).catch(() => {
    })
}

function getAllServices() {
    return fetch(`${url}/service_all`, {
        method: 'GET',
        headers,
        credentials: "omit"
    }).then(res => {
        if (res.status !== 200) {
            throw Error
        }
        return res.json();
    }).then(data => {
        return data.data
    }).catch(() => {
    })
}

function getColor(index) {
    if (index % 2 === 0) {
        return 'bg-light-yellow'
    } else if (index % 3 === 0) {
        return 'bg-light-green';
    } else if (index % 5 === 0) {
        return 'bg-orange';
    } else {
        return 'bg-green'
    }
}

function setLoader() {
    servicesDiv.innerHTML = spinner;
}