# Template: Automated API Test Coverage and Generation

<!-- 
PLACEHOLDER DOCUMENTATION:

Replace the following placeholders when using this template:

FRAMEWORK PLACEHOLDERS:
- [PROJECT_NAME] - Your project name (e.g., "MyApp", "Invertly")
- [FRAMEWORK] - Your web framework (e.g., "Next.js 15", "Express.js", "FastAPI")
- [APP_ROUTER_TYPE] - Routing system (e.g., "App Router", "Pages Router", "Express Router")
- [TEST_FRAMEWORK] - Testing framework (e.g., "Jest", "Vitest", "Mocha")
- [PACKAGE_MANAGER] - Package manager (e.g., "pnpm", "npm", "yarn")

PATH PLACEHOLDERS:
- [TEST_PATH] - Path to test files (e.g., "__tests__/api/", "tests/", "src/__tests__/")
- [API_BASE_PATH] - Base API path (e.g., "app/api/", "src/api/", "routes/")
- [SOURCE_FILTER] - Filter for running source (e.g., "web", "api", "server")

DATABASE/AUTH PLACEHOLDERS:
- [DATABASE_CLIENT] - Database client (e.g., "Supabase", "Prisma", "Mongoose")
- [AUTH_PROVIDER] - Auth provider (e.g., "Supabase Auth", "Auth0", "NextAuth")
- [SERVER_CLIENT_MOCK] - Server client mock path
- [ADMIN_CLIENT_MOCK] - Admin client mock path
- [LOGGER_MOCK] - Logger mock path
- [ROUTE_HANDLER_MOCK] - Route handler mock path

TABLE/SCHEMA PLACEHOLDERS:
- [TABLE_NAME] - Database table name (e.g., "users", "companies", "products")
- [SCHEMA_NAME] - Database schema name if applicable

MOCK DATA PLACEHOLDERS:
- [MOCK_USER_ID] - Test user ID (e.g., "test-user-id", "user123")
- [MOCK_EMAIL] - Test email (e.g., "test@example.com")
- [SAMPLE_FIELD] - Sample field name (e.g., "name", "title", "description")
- [SAMPLE_VALUE] - Sample field value (e.g., "Test Name", "Sample Title")

ENDPOINT PLACEHOLDERS:
- {endpoint-name} - Specific endpoint name
- {METHOD} - HTTP method (GET, POST, PUT, DELETE)
- {HANDLER} - Handler function name
- {description} - Endpoint description
- {functionality} - What the endpoint does
- {auth requirements} - Authentication requirements
- {parameters} - Expected parameters
- {endpoint-path} - Full endpoint path

ENVIRONMENT PLACEHOLDERS:
- [NODE_ENV] - Node environment setting (if different from "node")
- [TEST_ENV_DECORATOR] - Test environment decorator (e.g., "@jest-environment node")
-->

You are tasked with checking test coverage and building comprehensive tests for API endpoints in the [PROJECT_NAME] application. Your goal is to ensure all API endpoints have proper test coverage of at least 90%.

## Test Environment Setup

The application uses:
- [FRAMEWORK] with [APP_ROUTER_TYPE]
- [TEST_FRAMEWORK] for testing with TypeScript support
- Test files location: `[TEST_PATH]`
- Coverage command: `[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:coverage`
- Test specific endpoint: `[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:api -- path/to/test.test.ts`

## Test File Structure and Conventions

1. **File Naming**: Tests should follow the pattern `{endpoint-name}.test.ts` matching the API route structure
2. **File Header**: Include appropriate JSDoc comments explaining what the endpoint does
3. **Test Environment**: Use `[TEST_ENV_DECORATOR]` when needed

## Required Mock Setup Pattern

