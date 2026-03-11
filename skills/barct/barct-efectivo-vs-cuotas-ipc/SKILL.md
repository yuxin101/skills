---
name: barct-efectivo-vs-cuotas-ipc
description: Evaluar conveniencia de pago entre efectivo con descuento, cuotas (con o sin recargo) y tarjeta a fin de mes, incluyendo inflación oficial de Argentina (IPC) para comparar costo nominal y financiero.
---

# Skill: Evaluación de conveniencia de compra (efectivo vs cuotas vs tarjeta a fin de mes)

## Objetivo

Este skill ayuda a determinar qué opción de pago conviene más desde el punto de vista económico entre:

1. **Pago en efectivo con descuento**
2. **Pago en cuotas sin descuento**
3. **Pago en cuotas con recargo**
4. **Un solo pago a fin de mes con tarjeta, sin descuento**

La respuesta debe ser clara, numérica y explicativa, indicando:

- cuál opción tiene **menor costo nominal total**,
- cuál opción tiene **mejor conveniencia financiera**, considerando el valor del dinero en el tiempo,
- y cómo impacta la **inflación oficial reciente**, obtenida automáticamente desde la API oficial.

---

## Cuándo usar este skill

Usar este skill cuando el usuario consulte si conviene una compra en distintas modalidades de pago, por ejemplo:

- “¿Me conviene pagar en efectivo con 15% de descuento o en 6 cuotas sin interés?”
- “Si en efectivo me hacen descuento pero con tarjeta va al resumen de fin de mes, ¿qué me conviene?”
- “Comparame contado contra 12 cuotas con recargo.”
- “¿Conviene 1 pago con tarjeta sin descuento o efectivo con descuento?”

---

## Entradas esperadas

El skill debe intentar obtener o inferir los siguientes datos:

- **precio_lista**: precio base del producto o servicio
- **descuento_efectivo_pct**: porcentaje de descuento por pago en efectivo (si existe)
- **cantidad_cuotas**: número de cuotas
- **recargo_pct**: porcentaje de recargo total sobre precio de lista para pago en cuotas (si existe)
- **pago_fin_mes**: si la tarjeta permite pagar en un solo pago al cierre o vencimiento del resumen
- **dias_hasta_pago**: días estimados hasta el pago real si se difiere al resumen
- **tasa_oportunidad_mensual**: rendimiento mensual alternativo del dinero o costo financiero de oportunidad
- **usar_ipc_oficial**: debe asumirse como `true` por defecto para consultar IPC oficial reciente mediante API

Si faltan datos, el skill debe trabajar con lo disponible y explicitar los supuestos. La inflación no debe pedirse al usuario: debe obtenerse desde la API oficial, salvo falla de la API.

---

## Supuestos de cálculo

### 1. Efectivo con descuento

Calcular:

`precio_efectivo = precio_lista × (1 - descuento_efectivo_pct / 100)`

### 2. Cuotas sin descuento

Si no hay recargo:

`total_cuotas = precio_lista`

`valor_cuota = total_cuotas / cantidad_cuotas`

### 3. Cuotas con recargo

Si hay recargo:

`total_cuotas = precio_lista × (1 + recargo_pct / 100)`

`valor_cuota = total_cuotas / cantidad_cuotas`

### 4. Tarjeta en un pago a fin de mes

Si no hay descuento ni recargo:

`total_tarjeta_1pago = precio_lista`

Opcionalmente, puede calcularse el beneficio financiero del diferimiento del pago.

---

## Criterio de análisis

El skill debe analizar la conveniencia en **tres niveles**:

### A. Comparación nominal simple

Comparar cuánto se paga en total en cada opción, sin considerar el tiempo.

- La opción con menor total nominal es la más barata en términos absolutos.

### B. Comparación financiera

Si hay cuotas o pago diferido, descontar los pagos futuros a valor presente usando una tasa mensual de oportunidad.

#### Valor presente de cuotas

Para cada cuota:

`VP = cuota / (1 + tasa_mensual) ^ n`

Donde `n` es el número de períodos hasta cada pago.

La suma de todos los valores presentes da el **costo financiero real hoy** de la alternativa en cuotas.

#### Valor presente de pago a fin de mes

Si el pago ocurre dentro de cierto número de días:

`VP_tarjeta = precio_lista / (1 + tasa_mensual) ^ (dias_hasta_pago / 30)`

Esto permite medir si perder el descuento se compensa por conservar el dinero más tiempo.

### C. Comparación contra inflación

El skill debe contrastar la conveniencia de financiarse contra la evolución reciente del IPC nacional.

