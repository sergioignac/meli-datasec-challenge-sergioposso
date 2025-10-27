/*
solution_failures_report.sql
----------------------------
Genera un reporte de los clientes con mayor número de eventos fallidos 
(status = 'failure') dentro del sistema publicitario de HackerAd.

Objetivo:
- Identificar todos los clientes que presentan más de 3 eventos con estado 'failure'.
- Mostrar el nombre completo del cliente y el número total de fallos.

Comportamiento:
- Se realiza una unión entre las tablas customers, campaigns y events.
- Se filtran únicamente los registros cuyo status sea 'failure'.
- Se agrupan los resultados por cliente.
- Solo se muestran aquellos clientes con más de 3 fallos.
- El resultado se ordena por número de fallos (descendente) y nombre (ascendente).

Formato de salida:
customer | failures

Ejemplo:
Whitney Ferrero | 6
*/

SELECT 
CONCAT(c.first_name,' ',c.last_name) AS customer,
COUNT(e.status) AS failures
FROM customers c
JOIN campaigns ca
ON c.id = ca.customer_id
JOIN events e
ON ca.id = e.campaign_id
WHERE e.status = 'failure'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(e.status) > 3
ORDER BY failures DESC, customer ASC