```typescript
// TypeScript globals declaration
declare global {
  var jest: any;
  var describe: any;
  var it: any;
  var expect: any;
  var beforeEach: any;
}

// Standard mocks for all API tests
jest.mock('[LOGGER_MOCK]', () => ({
  getLogger: jest.fn().mockResolvedValue({
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  }),
}));

jest.mock('[ROUTE_HANDLER_MOCK]', () => ({
  enhanceRouteHandler: jest.fn((handler: any, options: any) => {
    return async (req: NextRequest) => {
      // Mock implementation based on auth requirements
      if (options.auth) {
        const mockUser = {
          id: '[MOCK_USER_ID]',
          email: '[MOCK_EMAIL]',
        };
        return handler({ request: req, user: mockUser });
      }
      return handler({ request: req, user: null });
    };
  }),
}));

// Database client mocks with chainable query methods
const mockQuery = {
  select: jest.fn().mockReturnThis(),
  eq: jest.fn().mockReturnThis(),
  ilike: jest.fn().mockReturnThis(),
  order: jest.fn().mockReturnThis(),
  range: jest.fn().mockReturnThis(),
  single: jest.fn().mockResolvedValue({ data: null, error: null }),
  returns: jest.fn().mockResolvedValue({ data: [], error: null, count: 0 }),
};

const mockDatabaseClient = {
  from: jest.fn().mockReturnValue(mockQuery),
  rpc: jest.fn(),
  storage: { from: jest.fn() },
};

jest.mock('[SERVER_CLIENT_MOCK]', () => ({
  getDatabaseServerClient: jest.fn(() => mockDatabaseClient),
}));

jest.mock('[ADMIN_CLIENT_MOCK]', () => ({
  getDatabaseServerAdminClient: jest.fn(() => mockDatabaseAdminClient),
}));

// For request creation
import { createMocks } from 'node-mocks-http';
import type { NextRequest } from 'next/server';
```

## Test Categories to Include

For each API endpoint, create tests covering:

### 1. Successful Operations
- Valid request with all required parameters
- Valid request with optional parameters
- Different valid data scenarios
- Pagination handling (if applicable)
- Sorting and filtering (if applicable)

### 2. Authentication & Authorization
- Unauthenticated requests
- Invalid authentication tokens
- Insufficient permissions
- Role-based access control

### 3. Input Validation
- Missing required parameters
- Invalid parameter types
- Invalid parameter values (e.g., invalid UUIDs)
- Out-of-range values
- SQL injection attempts (if applicable)

### 4. Error Handling
- Database connection failures
- Database query errors
- External service failures
- Unexpected exceptions
- Timeout scenarios

### 5. Edge Cases
- Empty results
- Maximum limits
- Concurrent requests (if applicable)
- Null/undefined handling

## Test Structure Template

```typescript
/**
 * API Tests for /api/{endpoint-name}
 * 
 * Tests the {description} endpoint which {functionality}.
 * 
 * This endpoint requires {auth requirements} and validates {parameters}.
 */

describe('/api/{endpoint-name}', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Reset mock return values to defaults
    mockQuery.returns.mockResolvedValue({
      data: [],
      error: null,
      count: 0,
    });
  });

  describe('{METHOD} /api/{endpoint-name}', () => {
    it('should return {expected} for valid request', async () => {
      // Setup mock data
      const mockData = [{[SAMPLE_FIELD]: '[SAMPLE_VALUE]'}];
      mockQuery.returns.mockResolvedValue({
        data: mockData,
        error: null,
        count: mockData.length,
      });

      // Create request
      const { req } = createMocks({
        method: '{METHOD}',
        url: 'http://localhost:3000/api/{endpoint}?param=value',
        headers: {
          'Content-Type': 'application/json',
        },
        body: {
          // Request body if POST/PUT
        },
      });

      // Call handler
      const response = await {HANDLER}(req as unknown as NextRequest);
      const data = await response.json();

      // Assert response
      expect(response.status).toBe(200);
      expect(data).toHaveProperty('expectedProperty');
      
      // Verify mock calls
      expect(mockDatabaseClient.from).toHaveBeenCalledWith('[TABLE_NAME]');
      expect(mockQuery.select).toHaveBeenCalled();
    });

    it('should return 400 for invalid parameters', async () => {
      const { req } = createMocks({
        method: '{METHOD}',
        url: 'http://localhost:3000/api/{endpoint}?invalidParam=bad',
      });

      const response = await {HANDLER}(req as unknown as NextRequest);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data).toHaveProperty('error');
    });

    it('should return 403 for unauthorized access', async () => {
      // Test authorization failures
    });

    it('should handle database errors gracefully', async () => {
      mockQuery.returns.mockResolvedValue({
        data: null,
        error: { message: 'Database error' },
        count: null,
      });

      // Test error handling
    });
  });
});
```

## Coverage Analysis Process

