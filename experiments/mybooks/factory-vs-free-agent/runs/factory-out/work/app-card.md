routes and data to walk with; expectations come only from the case's Thens
## Stand
- API: http://localhost:3000
- Frontend: http://localhost:3000
## Entry routes
- Read in the application repository `../MyBooks` (second pass):
- Stack: Next.js 14 (App Router), React 18, TypeScript, Tailwind, Prisma 5 with PostgreSQL, NextAuth credentials with JWT sessions, zod, Vitest.
- Screens: home and catalog, book detail, cart, checkout, orders, profile, wishlist, register, login, email verification, password reset, admin.
- API routes under `src/app/api/`: account, addresses, admin, auth, books, cart (with merge, total and item routes), categories, checkout/quote, health, openapi, orders, push, register, reviews, shipping-methods, test, wishlist. The contract is `docs/openapi.json`.
- Data: about 20 Prisma models (User, Book, CartItem, Order, OrderItem, OrderEvent, Category, PromoCode, Address, Payment, Review, WishlistItem, EmailOutbox, AuthToken, AuditLog and others) and 16 migrations.
- Cart code: `src/lib/cartRules.ts`, `src/lib/cartOwner.ts`, `src/app/api/cart/*`, `src/components/pages/CartPage.tsx`.
- Test support: `/api/test/*` (reset, seed, emails, push) exist only when `ENABLE_TEST_ENDPOINTS=true`, guarded by the `x-test-secret` header; otherwise they answer 404. They are product code, not tests.
- Mail: Mailpit catches mail (UI at `http://localhost:8025`).
- Payment: a mock provider (test cards are in `../MyBooks/TEST_IDS_REFERENCE.md`).
- Runtime provenance: `/api/health` answers 200. No build identifier was found: unknown.
- not known: work/flow-requests.json lists no request
## First look
not known: there was no first look: the stand was not walked (no stand)
## Sign-in
- Sign-in route: /login; fields: username field "", password field "", submit field ""
Sign-in: not proven at gate A — sign in with fill-account
## Accounts
- Accounts: --as default; --as "admin", --as "user" (names only)
- Env keys: EMAIL_USER, EMAIL_PASS, USER_EMAIL, USER_PASSWORD, TEST_SECRET
- Default account: keys EMAIL_USER / EMAIL_PASS in .env (`--as default`; names only)
## Test data
- Accounts by role: a seeded admin (`EMAIL_USER` / `EMAIL_PASS`) and a seeded regular user (`USER_EMAIL` / `USER_PASSWORD`), created by the stand's fixed seed.
- Seeds: the fixed seed (38 books, 8 categories, the two accounts), restored by the reset.
- Generators: none; a test creates what it needs through the UI or the API.
- Real data and masking: all data is synthetic. There is no real data and no PII.
- Cleanup: a test removes what it creates when it can. The factory resets the stand when it needs a clean state. Nobody else resets it.
- Shared records: books, categories and the two seeded accounts. Anything else a test creates itself.
- config test_data.accounts_by_role: Seeded admin (EMAIL_USER/EMAIL_PASS) and regular user (USER_EMAIL/USER_PASSWORD), created by the stand's fixed seed
- config test_data.seeds: Fixed seed (38 books, 8 categories, two accounts) restored by the stand reset command; no data factories
- config test_data.generators: none; a test creates what it needs through the UI or API
- config test_data.pii_and_masking: All data is synthetic; no real data and no PII
- config test_data.cleanup_owner: A test removes what it creates when it can; the factory resets the stand with the reset command when it needs a clean state; nobody else
- config test_data.shared_records: 3 items
## Page objects
not known: work/briefs/repo-map-07f6ebdcc3.md names no page object or helper module
## Notes from walkers
not known: no walker has left a note yet (work/app-card-notes.jsonl)
inputs: 5e07406face9b8ade99e80fe
