// Decode the SWA-injected authenticated user from the x-ms-client-principal header.
// Returns null when the request is anonymous.
function getUser(request) {
  const header = request.headers.get('x-ms-client-principal');
  if (!header) return null;
  try {
    const principal = JSON.parse(Buffer.from(header, 'base64').toString('utf8'));
    if (!principal || !principal.userId) return null;
    return {
      userId: principal.userId,
      userDetails: principal.userDetails,
      roles: principal.userRoles || [],
    };
  } catch {
    return null;
  }
}

module.exports = { getUser };
