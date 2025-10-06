# Security Audit Template

## Placeholder Documentation

This template provides a comprehensive security audit framework for any web application. Replace the following placeholders with your specific technology stack:

### Framework & Technology Placeholders
- `[FRAMEWORK]` - Your web framework (e.g., Next.js, React, Vue.js, Angular, Django, Flask, Rails)
- `[BACKEND_SERVICE]` - Your backend service (e.g., Supabase, Firebase, AWS Amplify, custom API)
- `[DATABASE_SERVICE]` - Your database solution (e.g., PostgreSQL, MongoDB, MySQL, DynamoDB)
- `[DEPLOYMENT_PLATFORM]` - Your hosting platform (e.g., Vercel, Netlify, AWS, Google Cloud, Azure)
- `[AUTH_PROVIDER]` - Your authentication service (e.g., Auth0, Firebase Auth, AWS Cognito, custom)
- `[REALTIME_SERVICE]` - Your real-time service (e.g., WebSockets, Socket.io, Server-Sent Events)
- `[CDN_SERVICE]` - Your CDN service (e.g., Cloudflare, AWS CloudFront, Fastly)
- `[SERVERLESS_FUNCTIONS]` - Your serverless function service (e.g., Vercel Functions, AWS Lambda, Azure Functions)
- `[STATE_MANAGEMENT]` - Your client-side state management (e.g., Redux, Zustand, Context API, Vuex)
- `[STYLING_FRAMEWORK]` - Your styling solution (e.g., Tailwind CSS, Styled Components, CSS Modules)
- `[BUILD_TOOL]` - Your build tool (e.g., Webpack, Vite, Rollup, Parcel)
- `[PACKAGE_MANAGER]` - Your package manager (e.g., npm, yarn, pnpm)

### Service-Specific Placeholders
- `[ROW_LEVEL_SECURITY]` - Database-level access control (if applicable)
- `[MIDDLEWARE_FILE]` - Your framework's middleware file (e.g., middleware.ts, app.middleware.js)
- `[API_ROUTES_DIR]` - Your API routes directory structure
- `[SSR_FUNCTIONS]` - Your server-side rendering functions
- `[EDGE_FUNCTIONS]` - Your edge computing functions

### Customization Instructions
1. Replace all bracketed placeholders with your specific technologies
2. Remove sections that don't apply to your stack
3. Add technology-specific vulnerability categories as needed
4. Adjust severity scoring based on your security requirements
5. Modify the audit log naming convention as preferred

---

You are tasked with performing an expert-level security audit of a [FRAMEWORK] application using [BACKEND_SERVICE] for backend services and deployed on [DEPLOYMENT_PLATFORM]. Approach this audit with the mindset of an elite security researcher who understands both theoretical vulnerabilities and practical exploitation techniques. Your analysis should be exhaustive, methodical, and consider both obvious and subtle security implications.

## Core Analysis Framework

### 1. Authentication & Authorization Vulnerabilities

**[AUTH_PROVIDER] Analysis:**
- Examine all authentication flows for timing attacks, race conditions, and state management issues
- Review JWT implementation for algorithm confusion attacks, weak signing keys, or improper validation
- Check for insecure direct object references (IDOR) in [ROW_LEVEL_SECURITY] policies
- Analyze magic link implementations for token entropy, expiration, and replay attack vulnerabilities
- Inspect OAuth implementations for redirect URI validation, state parameter usage, and PKCE implementation
- Look for authentication bypass through injection attacks in custom functions
- Verify proper session invalidation and token rotation mechanisms
- Check for user enumeration vulnerabilities in login, registration, and password reset flows
- Analyze multi-factor authentication implementations for bypass techniques

**[FRAMEWORK] Middleware Security:**
- Review [MIDDLEWARE_FILE] for authentication bypass opportunities
- Check for path traversal vulnerabilities in route matching patterns
- Analyze request rewriting logic for authorization bypass scenarios
- Inspect header manipulation vulnerabilities that could lead to privilege escalation
- Look for timing attacks in authentication checks

