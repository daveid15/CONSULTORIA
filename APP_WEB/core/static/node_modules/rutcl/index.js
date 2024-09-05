"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDigit = exports.format = exports.validate = exports.clean = void 0;
function clean(rut) {
    rut = rut.toString();
    return rut.replace(/^0+|[^0-9kK]+/g, '').toUpperCase();
}
exports.clean = clean;
function validate(rut) {
    rut = rut.toString();
    if (/^0+/.test(rut) || rut.startsWith("0")) {
        return false;
    }
    if (!/^0*(\d{1,3}(\.?\d{3})*)-?([\dkK])$/.test(rut)) {
        return false;
    }
    rut = clean(rut);
    let t = parseInt(rut.slice(0, -1), 10);
    let m = 0;
    let s = 1;
    while (t > 0) {
        s = (s + (t % 10) * (9 - m++ % 6)) % 11;
        t = Math.floor(t / 10);
    }
    let v = s > 0 ? '' + (s - 1) : 'K';
    return v === rut.slice(-1);
}
exports.validate = validate;
function format(rut, options = {
    dots: true
}) {
    rut = clean(rut);
    let result;
    if (options.dots) {
        result = rut.slice(-4, -1) + '-' + rut.substr(rut.length - 1);
        for (let i = 4; i < rut.length; i += 3) {
            result = rut.slice(-3 - i, -i) + '.' + result;
        }
    }
    else {
        result = rut.slice(0, -1) + '-' + rut.substr(rut.length - 1);
    }
    return result;
}
exports.format = format;
function getDigit(rut) {
    rut = clean(rut);
    // type check
    if (!rut || !rut.length) {
        return;
    }
    // serie numérica
    let secuencia = [2, 3, 4, 5, 6, 7, 2, 3];
    let sum = 0;
    //
    for (let i = rut.length - 1; i >= 0; i--) {
        let d = rut.charAt(i);
        sum += Number(d) * secuencia[rut.length - (i + 1)];
    }
    // sum mod 11
    let rest = 11 - (sum % 11);
    // si es 11, retorna 0, sino si es 10 retorna K,
    // en caso contrario retorna el numero
    return rest === 11 ? "0" : rest === 10 ? "K" : rest.toString();
}
exports.getDigit = getDigit;
