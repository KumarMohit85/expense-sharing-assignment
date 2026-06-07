# Expense Sharing Service

A simple expense-sharing API built with FastAPI. The idea is to track expenses within a group and suggest who should pay whom to settle up. It's like Splitwise but simpler and meant for learning.

## Quick Start

### Without Docker

1. Clone the repo
   ```bash
   git clone <repo-url>
   cd expense-sharing-service
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (required, not included in repo)
   
   This file is ignored by Git for security. Create it manually:
   
   ```bash
   # On Windows
   type nul > .env
   
   # On Linux/Mac
   touch .env
   ```
   
   Then add the following environment variables to `.env`:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5433/expense_sharing_db
   APP_NAME=Expense Sharing Service
   APP_ENV=development
   DEBUG=True
   ```
   
   **Note**: Adjust `DATABASE_URL` if your PostgreSQL credentials or port are different.

5. Set up database
   Make sure PostgreSQL is running locally on port 5433 (or update `.env`).
   ```bash
   alembic upgrade head
   ```

5. Run the server
   ```bash
   uvicorn app.main:app --reload
   ```

   App runs on `http://localhost:8000`

### With Docker

```bash
docker compose up --build
```

Services:
- App: `http://localhost:8000`
- PostgreSQL: `localhost:5433`
- pgAdmin (database UI): `http://localhost:5050`

For more details, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## Architecture

The project follows a **feature-based module structure**. Each feature (users, groups, expenses, etc.) is its own module under `app/modules/`.

```
app/
├── core/
│   ├── config.py        # Basic config
│   ├── database.py      # SQLAlchemy setup
│   ├── dependencies.py  # Shared dependencies
│   └── settings.py      # Environment variables
│
├── modules/
│   ├── users/           # User management
│   ├── groups/          # Groups and memberships
│   ├── expenses/        # Expense tracking
│   ├── balances/        # Balance calculations
│   └── settlements/     # Settlement suggestions
│
└── main.py              # App entry point
```

### Why This Structure?

Each module is self-contained with:
- `router.py` - HTTP endpoints
- `service.py` - Business logic
- `repository.py` - Database queries
- `schemas.py` - Request/response types
- `models.py` - Database models

This makes it easy to find code and add new features without touching existing ones.

## Database Design

### Tables

**users**
- `user_id` (UUID primary key)
- `name` (string)
- `created_at` (timestamp)

**groups**
- `group_id` (UUID primary key)
- `name` (string)
- `created_at` (timestamp)

**group_members** (join table)
- `id` (auto-increment primary key)
- `group_id` (foreign key → groups)
- `user_id` (foreign key → users)
- `joined_at` (timestamp)

**expenses**
- `expense_id` (UUID primary key)
- `group_id` (foreign key → groups)
- `paid_by` (foreign key → users)
- `amount` (float)
- `description` (string)
- `created_at` (timestamp)

**expense_shares** (split records)
- `id` (auto-increment primary key)
- `expense_id` (foreign key → expenses)
- `user_id` (foreign key → users)
- `share_amount` (float)

### Why This Design?

- `group_members` is a join table to allow users to be in multiple groups.
- `expense_shares` stores each person's individual share, so we can support unequal splits later if needed.
- UUIDs for main entities because they're easier to work with across systems.

## Key Concepts

### Expense Splitting

When you create an expense, it splits equally among all group members:

```
Expense: $100 for 4 people
Each person's share = $100 / 4 = $25
```

The last person gets any remainder (to handle rounding):
```
If 3 people get $33.33, the 4th gets $33.34
```

### Net Balance

For each person, we calculate: `money received - money owed`

```
Alice paid $100 (balance = +100)
Alice's share of that = $25 (balance = +100 - 25 = +75)
Bob paid $0 (balance = 0)
Bob's share = $25 (balance = 0 - 25 = -25)
```

Positive = should receive money
Negative = owes money

### Settlement Algorithm

We want to suggest minimum transactions to settle everyone up.

The approach:
1. Get all net balances
2. Sort debtors (most owed) and creditors (most owed to) separately
3. Pair them greedily (biggest debtor with biggest creditor)
4. Repeat until everyone is settled

This isn't always the absolute minimum (that's NP-hard), but it works well in practice.

See [algorithm_implementation.md](algorithm_implementation.md) for detailed flow.

## Assumptions Made

