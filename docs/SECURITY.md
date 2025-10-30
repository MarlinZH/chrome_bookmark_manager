# Security Policy

## Credential Storage

### Encryption

The AI Bookmark Manager uses **AES-GCM encryption** to protect your sensitive credentials (Notion API tokens and database IDs) stored in Chrome's local storage.

#### How It Works

1. **Key Generation**: A unique encryption key is generated for each installation using:
   - The Chrome extension ID (unique per installation)
   - A salt value
   - SHA-256 hashing
   - The result is used to create an AES-256-GCM key

2. **Encryption Process**:
   - When you save credentials, they are encrypted using AES-GCM
   - A random 96-bit IV (Initialization Vector) is generated for each encryption
   - The IV and encrypted data are combined and stored as Base64

3. **Decryption Process**:
   - When retrieving credentials, the IV is extracted
   - The data is decrypted using the same key
   - Original plaintext is returned

### Important Security Notes

⚠️ **Limitations**:

1. **Not Zero-Knowledge**: The encryption key is derived from the extension ID, which means:
   - Anyone with access to your Chrome profile can decrypt the data
   - This is NOT end-to-end encryption
   - This protects against casual browsing but not determined attackers with profile access

2. **Physical Access**: If someone has physical access to your computer and Chrome profile, they can potentially access your credentials.

3. **Profile Sync**: If you sync your Chrome profile, encrypted data may sync across devices, but the key derivation is per-installation.

### Best Practices

✅ **Recommended Actions**:

1. **Use Integration Tokens, Not Personal Tokens**
   - Create a dedicated Notion integration for this extension
   - Don't use your personal Notion API token

2. **Limit Integration Permissions**
   - Only grant the integration access to specific databases
   - Use Notion's sharing settings to restrict access

3. **Rotate Tokens Regularly**
   - Change your integration tokens periodically
   - Revoke old tokens after updating

4. **Lock Your Computer**
   - Always lock your computer when stepping away
   - Use a strong user password

5. **Don't Share Your Chrome Profile**
   - Keep your Chrome profile private
   - Use separate Chrome profiles for different purposes

6. **Clear Credentials When Not Needed**
   - Use the "Clear" button to remove stored credentials
   - Re-enter them only when needed

### Comparison to Plain Storage

**Without Encryption** (previous versions):
- Credentials stored as plain text
- Readable by any script or extension
- Visible in Chrome DevTools
- Easy to extract

**With Encryption** (current version):
- Credentials encrypted with AES-256-GCM
- Requires decryption key to read
- Not visible in DevTools
- Significantly harder to extract

### Technical Details

```javascript
// Encryption algorithm
Algorithm: AES-GCM
Key Length: 256 bits
IV Length: 96 bits (12 bytes)
Key Derivation: SHA-256 hash of (Extension ID + Salt)
```

## Reporting Security Issues

If you discover a security vulnerability, please email the maintainer or create a private security advisory on GitHub. Do not create public issues for security vulnerabilities.

### What to Report

- Encryption weaknesses
- Credential leakage
- XSS vulnerabilities
- Unauthorized data access
- Any security-related bugs

## Updates and Patches

Security updates will be released as soon as possible after a vulnerability is confirmed. Always keep your extension updated to the latest version.

## Additional Resources

- [Web Crypto API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [Chrome Extension Security](https://developer.chrome.com/docs/extensions/mv3/security/)
- [Notion API Security](https://developers.notion.com/docs/authorization)

## License

This security documentation is part of the AI Bookmark Manager project and is subject to the same license terms.