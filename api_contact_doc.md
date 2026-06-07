# Expense Sharing Service - Development Guidelines

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest

## Architecture

Use Feature-Based Architecture.

```text
app/
├── core/
│   ├── config.py
│   ├── database.py
│   └── dependencies.py
│
├── modules/
│   ├── users/
│   ├── groups/
│   ├── expenses/
│   ├── balances/
│   └── settlements/
│
└── main.py
```

Each module must contain:

- models.py
- schemas.py
- repository.py
- service.py
- router.py

## API Contracts

### User Module

#### Create User
POST /users

Request body:
```json
{
  "name": "Alice"
}
```
- `name`: string, required, min length 2, max length 100

Response body:
```json
{
  "user_id": "uuid-string",
  "name": "Alice",
  "created_at": "2026-06-07T10:00:00Z"
}
```
- Returns the newly created user record with generated `user_id` and timestamp

#### Get All Users
GET /users

Response body:
```json
[
  {
    "user_id": "uuid-1",
    "name": "Alice",
    "created_at": "2026-06-07T10:00:00Z"
  },
  {
    "user_id": "uuid-2",
    "name": "Bob",
    "created_at": "2026-06-07T10:01:00Z"
  }
]
```
- Returns a list of all user objects

#### Get User By ID
GET /users/{user_id}

Response body:
```json
{
  "user_id": "uuid-1",
  "name": "Alice",
  "created_at": "2026-06-07T10:00:00Z"
}
```
- Returns the single user record for the provided `user_id`

### Group Module

#### Create Group
POST /groups

Request body:
```json
{
  "name": "Goa Trip"
}
```
- `name`: string, required, min length 2, max length 100

Response body:
```json
{
  "group_id": "uuid-string",
  "name": "Goa Trip",
  "created_at": "2026-06-07T10:05:00Z"
}
```
- Returns created group metadata

#### Get All Groups
GET /groups

Response body:
```json
[
  {
    "group_id": "uuid-1",
    "name": "Goa Trip",
    "created_at": "2026-06-07T10:05:00Z"
  }
]
```
- Returns all groups

#### Get Group By ID
GET /groups/{group_id}

Response body:
```json
{
  "group_id": "uuid-1",
  "name": "Goa Trip",
  "created_at": "2026-06-07T10:05:00Z"
}
```
- Returns a single group record

#### Add Member To Group
POST /groups/{group_id}/members

Request body:
```json
{
  "user_ids": [
    "uuid-user-1",
    "uuid-user-2"
  ]
}
```
- `user_ids`: array of strings, each an existing user UUID

Response body:
```json
[
  {
    "id": 1,
    "group_id": "uuid-1",
    "user_id": "uuid-user-1",
    "joined_at": "2026-06-07T10:10:00Z"
  },
  {
    "id": 2,
    "group_id": "uuid-1",
    "user_id": "uuid-user-2",
    "joined_at": "2026-06-07T10:10:05Z"
  }
]
```
- Returns the list of new membership records created for the group

#### Get Group Members
GET /groups/{group_id}/members

Response body:
```json
[
  {
    "id": 1,
    "group_id": "uuid-1",
    "user_id": "uuid-user",
    "joined_at": "2026-06-07T10:10:00Z"
  }
]
```
- Returns all members currently in the group

### Expense Module

#### Create Expense
POST /expenses

Request body:
```json
{
  "group_id": "uuid-group",
  "paid_by": "uuid-user",
  "amount": 100.0,
  "description": "Dinner"
}
```
- `group_id`: string, group UUID
- `paid_by`: string, user UUID who paid
- `amount`: float, must be > 0
- `description`: string, required

Response body:
```json
{
  "expense_id": "uuid-expense",
  "group_id": "uuid-group",
  "paid_by": {
    "user_id": "uuid-user",
    "name": "Alice"
  },
  "amount": 100.0,
  "description": "Dinner",
  "created_at": "2026-06-07T10:15:00Z"
}
```
- Returns the created expense with payer details embedded in `paid_by`

#### Get Expense By ID
GET /expenses/{expense_id}

Response body:
```json
{
  "expense_id": "uuid-expense",
  "group_id": "uuid-group",
  "paid_by": {
    "user_id": "uuid-user",
    "name": "Alice"
  },
  "amount": 100.0,
  "description": "Dinner",
  "created_at": "2026-06-07T10:15:00Z"
}
```
- Returns details for a single expense

#### Get Group Expenses
GET /groups/{group_id}/expenses

Response body:
```json
[
  {
    "expense_id": "uuid-expense",
    "group_id": "uuid-group",
    "paid_by": {
      "user_id": "uuid-user",
      "name": "Alice"
    },
    "amount": 100.0,
    "description": "Dinner",
    "created_at": "2026-06-07T10:15:00Z"
  }
]
```
- Returns all expenses created for the group

### Balance Module

#### Get Group Balances
GET /groups/{group_id}/balances

Response body:
```json
[
  {
    "user_id": "uuid-user",
    "name": "Alice",
    "balance": 200.0
  },
  {
    "user_id": "uuid-other",
    "name": "Bob",
    "balance": -100.0
  }
]
```
- Returns net balance for each member in the group
- Positive balance means user should receive money
- Negative balance means user owes money

#### Get Pairwise Balances
GET /groups/{group_id}/balances/pairwise

Response body:
```json
{
  "Bob": {
    "owes": {
      "Alice": 100.0,
      "Charlie": 50.0
    }
  },
  "Charlie": {
    "owes": {
      "Alice": 25.0
    }
  }
}
```
- Returns explicit debts between users
- Each top-level key is a debtor name
- `owes` maps creditor names to amounts owed
- Useful for raw debt reporting before settlement

### Settlement Module

#### Get Settlement Suggestions
GET /groups/{group_id}/settlements

Response body:
```json
[
  {
    "from_user": {
      "user_id": "uuid-owing",
      "name": "Bob"
    },
    "to_user": {
      "user_id": "uuid-receiving",
      "name": "Alice"
    },
    "amount": 100.0
  }
]
```
- Returns a set of optimized transactions to settle all net balances
- `from_user` owes money and should pay `to_user`
- The algorithm minimizes the number of transfers required

## Database Design

### Users
- user_id (UUID)
- name
- created_at

### Groups
- group_id (UUID)
- name
- created_at

### Group Members
- id
- group_id
- user_id
- joined_at

### Expenses
- expense_id
- group_id
- paid_by
- amount
- description
- created_at

### Expense Shares
- id
- expense_id
- user_id
- share_amount

## Rules

- Amount must be greater than zero
- Group must exist
- User must exist
- Duplicate group membership not allowed
- Expense should be split equally among group members
- Payer should not owe themselves

## Architecture Rules

Router → Service → Repository

- Router handles HTTP requests
- Service contains business logic
- Repository contains database logic
- Models contain SQLAlchemy entities
- Schemas contain Pydantic DTOs