### 1. Initial Coverage Check
```bash
[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:coverage
```
Look for:
- File coverage percentage
- Uncovered lines
- Uncovered branches
- Uncovered functions

### 2. Identify Missing Coverage
- Check coverage report in `coverage/lcov-report/index.html`
- Focus on:
  - Error handling paths
  - Edge cases
  - Conditional branches
  - Different parameter combinations

### 3. Generate Additional Tests
For each uncovered scenario:
- Create a test case that exercises that specific code path
- Ensure proper mock setup for the scenario
- Add meaningful assertions

### 4. Iteration Process
Repeat until coverage > 90%:
1. Run coverage check
2. Identify uncovered code
3. Write tests for uncovered scenarios
4. Verify tests pass
5. Check coverage again

## Special Considerations

1. **Request Mocking**: Use `node-mocks-http` for creating mock requests
2. **Async Operations**: Always use async/await for API handlers
3. **Type Safety**: Ensure TypeScript types are properly handled
4. **Mock Cleanup**: Always clear mocks in `beforeEach`
5. **Realistic Data**: Use realistic test data that matches your domain
6. **Chain Mocking**: Ensure all database query methods return `this` for chaining

## Workflow Instructions

When a new API endpoint is created:

### 1. Analyze the endpoint
- Identify all parameters (required/optional)
- Understand authentication requirements
- Map database operations
- Note external service calls

### 2. Create initial test file
- Follow naming convention
- Set up all required mocks
- Create basic happy path test

### 3. Run initial coverage
```bash
[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:coverage -- [API_BASE_PATH]{endpoint-path}
```

### 4. Iterate to 90% coverage
- Add tests for each uncovered scenario
- Focus on error paths and edge cases
- Ensure all branches are covered

### 5. Final validation
- All tests pass: `[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:api`
- Coverage > 90%: `[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:coverage`
- No linting errors: `[PACKAGE_MANAGER] lint`
- Type checking passes: `[PACKAGE_MANAGER] typecheck`

## Example Test Generation Checklist

For each new endpoint, ensure tests for:
- [ ] Happy path with valid data
- [ ] Authentication required (401 without auth)
- [ ] Authorization checks (403 without permission)
- [ ] Invalid UUID formats (400)
- [ ] Missing required fields (400)
- [ ] Database query failure (500)
- [ ] External service failure (if applicable)
- [ ] Empty results handling
- [ ] Pagination boundaries
- [ ] Sort/filter combinations
- [ ] Concurrent request handling
- [ ] Rate limiting (if implemented)

## Common Mock Patterns

### Database Error Mock
```typescript
mockQuery.returns.mockResolvedValue({
  data: null,
  error: { message: 'Database connection failed' },
  count: null,
});
```

### Successful Data Mock
```typescript
const mockData = [
  { id: '123', [SAMPLE_FIELD]: '[SAMPLE_VALUE]', created_at: '2024-01-01' }
];
mockQuery.returns.mockResolvedValue({
  data: mockData,
  error: null,
  count: mockData.length,
});
```

### RPC Call Mock
```typescript
mockDatabaseClient.rpc.mockResolvedValue({
  data: true,
  error: null,
});
```

### Storage Mock
```typescript
const mockStorage = {
  upload: jest.fn().mockResolvedValue({
    data: { path: 'uploads/file.json' },
    error: null,
  }),
};
mockDatabaseClient.storage.from.mockReturnValue(mockStorage);
```

## Output Requirements

When generating tests:
1. Follow exact mock patterns from existing tests
2. Use consistent error messages and status codes
3. Include meaningful test descriptions
4. Add comments for complex test scenarios
5. Ensure all async operations are properly awaited
6. Match the exact indentation and formatting style

Continue iterating until `[PACKAGE_MANAGER] --filter [SOURCE_FILTER] test:coverage` shows >90% coverage for the endpoint file.

Once you complete one endpoint you should always continue to iterate until all endpoints are at least at 90% coverage.
In the end always commit tests to the working branch.

## Integration with Git Workflow

This prompt can be used:
1. As a pre-commit hook to ensure test coverage
2. In CI/CD pipelines to validate new endpoints
3. As part of code review process
4. Through automated tools that monitor git commits

Remember: The goal is not just high coverage numbers, but meaningful tests that validate the endpoint's behavior under all conditions.