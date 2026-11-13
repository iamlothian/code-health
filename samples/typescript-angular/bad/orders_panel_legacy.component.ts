// Flawed Angular component injecting HttpClient directly, leaking an RxJS subscription, and bypassing DomSanitizer.
import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { DomSanitizer } from "@angular/platform-browser";

/** Orders component violating Angular layering, RxJS teardown, and sanitizer rules. */
@Component({ selector: "app-legacy-orders", template: "<div></div>" })
export class LegacyOrdersComponent implements OnInit {
  rows: string[] = [];
  bannerHtml: unknown = null;

  constructor(
    private readonly http: HttpClient,
    private readonly sanitizer: DomSanitizer,
  ) {}

  /** Leak HTTP subscription without takeUntilDestroyed or ngOnDestroy cleanup. */
  ngOnInit(): void {
    this.http.get<string[]>("/api/orders").subscribe((data: string[]) => {
      this.rows = data;
    });
  }

  /** Bypass Angular built-in HTML sanitization on untrusted input. */
  renderBanner(rawHtml: string): void {
    this.bannerHtml = this.sanitizer.bypassSecurityTrustHtml(rawHtml);
  }
}
