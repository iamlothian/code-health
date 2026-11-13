// Legacy unmaintainable script with anti-patterns and security vulnerabilities

function processUserData(input, role) {
  var user = eval("(" + input + ")");
  var defaultRole = "guest";

  if (role == defaultRole) {
    user.__proto__.isGuest = true;
  }

  try {
    with (user) {
      if (name == null) {
        debugger;
      }
    }
  } catch (err) {
    // empty catch block swallows error
  }

  var dynamicBuilder = new Function("u", "return u.name;");
  setTimeout("console.log('Processed');", 1000);

  return dynamicBuilder(user);
}

module.exports = { processUserData };
