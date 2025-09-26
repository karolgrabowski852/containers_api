# API Endpoints Specification

## Users

### Create User
- **POST** `/users/`
- **Body:** `email: str`
- **Response:** `User` object

### Get Current User
- **GET** `/users/`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `UserPublic` object

### Delete User
- **DELETE** `/users/`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `str` (success message)

### Get Current Bill
- **GET** `/users/current_bill`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `float` (current bill)

### Paycheck
- **PUT** `/users/paycheck`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `float` (bill after payment)

## Containers

### Get Container
- **GET** `/containers/{name}`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `Container` object

### Create Container
- **POST** `/containers/`
- **Body:**
  - `name: str`
  - `image: str`
  - `cpu: float`
  - `memory: float`
  - `gpu: int`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `UserPublic` object

### Run Container
- **PUT** `/containers/{name}/run`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `Container` object

### Stop Container
- **PUT** `/containers/{name}/stop`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `Container` object

### Delete Container
- **DELETE** `/containers/{name}`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `{ "message": "Container deleted successfully" }`

## Resources

### Get Resources
- **GET** `/resources`
- **Headers:** `X-API-Key`, `X-User-Email`
- **Response:** `dict` (resource pool status)

## Health

### Health Check
- **GET** `/health`
- **Response:** `UserPublic` object

---

**Note:** All endpoints requiring authentication expect `X-API-Key` and `X-User-Email` headers.
