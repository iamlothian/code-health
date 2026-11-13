# Angular Refactoring Playbook

**Profile:** `angular`  
**Detection:** TypeScript (`.ts`) files importing `@angular/*`  
**Force:** `--framework angular` (only activates on TypeScript files)  
**Builds on:** [TypeScript Playbook](typescript-playbook.md)  
**Worked examples:**  
- Clean: [orders_panel_clean.component.ts](../../../samples/typescript-angular/good/orders_panel_clean.component.ts), [header.component.ts](../../../samples/typescript-angular/good/header.component.ts), [article_preview.component.ts](../../../samples/typescript-angular/good/article_preview.component.ts), [favorite_button.component.ts](../../../samples/typescript-angular/good/favorite_button.component.ts)  
- Flagged: [orders_panel_legacy.component.ts](../../../samples/typescript-angular/bad/orders_panel_legacy.component.ts), [search_result.component.ts](../../../samples/typescript-angular/bad/search_result.component.ts), [complaint.component.ts](../../../samples/typescript-angular/bad/complaint.component.ts), [score_board.component.ts](../../../samples/typescript-angular/bad/score_board.component.ts)

---

## Profile Exemptions

- **DI Constructors:** Constructors on `@Component`, `@Directive`, `@Injectable`, `@Pipe`, and `@NgModule` classes are **exempt** from `Clean: missing public docstring`. All other public methods on those classes still require JSDoc docstrings and explicit return types.
- **Decorator `LCOM4` Exemption:** `@Component`, `@Directive`, `@Pipe`, and `@NgModule` classes are **exempt** from class `LCOM4` penalties (because Angular templates and lifecycle hooks legitimately split reactive state across methods). Class **attribute count** (`> 7`), **method count** (`> 10`), **effective class LOC** (`> 150`), and **total class cyclomatic complexity** (`> 25`) still apply.
- **`@HostListener` Entrypoints:** Methods decorated with `@HostListener` receive entrypoint parameter allowance (`<= 6` parameters instead of `<= 4`) and are exempt from boolean-default flag SRP penalties.

---

## 1. Direct `HttpClient` Injection in `@Component` / `@Directive`

**Finding:** `SRP (Angular): @Component/@Directive injects HttpClient directly instead of a service (-20.0 pts)` (class-level)

Triggers when a `@Component` or `@Directive` declares `HttpClient` in constructor parameters or class fields.

**Fix:** Move HTTP calls, endpoint URLs, and response mapping into an `@Injectable` domain service, and inject that service into the component.

```ts
// Before (-20.0 pts SRP (Angular))
@Component({ selector: 'app-orders', template: '...' })
export class OrdersPanelLegacyComponent {
  constructor(private readonly http: HttpClient) {}
  ngOnInit(): void {
    this.http.get('/api/orders').subscribe(/* ... */);
  }
}

// After (0 pts)
@Injectable({ providedIn: 'root' })
export class OrdersService {
  constructor(private readonly http: HttpClient) {}

  /** Fetches the active orders list. */
  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>('/api/orders');
  }
}

@Component({ selector: 'app-orders', template: '...' })
export class OrdersPanelCleanComponent implements OnInit {
  constructor(private readonly ordersService: OrdersService) {}
  // ...
}
```

See [orders_panel_legacy.component.ts](../../../samples/typescript-angular/bad/orders_panel_legacy.component.ts) vs. [orders_panel_clean.component.ts](../../../samples/typescript-angular/good/orders_panel_clean.component.ts).

---

## 2. Unmanaged `.subscribe()` Lifecycles

**Finding:** `Clean (Angular): unmanaged .subscribe() at L{sub_line} without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)` (class-level)

Triggers on `@Component` / `@Directive` classes that call `.subscribe(` without one of:
- `takeUntilDestroyed(...)` (modern Angular with `DestroyRef`), or
- `takeUntil(...)` coupled with teardown, or
- `ngOnDestroy()` calling `.unsubscribe()` (or storing `Subscription`s and unsubscribing), or
- Replacing manual subscriptions with Angular's `async` pipe (`| async`) or signals (`toSignal(...)`) in templates.

```ts
// Before (-15.0 pts Clean (Angular))
ngOnInit(): void {
  this.ordersService.getOrders().subscribe((rows) => {
    this.orders = rows;
  });
}

// After (0 pts — modern Angular DestroyRef + takeUntilDestroyed)
private readonly destroyRef = inject(DestroyRef);

/** Loads orders and clears error state when complete. */
ngOnInit(): void {
  this.ordersService
    .getOrders()
    .pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe((rows) => {
      this.orders = rows;
    });
}
```

---

## 3. Unsafe XSS / DOM Sinks & `DomSanitizer.bypassSecurityTrust*`

**Finding:** `Security (Angular): unsafe XSS/DOM sink '{sink_name}' at L{line} (-{pts:.1f} pts)` (`-35.0 pts` per occurrence, capped at `-70.0 pts`)

Flagged sinks:
- Angular sanitizer bypasses: `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustUrl`, `bypassSecurityTrustResourceUrl`
- Direct DOM sinks: `innerHTML`, `outerHTML`, `document.write`, `document.writeln`, `insertAdjacentHTML`

**Fix:** Let Angular's built-in context-aware escaping handle template bindings (`{{ value }}`), validate URL schemes with an allowlist before passing `[href]`, or use `DomSanitizer.sanitize(SecurityContext.HTML, raw)` instead of bypassing Angular security. See [search_result.component.ts](../../../samples/typescript-angular/bad/search_result.component.ts) and [score_board.component.ts](../../../samples/typescript-angular/bad/score_board.component.ts).

---

## 4. God Components, JSDoc, and Fan-Out in Large Angular Classes

Even though `@Component` classes are exempt from `LCOM4`, legacy Angular components still lose heavy points in **Size**, **SRP**, **Complexity**, and **Clean** when they accumulate state, form builders, snackbars, routers, dialogs, and filter logic in one class (as in [search_result.component.ts](../../../samples/typescript-angular/bad/search_result.component.ts), [complaint.component.ts](../../../samples/typescript-angular/bad/complaint.component.ts), and [score_board.component.ts](../../../samples/typescript-angular/bad/score_board.component.ts)).

Use these concrete fixes when refactoring large Angular components:
1. **Extract pure helpers & facades (`methods > 10`, `attributes > 7`, `total class CC > 25`):** Move search filtering, chart/score formatting, and multipart upload builders into injectable services or pure TypeScript helper functions.
2. **Trim method fan-out (`> 6` distinct external calls per method):** Group repeated snackbar/i18n/dialog calls behind a notification helper service so `ngOnInit` / `submit` coordinate `<= 6` calls cleanly.
3. **Add JSDoc (`/** ... */`) and return types on non-constructor methods:** Add `/** ... */` and `: void` / `: Observable<T>` on `ngOnInit`, event handlers, and helpers (`missing public docstring` costs `-6.0 pts` per method in modules).
4. **Replace `any` with explicit interfaces and remove `var`:** Typed component models and strict equality eliminate remaining TypeScript `Clean` penalties (`TypeScript Playbook`).

