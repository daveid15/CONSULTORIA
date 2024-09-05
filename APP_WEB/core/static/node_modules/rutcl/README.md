# rutcl

Package para validar, limpiar, obtener dígito verificador y dar formato al RUT

## Funciones

`clean(rut: string)` Se envía un rut de tipo string y retorna el rut sin puntos ni guion.

`validate(rut: string)` Se envía un rut de tipo string y retorna si el rut es válido o no (true or false).

`format(rut: string, {dots: boolean})` Se envía un rut de tipo string, además de un campo `dots` opcional (default `true`). En caso de no
enviar `dots`, retorna el rut con puntos y guion. En caso contrario, se define `dots` como `false` y retorna el rut solo con guion.

`getDigit(rut: string)` Se envía un rut sin dígito verificador de tipo string y retorna digito verificador correspondiente al rut ingresado.

---

```js
const { validate, clean, format, getDigit } = require('rut.js')

/**
 * Validar un RUT
 */

// true
validate('20.288.020-7')
validate('20288020-7')
validate('202880207')
validate('19.670.978-9')
validate('19670978-9')
validate('196709789')

// false
validate('20.288.020-0')
validate('20,288,020-7')
validate('20*288*020-7')
validate('20-288-020-7')
validate('error20.288.020-7')
validate('19670978-1')
validate('')
validate('0')
validate(0)

/**
 * Limpiar un RUT
 */

clean('202880207')      // '202880207'
clean('20.288.020-7')   // '202880207'
clean('19.670.978-1')   // '196709789'
clean('19*670*978-9')   // '196709789'
clean('000202880207')   // '202880207'

/**
 * Dar formato a un RUT
 */

format('20.288.020-7')  // '20.288.020-7'
format('20288020-7')     // '20.288.020-7'
format('19.670.978-9')  // '19.670.978-9'
format('196709789')     // '19.670.978-9'
format('20.288.020-7',{dots: false})  // '20288020-7'
format('20288020-7',{dots: false})     // '20288020-7'
format('19.670.978-9',{dots: false})  // '19670978-9'
format('196709789',{dots: false})     // '19670978-9'

/**
 * Obtener el dígito verificador de un RUT
 */

getDigit('20.288.020') // '7'
getDigit('20288020') // '7'
getDigit('20288020') // '7'
getDigit('19.670.978') // '9'
getDigit('19670978') // '9'
getDigit('19670978') // '9'
```

## Instalación

```bash
npm install --save rutcl
```

## Testing

```bash
npm install
npm test
```
