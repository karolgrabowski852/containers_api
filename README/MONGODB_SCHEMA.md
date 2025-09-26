# MongoDB Database Schema

## Collections

### users
- **Document Example:**
```json
{
  "email": "user@example.com",
  "api_key": "hexstring",
  "global_bill": 0.0,
  "containers": ["container1", "container2"]
}
```

### containers
- **Document Example:**
```json
{
  "owner_email": "user@example.com",
  "name": "container1",
  "image": "ubuntu:latest",
  "status": "running", // or "stopped", "created"
  "last_billed": "2025-09-26T12:31:18.786+00:00",
  "settings": {
    "owner_email": "user@example.com",
    "cpu": 2.0,
    "memory": 4.0,
    "gpu": 1
  }
}
```

### billing_records
- **Document Example:**
```json
{
  "owner_email": "user@example.com",
  "container_name": "container1",
  "amount": 1.23,
  "timestamp": "2025-09-26T12:31:18.786+00:00"
}
```

### resources
- **Document Example:**
```json
{
  "id": 1,
  "cpu": 10.0,
  "memory": 10.0,
  "gpu": 2
}
```

## Notes

- `users.containers` is an array of container names owned by the user.
- `resources` collection is a singleton (id=1) representing the global resource pool.

