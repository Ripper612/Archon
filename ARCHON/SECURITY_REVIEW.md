# 🔒 Archon Security Review

**Review Date:** 2025-10-12
**Reviewer:** AI Security Audit
**Repository:** cursor-archon/ARCHON
**Version:** Beta (from GitHub stable branch)

---

## 📋 Executive Summary

This security review identifies vulnerabilities in the Archon knowledge management system installation. **4 critical issues** require immediate attention, particularly regarding credential exposure and encryption weaknesses. The codebase demonstrates good security practices in input validation and SQL injection prevention, but needs hardening for production deployment.

**Overall Security Posture:** ⚠️ **DEVELOPMENT-SAFE / PRODUCTION-RISKY**

### Risk Overview
- 🔴 **Critical Issues:** 2 (API key exposure, weak encryption)
- 🟠 **High Severity:** 3 (CORS misconfiguration, Docker socket, no Git repo)
- 🟡 **Medium Severity:** 4 (authentication, file uploads, rate limiting, secrets management)
- 🟢 **Low Severity:** 2 (security headers, logging)
- ✅ **Strengths:** 6 (encryption at rest, input validation, SQL safety)

---

## 🚨 CRITICAL ISSUES

### 1. API Keys Exposed in `.env` File

**Severity:** 🔴 CRITICAL
**Location:** `C:\cursor\cursor-archon\ARCHON\.env`
**CWE:** CWE-798 (Use of Hard-coded Credentials)

#### Issue
Your `.env` file contains fully visible API keys in plaintext:
- **Supabase Service Key** (lines 7, 9)
- **OpenAI API Key** (line 15)
- **Supabase API Key (anon)** (line 8)

```env
# ACTUAL FILE CONTENT (REDACTED FOR THIS REPORT)
SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
OPENAI_API_KEY="sk-proj--RMWhSZ..."
```

#### Risk Assessment
- **Impact:** Complete compromise of Supabase database and OpenAI account
- **Likelihood:** HIGH if file is committed to Git or shared
- **Exploitability:** Trivial (read file = full access)

#### Attack Scenarios
1. **Git History Leak:** If committed, keys are permanently in repository history
2. **Backup Exposure:** Backup files may contain plaintext credentials
3. **Shared Access:** Anyone with machine access can read these keys
4. **Accidental Sharing:** Copy/paste of directory contents exposes keys

#### Immediate Actions Required

```bash
# Step 1: Check if .env was committed to Git
cd /c/cursor/cursor-archon/ARCHON
git log --all --full-history -- .env

# Step 2: If committed, IMMEDIATELY rotate credentials:
# - Supabase: Dashboard → Settings → API → Regenerate service_role key
# - OpenAI: Platform → API Keys → Revoke & create new key

# Step 3: Verify .env is in .gitignore
grep "^\.env$" .gitignore

# Step 4: If .env was committed, purge from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Step 5: Force push to remote (if repository exists)
git push origin --force --all
```

#### Long-term Solution
Use environment-specific secret management:
- **Development:** `.env` (gitignored)
- **Production:** Docker secrets, AWS Secrets Manager, or HashiCorp Vault

---

### 2. Weak Encryption Key Derivation

**Severity:** 🔴 CRITICAL
**Location:** `python/src/server/services/credential_service.py:84-97`
**CWE:** CWE-330 (Use of Insufficiently Random Values)

#### Issue
The encryption salt is **static and hardcoded** in the source code:

```python
# Line 93: STATIC SALT FOR ALL INSTALLATIONS!
salt=b"static_salt_for_credentials",
```

#### Why This Is Critical
1. **Same salt across all Archon installations worldwide**
2. **If Supabase service key leaks, ALL encrypted API keys can be decrypted**
3. **No key rotation mechanism exists**
4. **Salt is visible in public GitHub repository**

#### Attack Scenario
```python
# Attacker with your Supabase service key can:
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

# Use PUBLIC values from GitHub
service_key = "YOUR_LEAKED_SUPABASE_KEY"
salt = b"static_salt_for_credentials"  # From source code

# Derive encryption key
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                 salt=salt, iterations=100000)
key = base64.urlsafe_b64encode(kdf.derive(service_key.encode()))
fernet = Fernet(key)

# Decrypt ALL your encrypted credentials from database
decrypted = fernet.decrypt(encrypted_api_key_from_db)
```