#### Objetivo

Determinar si el costo de pagar en cuotas o diferir el pago queda por debajo, cerca o por encima de la inflación reciente, lo cual ayuda a interpretar si la financiación “licúa” el precio en términos reales.

#### Fuente oficial

Serie a consultar:

- `145.3_INGNACNAL_DICI_M_15` — IPC nivel general nacional

API base:

- `https://apis.datos.gob.ar/series/api/series`

Consulta requerida:

- `https://apis.datos.gob.ar/series/api/series/?ids=145.3_INGNACNAL_DICI_M_15`

#### Reglas de procesamiento del IPC

1. Hacer una request GET a la URL indicada.
2. Verificar que la respuesta tenga la clave `data`.
3. Verificar que `data` tenga al menos un registro.
4. Interpretar cada fila de `data` con el formato:
   - `[fecha, valor]`
   - donde `fecha` es ISO, por ejemplo `2025-12-01`
5. Transformar la respuesta a una estructura clara con campos:
   - `date`
   - `value`
6. Ordenar los resultados de más reciente a más antigua.
7. Si no hay datos, informar un error claro y mostrar la URL consultada.
8. No inventar valores ni fechas.

#### Uso del IPC en el análisis

Con los últimos 12 valores disponibles, el skill puede:

- mostrar la inflación mensual reciente,
- tomar el último dato como referencia de inflación mensual,
- calcular una inflación acumulada estimada para el plazo de las cuotas,
- comparar esa inflación acumulada con:
  - el descuento perdido por no pagar en efectivo,
  - el recargo total de la financiación,
  - el costo implícito de pagar más adelante.

#### Criterio interpretativo frente al IPC

- Si el **recargo total** de las cuotas es menor que la **inflación acumulada esperable** del período, la financiación puede resultar razonable en términos reales.
- Si el recargo supera claramente la inflación acumulada del período, el plan en cuotas pierde atractivo real.
- Si las cuotas son sin interés o sin recargo significativo y la inflación sigue siendo positiva, normalmente las cuotas mejoran en términos reales, salvo que el descuento por efectivo sea muy alto.

---

## Regla de decisión

El skill debe responder siguiendo esta lógica:

1. **Identificar la opción más barata nominalmente**.
2. **Calcular valor presente** de las alternativas diferidas si hay tasa disponible o puede inferirse una tasa razonable.
3. **Consultar IPC oficial** desde la API indicada y procesar la serie reciente.
4. **Comparar el ahorro por descuento** contra el **beneficio financiero de pagar más tarde** y contra la **inflación reciente/acumulada**.
5. Indicar una conclusión en lenguaje simple:
   - “Conviene efectivo”
   - “Convienen las cuotas”
   - “Conviene un pago a fin de mes”
   - “Nominalmente conviene una, pero financieramente la diferencia es marginal”

---

## Reglas de interpretación

### Conviene efectivo cuando:

- el descuento es alto,
- el pago en cuotas tiene recargo considerable,
- el beneficio de conservar el dinero no compensa el descuento perdido,
- o el recargo supera con claridad la inflación esperada para el período.

### Convienen las cuotas cuando:

- son sin interés real,
- la tasa de oportunidad o inflación esperada es significativa,
- el valor presente de las cuotas resulta menor que el precio de contado con descuento o suficientemente cercano,
- o el recargo es menor que la inflación acumulada estimada para el plazo financiado.

### Puede convenir un pago a fin de mes cuando:

- no hay cuotas,
- se pierde el descuento por efectivo,
- pero el diferimiento de 20–40 días permite conservar liquidez,
- y el descuento perdido es bajo.

### Comparación con inflación

El skill debe decir expresamente si:

- la alternativa financiada **gana contra la inflación**,
- **empata aproximadamente con la inflación**,
- o **pierde contra la inflación**.

Esto debe expresarse en lenguaje simple, por ejemplo:

> Aunque nominalmente pagás más, el recargo total queda por debajo de la inflación acumulada estimada para el período, así que financieramente las cuotas no lucen malas en términos reales.

---

## Formato de respuesta esperado

La respuesta debe incluir:

### 1. Resumen breve

Una frase inicial con la recomendación principal.

Ejemplo:

> Te conviene pagar en efectivo, porque aun considerando el beneficio de diferir el pago, el descuento del 15% supera ampliamente la ventaja financiera de pagar más adelante.

### 2. Desglose numérico