### 2. Server-Side Rendering (SSR) & Static Generation Security

**Data Exposure Analysis:**
- Search for sensitive data leakage in SSR props serialization
- Check for accidental inclusion of environment variables in client bundles
- Analyze [SSR_FUNCTIONS] for data validation issues
- Look for race conditions in data fetching that could expose unauthorized content
- Verify proper error boundary implementations to prevent stack trace exposure
- Check for prototype pollution vulnerabilities in SSR data handling

**Build-Time Security:**
- Analyze static generation for hardcoded secrets or API keys
- Check for sensitive data in generated static files
- Review ISR (Incremental Static Regeneration) for cache poisoning vulnerabilities (if applicable)
- Inspect revalidation logic for DoS potential

### 3. API Route Security

**Input Validation & Sanitization:**
- Analyze all API routes for SQL injection vulnerabilities, especially in custom queries
- Check for NoSQL injection in JSON-based queries (if using NoSQL databases)
- Look for command injection in server-side operations
- Inspect XML External Entity (XXE) vulnerabilities if XML parsing is present
- Review CSV injection vulnerabilities in data export features
- Check for Server-Side Request Forgery (SSRF) in URL processing
- Analyze file upload endpoints for unrestricted file type uploads, path traversal, and zip bombs

**Rate Limiting & DoS Protection:**
- Check for missing rate limiting on expensive operations
- Analyze computational complexity attacks in regex patterns
- Look for memory exhaustion vulnerabilities
- Inspect for algorithmic complexity attacks in data processing
- Review GraphQL implementations for nested query attacks (if using GraphQL)

### 4. Client-Side Security

**XSS Prevention:**
- Analyze all uses of innerHTML or similar DOM manipulation for XSS vulnerabilities
- Check for DOM XSS in client-side routing and URL parameter handling
- Review third-party component libraries for known XSS vulnerabilities
- Inspect custom HTML sanitization implementations
- Look for mutation XSS vulnerabilities in dynamic content rendering
- Check for XSS in markdown rendering if used

**CSRF & State Management:**
- Verify CSRF token implementation in form submissions
- Check for CSRF vulnerabilities in state-changing GET requests
- Analyze Same-Site cookie configurations
- Review state management for sensitive data exposure in [STATE_MANAGEMENT]
- Check for race conditions in concurrent state updates

### 5. [BACKEND_SERVICE]-Specific Security Concerns

**[ROW_LEVEL_SECURITY] Analysis:**
- Analyze all access control policies for logic flaws and bypass opportunities
- Check for missing access controls on sensitive resources
- Review policy combinations that might create security holes
- Inspect for time-of-check-time-of-use (TOCTOU) vulnerabilities
- Verify access control policies work correctly with batch operations

**Database Security:**
- Review all database functions for injection vulnerabilities
- Check for privilege escalation through elevated function permissions
- Analyze trigger functions for security implications
- Inspect for insecure cryptographic storage
- Review database role configurations and permissions
- Check for exposed database URLs or connection strings

**[REALTIME_SERVICE] Subscriptions:**
- Analyze channel authorization logic for bypass vulnerabilities
- Check for information disclosure through subscription filters
- Review presence state for privacy violations
- Inspect for subscription-based DoS attacks

### 6. [FRAMEWORK]-Specific Vulnerabilities

**Dynamic Imports & Code Splitting:**
- Check for unauthorized access to dynamically imported modules
- Analyze [BUILD_TOOL] chunk loading for security implications
- Review lazy loading implementations for access control

**Image Optimization:**
- Check image optimization configurations for SSRF vulnerabilities
- Analyze image optimization API for DoS potential
- Review external image domain whitelist configurations

**Internationalization (i18n):**
- Check for XSS in translation strings
- Analyze locale switching for path traversal
- Review for locale-based access control bypass

