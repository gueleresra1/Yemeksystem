# Yemeksystem - Project Requirements and Guidelines

## Project Overview
Yemeksystem is a FastAPI-based food management system that allows dealers to manage food items, recipes, and serves customers with a comprehensive food ordering platform. The system includes multi-language support, allergen management, and role-based access control.

## System Architecture

### Technology Stack
- **Backend Framework**: FastAPI 0.104.1+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with Bearer authentication
- **Migration**: Alembic for database migrations
- **Validation**: Pydantic for data validation
- **Password Hashing**: Passlib with bcrypt
- **Environment**: python-dotenv for configuration

### Database Schema

#### Core Models
1. **Users** (`users` table)
   - Primary key: `id` (Integer)
   - `email` (String, unique, indexed)
   - `password` (String, hashed)
   - `role_id` (ForeignKey to roles.id)
   - Timestamps: `created_at`, `updated_at`

2. **Roles** (`roles` table)
   - Primary key: `id` (Integer)
   - `name` (String, unique) - Values: "admin", "customer", "dealer"
   - `description` (String, optional)
   - Timestamps: `created_at`, `updated_at`

3. **Foods** (`foods` table)
   - Primary key: `id` (Integer)
   - `name` (String, indexed)
   - `description` (Text, optional)
   - `price` (Float)
   - `category` (String)
   - `dealer_id` (ForeignKey to users.id)
   - `is_active` (Boolean, default=True)
   - Timestamps: `created_at`, `updated_at`

4. **Recipes** (`recipes` table)
   - Primary key: `id` (Integer)
   - `food_id` (ForeignKey to foods.id)
   - `ingredient_name` (String)
   - `quantity` (String)
   - `step_order` (Integer)
   - `instruction` (Text, optional)
   - Timestamps: `created_at`, `updated_at`

5. **Allergens** (`allergens` table)
   - For managing food allergen information

6. **Languages** (`languages` table)
   - For multi-language support

7. **FoodTranslations** (`food_translations` table)
   - For storing food names/descriptions in different languages

### Role-Based Access Control

#### Role Hierarchy
1. **Admin (role_id=1)**
   - Full system access
   - Can create dealer accounts
   - Can manage all foods and users

2. **Customer (role_id=2)**
   - Default role for new registrations
   - Can view foods and place orders
   - Limited access to personal data

3. **Dealer (role_id=3)**
   - Can create, update, and manage their own foods
   - Can manage their own recipes
   - Cannot access other dealers' data

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new customer account
- `POST /auth/login` - User authentication, returns JWT token

### User Management (`/users`)
- `GET /users/me` - Get current user information (Protected)
- `GET /users/protected` - Example protected route

### Dealer Management (`/dealer`)
- `POST /dealer/register` - Create dealer account (Admin only)

### Food Management (`/foods`)
- `POST /foods/create` - Create new food (Dealer only)
- `GET /foods/` - List all foods with filtering options
- `GET /foods/{food_id}` - Get specific food details with recipes
- `PUT /foods/{food_id}` - Update food (Owner or Admin only)
- `DELETE /foods/{food_id}` - Soft delete food (Owner or Admin only)
- `GET /foods/my/foods` - Get dealer's own foods (Dealer only)

## Development Guidelines

### Code Organization
```
/
├── main.py                 # FastAPI application entry point
├── database.py            # Database configuration
├── auth.py                # Authentication logic
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── role.py
│   ├── food.py
│   ├── recipe.py
│   ├── allergen.py
│   ├── language.py
│   └── food_translation.py
├── dtos/                  # Data Transfer Objects (Pydantic schemas)
│   ├── __init__.py
│   ├── user_dto.py
│   ├── auth_dto.py
│   ├── recipe_dto.py
│   └── food_dto.py
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   ├── dealer.py
│   └── foods.py
└── alembic/              # Database migrations
```

### DTO (Data Transfer Object) Standards
- All DTOs should end with `DTO` suffix
- Use clear, descriptive names (e.g., `UserCreateDTO`, `FoodOutDTO`)
- Include proper type hints and validation
- Separate request DTOs (Create, Update) from response DTOs (Out)
- Use `from_attributes = True` in Config for ORM compatibility

### Authentication Requirements
- All protected routes must use `Depends(get_current_user)`
- JWT tokens expire in 30 minutes (configurable via environment)
- Bearer token format: `Authorization: Bearer <token>`
- Password hashing uses bcrypt

### Database Guidelines
- Use Alembic for all database schema changes
- All models should inherit from `Base`
- Include timestamps (`created_at`, `updated_at`) on all tables
- Use proper foreign key relationships
- Implement soft deletes where appropriate (`is_active` flag)

### Environment Configuration
Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

### Development Commands

#### Database Operations
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Check current migration status
alembic current

# View migration history
alembic history
```

#### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (using Docker)
docker-compose up -d postgres

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Database Setup (Docker)
```bash
# Start PostgreSQL and pgAdmin
docker-compose up -d

# Access pgAdmin at http://localhost:8080
# Email: admin@admin.com
# Password: admin
```

### Security Best Practices
- Never expose or log sensitive information (passwords, tokens)
- Always hash passwords before storing
- Validate all input data using Pydantic schemas
- Implement proper authorization checks for each endpoint
- Use HTTPS in production

### Error Handling Standards
- Use appropriate HTTP status codes
- Return consistent error response format:
  ```json
  {
    "detail": "Error message description"
  }
  ```
- Implement proper error messages in Turkish for user-facing errors

### Testing Guidelines
- Test all API endpoints for different user roles
- Verify authentication and authorization logic
- Test database constraints and relationships
- Validate DTO serialization/deserialization

### Business Logic Rules

#### Food Management
- Only dealers can create foods
- Foods belong to the dealer who created them
- Dealers can only modify their own foods
- Admins can modify any food
- Soft delete foods by setting `is_active = False`
- Each food can have multiple recipes with step ordering

#### User Registration
- New users get "customer" role by default
- Only admins can create dealer accounts
- Email addresses must be unique across the system

#### Recipe Management
- Recipes are tied to specific foods
- Include ingredient name, quantity, and step order
- Optional instruction field for additional details
- When updating food, replace all recipes

### Multi-language Support
- Food names and descriptions can be translated
- Language table stores supported languages
- FoodTranslation table links foods to their translations
- Future enhancement: API endpoints for managing translations

### Performance Considerations
- Use database indexing on frequently queried fields
- Implement pagination for list endpoints
- Consider caching for frequently accessed data
- Use query optimization for complex joins

### Deployment Notes
- Configure proper CORS settings for production
- Use environment variables for all configuration
- Set up proper logging for production monitoring
- Implement database connection pooling
- Use proper SSL certificates

## Future Enhancements
1. Order management system
2. Payment integration
3. Real-time notifications
4. Advanced search and filtering
5. Image upload for foods
6. Rating and review system
7. Inventory management
8. Analytics and reporting

## Troubleshooting Common Issues

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL environment variable
- Verify database exists and credentials are correct

### Authentication Issues
- Verify SECRET_KEY is set
- Check token expiration time
- Ensure proper Bearer token format

### Migration Issues
- Always backup database before migrations
- Check for model import issues
- Verify Alembic configuration

This documentation should be kept updated as the project evolves and new features are added.