- **Equal splits only**: For now, all expenses split equally. No custom proportions.
- **Single currency**: No currency conversion. Everything in one currency.
- **Trusted users**: No authentication. Anyone can create users and groups. (Don't use in production!)
- **No partial payments**: Settlements are all-or-nothing. Can't mark a partial payment as done.
- **Positive amounts only**: Expenses must be > 0. No refunds/negative expenses.
- **No expense editing**: Once created, expenses can't be changed. Only way to fix is create an opposite expense.

## Design Decisions

### Why Pairwise Debts API?

We have two balance endpoints:
- `GET /groups/{group_id}/balances` - net balance for each person
- `GET /groups/{group_id}/balances/pairwise` - raw debts between individuals

The pairwise one shows who owes whom explicitly, which is useful for debugging and transparency. The net balance is simpler but hides direct relationships.

### Why ServiceLayerWithRepository?

The `Service` layer has the business logic (calculations, validation), and `Repository` handles database queries. This keeps them separate and makes testing easier.

### Why Bulk Add Members?

The add-members endpoint takes an array of user IDs instead of one at a time. This is faster for seeding data and more realistic (most apps let you bulk-invite people to a group).

### Why Pydantic Schemas?

Schemas define request/response shapes and validate data before it hits the database. If someone sends invalid JSON or wrong types, FastAPI rejects it immediately.

### Why Alembic for Migrations?

Database schema changes are tracked in version-controlled SQL scripts. Makes it easy to replay changes on new environments.

## API Endpoints

### Users
- `POST /users` - create user
- `GET /users` - list all users
- `GET /users/{user_id}` - get one user

### Groups
- `POST /groups` - create group
- `GET /groups` - list all groups
- `GET /groups/{group_id}` - get one group
- `POST /groups/{group_id}/members` - add members (accepts array)
- `GET /groups/{group_id}/members` - list group members

### Expenses
- `POST /expenses` - create expense (splits equally)
- `GET /expenses/{expense_id}` - get one expense
- `GET /groups/{group_id}/expenses` - list group expenses

### Balances
- `GET /groups/{group_id}/balances` - net balance per person
- `GET /groups/{group_id}/balances/pairwise` - raw debts

### Settlements
- `GET /groups/{group_id}/settlements` - settlement suggestions

For request/response formats, see [api_contact_doc.md](api_contact_doc.md).

## Testing the API

Use the included Postman collection: `postman-collection.json`

Or curl:
```bash
# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Get all users
curl http://localhost:8000/users
```

## Improvements I'd Make With More Time

### Authentication
Right now there's no auth. In production you'd want:
- JWT tokens or OAuth
- User sign-up/login
- Only allow users to see their own groups

### Richer Expense Types
- Custom splits (30/50/20 instead of equal)
- Unequal shares marked at creation time
- Itemized expenses (track who ate what)

### Expense Editing
- Allow editing/deleting expenses
- Track change history for audit

### Partial Payments
- Record when someone pays back only part of what they owe
- Show progress toward settlement

### Better Settlement Algorithm
- Use a proper minimum-transfer algorithm (currently just greedy)
- Calculate the true minimum number of transactions needed

### Notifications
- Email notifications when added to a group
- Reminders when you owe money
- Settlement confirmations

### UI Dashboard
- Simple frontend to visualize balances
- Create expenses from the UI instead of API
- See settlement suggestions and mark as paid

### Database Improvements
- Add indexes on foreign keys and frequently-queried columns
- Archive old groups instead of deleting
- Add soft deletes for expenses

### Better Error Handling
- More specific error messages
- Custom exception classes
- Proper error logging

### Validation Rules
- Prevent adding same person to group twice (currently errors, but could be friendlier)
- Prevent circular debt scenarios earlier
- Show warnings for edge cases

### Tests
- Unit tests for service logic
- Integration tests for API endpoints
- Load testing for performance

### Documentation
- OpenAPI/Swagger UI (FastAPI has this built-in, just need to enable)
- More inline code comments
- Architecture decision records (ADRs)

## Files to Configure Manually

The following files are **ignored by Git** for security and environment-specific reasons. They are not in the repository, so you must create them manually when setting up:

### `.env` (Required)
Environment variables configuration file.

**Create it** in the project root:
```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

**Add these variables**:
```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5433/expense_sharing_db
APP_NAME=Expense Sharing Service
APP_ENV=development
DEBUG=True
```

**Why it's ignored**: Contains sensitive data like database passwords. Never commit this to Git.

### `venv/` (Virtual Environment)
Python virtual environment directory.

**Create it** by running:
```bash
python -m venv venv
```

This directory is excluded from Git because it's specific to each developer's machine and contains many files.

## Running Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of change"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback one version:
```bash
alembic downgrade -1
```

## Troubleshooting

**"Database connection refused"**
- Make sure PostgreSQL is running
- Check `.env` has correct DATABASE_URL
- For Docker: make sure postgres service is healthy

**"User/Group not found"**
- Create the resource first via API
- Check you're using the right IDs

**"Migration fails"**
- Make sure database exists and is empty for first migration
- Check alembic is configured correctly in `alembic.ini`

## Environment Variables

See `.env` file. Key ones:
- `DATABASE_URL` - PostgreSQL connection string
- `APP_ENV` - "development" or "production"
- `DEBUG` - True/False for debug logging

For Docker, DATABASE_URL is overridden in `docker-compose.yml` to point to the postgres service.

## Project Structure Summary

```
expense-sharing-service/
├── app/                          # Main app code
│   ├── core/                     # Shared utilities
│   ├── modules/                  # Feature modules
│   └── main.py                   # Entry point
├── alembic/                      # Database migrations
├── tests/                        # Test files
├── Dockerfile                    # Container config
├── docker-compose.yml            # Multi-container setup
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── README.md                     # This file
├── api_contact_doc.md            # API reference
├── algorithm_implementation.md   # Algorithm explanations
└── DOCKER_SETUP.md              # Docker instructions
```

## Notes

- The service is stateless (no sessions). Every request is independent.
- Database is the source of truth. No caching layer yet.
- No rate limiting. Not suitable for public APIs.
- Expenses are immutable after creation. Design choice to keep logic simple.
- Settlement algorithm is deterministic - same data always produces same suggestions.

Good luck! Feel free to fork and extend.
# expense-sharing-assignment
