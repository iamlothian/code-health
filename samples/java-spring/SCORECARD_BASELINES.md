# Java Spring Boot Code Health Scorecard Baselines

This catalog provides 10 functionally comparable, verbatim real-world **Good** and **Bad** Java Spring Boot code sample pairs (20 files total) from [`spring-projects/spring-petclinic`](https://github.com/spring-projects/spring-petclinic), [`spring-petclinic/spring-petclinic-microservices`](https://github.com/spring-petclinic/spring-petclinic-microservices), [`OWASP WebGoat`](https://github.com/WebGoat/WebGoat), and [`gothinkster/spring-boot-realworld-example-app`](https://github.com/gothinkster/spring-boot-realworld-example-app).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file and is listed in [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `java (spring-boot)` | 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC) | **GOOD** | [`good/ApiGatewayController.java`](good/ApiGatewayController.java) | [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayController.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) | 40 | 94.0 | 100.0 | 100.0 | 92.5 | 100.0 | **97.1** | **A** |
| `java (spring-boot)` | 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC) | **BAD** | [`bad/PetResource.java`](bad/PetResource.java) | [spring-petclinic/spring-petclinic-microservices (customers/web/PetResource.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java) | 48 | 58.7 | 100.0 | 100.0 | 94.3 | 100.0 | **63.7** | **D** |
| `java (spring-boot)` | 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/) | **GOOD** | [`good/Servers.java`](good/Servers.java) | [OWASP WebGoat (sqlinjection/mitigation/Servers.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/mitigation/Servers.java) | 46 | 100.0 | 98.5 | 100.0 | 77.5 | 100.0 | **96.2** | **A** |
| `java (spring-boot)` | 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/) | **BAD** | [`bad/SqlInjectionLesson8.java`](bad/SqlInjectionLesson8.java) | [OWASP WebGoat (sqlinjection/introduction/SqlInjectionLesson8.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/introduction/SqlInjectionLesson8.java) | 104 | 90.4 | 94.0 | 97.6 | 77.0 | 60.0 | **65.0** | **D** |
| `java (spring-boot)` | 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC) | **GOOD** | [`good/PetControllerTests.java`](good/PetControllerTests.java) | [spring-projects/spring-petclinic (owner/PetControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java) | 193 | 100.0 | 100.0 | 100.0 | 92.0 | 100.0 | **98.8** | **A** |
| `java (spring-boot)` | 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC) | **BAD** | [`bad/OwnerControllerTests.java`](bad/OwnerControllerTests.java) | [spring-projects/spring-petclinic (owner/OwnerControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerTests.java) | 224 | 60.0 | 90.4 | 100.0 | 91.8 | 100.0 | **65.0** | **D** |
| `java (spring-boot)` | 4. Spring Security & JWT Service Dependency Injection (spring-boot-realworld-example-app, ~38 LOC) | **GOOD** | [`good/DefaultJwtService.java`](good/DefaultJwtService.java) | [gothinkster/spring-boot-realworld-example-app (infrastructure/service/DefaultJwtService.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/infrastructure/service/DefaultJwtService.java) | 34 | 97.8 | 100.0 | 100.0 | 80.0 | 100.0 | **96.3** | **A** |
| `java (spring-boot)` | 4. Spring Security & JWT Service Dependency Injection (spring-boot-realworld-example-app, ~38 LOC) | **BAD** | [`bad/JwtTokenFilter.java`](bad/JwtTokenFilter.java) | [gothinkster/spring-boot-realworld-example-app (api/security/JwtTokenFilter.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/security/JwtTokenFilter.java) | 42 | 88.0 | 100.0 | 100.0 | 59.0 | 100.0 | **64.0** | **D** |
| `java (spring-boot)` | 5. Spring Boot REST API Controller Layering (spring-boot-realworld-example-app api/, ~38 LOC) | **GOOD** | [`good/ArticlesApi.java`](good/ArticlesApi.java) | [gothinkster/spring-boot-realworld-example-app (api/ArticlesApi.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/ArticlesApi.java) | 37 | 100.0 | 100.0 | 100.0 | 76.7 | 100.0 | **96.5** | **A** |
| `java (spring-boot)` | 5. Spring Boot REST API Controller Layering (spring-boot-realworld-example-app api/, ~38 LOC) | **BAD** | [`bad/ArticleFavoriteApi.java`](bad/ArticleFavoriteApi.java) | [gothinkster/spring-boot-realworld-example-app (api/ArticleFavoriteApi.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/ArticleFavoriteApi.java) | 39 | 54.0 | 100.0 | 100.0 | 78.3 | 100.0 | **59.0** | **F** |
| `java (spring-boot)` | 6. Spring JDBC Query Parameterization vs SQL String Concatenation (OWASP WebGoat sqlinjection/advanced/) | **GOOD** | [`good/SqlInjectionLesson6b.java`](good/SqlInjectionLesson6b.java) | [OWASP WebGoat (sqlinjection/advanced/SqlInjectionLesson6b.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/advanced/SqlInjectionLesson6b.java) | 36 | 99.0 | 100.0 | 100.0 | 78.3 | 100.0 | **96.4** | **A** |
| `java (spring-boot)` | 6. Spring JDBC Query Parameterization vs SQL String Concatenation (OWASP WebGoat sqlinjection/advanced/) | **BAD** | [`bad/SqlInjectionChallenge.java`](bad/SqlInjectionChallenge.java) | [OWASP WebGoat (sqlinjection/advanced/SqlInjectionChallenge.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/advanced/SqlInjectionChallenge.java) | 60 | 84.0 | 97.5 | 100.0 | 76.7 | 60.0 | **65.0** | **D** |
| `java (spring-boot)` | 7. WebAuthn Endpoint Decomposition vs Oversized Handler Method (OWASP WebGoat webauthn/, ~110 LOC) | **GOOD** | [`good/GoatBankCeremonyEndpoints.java`](good/GoatBankCeremonyEndpoints.java) | [OWASP WebGoat (webauthn/GoatBankCeremonyEndpoints.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/GoatBankCeremonyEndpoints.java) | 119 | 87.6 | 98.9 | 100.0 | 97.1 | 100.0 | **95.6** | **A** |
| `java (spring-boot)` | 7. WebAuthn Endpoint Decomposition vs Oversized Handler Method (OWASP WebGoat webauthn/, ~110 LOC) | **BAD** | [`bad/WebAuthnRegistrationAssignment.java`](bad/WebAuthnRegistrationAssignment.java) | [OWASP WebGoat (webauthn/WebAuthnRegistrationAssignment.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/WebAuthnRegistrationAssignment.java) | 103 | 82.0 | 50.0 | 50.0 | 92.5 | 100.0 | **55.0** | **F** |
| `java (spring-boot)` | 8. WebAuthn Codec Decomposition vs High-Complexity Authentication Handler (OWASP WebGoat webauthn/) | **GOOD** | [`good/Cbor.java`](good/Cbor.java) | [OWASP WebGoat (webauthn/Cbor.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/Cbor.java) | 175 | 97.9 | 97.4 | 100.0 | 94.3 | 100.0 | **97.9** | **A** |
| `java (spring-boot)` | 8. WebAuthn Codec Decomposition vs High-Complexity Authentication Handler (OWASP WebGoat webauthn/) | **BAD** | [`bad/WebAuthnSecurityKeyAssignment.java`](bad/WebAuthnSecurityKeyAssignment.java) | [OWASP WebGoat (webauthn/WebAuthnSecurityKeyAssignment.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/WebAuthnSecurityKeyAssignment.java) | 89 | 82.0 | 52.5 | 61.2 | 92.5 | 100.0 | **57.5** | **F** |
| `java (spring-boot)` | 9. Spring MVC Controller Cohesion & LCOM4 (spring-projects/spring-petclinic, ~44 LOC) | **GOOD** | [`good/VetController.java`](good/VetController.java) | [spring-projects/spring-petclinic (vet/VetController.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/vet/VetController.java) | 37 | 80.0 | 100.0 | 100.0 | 95.0 | 100.0 | **93.2** | **A** |
| `java (spring-boot)` | 9. Spring MVC Controller Cohesion & LCOM4 (spring-projects/spring-petclinic, ~44 LOC) | **BAD** | [`bad/VisitController.java`](bad/VisitController.java) | [spring-projects/spring-petclinic (owner/VisitController.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/VisitController.java) | 50 | 54.0 | 100.0 | 100.0 | 95.0 | 100.0 | **59.0** | **F** |
| `java (spring-boot)` | 10. JUnit 5 Spring Test Assertions & Injection Hygiene (realworld vs petclinic-microservices) | **GOOD** | [`good/DefaultJwtServiceTest.java`](good/DefaultJwtServiceTest.java) | [gothinkster/spring-boot-realworld-example-app (infrastructure/service/DefaultJwtServiceTest.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/test/java/io/spring/infrastructure/service/DefaultJwtServiceTest.java) | 27 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (spring-boot)` | 10. JUnit 5 Spring Test Assertions & Injection Hygiene (realworld vs petclinic-microservices) | **BAD** | [`bad/ApiGatewayControllerTest.java`](bad/ApiGatewayControllerTest.java) | [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayControllerTest.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/main/spring-petclinic-api-gateway/src/test/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayControllerTest.java) | 60 | 100.0 | 100.0 | 100.0 | 62.0 | 100.0 | **67.0** | **D** |

---

## Detailed Scenario Scorecards

### JAVA (`--framework spring-boot`) — 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC)

#### Good Baseline: [`good/ApiGatewayController.java`](good/ApiGatewayController.java) ([sidecar JSON](good/ApiGatewayController.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayController.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 97.1/100 (Grade A)` — `SRP: 94.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 92.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.1/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 94.0 | Size: 100.0 | Complexity: 100.0 | Clean: 92.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java src      40    -  94.0 100.0 100.0  92.5 100.0   97.1   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java    40    4     1    4   97.1   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java:5   12   1    0   1   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ApiGatewayController.java:6   11   1    0   1   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ApiGatewayController.java:4    7   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/ApiGatewayController.java:8    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/PetResource.java`](bad/PetResource.java) ([sidecar JSON](bad/PetResource.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-petclinic/spring-petclinic-microservices (customers/web/PetResource.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 63.7/100 (Grade D)` — `SRP: 58.7` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 94.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 63.7/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 58.7 | Size: 100.0 | Complexity: 100.0 | Clean: 94.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java       src      48    -  58.7 100.0 100.0  94.3 100.0   63.7   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java:36 PetRes    48    7     1    7   63.7   D
    - SRP (Spring): @RestController directly injects petRepository (-20.0 pts)
    - SRP (Spring): @RestController directly injects ownerRepository (-20.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java:77 PetResou    8   1    0   2   0   96.5   A
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:55 PetResou   11   1    0   2   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/PetResource.java:45 PetResou    4   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:50 PetResou    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:69 PetResou    6   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:89 PetResou    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:96 PetResou    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/)

#### Good Baseline: [`good/Servers.java`](good/Servers.java) ([sidecar JSON](good/Servers.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/mitigation/Servers.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/mitigation/Servers.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 96.2/100 (Grade A)` — `SRP: 100.0` | `Size: 98.5` | `Complexity: 100.0` | `Clean: 77.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 98.5 | Complexity: 100.0 | Clean: 77.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java          src      46    - 100.0  98.5 100.0  77.5 100.0   96.2   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java:20 Servers      46    2     1    3   96.2   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java:43 Servers.sor   27   2    1   1   1   97.8   A
    - Size: LOC=27 (>25) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/Servers.java:39 Servers.Ser    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/SqlInjectionLesson8.java`](bad/SqlInjectionLesson8.java) ([sidecar JSON](bad/SqlInjectionLesson8.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/introduction/SqlInjectionLesson8.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/introduction/SqlInjectionLesson8.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 90.4` | `Size: 94.0` | `Complexity: 97.6` | `Clean: 77.0` | `Security: 60.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 90.4 | Size: 94.0 | Complexity: 97.6 | Clean: 77.0 | Security: 60.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java src     104    -  90.4  94.0  97.6  77.0  60.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java:2   104    5     1   14   65.0   D
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java:47    44   5    4   2   1   65.0   D
    - SRP: high external call fan-out=25 (>6) (-36.0 pts)
    - Size: LOC=44 (>25) (-28.5 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Spring): potential SQL/JPQL injection in statement.executeQuery via string concatenation (-40.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:131   14   2    1   2   0   65.0   D
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Spring): potential SQL/JPQL injection in statement.executeUpdate via string concatenation (-40.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:100   26   5    4   1   1   96.3   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Size: LOC=26 (>25) (-1.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:37     3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:41     5   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC)

#### Good Baseline: [`good/PetControllerTests.java`](good/PetControllerTests.java) ([sidecar JSON](good/PetControllerTests.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (owner/PetControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 98.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 92.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.8/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 92.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java test    193    - 100.0 100.0 100.0  92.0 100.0   98.8   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java:5   193    5     1    5   98.8   A
    - Clean (Spring): @Autowired field injection detected on 'mockMvc' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java:70    17   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:89     7   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:97     9   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:191    9   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:201    8   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/OwnerControllerTests.java`](bad/OwnerControllerTests.java) ([sidecar JSON](bad/OwnerControllerTests.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (owner/OwnerControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerTests.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 60.0` | `Size: 90.4` | `Complexity: 100.0` | `Clean: 91.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 20
Dimensions -> SRP: 60.0 | Size: 90.4 | Complexity: 100.0 | Clean: 91.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java test    224    -  60.0  90.4 100.0  91.8 100.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java:   224   20     1   22   65.0   D
    - SRP: methods=20 (>10) (-40.0 pts)
    - Size: class LOC=224 (>200) (-9.6 pts)
    - Clean (Spring): @Autowired field injection detected on 'mockMvc' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java:28   14   1    0   0   0   99.5   A
    - Clean (Test): 9 assertions in single test (>8) (-3.0 pts)
samples/java-spring/bad/OwnerControllerTests.java:73   18   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:92   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:10    7   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:11   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:12   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:13   14   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:15   14   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:16    7   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:17    6   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:18    8   2    1   0   1  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:19    8   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:19   11   2    1   0   1  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:21    9   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:22   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:23   12   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:25   11   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:26    6   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:26   13   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:29   16   1    0   0   0  100.0   A
```

### JAVA (`--framework spring-boot`) — 4. Spring Security & JWT Service Dependency Injection (spring-boot-realworld-example-app, ~38 LOC)

#### Good Baseline: [`good/DefaultJwtService.java`](good/DefaultJwtService.java) ([sidecar JSON](good/DefaultJwtService.java.expected.json))

- **Upstream Dataset / Benchmark:** [gothinkster/spring-boot-realworld-example-app (infrastructure/service/DefaultJwtService.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/infrastructure/service/DefaultJwtService.java) (`MIT`)
- **Expected Scorecard:** `Composite 96.3/100 (Grade A)` — `SRP: 97.8` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.3/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 97.8 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtService.java src      34    -  97.8 100.0 100.0  80.0 100.0   96.3   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtService.java:17    34    4     1    5   96.3   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtService.java:40 D   10   2    1   1   0   97.5   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/DefaultJwtService.java:31 D    8   1    0   1   0   98.3   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/DefaultJwtService.java:23 D    7   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/DefaultJwtService.java:51 D    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/JwtTokenFilter.java`](bad/JwtTokenFilter.java) ([sidecar JSON](bad/JwtTokenFilter.java.expected.json))

- **Upstream Dataset / Benchmark:** [gothinkster/spring-boot-realworld-example-app (api/security/JwtTokenFilter.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/security/JwtTokenFilter.java) (`MIT`)
- **Expected Scorecard:** `Composite 64.0/100 (Grade D)` — `SRP: 88.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 59.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 64.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 88.0 | Size: 100.0 | Complexity: 100.0 | Clean: 59.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/JwtTokenFilter.java    src      42    -  88.0 100.0 100.0  59.0 100.0   64.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/JwtTokenFilter.java:18 Jwt    42    2     1    5   64.0   D
    - Clean: missing class docstring (-15.0 pts)
    - Clean (Spring): @Autowired field injection detected on 'userRepository' (-8.0 pts)
    - Clean (Spring): @Autowired field injection detected on 'jwtService' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/JwtTokenFilter.java:24 JwtTo   24   2    1   3   1   91.3   A
    - SRP: high external call fan-out=14 (>6) (-24.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/JwtTokenFilter.java:50 JwtTo   12   3    2   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

### JAVA (`--framework spring-boot`) — 5. Spring Boot REST API Controller Layering (spring-boot-realworld-example-app api/, ~38 LOC)

#### Good Baseline: [`good/ArticlesApi.java`](good/ArticlesApi.java) ([sidecar JSON](good/ArticlesApi.java.expected.json))

- **Upstream Dataset / Benchmark:** [gothinkster/spring-boot-realworld-example-app (api/ArticlesApi.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/ArticlesApi.java) (`MIT`)
- **Expected Scorecard:** `Composite 96.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 76.7` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 76.7 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ArticlesApi.java      src      37    - 100.0 100.0 100.0  76.7 100.0   96.5   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ArticlesApi.java:21 Artic    37    3     1    3   96.5   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ArticlesApi.java:28 Article   11   1    0   2   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ArticlesApi.java:48 Article   12   1    0   6   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ArticlesApi.java:40 Article    7   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/ArticleFavoriteApi.java`](bad/ArticleFavoriteApi.java) ([sidecar JSON](bad/ArticleFavoriteApi.java.expected.json))

- **Upstream Dataset / Benchmark:** [gothinkster/spring-boot-realworld-example-app (api/ArticleFavoriteApi.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/main/java/io/spring/api/ArticleFavoriteApi.java) (`MIT`)
- **Expected Scorecard:** `Composite 59.0/100 (Grade F)` — `SRP: 54.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 78.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 59.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 54.0 | Size: 100.0 | Complexity: 100.0 | Clean: 78.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ArticleFavoriteApi.java src      39    -  54.0 100.0 100.0  78.3 100.0   59.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ArticleFavoriteApi.java:21    39    3     1    3   59.0   F
    - Clean: missing class docstring (-15.0 pts)
    - SRP (Spring): @RestController directly injects articleFavoriteRepository (-20.0 pts)
    - SRP (Spring): @RestController directly injects articleRepository (-20.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ArticleFavoriteApi.java:39 A   13   1    0   2   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/ArticleFavoriteApi.java:29 A    9   1    0   2   0   97.5   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/ArticleFavoriteApi.java:53 A    9   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 6. Spring JDBC Query Parameterization vs SQL String Concatenation (OWASP WebGoat sqlinjection/advanced/)

#### Good Baseline: [`good/SqlInjectionLesson6b.java`](good/SqlInjectionLesson6b.java) ([sidecar JSON](good/SqlInjectionLesson6b.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/advanced/SqlInjectionLesson6b.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/advanced/SqlInjectionLesson6b.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 96.4/100 (Grade A)` — `SRP: 99.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 78.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.4/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 99.0 | Size: 100.0 | Complexity: 100.0 | Clean: 78.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/SqlInjectionLesson6b.java src      36    -  99.0 100.0 100.0  78.3 100.0   96.4   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/SqlInjectionLesson6b.java    36    3     1    6   96.4   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/SqlInjectionLesson6b.java:4   20   3    2   0   1   97.6   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/SqlInjectionLesson6b.java:2    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/SqlInjectionLesson6b.java:3    9   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/SqlInjectionChallenge.java`](bad/SqlInjectionChallenge.java) ([sidecar JSON](bad/SqlInjectionChallenge.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/advanced/SqlInjectionChallenge.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/advanced/SqlInjectionChallenge.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 84.0` | `Size: 97.5` | `Complexity: 100.0` | `Clean: 76.7` | `Security: 60.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 84.0 | Size: 97.5 | Complexity: 100.0 | Clean: 76.7 | Security: 60.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionChallenge.java src      60    -  84.0  97.5 100.0  76.7  60.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionChallenge.java    60    3     1    7   65.0   D
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionChallenge.java:4   30   3    2   3   1   65.0   D
    - SRP: high external call fan-out=19 (>6) (-36.0 pts)
    - Size: LOC=30 (>25) (-7.5 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Spring): potential SQL/JPQL injection in statement.executeQuery via string concatenation (-40.0 pts)
samples/java-spring/bad/SqlInjectionChallenge.java:8   13   3    2   3   1   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/SqlInjectionChallenge.java:4    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 7. WebAuthn Endpoint Decomposition vs Oversized Handler Method (OWASP WebGoat webauthn/, ~110 LOC)

#### Good Baseline: [`good/GoatBankCeremonyEndpoints.java`](good/GoatBankCeremonyEndpoints.java) ([sidecar JSON](good/GoatBankCeremonyEndpoints.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (webauthn/GoatBankCeremonyEndpoints.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/GoatBankCeremonyEndpoints.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 95.6/100 (Grade A)` — `SRP: 87.6` | `Size: 98.9` | `Complexity: 100.0` | `Clean: 97.1` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 95.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 87.6 | Size: 98.9 | Complexity: 100.0 | Clean: 97.1 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/GoatBankCeremonyEndpoints.java src     119    -  87.6  98.9 100.0  97.1 100.0   95.6   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/GoatBankCeremonyEndpoints   119    7     1   11   95.6   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/GoatBankCeremonyEndpoints.j   30   3    2   3   1   69.0   D
    - SRP: high external call fan-out=19 (>6) (-36.0 pts)
    - Size: LOC=30 (>25) (-7.5 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j   23   1    0   3   0   93.7   A
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j   25   3    2   3   1   94.6   A
    - SRP: high external call fan-out=12 (>6) (-18.0 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j   22   1    0   4   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j    5   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/GoatBankCeremonyEndpoints.j    4   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/WebAuthnRegistrationAssignment.java`](bad/WebAuthnRegistrationAssignment.java) ([sidecar JSON](bad/WebAuthnRegistrationAssignment.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (webauthn/WebAuthnRegistrationAssignment.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/WebAuthnRegistrationAssignment.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 55.0/100 (Grade F)` — `SRP: 82.0` | `Size: 50.0` | `Complexity: 50.0` | `Clean: 92.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 55.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 82.0 | Size: 50.0 | Complexity: 50.0 | Clean: 92.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnRegistrationAssignment.java src     103    -  82.0  50.0  50.0  92.5 100.0   55.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnRegistrationAssign   103    2     1   15   55.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnRegistrationAssignme   88  14   13   4   1    5.0   F
    - SRP: high external call fan-out=59 (>6) (-36.0 pts)
    - Size: LOC=88 (>25) (-100.0 pts)
    - Complexity: CC=14 (>5) (-48.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Complexity: returns=14 (>3) (-44.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/WebAuthnRegistrationAssignme    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 8. WebAuthn Codec Decomposition vs High-Complexity Authentication Handler (OWASP WebGoat webauthn/)

#### Good Baseline: [`good/Cbor.java`](good/Cbor.java) ([sidecar JSON](good/Cbor.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (webauthn/Cbor.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/Cbor.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 97.9/100 (Grade A)` — `SRP: 97.9` | `Size: 97.4` | `Complexity: 100.0` | `Clean: 94.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 97.9 | Size: 97.4 | Complexity: 100.0 | Clean: 94.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Cbor.java             src     175    -  97.9  97.4 100.0  94.3 100.0   97.9   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Cbor.java:22 Cbor           175    7     1   15   97.9   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Cbor.java:52 Cbor.write       37   3    2   2   1   89.5   B
    - SRP: high external call fan-out=11 (>6) (-15.0 pts)
    - Size: LOC=37 (>25) (-18.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/Cbor.java:90 Cbor.writeHead   18   5    4   3   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/Cbor.java:26 Cbor.Cbor         1   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/Cbor.java:28 Cbor.decode       8   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/Cbor.java:46 Cbor.encode       5   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/Cbor.java:109 Cbor.writeBig    5   2    1   3   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/Cbor.java:38 Cbor.decodeFir    5   1    0   2   0  100.0   A
```

#### Bad Baseline: [`bad/WebAuthnSecurityKeyAssignment.java`](bad/WebAuthnSecurityKeyAssignment.java) ([sidecar JSON](bad/WebAuthnSecurityKeyAssignment.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (webauthn/WebAuthnSecurityKeyAssignment.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/webauthn/WebAuthnSecurityKeyAssignment.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 57.5/100 (Grade F)` — `SRP: 82.0` | `Size: 52.5` | `Complexity: 61.2` | `Clean: 92.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 57.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 82.0 | Size: 52.5 | Complexity: 61.2 | Clean: 92.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnSecurityKeyAssignment.java src      89    -  82.0  52.5  61.2  92.5 100.0   57.5   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnSecurityKeyAssignm    89    2     1   13   57.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/WebAuthnSecurityKeyAssignmen   73  12   11   4   1   10.0   F
    - SRP: high external call fan-out=45 (>6) (-36.0 pts)
    - Size: LOC=73 (>25) (-95.0 pts)
    - Complexity: CC=12 (>5) (-34.0 pts)
    - Complexity: cognitive=11 (>8) (-7.5 pts)
    - Complexity: returns=12 (>3) (-36.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/WebAuthnSecurityKeyAssignmen    6   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 9. Spring MVC Controller Cohesion & LCOM4 (spring-projects/spring-petclinic, ~44 LOC)

#### Good Baseline: [`good/VetController.java`](good/VetController.java) ([sidecar JSON](good/VetController.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (vet/VetController.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/vet/VetController.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 93.2/100 (Grade A)` — `SRP: 80.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 93.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 80.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/VetController.java    src      37    -  80.0 100.0 100.0  95.0 100.0   93.2   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/VetController.java:36 Vet    37    5     1    6   93.2   A
    - SRP (Spring): @RestController directly injects vetRepository (-20.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/VetController.java:41 VetCo    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/VetController.java:45 VetCo   10   2    1   3   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/VetController.java:56 VetCo    8   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/VetController.java:65 VetCo    6   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/VetController.java:72 VetCo    6   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/VisitController.java`](bad/VisitController.java) ([sidecar JSON](bad/VisitController.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (owner/VisitController.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/VisitController.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 59.0/100 (Grade F)` — `SRP: 54.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 59.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 6
Dimensions -> SRP: 54.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/VisitController.java   src      50    -  54.0 100.0 100.0  95.0 100.0   59.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/VisitController.java:42 Vi    50    6     4    9   59.0   F
    - SRP: LCOM4=4 disconnected method groups (-45.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/VisitController.java:97 Visi   14   3    2   5   1   96.7   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/VisitController.java:47 Visi    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/VisitController.java:51 Visi    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/VisitController.java:83 Visi    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/VisitController.java:90 Visi    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/VisitController.java:63 Visi   17   2    1   3   1  100.0   A
```

### JAVA (`--framework spring-boot`) — 10. JUnit 5 Spring Test Assertions & Injection Hygiene (realworld vs petclinic-microservices)

#### Good Baseline: [`good/DefaultJwtServiceTest.java`](good/DefaultJwtServiceTest.java) ([sidecar JSON](good/DefaultJwtServiceTest.java.expected.json))

- **Upstream Dataset / Benchmark:** [gothinkster/spring-boot-realworld-example-app (infrastructure/service/DefaultJwtServiceTest.java)](https://github.com/gothinkster/spring-boot-realworld-example-app/blob/master/src/test/java/io/spring/infrastructure/service/DefaultJwtServiceTest.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtServiceTest.java test     27    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtServiceTest.jav    27    4     1    4  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/DefaultJwtServiceTest.java:    4   1    0   0   0  100.0   A
samples/java-spring/good/DefaultJwtServiceTest.java:    9   1    0   0   0  100.0   A
samples/java-spring/good/DefaultJwtServiceTest.java:    5   1    0   0   0  100.0   A
samples/java-spring/good/DefaultJwtServiceTest.java:    6   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/ApiGatewayControllerTest.java`](bad/ApiGatewayControllerTest.java) ([sidecar JSON](bad/ApiGatewayControllerTest.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayControllerTest.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/main/spring-petclinic-api-gateway/src/test/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayControllerTest.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 67.0/100 (Grade D)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 62.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 67.0/100 (Grade D) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 62.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ApiGatewayControllerTest.java test     60    - 100.0 100.0 100.0  62.0 100.0   67.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ApiGatewayControllerTest.j    60    2     1    2   67.0   D
    - Clean (Spring): @Autowired field injection detected on 'client' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/ApiGatewayControllerTest.jav   26   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java-spring/bad/ApiGatewayControllerTest.jav   24   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
```