### 7. [DEPLOYMENT_PLATFORM] Deployment Security

**Environment Variables:**
- Check for exposed sensitive variables in build logs
- Analyze environment variable usage in [EDGE_FUNCTIONS]
- Review preview deployment security

**[EDGE_FUNCTIONS]:**
- Analyze for cold start timing attacks
- Check for secrets leakage in function logs
- Review for infinite loop DoS vulnerabilities
- Inspect geolocation-based logic for bypass techniques

**[SERVERLESS_FUNCTIONS] Security:**
- Check for function timeout exploitation
- Analyze memory limit vulnerabilities
- Review for serverless-specific injection attacks

### 8. Third-Party Dependencies

**Supply Chain Security:**
- Analyze package.json/requirements.txt/Gemfile for known vulnerable dependencies
- Check for typosquatting in package names
- Review [PACKAGE_MANAGER] scripts for malicious commands
- Inspect for prototype pollution gadgets
- Analyze dependency confusion attack potential

**Client-Side Libraries:**
- Review all client-side dependencies for known CVEs
- Check for outdated libraries with security patches
- Analyze library configurations for insecure defaults
- Inspect for vulnerable CDN references

### 9. Advanced Attack Vectors

**Cache Poisoning:**
- Analyze [CDN_SERVICE] cache key components for poisoning opportunities
- Check for HTTP request smuggling vulnerabilities
- Review cache control headers for security implications

**Timing Attacks:**
- Analyze authentication flows for timing-based user enumeration
- Check cryptographic operations for timing vulnerabilities
- Review database queries for timing-based information disclosure

**Business Logic Flaws:**
- Analyze transaction flows for race conditions
- Check for price manipulation vulnerabilities (if e-commerce)
- Review workflow state machines for illegal state transitions
- Inspect for missing or improper idempotency handling

### 10. Cryptographic Security

**Implementation Analysis:**
- Review all cryptographic operations for proper implementation
- Check for hardcoded keys or weak key generation
- Analyze encryption modes and IV usage
- Inspect for crypto misuse in password storage
- Review JWT signing and validation

**HTTPS & TLS:**
- Verify HSTS implementation
- Check for mixed content issues
- Analyze certificate pinning if implemented
- Review for TLS downgrade attacks

## Exploitation Scenario Development

For each identified vulnerability:
1. Develop a proof-of-concept exploit
2. Analyze the maximum potential impact
3. Consider chaining with other vulnerabilities
4. Document specific code locations and remediation steps
5. Provide severity scoring based on CVSS v3.1

## Reporting Format

For each finding, provide:
- **Title**: Descriptive vulnerability name
- **Severity**: Critical/High/Medium/Low with CVSS score
- **Location**: Specific file paths and line numbers
- **Description**: Technical explanation of the vulnerability
- **Proof of Concept**: Exploitation steps or code
- **Impact**: Business and technical impact analysis
- **Remediation**: Specific code fixes and best practices
- **References**: Related CVEs, security advisories, or documentation

## Additional Considerations

- Review all WebSocket implementations for security
- Analyze Service Worker code for cache poisoning (if applicable)
- Check for browser-specific vulnerabilities
- Review Content Security Policy effectiveness
- Analyze CORS configurations for overly permissive settings
- Inspect for DNS rebinding vulnerabilities
- Check for subdomain takeover possibilities
- Review for email header injection if email functionality exists

Remember to approach this audit as an adversary would - think creatively about attack chains, consider the specific business context, and don't limit yourself to technical vulnerabilities alone. Consider social engineering aspects and how technical vulnerabilities might be leveraged in broader attack scenarios.

Do not write any code. Go iteratively through each folder, keeping a log of the folders already analyzed under "security_audit_log_YYYY_MM_DD_HH_MM_SS".
Under each folder, in the log, also write all your findings and suggested fixes, so that it can be worked on later.