# Summit Market - Backend Engineer Interview Questions

This document contains interview questions designed to test a candidate's ability to identify, understand, and fix the intentional bugs and issues in the Summit Market Django application.

## 🚨 Security-Focused Questions

### 1. Django Security Configuration
**Question:** "I notice the Django settings have some security configurations. Can you identify any security issues in the current setup?"

**Expected Answer:** Candidate should identify:
- Hardcoded SECRET_KEY in production settings
- DEBUG=True in production
- Overly permissive CORS configuration
- Wildcard ALLOWED_HOSTS

**Follow-up:** "How would you fix these issues?"

### 2. Authentication & Authorization
**Question:** "Looking at the GraphQL schema, what security concerns do you see with the current implementation?"

**Expected Answer:** Candidate should identify:
- No authentication required for queries/mutations
- All fields exposed with `fields='__all__'`
- Plain text password handling
- No permission checks

**Follow-up:** "How would you implement proper authentication and authorization for GraphQL?"

### 3. API Security
**Question:** "The gRPC service is running on an insecure port. What are the security implications and how would you secure it?"

**Expected Answer:** Candidate should identify:
- Unencrypted communication
- No TLS/SSL
- Man-in-the-middle attack vulnerability
- Need for mutual TLS authentication

## 🔧 Dependency & Environment Questions

### 4. Dependency Management
**Question:** "Can you review the requirements.txt file and identify any issues?"

**Expected Answer:** Candidate should identify:
- Duplicate packages with conflicting versions
- Missing GraphQL dependencies (graphene-django, graphene)
- Missing gRPC dependencies (grpcio, grpcio-tools, protobuf)
- Outdated packages with security vulnerabilities

**Follow-up:** "How would you resolve these dependency conflicts?"

### 5. Environment Configuration
**Question:** "The Docker Compose file has hardcoded credentials. What's wrong with this approach?"

**Expected Answer:** Candidate should identify:
- Credentials exposed in version control
- Security risk if repository is compromised
- Need for environment variables or secrets management
- Docker secrets or external configuration management

## 🐛 Code Quality & Logic Questions

### 6. Model Validation
**Question:** "Looking at the User model, there's a phone number validation issue. Can you spot it?"

**Expected Answer:** Candidate should identify:
- Phone regex changed to require exactly 10 digits
- Breaks international phone number support
- Should support international formats with country codes

**Follow-up:** "How would you design a more robust phone number validation system?"

### 7. Database Design
**Question:** "The Product model has a nullable price field. What problems could this cause?"

**Expected Answer:** Candidate should identify:
- Products can be created without prices
- Order calculations will fail
- Business logic inconsistencies
- Need for proper validation or default values

### 8. SKU Generation Logic
**Question:** "There's a bug in the Product model's save method for SKU generation. Can you find it?"

**Expected Answer:** Candidate should identify:
- References `self.id` before the object is saved
- Will always use 'NEW' for new products
- Should generate SKU after saving or use a different approach

## 🔄 Performance & Optimization Questions

### 9. Database Query Optimization
**Question:** "The user_stats endpoint performs multiple database queries. How would you optimize it?"

**Expected Answer:** Candidate should identify:
- Multiple separate count queries
- Should use single aggregated query with annotations
- Example: `User.objects.aggregate(total=Count('id'), active=Count('id', filter=Q(is_active=True)))`

**Follow-up:** "What other performance optimizations would you implement?"

### 10. N+1 Query Problem
**Question:** "Looking at the views, can you identify any N+1 query problems?"

**Expected Answer:** Candidate should identify:
- Related objects not properly prefetched
- Multiple database hits for related data
- Need for `select_related()` and `prefetch_related()`

### 11. Celery Task Performance
**Question:** "The Celery tasks have some performance issues. Can you identify them?"

**Expected Answer:** Candidate should identify:
- Inefficient database operations in loops
- Blocking operations (`time.sleep()`)
- Memory-intensive operations
- Need for bulk operations and async patterns

## 🚀 Architecture & Design Questions

### 12. Microservices Communication
**Question:** "The gRPC service is designed for microservices communication. What improvements would you suggest?"

**Expected Answer:** Candidate should identify:
- Need for service discovery
- Circuit breaker patterns
- Retry mechanisms
- Proper error handling and logging
- Health checks

### 13. Event-Driven Architecture
**Question:** "How would you implement event-driven architecture for this e-commerce system?"

**Expected Answer:** Candidate should discuss:
- Message queues (RabbitMQ, Kafka)
- Event sourcing
- CQRS patterns
- Event-driven order processing
- Inventory management events

### 14. Caching Strategy
**Question:** "What caching strategy would you implement for this application?"

**Expected Answer:** Candidate should discuss:
- Redis for session storage
- Product catalog caching
- User data caching
- Cache invalidation strategies
- CDN for static assets

## 🐳 DevOps & Infrastructure Questions

### 15. Container Security
**Question:** "The Dockerfile has some security issues. Can you identify them?"

**Expected Answer:** Candidate should identify:
- Running as root user
- No security hardening
- No multi-stage builds
- Missing security scanning
- Need for non-root user

### 16. CI/CD Pipeline
**Question:** "How would you design a CI/CD pipeline for this application?"

**Expected Answer:** Candidate should discuss:
- Automated testing (unit, integration, security)
- Code quality checks (linting, security scanning)
- Docker image building and scanning
- Deployment strategies (blue-green, canary)
- Monitoring and alerting

### 17. Monitoring & Observability
**Question:** "What monitoring and observability tools would you implement?"

