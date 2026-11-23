# Spring Boot Architectural Refactoring Playbook

> **Profile:** `spring-boot` · **Detection:** `org.springframework` imports, `@SpringBootApplication`, or `spring-boot`/`org.springframework` in `pom.xml`/`build.gradle(.kts)` · **Force:** `--lang java --framework spring-boot` (disable with `--framework none`)
> **Builds on:** [Java Refactoring Playbook](java-playbook.md)
> **Worked examples:** [good](../../../samples/java-spring/good/) · [bad](../../../samples/java-spring/bad/)

This reference provides targeted before/after refactoring patterns to eliminate code smells and architectural violations detected by the Java / Spring Boot health analyzer.

---

## 1. Eliminate `@Autowired` Field Injection

### The Smell
Using `@Autowired` directly on fields bypasses immutability, complicates unit testing without Reflection/Spring context, and hides circular dependency problems.
- **Finding:** `Clean (Spring): @Autowired field injection detected on '<field>' (-8.0 pts)` per field (`@Autowired` or `@Inject`).

### Before (Smell)
```java
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private PaymentClient paymentClient;
}
```

### After (Refactored: Explicit Constructor Injection)
```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentClient paymentClient;

    public OrderService(OrderRepository orderRepository, PaymentClient paymentClient) {
        this.orderRepository = orderRepository;
        this.paymentClient = paymentClient;
    }
}
```

### After (Refactored: Lombok `@RequiredArgsConstructor`)
```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentClient paymentClient;
}
```

---

## 2. Decouple `@RestController` from Direct `@Repository` Injection

### The Smell
Controllers directly injecting persistence entities or repositories blur architectural boundaries, skipping validation, transaction management, and business logic layers.
- **Finding:** `SRP (Spring): @RestController directly injects <field> (-20.0 pts)`.

### Before (Smell)
```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderRepository orderRepository; // Direct DB access from web layer!

    public OrderController(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @GetMapping
    public List<Order> listOrders() {
        return orderRepository.findAll();
    }
}
```

### After (Refactored: Introduce Domain Service)
```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping
    public List<OrderResponse> listOrders() {
        return orderService.getAllOrders();
    }
}
```

---

## 3. Correct `@Transactional` Boundary Misplacement

### The Smell
- **Controllers:** `@Transactional` on controllers keeps database transactions open during HTTP response serialization, risking connection pool exhaustion.
- **Private Methods:** Spring uses proxy-based AOP. Internal calls to `private` methods bypass the proxy completely, so `@Transactional` is silently ignored.
- **Findings:**
  - `SRP (Spring): @Transactional should not be placed on web controllers (-15.0 pts)`
  - `SRP (Spring): @Transactional on private method has no effect in Spring proxy (-15.0 pts)`

### Before (Smell)
```java
@RestController
public class BadController {
    @Transactional // Wrong: Transaction in web layer
    @PostMapping("/submit")
    public ResponseEntity<Void> submit(@RequestBody Request req) {
        processOrder(req);
        return ResponseEntity.ok().build();
    }

    @Transactional // Wrong: Ineffective on private method
    private void processOrder(Request req) {
        // ...
    }
}
```

### After (Refactored: Public Method on Service Layer)
```java
@Service
public class OrderProcessingService {
    @Transactional
    public void processOrder(Request req) {
        // Transaction correctly managed at service boundary
    }
}
```

---

## 4. Parameterize Dynamic SQL Queries (Prevent Injection)

### The Smell
Concatenating variables into SQL or JPQL queries using `+` creates severe SQL injection vulnerabilities.
- **Finding:** `Security (Spring): potential SQL/JPQL injection in <call> via string concatenation (-40.0 pts)`.

### Before (Smell)
```java
@Repository
public class CustomOrderRepository {
    private final JdbcTemplate jdbcTemplate;

    public List<Order> findByStatus(String status) {
        String sql = "SELECT * FROM orders WHERE status = '" + status + "'";
        return jdbcTemplate.query(sql, new OrderRowMapper());
    }
}
```

### After (Refactored: Parameterized Query)
```java
@Repository
public class CustomOrderRepository {
    private final JdbcTemplate jdbcTemplate;

    public List<Order> findByStatus(String status) {
        String sql = "SELECT * FROM orders WHERE status = ?";
        return jdbcTemplate.query(sql, new OrderRowMapper(), status);
    }
}
```

---

## 5. Test Assertion Hygiene

### The Smell
- Test methods with `0` assertions pass vacuously without verifying behavior (-30.0 pts Clean Code).
- Test methods with $> 8$ assertions test too many distinct conditions (-3.0 pts per excess assertion).

### Before (Smell)
```java
@Test
void testOrderCreation() {
    orderService.createOrder(new OrderRequest());
    // 0 assertions!
}
```

### After (Refactored: AssertJ / JUnit 5 / MockMvc)
```java
@Test
void testOrderCreation() {
    Order order = orderService.createOrder(new OrderRequest());
    assertThat(order).isNotNull();
    assertThat(order.getStatus()).isEqualTo(OrderStatus.CREATED);
}

@Test
void testOrderEndpoint(MockMvc mockMvc) throws Exception {
    mockMvc.perform(get("/orders/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.id").value(1));
}
```

---

## 6. Deduplicate Repeated Endpoint Validation & Mapping Logic

- **Finding:** `Clean (DRY): DRY-XXX (type1|type2|type3, N toks, M LOC) L<start>-<end> in <symbol> matches <peer>:<start>-<end> (<peer_symbol>)`
- *Cause:* Controllers, services, or `*Tests.java` MockMvc integration suites copy-paste authorization guards, DTO mapping boilerplate, or MockMvc request/assertion chains ($\ge 35$ tokens in source; $\ge 55$ tokens in tests).
- *Fix:* Move repeated mapping/validation blocks into Spring `@Component` mappers or service helpers, and extract reusable `ResultActions` helper methods or `@ParameterizedTest` scenarios for MockMvc tests.