#### Remediation

**Option A: Unique Salt Per Installation (Recommended)**
```python
# credential_service.py:_get_encryption_key()
def _get_encryption_key(self) -> bytes:
    """Generate encryption key with unique salt."""
    service_key = os.getenv("SUPABASE_SERVICE_KEY")

    # Get unique salt from environment or generate
    salt_b64 = os.getenv("ENCRYPTION_SALT")
    if not salt_b64:
        raise ValueError(
            "ENCRYPTION_SALT must be set in environment. "
            "Generate with: python -c 'import os, base64; "
            "print(base64.b64encode(os.urandom(32)).decode())'"
        )

    salt = base64.b64decode(salt_b64.encode())

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,  # Unique per installation
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(service_key.encode()))
```

**Generate Salt:**
```bash
# Generate unique salt for your installation
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"

# Add to .env (example output):
# ENCRYPTION_SALT=7KZ8x3Q9mN2pL5vR8wT4yU6hG1jF3sA9bC0eD7fK2mN=
```

**Option B: Hardware Security Module (Production)**
- Use AWS KMS, Azure Key Vault, or HashiCorp Vault
- Keys never leave the HSM
- Automatic key rotation

---

## 🟠 HIGH SEVERITY ISSUES

### 3. No Git Repository Initialized

**Severity:** 🟠 HIGH
**Location:** Root directory
**CWE:** CWE-1004 (Sensitive Cookie Without 'HttpOnly' Flag) - analogous issue

#### Issue
Your Archon working directory is **not a Git repository**, despite having `.gitignore` files present. This creates risk of:
- Accidental credential commits
- No version control for security patches
- Inability to audit changes

#### Verification
```bash
$ cd /c/cursor/cursor-archon/ARCHON
$ git status
fatal: not a git repository (or any of the parent directories): .git
```

#### Immediate Action
```bash
cd /c/cursor/cursor-archon/ARCHON

# Initialize repository
git init

# Verify .env is excluded BEFORE any commits
git add * --dry-run | grep ".env"
# Should return NOTHING

# Create initial commit
git add .gitignore
git add .
git commit -m "Initial commit - verified no secrets"

# Verify no secrets in first commit
git show HEAD | grep -i "sk-proj\|eyJ"
# Should return NOTHING
```

---

### 4. CORS Allows All Origins

**Severity:** 🟠 HIGH
**Location:** `python/src/server/main.py:156-162`
**CWE:** CWE-942 (Permissive Cross-domain Policy)

#### Issue
CORS middleware allows **ANY website** to make requests to your Archon API:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ ALLOWS ANY DOMAIN!
    allow_credentials=True,  # ⚠️ WITH CREDENTIALS!
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Attack Scenario
1. Attacker creates malicious website `evil.com`
2. User visits `evil.com` while Archon is running
3. JavaScript on `evil.com` makes requests to `http://localhost:8181`
4. API keys, knowledge base content extracted via CSRF

#### Risk Matrix
| Archon Running | Browser | Risk Level |
|----------------|---------|------------|
| localhost:8181 | Same machine | CRITICAL |
| localhost:8181 | Different machine | Low |
| Public IP | Any | CRITICAL |

#### Remediation

**Development Configuration:**
```python
# main.py
ALLOWED_ORIGINS = [
    "http://localhost:3737",  # Frontend UI
    "http://127.0.0.1:3737",
    os.getenv("ARCHON_UI_URL", "http://localhost:3737"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=3600,  # Cache preflight for 1 hour
)
```

**Production Configuration:**
```python
# Use environment variable for production URLs
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3737").split(",")

# Example .env:
# ALLOWED_ORIGINS=https://archon.yourdomain.com,https://app.yourdomain.com
```

---

### 5. Docker Socket Mounted in Container

**Severity:** 🟠 HIGH
**Location:** `docker-compose.yml:35`
**CWE:** CWE-250 (Execution with Unnecessary Privileges)

