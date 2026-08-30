# Database Indexes

- Client codes, machine codes, serial numbers, and inventory item codes are unique lookup keys and indexed.
- Client name, city, machine model, machine status, inventory item name, category, and assignment status support the documented filters and searches.
- A conditional unique constraint guarantees one active assignment per machine.
- Timestamp ordering is handled by query ordering where needed; no broad, unused indexes are added.
