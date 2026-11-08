"""Java language and Spring Boot framework profile definitions."""

from __future__ import annotations

from _code_health.ir_models import FrameworkProfile, IRClass, IRFunction, LanguageProfile, RulePenalty

SPRING_CONCERN_MAP = {
    "ResponseEntity": "http_transport",
    "HttpServletRequest": "http_transport",
    "HttpServletResponse": "http_transport",
    "JdbcTemplate": "persistence_db",
    "EntityManager": "persistence_db",
    "CrudRepository": "persistence_db",
    "JpaRepository": "persistence_db",
    "RestTemplate": "external_client",
    "WebClient": "external_client",
    "KafkaTemplate": "external_client",
    "ObjectMapper": "serialization",
    "Files.readString": "filesystem_io",
    "Files.writeString": "filesystem_io",
}

SPRING_ENTRYPOINTS = {
    "GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping",
    "RequestMapping", "Bean", "KafkaListener", "Scheduled", "EventListener"
}

SPRING_EXEMPT_LCOM = {"Entity", "Data", "Value", "Configuration", "ConfigurationProperties", "SpringBootApplication"}


class SpringBootFrameworkProfile(FrameworkProfile):
    """Spring Boot architectural rules, stereotype checks, and concern mappings."""

    def __init__(self) -> None:
        super().__init__(
            name="spring-boot",
            target_language="java",
            concern_map=SPRING_CONCERN_MAP,
            entrypoint_annotations=SPRING_ENTRYPOINTS,
            lcom4_exempt_annotations=SPRING_EXEMPT_LCOM,
        )

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate class-level Spring Boot architectural rules (field injection, layering)."""
        penalties: list[RulePenalty] = []
        is_controller = any(a.name in {"RestController", "Controller"} for a in cls.annotations)
        for f in cls.fields:
            if any(a.name in {"Autowired", "Inject"} for a in f.annotations):
                penalties.append(
                    RulePenalty("clean", 8.0, f"Clean (Spring): @Autowired field injection detected on '{f.name}' (-8.0 pts)", f.lineno)
                )
            if is_controller and (f.name.lower().endswith("repository") or "repository" in f.name.lower()):
                penalties.append(
                    RulePenalty("srp", 20.0, f"SRP (Spring): @RestController directly injects {f.name} (-20.0 pts)", f.lineno)
                )
        return penalties

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate method-level Spring Boot rules (transaction boundaries, SQL concatenation)."""
        penalties: list[RulePenalty] = []
        has_tx = any(a.name == "Transactional" for a in func.annotations)
        is_ctrl = parent and any(a.name in {"RestController", "Controller"} for a in parent.annotations)
        if has_tx and is_ctrl:
            penalties.append(
                RulePenalty("srp", 15.0, "SRP (Spring): @Transactional should not be placed on web controllers (-15.0 pts)", func.lineno)
            )
        if has_tx and "private" in func.modifiers:
            penalties.append(
                RulePenalty("srp", 15.0, "SRP (Spring): @Transactional on private method has no effect in Spring proxy (-15.0 pts)", func.lineno)
            )
        sql_keywords = ("query", "update", "execute", "createQuery", "createNativeQuery")
        for call in func.calls:
            if any(kw in call.name for kw in sql_keywords) and call.has_string_concat:
                penalties.append(
                    RulePenalty("security", 40.0, f"Security (Spring): potential SQL/JPQL injection in {call.name} via string concatenation (-40.0 pts)", call.lineno)
                )
        return penalties

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize Spring MockMvc, AssertJ, and JUnit 5 assertions."""
        short = call_name.split(".")[-1]
        return short in {"assertEquals", "assertTrue", "assertFalse", "assertNotNull", "assertNull", "assertThrows", "assertAll", "assertThat", "verify", "andExpect"}


SPRING_BOOT_FRAMEWORK = SpringBootFrameworkProfile()
JAVA_PROFILE = LanguageProfile(name="java", file_extensions=(".java",), frameworks=[SPRING_BOOT_FRAMEWORK])