#### Issue
The `archon-server` container has **full access** to the Docker daemon:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock  # FULL DOCKER CONTROL!
```

#### Why This Is Dangerous
1. **Container Escape:** Can create privileged containers to escape to host
2. **Access All Containers:** Can read secrets from other containers
3. **Access All Volumes:** Can mount and read any Docker volume
4. **Host Compromise:** Can run commands on host via Docker exec

#### Proof of Concept
```bash
# From inside archon-server container:
docker run --rm -v /:/host alpine cat /host/etc/shadow
# → Full access to host filesystem
```

#### Risk Assessment
- **Likelihood:** LOW (requires container compromise first)
- **Impact:** CRITICAL (full host system compromise)
- **Attack Vector:** RCE vulnerability in Archon → Docker access → host root

#### Remediation Options

**Option A: Remove If Not Needed (Best)**
```yaml
# docker-compose.yml - remove this line entirely
volumes:
  # - /var/run/docker.sock:/var/run/docker.sock  # REMOVED
  - ./python/src:/app/src  # Keep source mount
```

**Option B: Docker Socket Proxy (Good)**
```yaml
services:
  docker-proxy:
    image: tecnativa/docker-socket-proxy
    environment:
      CONTAINERS: 1  # Allow only container operations
      POST: 0        # No create/start/stop
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  archon-server:
    environment:
      DOCKER_HOST: tcp://docker-proxy:2375
    # No socket mount needed
```

**Option C: Rootless Docker (Acceptable)**
```bash
# Run Docker in rootless mode
dockerd-rootless-setuptool.sh install