**Expected Answer:** Candidate should discuss:
- Application performance monitoring (APM)
- Distributed tracing
- Centralized logging
- Metrics collection
- Alerting and dashboards

## 🛡️ Advanced Security Questions

### 18. Input Validation
**Question:** "How would you implement comprehensive input validation across the application?"

**Expected Answer:** Candidate should discuss:
- Serializer validation
- Model validation
- Custom validators
- SQL injection prevention
- XSS protection
- Rate limiting

### 19. Data Encryption
**Question:** "What data should be encrypted and how would you implement it?"

**Expected Answer:** Candidate should discuss:
- Sensitive user data encryption
- Database encryption at rest
- TLS for data in transit
- Key management
- Compliance requirements (GDPR, PCI-DSS)

### 20. Audit Logging
**Question:** "How would you implement comprehensive audit logging?"

**Expected Answer:** Candidate should discuss:
- User action logging
- Data access logging
- Security event logging
- Compliance logging
- Log retention policies

## 🔍 Debugging & Troubleshooting Questions

### 21. Production Debugging
**Question:** "A user reports that orders are not being processed. How would you debug this issue?"

**Expected Answer:** Candidate should discuss:
- Log analysis
- Database query investigation
- Celery task monitoring
- Error tracking tools
- Performance profiling

### 22. Performance Investigation
**Question:** "The application is running slowly. What steps would you take to identify the bottleneck?"

**Expected Answer:** Candidate should discuss:
- Database query analysis
- Application profiling
- Infrastructure monitoring
- Load testing
- Performance metrics analysis

## 📊 System Design Questions

### 23. Scalability Design
**Question:** "How would you design this system to handle 10x more traffic?"

**Expected Answer:** Candidate should discuss:
- Horizontal scaling strategies
- Database sharding
- Load balancing
- Caching layers
- Microservices architecture
- CDN implementation

### 24. High Availability
**Question:** "How would you ensure high availability for this e-commerce platform?"

**Expected Answer:** Candidate should discuss:
- Multi-region deployment
- Database replication
- Failover strategies
- Disaster recovery
- Backup strategies
- Health checks and monitoring

## 🎯 Behavioral Questions

### 25. Code Review Process
**Question:** "How do you approach code reviews? What do you look for?"

**Expected Answer:** Candidate should discuss:
- Security vulnerabilities
- Performance issues
- Code quality and maintainability
- Testing coverage
- Documentation
- Best practices

### 26. Technical Leadership
**Question:** "How would you mentor junior developers on this team?"

**Expected Answer:** Candidate should discuss:
- Code review practices
- Knowledge sharing sessions
- Documentation standards
- Best practices training
- Pair programming
- Technical guidance

### 27. Problem-Solving Approach
**Question:** "Walk me through how you would approach fixing the bugs in this codebase."

**Expected Answer:** Candidate should discuss:
- Systematic approach to bug identification
- Prioritization of issues
- Testing strategies
- Documentation of fixes
- Code review process
- Deployment considerations

## 📝 Practical Coding Questions

### 28. Fix the Phone Validation
**Question:** "Can you fix the phone number validation in the User model to support international numbers?"

**Expected Answer:** Candidate should provide code that:
- Supports international formats
- Uses a robust regex pattern
- Handles country codes
- Provides proper error messages

### 29. Optimize the User Stats Query
**Question:** "Can you optimize the user_stats endpoint to use a single database query?"

**Expected Answer:** Candidate should provide code that:
- Uses Django's aggregation functions
- Performs a single database query
- Returns the same data structure
- Improves performance

### 30. Implement Rate Limiting
**Question:** "How would you implement rate limiting for the API endpoints?"

**Expected Answer:** Candidate should discuss:
- Django REST framework throttling
- Redis-based rate limiting
- Custom rate limiting logic
- Different limits for different endpoints
- Rate limiting headers

## 🎯 Evaluation Criteria

### Technical Skills (40%)
- Ability to identify security vulnerabilities
- Understanding of performance optimization
- Knowledge of Django best practices
- Familiarity with modern backend technologies

### Problem-Solving (30%)
- Systematic approach to debugging
- Ability to prioritize issues
- Creative solutions to complex problems
- Attention to detail

### Communication (20%)
- Clear explanation of technical concepts
- Ability to discuss trade-offs
- Documentation and code comments
- Team collaboration skills

### Experience Level (10%)
- Depth of knowledge in specific areas
- Real-world experience with similar problems
- Understanding of enterprise-scale applications
- Familiarity with DevOps practices

## 📋 Interview Process

### Phase 1: Code Review (30 minutes)
- Present the codebase with bugs
- Ask candidate to identify issues
- Discuss severity and impact
- Evaluate systematic approach

### Phase 2: Technical Deep Dive (45 minutes)
- Focus on specific technical areas
- Ask detailed implementation questions
- Discuss trade-offs and alternatives
- Evaluate problem-solving skills

### Phase 3: System Design (30 minutes)
- Discuss scalability and architecture
- Explore design decisions
- Evaluate system thinking
- Assess experience level

### Phase 4: Behavioral & Leadership (15 minutes)
- Discuss team collaboration
- Explore mentoring experience
- Evaluate communication skills
- Assess cultural fit

## 🎯 Success Indicators

A strong candidate should demonstrate:
- **Security-first mindset** - Identifies security issues quickly
- **Performance awareness** - Understands optimization opportunities
- **System thinking** - Considers broader architectural implications
- **Practical experience** - Provides real-world solutions
- **Communication skills** - Explains complex concepts clearly
- **Leadership potential** - Shows mentoring and collaboration abilities

The candidate should be able to identify at least 70% of the intentional bugs and provide reasonable solutions for fixing them.