- Precio de lista
- Precio en efectivo
- Total en cuotas
- Valor de cada cuota
- Total en tarjeta 1 pago
- Valor presente estimado de cada alternativa, si corresponde
- Últimos datos de IPC procesados, si se usó la API oficial
- Inflación acumulada estimada para el plazo analizado, si corresponde

### 3. Conclusión interpretativa

Explicar por qué conviene una opción y en qué contexto podría elegirse otra por liquidez.

---

## Manejo de faltantes

Si faltan datos, el skill debe:

- pedir el dato faltante si es indispensable,
- o hacer una estimación razonable y explicitarla.

Ejemplo:

> Como no indicaste tasa de oportunidad, hago una comparación nominal. Si querés, también puedo recalcularlo suponiendo, por ejemplo, una tasa mensual del 3% o del 5%.

Si la consulta al IPC oficial falla o no devuelve datos válidos, el skill debe decirlo claramente. No debe pedirle al usuario que informe la inflación manualmente.

Ejemplo:

> No pude obtener datos válidos de IPC desde la API oficial. URL consultada: `https://apis.datos.gob.ar/series/api/series?ids=145.3_INGNACNAL_DICI_M_15&last=12&format=json&metadata=simple`

En ese caso, no debe inventar inflación ni usar fechas supuestas.

---

## Ejemplo de entrada

```json
{
  "precio_lista": 1200000,
  "descuento_efectivo_pct": 15,
  "cantidad_cuotas": 6,
  "recargo_pct": 0,
  "pago_fin_mes": true,
  "dias_hasta_pago": 25,
  "tasa_oportunidad_mensual": 0.04
}
```

## Ejemplo de salida

Te conviene pagar en efectivo si tenés disponible el dinero.

El precio de lista es $1.200.000 y en efectivo con 15% de descuento pagarías $1.020.000.
En 6 cuotas sin recargo pagarías $1.200.000 en total, es decir $200.000 por mes.
Aun descontando financieramente esas cuotas con una tasa del 4% mensual, el valor presente sigue siendo mayor que el pago en efectivo.
Además, al contrastarlo con el IPC oficial reciente, la licuación inflacionaria no alcanza a compensar perder un descuento del 15%.
El pago a fin de mes en una sola cuota mejora un poco la conveniencia frente al pago inmediato, pero no alcanza para compensar perder un descuento del 15%.

Conclusión: económicamente conviene efectivo; solo elegiría cuotas o pago a fin de mes si priorizás liquidez.

---

## Restricciones

- No asumir que “cuotas sin interés” siempre convienen.
- No asumir que “efectivo con descuento” siempre conviene.
- Explicar siempre el criterio usado.
- Si la diferencia es chica, decirlo explícitamente.
- Si hay incertidumbre por falta de tasa, aclararlo.
- No pedir al usuario un valor de inflación manual cuando la API oficial esté disponible.
- La referencia de inflación debe salir de la API oficial indicada.

---

## Extensión opcional

El skill puede ampliarse para calcular:

- tasa implícita de financiación,
- costo financiero total equivalente,
- comparación contra rendimiento de plazo fijo o fondo money market,
- sensibilidad con distintos escenarios de tasa mensual,
- tabla de IPC reciente procesada automáticamente desde la API oficial.

---

## Procedimiento técnico para obtener IPC oficial

El skill debe seguir este procedimiento exacto para obtener IPC oficial en cada análisis:

### Endpoint

`https://apis.datos.gob.ar/series/api/series?ids=145.3_INGNACNAL_DICI_M_15&last=12&format=json&metadata=simple`

### Método

- `GET`
- sin autenticación

### Validaciones

1. Confirmar que la respuesta sea JSON válido.
2. Confirmar que exista la clave `data`.
3. Confirmar que `data` no esté vacía.
4. Confirmar que cada elemento tenga:
   - una fecha ISO,
   - un valor numérico.

### Transformación esperada

Transformar cada fila:

```json
["2025-12-01", 2.7]
```

a:

```json
{
  "date": "2025-12-01",
  "value": 2.7
}
```

### Orden

Ordenar desde la fecha más reciente hacia la más antigua.

### Manejo de error

Si no hay datos, responder con un error claro, por ejemplo:

`Error al obtener IPC oficial: la API no devolvió datos en data. URL consultada: https://apis.datos.gob.ar/series/api/series?ids=145.3_INGNACNAL_DICI_M_15&last=12&format=json&metadata=simple`

### Restricción crítica

- No inventar valores.
- No inventar fechas.
- No asumir IPC si la API no respondió correctamente.

---

Si querés, te lo convierto en una versión más corta y más ejecutable para usar como skill real.