# Socket at: /run/user/$(id -u)/docker.sock
```

**Decision Matrix:**
| Feature Needed | Recommendation |
|----------------|----------------|
| MCP container control | Option B (proxy) |
| Read-only container info | Option B (proxy) |
| No Docker features | Option A (remove) |

---

## 🟡 MEDIUM SEVERITY ISSUES

### 6. No Authentication on API Endpoints

**Severity:** 🟡 MEDIUM
**Location:** All `python/src/server/api_routes/*.py`
**CWE:** CWE-306 (Missing Authentication)

#### Issue
**Zero authentication** on all API endpoints:
- `/api/credentials` - Read encrypted API keys metadata
- `/api/knowledge-items` - Access knowledge base
- `/api/knowledge-items/crawl` - Start expensive crawl operations
- `/api/settings` - Modify system configuration

#### Current Design Philosophy
Archon is beta software designed for **single-user local deployment**. Authentication is not implemented because:
1. Runs on `localhost` only
2. Assumes trusted user environment
3. No multi-user support planned for beta

#### Risk in Current Setup
- **LOW** if accessed only via `localhost` on your machine
- **MEDIUM** if exposed on home network
- **CRITICAL** if exposed to internet

#### When Authentication Is Required
- Exposing Archon beyond localhost
- Multi-user access
- Integration with untrusted clients
- Production deployment

#### Future Implementation (Post-Beta)
```python
# middleware/auth.py
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    valid_key = await credential_service.get_credential("ARCHON_API_KEY")
    if api_key != valid_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Apply to all routes
app.include_router(settings_router, dependencies=[Depends(verify_api_key)])
```

---

### 7. File Upload Risks

**Severity:** 🟡 MEDIUM
**Location:** `python/src/server/api_routes/knowledge_api.py:894-973`
**CWE:** CWE-434 (Unrestricted Upload of File with Dangerous Type)

#### Issues Identified
1. **No file size limits** - Can cause disk space exhaustion
2. **No MIME type validation** - Trusts Content-Type header
3. **No malware scanning** - Could upload malicious files

#### Current Mitigations ✅
- Only text extraction (no execution)
- Content stored in database (not filesystem)
- Pydantic validation on metadata

#### Attack Scenarios
| Attack | Current Risk | Mitigation Needed |
|--------|-------------|-------------------|
| DoS via large files | MEDIUM | File size limit |
| Malicious PDF with exploits | LOW | Text-only extraction |
| Billion laughs XML | LOW | No XML processing |
| Zip bombs | LOW | No archive handling |

#### Recommendations

```python
# knowledge_api.py:upload_document
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}

async def upload_document(file: UploadFile = File(...), ...):
    # Read file with size limit
    file_content = await file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB")

    # Validate actual MIME type (not just header)
    import magic
    actual_mime = magic.from_buffer(file_content, mime=True)

    if actual_mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, f"Unsupported file type: {actual_mime}")

    # Continue with text extraction...
```

---

### 8. No Rate Limiting

**Severity:** 🟡 MEDIUM
**Location:** All expensive operations
**CWE:** CWE-770 (Allocation of Resources Without Limits)

#### Vulnerable Endpoints
| Endpoint | Resource Cost | Risk |
|----------|--------------|------|
| `/api/knowledge-items/crawl` | High CPU/network | DoS |
| `/api/documents/upload` | High CPU/storage | DoS |
| `/api/rag/query` | OpenAI API calls | Cost |
| `/api/rag/code-examples` | Database scans | Performance |

#### Current Protection
```python
# knowledge_api.py:54
CONCURRENT_CRAWL_LIMIT = 3  # Semaphore limit
```
✅ Prevents more than 3 concurrent crawls (good!)

#### Missing Protection
- **No per-user limits**
- **No time-based limits** (requests per hour)
- **No API key cost tracking**

#### Recommendation

```python
# Install: pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Apply to expensive operations
@app.post("/api/knowledge-items/crawl")
@limiter.limit("5/hour")  # 5 crawls per hour
async def crawl_knowledge_item(request: Request, ...):
    ...

@app.post("/api/rag/query")
@limiter.limit("100/hour")  # 100 queries per hour
async def perform_rag_query(request: Request, ...):
    ...
```

---

### 9. Secrets in Docker Environment Variables

**Severity:** 🟡 MEDIUM
**Location:** `docker-compose.yml:20-31`
**CWE:** CWE-526 (Exposure of Sensitive Information)

#### Issue
API keys passed as environment variables are visible via:
```bash
docker inspect archon-server | grep -i "OPENAI_API_KEY"
# Returns full API key!
```

#### Attack Scenario
1. Attacker gains non-root access to host
2. Runs `docker inspect` (requires Docker group membership)
3. Extracts all API keys from environment

#### Current Configuration
```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY:-}  # Visible in inspect
  - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}  # Visible in inspect
```

#### Best Practice: Docker Secrets

```yaml
# Create secrets files
secrets:
  openai_api_key:
    file: ./secrets/openai_api_key.txt
  supabase_service_key:
    file: ./secrets/supabase_service_key.txt

services:
  archon-server:
    secrets:
      - openai_api_key
      - supabase_service_key
    environment:
      - SUPABASE_URL=${SUPABASE_URL}  # Non-sensitive OK
```

```python
# Read secrets in application
def get_secret(secret_name):
    with open(f"/run/secrets/{secret_name}") as f:
        return f.read().strip()

openai_key = get_secret("openai_api_key")
```

**Benefits:**
- Not visible in `docker inspect`
- Not in process environment
- Can use encrypted secrets in Swarm mode

---

## 🟢 LOW SEVERITY ISSUES

### 10. Missing Security Headers

**Severity:** 🟢 LOW
**Location:** `python/src/server/main.py`
**CWE:** CWE-693 (Protection Mechanism Failure)

#### Issue
No security headers configured for HTTP responses.

#### Missing Headers
| Header | Purpose | Risk if Missing |
|--------|---------|----------------|
| X-Content-Type-Options | Prevent MIME sniffing | XSS |
| X-Frame-Options | Prevent clickjacking | UI redress |
| X-XSS-Protection | Browser XSS filter | XSS (legacy) |
| Strict-Transport-Security | Force HTTPS | MITM |
| Content-Security-Policy | Prevent XSS/injection | XSS |

#### Implementation

```python
# main.py - Add middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # Enable browser XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Force HTTPS (if using HTTPS)
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:;"
    )

    return response
```

---

### 11. Potential Logging of Sensitive Data

**Severity:** 🟢 LOW
**Location:** Various `api_routes/*.py` files
**CWE:** CWE-532 (Insertion of Sensitive Information into Log File)

#### Current Status: ✅ Mostly Safe

**Good Practices Found:**
- API keys not logged in error messages ✅
- Provider error sanitization ✅ (`ProviderErrorFactory.sanitize_provider_error()`)
- Credential keys logged, not values ✅

#### Minor Issue
URLs logged in full, may contain tokens:
```python
# knowledge_api.py:750
safe_logfire_info(f"Starting crawl | url={str(request.url)}")
# If URL is: https://api.example.com?token=SECRET123
# Token gets logged!
```

#### Recommendation
```python
from urllib.parse import urlparse, parse_qs

def sanitize_url_for_logging(url: str) -> str:
    """Remove sensitive query parameters from URLs."""
    parsed = urlparse(url)
    # Remove all query parameters for safety
    return parsed._replace(query="").geturl()

# Usage
safe_logfire_info(f"Starting crawl | url={sanitize_url_for_logging(request.url)}")
```

---

## ✅ SECURITY STRENGTHS

### What Archon Does Well

#### 1. Encryption at Rest ✅
**Location:** `credential_service.py:99-124`

- API keys encrypted with **Fernet** (AES-128 CBC + HMAC)
- **PBKDF2** key derivation with 100,000 iterations
- Encrypted values stored in database, not plaintext

```python
# Cryptography library (industry standard)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
```

**Note:** Weakened by static salt (see Critical Issue #2)

---

#### 2. Supabase Service Key Validation ✅
**Location:** `config.py:52-93`

Prevents common misconfiguration:
```python
# Decodes JWT to check role claim
role = decoded.get("role")
if role == "anon":
    raise ConfigurationError(
        "CRITICAL: You are using a Supabase ANON key instead of SERVICE key"
    )
```

**Prevents:**
- Using public anon key (read-only)
- Permission denied errors
- Accidental key exposure

---

#### 3. HTTPS Enforcement ✅
**Location:** `config.py:95-135`

```python
def validate_supabase_url(url: str) -> bool:
    # Require HTTPS for production
    if parsed.scheme == "http":
        # Allow HTTP only for localhost/private IPs
        if hostname in ["localhost", "127.0.0.1", "host.docker.internal"]:
            return True
        raise ConfigurationError("Must use HTTPS for non-local environments")
```

**Benefits:**
- Prevents accidental HTTP in production
- Allows localhost development
- Validates private IP ranges (RFC 1918)

---

#### 4. Input Validation ✅
**Location:** All API routes use Pydantic models

```python
class KnowledgeItemRequest(BaseModel):
    url: str
    knowledge_type: str = "technical"
    max_depth: int = 2  # Validated range

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v
```

**Protections:**
- Type validation
- Range checking
- Format validation
- JSON parsing safety

---

#### 5. SQL Injection Protection ✅
**Location:** All database operations

Uses Supabase client with parameterized queries:
```python
# ✅ SAFE - Parameterized
query.eq("source_id", source_id)

# ✅ SAFE - Builder pattern
supabase.table("archon_settings").select("*").eq("key", key).execute()

# ❌ UNSAFE (not found in codebase)
# supabase.rpc("SELECT * FROM table WHERE id = " + user_input)
```

**No SQL injection vectors found in entire codebase.**

---

#### 6. Error Handling ✅
**Location:** Throughout codebase

- Fails fast on security errors
- Doesn't expose stack traces to clients
- Logs errors server-side only

```python
except Exception as e:
    logger.error(f"Error details: {e}", exc_info=True)  # Server logs
    raise HTTPException(500, detail={"error": "Operation failed"})  # Client gets generic message
```

---

## 🛡️ SECURITY HARDENING ROADMAP

### Phase 1: IMMEDIATE (Today)

**Priority:** 🔴 Critical

1. **Verify .env Git Status**
   ```bash
   cd /c/cursor/cursor-archon/ARCHON
   git log --all -- .env
   # If any results: ROTATE ALL CREDENTIALS
   ```

2. **Initialize Git Repository**
   ```bash
   git init
   git add .gitignore
   git status | grep .env  # Should NOT appear
   git add .
   git commit -m "Initial commit - verified no secrets"
   ```

3. **Generate Unique Encryption Salt**
   ```bash
   python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
   # Add output to .env as: ENCRYPTION_SALT=<generated_value>
   ```

4. **Restrict CORS Origins**
   - Edit `main.py` line 157
   - Change `allow_origins=["*"]` to `["http://localhost:3737"]`

---

### Phase 2: HIGH PRIORITY (This Week)

**Priority:** 🟠 High

5. **Evaluate Docker Socket Mount**
   - Determine if MCP container control is needed
   - If NO: Remove line 35 from `docker-compose.yml`
   - If YES: Implement Docker socket proxy (see Issue #5)

6. **Add File Upload Limits**
   ```python
   # knowledge_api.py:894
   MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
   if len(file_content) > MAX_FILE_SIZE:
       raise HTTPException(413, "File too large")
   ```

7. **Implement Rate Limiting**
   ```bash
   cd python
   uv pip install slowapi
   ```
   - Add limiter to `main.py`
   - Protect crawl, upload, query endpoints

---

### Phase 3: MEDIUM PRIORITY (This Month)

**Priority:** 🟡 Medium

8. **Migrate to Docker Secrets**
   ```bash
   mkdir -p secrets
   echo "$OPENAI_API_KEY" > secrets/openai_api_key.txt
   chmod 600 secrets/openai_api_key.txt
   ```
   - Update `docker-compose.yml` to use secrets
   - Modify `credential_service.py` to read from `/run/secrets/`

9. **Add Security Headers**
   - Implement middleware in `main.py` (see Issue #10)
   - Test with: `curl -I http://localhost:8181`

10. **URL Sanitization in Logs**
    - Implement `sanitize_url_for_logging()` function
    - Apply to all URL logging statements

---

### Phase 4: ONGOING

**Priority:** 🔵 Maintenance

11. **Regular Security Audits**
    - Review logs weekly for suspicious activity
    - Update dependencies monthly
    - Monitor Supabase access logs

12. **Credential Rotation Schedule**
    - Rotate OpenAI key: Every 90 days
    - Rotate Supabase key: Every 180 days
    - Document rotation in calendar

13. **Dependency Updates**
    ```bash
    # Check for security updates
    cd python
    uv pip list --outdated

    # Update critical security dependencies
    uv pip install --upgrade cryptography supabase fastapi
    ```

---

## 📋 QUICK REFERENCE CHECKLIST

### Pre-Deployment Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in Git history
- [ ] `ENCRYPTION_SALT` environment variable set
- [ ] CORS origins restricted to frontend URL
- [ ] Docker socket mount removed or proxied
- [ ] File upload size limits implemented
- [ ] Rate limiting configured
- [ ] Security headers middleware added
- [ ] Docker secrets used for production
- [ ] All dependencies up to date
- [ ] Supabase RLS policies reviewed
- [ ] Backup encryption verified

### Incident Response Checklist

**If API keys are compromised:**

1. **Immediate (5 minutes):**
   - [ ] Rotate compromised key in provider dashboard
   - [ ] Update `.env` with new key
   - [ ] Restart Archon services

2. **Short-term (1 hour):**
   - [ ] Review Supabase logs for unauthorized access
   - [ ] Review OpenAI usage logs for anomalies
   - [ ] Check for data exfiltration

3. **Long-term (1 day):**
   - [ ] Audit all API keys
   - [ ] Review Git history for exposure point
   - [ ] Implement additional monitoring

### Monthly Security Review

- [ ] Review Supabase database access logs
- [ ] Check OpenAI API usage for anomalies
- [ ] Update all Python dependencies
- [ ] Scan logs for failed authentication attempts
- [ ] Verify backup encryption
- [ ] Test disaster recovery procedure

---

## 📞 SECURITY CONTACTS & RESOURCES

### Reporting Security Issues

**Archon Project:**
- GitHub Issues: https://github.com/coleam00/archon/issues
- Security Email: (Check project README for contact)

**Dependencies:**
- Supabase: security@supabase.io
- OpenAI: security@openai.com
- FastAPI: https://github.com/tiangolo/fastapi/security

### Useful Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CWE Database:** https://cwe.mitre.org/
- **Docker Security:** https://docs.docker.com/engine/security/
- **Python Security:** https://python.readthedocs.io/en/latest/library/security_warnings.html

---

## 📝 REVIEW NOTES

### Scope Limitations

This review **did not include:**
- Frontend React application security
- Supabase database security configuration
- Network security (firewall rules, VPN)
- Host operating system hardening
- Physical security considerations
- Third-party MCP server security

### Methodology

- **Static code analysis** of Python backend
- **Configuration review** of Docker setup
- **Dependency audit** of Python packages
- **Threat modeling** of API endpoints
- **Best practices comparison** against OWASP guidelines

### Next Review

Recommended: **90 days** from today (2025-01-10)

---

**End of Security Review**
**Document Version:** 1.0
**Last Updated:** 2025-10-12
