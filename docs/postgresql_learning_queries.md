# PostgreSQL Learning Queries

These examples are for learning and inspection; application data access remains Django ORM through the REST API.

## JOIN
```sql
SELECT m.machine_code, c.client_name, ma.assigned_date
FROM machines_machineassignment ma
JOIN machines_machine m ON ma.machine_id = m.id
JOIN clients_client c ON ma.client_id = c.id
WHERE ma.assignment_status = 'ACTIVE';
```

## LEFT JOIN
```sql
SELECT c.client_name, COUNT(ma.id) AS assignment_count
FROM clients_client c LEFT JOIN machines_machineassignment ma ON ma.client_id = c.id
GROUP BY c.client_name;
```

## GROUP BY / HAVING
```sql
SELECT status, COUNT(*) FROM machines_machine GROUP BY status HAVING COUNT(*) > 1;
```

## Indexes and EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE SELECT * FROM machines_machine WHERE status = 'AVAILABLE';
```

## Transactions
```sql
BEGIN;
UPDATE inventory_inventoryitem SET current_quantity = current_quantity + 5 WHERE id = 1;
INSERT INTO inventory_inventorytransaction (inventory_item_id, transaction_type, quantity, transaction_date, remarks) VALUES (1, 'STOCK_IN', 5, CURRENT_DATE, 'Learning example');
COMMIT;
```
