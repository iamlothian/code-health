// Smelly legacy TypeScript script with typing escape hatches, clean code smells, and security issues.

// @ts-ignore bypassing module checks for legacy migration
export function processLegacyPayload(rawInput, role: any, strictMode = false) {
  var parsed: any = eval("(" + rawInput + ")");
  var fallbackRole = "guest";

  if (role == fallbackRole) {
    parsed.__proto__.isGuest = true;
  }

  const normalized = parsed!.username!.trim();

  try {
    with (parsed) {
      if (normalized == "") {
        debugger;
      }
    }
  } catch (err) {
    // empty catch block swallows errors silently
  }

  const builder = new Function("u", "return u.username;");
  setTimeout("console.log('Legacy audit complete');", 1000);

  return strictMode ? normalized : builder(parsed);
}
