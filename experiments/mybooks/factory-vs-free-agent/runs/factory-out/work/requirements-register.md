---
task: LOCAL-1
created: 2026-11-12
ids: [R-1, R-2, R-3, R-4, R-5, R-6, R-7, R-8, R-9, R-10, R-11, R-12, R-13]
by_source: {story: 5, feature: 0, assumption: 0, discussion: 0, ac: 3, derived: 5}
confidence: low
---

## Register

| R | Requirement (one verifiable statement) | source | derived_from | verifiable | ac_ref | observable | impact | delta | code_says |
|---|---|---|---|---|---|---|---|---|---|
| R-1 | From the product page of an in-stock book, "Add to Cart" puts the book in the cart with its correct price and quantity 1 | ac | — | yes | AC-1 | current-code:../MyBooks/src/lib/services/cartService.ts:60 | blocked-flow | new | meets: XPANBFLFA-44 S3 |
| R-2 | An out-of-stock book cannot be added: the shopper sees an out-of-stock message and no cart item appears | ac | — | yes | AC-2 | current-code:../MyBooks/src/lib/services/cartService.ts:36 | degraded | new | contradicts: XPANBFLFA-44 S2 |
| R-3 | Adding a chosen quantity (e.g. 3) gives a cart line with that quantity and the correct subtotal | ac | — | yes | AC-3 | current-code:../MyBooks/src/lib/services/cartService.ts:103 | money | new | meets: XPANBFLFA-44 S3 |
| R-4 | The price in the cart is the backend's current price, shown in dollars with two decimals | story | — | yes | — | current-code:../MyBooks/src/lib/services/cartService.ts:103 | money | new | meets: XPANBFLFA-44 S1 |
| R-5 | A guest's cart persists between visits of the same browser (the note says cookies/local storage) | story | — | yes | — | current-code:../MyBooks/src/lib/session.ts:34 | data-loss | new | contradicts: XPANBFLFA-44 QA notes |
| R-6 | The three entry paths (product page, catalog card, wishlist "Move to cart") each put the book in the cart with the same result: one line, the book's price, quantity 1 (or +1 if already there) | story | — | yes | — | current-code:../MyBooks/src/components/pages/WishlistPage.tsx:48 | blocked-flow | new | meets: fact-8 |
| R-13 | After an add the cart is shown in two places: the header cart count (Navigation badge, hidden at 0) and the cart page lists the added line; both match the cart content | story | — | yes | — | current-code:../MyBooks/src/components/Navigation.tsx:58 | degraded | new | unknown: no fact speaks to the count refresh after an add |
| R-7 | The quantity of a book in the cart never exceeds its stock, also over repeated adds | derived | aspect:stock and quantity limits | yes | — | current-code:../MyBooks/src/lib/services/cartService.ts:44 | degraded | new | meets: fact-4 |
| R-8 | Quantity must be a whole number in an accepted range; any other value is refused and changes nothing | derived | aspect:inputs and validation | yes | — | current-code:../MyBooks/src/lib/validation/schemas.ts:41 | degraded | new | meets: fact-5 |
| R-9 | At sign-in the guest cart moves into the user's cart without losing items, within stock | story | — | yes | — | current-code:../MyBooks/src/lib/services/cartService.ts:118 | data-loss | new | unknown: merge rule (higher wins) is a code value, see Q3 |
| R-10 | Adding a book already in the cart keeps one line for it with the quantity increased, no duplicate line | derived | norm:no data loss on repeated action | yes | — | current-code:../MyBooks/src/lib/services/cartService.ts:53 | degraded | new | meets: fact-4 |
| R-11 | A failed add (unknown book, refused input, no stock) is shown as a failure with a stable error and leaves the cart unchanged | derived | aspect:failure and error paths | yes | — | current-code:../MyBooks/src/lib/services/cartService.ts:33 | degraded | new | meets: XPANBFLFA-44 S2 |
| R-12 | An add never touches another owner's cart: a guest and a user, or two guests, stay apart | derived | norm:no access beyond the owner | yes | — | current-code:../MyBooks/src/lib/cartOwner.ts:7 | access | new | unknown: no fact speaks to cross-owner isolation |

## Functions

| Function | Requirements |
|---|---|
| Add a book to the cart (detail page, card, wishlist) | R-1, R-2, R-3, R-6, R-7, R-8, R-10, R-11 |
| See correct price and subtotal | R-4, R-13 |
| Keep the cart across visit and sign-in | R-5, R-9, R-12 |

## Branches

| BN | R | kind | source_ref | text |
|---|---|---|---|---|
| BN-1 | R-2 | refusal | description | "Given the product is out of stock" (stock 0) |
| BN-2 | R-7 | refusal | derived | already in cart plus adding is more than stock |
| BN-3 | R-3 | partition | description | "Given I select quantity = 3": below stock, equal to stock, above stock; subtotal = price x quantity, rounding to cents not stated (Q6) |
| BN-4 | R-8 | partition | derived | quantity 0, 1, 999, 1000, negative, fractional, not a number; bookId missing, zero, unknown |
| BN-5 | R-6 | variant | description | "Все пути как товар может попасть в корзину": product page, catalog card, wishlist |
| BN-8 | R-13 | partition | description | places the cart is shown: header count at 0, at 1, at many (badge hidden at 0); cart page line; count after a refused add stays unchanged |
| BN-6 | R-5 | variant | description | guest (cookie) versus signed-in user (cart by user id); cookie cleared or absent |
| BN-7 | R-9 | variant | description | merge: book only in guest cart, in both carts, zero stock, guest quantity above stock |

## Source obligations

| unit | home |
|---|---|
| U-d005d6809f98, U-1f54492bfb0e, U-f73da26cba4d, U-e6de673adc84, U-dc444b1c438a, U-6316a94160a8, U-8a4394097b44 | not_obligation: process or context sentence of the task (how to judge a bug, where the code and stand are); it obliges no check by itself |
| U-8ead2ea468ac, U-a5529e19280c, U-4bcbba957fed, U-c74ea9dc9cd2, U-62a57892599d, U-b7607f964333, U-c0d6e1fc60a3, U-593307edeb9f, U-cf3b5cab2cc4, U-c625113cb4aa, U-e551641242ce, U-f685ed9a179b, U-bf2dc6bced27, U-dfdbc4e267c6, U-40aac3edb82c, U-ad332335cfaa, U-3a2dc0ae21eb, U-160b6cfb56c3, U-44216ba9e876, U-0c5f6ffd3d4c, U-8fd44fc97eaa, U-1bc2c19eca4a, U-1fcc2ab526ae, U-a38e3b535e35, U-aac7246f5e97, U-40d9971728bc, U-a0125c734d6f, U-81a2bd665c9c, U-b88fc4238ac6, U-0b47459a617e, U-1d12f99f3ea8, U-ca004a0c7c9c, U-0d7f7e6e3544, U-eaf00c54010d, U-53f6151e31c5, U-ba535da0a0e7, U-0afd8ef12c38, U-de185a6eb04e, U-707fe6d389cc, U-37456e42fb14, U-2a920aa0ec9c, U-c040aa38515a, U-a9258f9dcd89, U-9bc91d12d817, U-8d0e6b4ab605, U-7a51dea8a4bc, U-e9b73471b7fd, U-d890393d012b, U-df1a844b2c63, U-d3186ddb7531, U-9a3415cd5e4a, U-8c2e015dc34f, U-0072e6b93494, U-6b9265abaae2, U-bba36dc4ca79, U-fb40e4cf239c, U-e9e92cae6a8a, U-5c2c1ea7071c, U-c8e5998f6a39, U-40b2635b546c, U-fc7bb66f487e, U-1c6434cd7154, U-e388a7ddc91c, U-dbc5430f8bdd, U-d47d7cb0e4f8, U-79a05cf4b252, U-954a6d67469a, U-d03e16aef94e, U-eb8f0172dc84, U-b19ba1137c5a, U-ff389f25a232, U-0ac8b7915246, U-ca004b7a6ddf, U-e0f3ca352c35, U-a5a68ca32651 | not_obligation: README text about setup, stack, design or areas other than adding to the cart |
| U-b2f43810c08a, U-5d20a74e5b46 | R-6 |
| U-0a1ea0771f5d | R-9 |
| U-b59957799832 | R-11 |
| U-da4be4129ed2, U-b8ee65650297 | R-4 |
| U-a49372cb6656 | BN-5 |
| U-bb02a92a2dd4, U-96d72a6f1b5f, U-d8d339dd0b53, U-9ddc531dab7a, U-cb6a450259ea, U-a46a578c87ee, U-703f7064fd12, U-21f5df5577d8, U-ac57063e66a2, U-1db4c6f4232b, U-247ebce19ed9, U-2516ce586366, U-7dc5c9f95aee, U-de16c8902348, U-9a0fa70ec0a6, U-b4ad50ac7573, U-7552ecf2c124, U-5b46d6e40cff, U-2176b7b6686e, U-f706874a9340, U-eba8c1e4d0c7, U-0885754a92c2, U-abda877cebf8, U-914fa595f9ee, U-461f14bea09d, U-3fdd9f9912b3, U-4b269f74afa5, U-20c516a9f016, U-cdb91826e695, U-b386a3ea5080, U-c86515561889, U-f8e58900ad67, U-891580e69464, U-985c4758012b, U-e5cd316bc56f, U-568a7da5a047, U-4bf606c69131, U-a061cd2665fb, U-7bee15d7af2a, U-408f11c8cd22, U-ae955798cbff, U-2a31e5148f57, U-dc1defc25a69, U-61788538d7fe, U-d73c4132a7c2, U-87e7cc4e5b9a, U-f37ea4895f06, U-cc3bd5790da4, U-3879956deb53, U-348870dc2ac2, U-098d10cbc8c7, U-42cbe00db572, U-61d79dc9054c, U-1a93b928050c, U-90ca30f10872, U-e4f422f77f0d, U-17fad926948c, U-4d4cb3b0fcbb, U-ef6739bf967e, U-73d0e3791a87, U-e347e35ef0b3, U-22d379cd5ff6, U-70ab47081a57, U-b3fbacb08605, U-8a1f14fc3420, U-0bf6def0a43c, U-05f9ee8e4634, U-8573ba85b77d, U-9b3e55881da5, U-41eef79541ec, U-7304f944e0c8, U-c3681e84083f, U-e55fa5ab1188, U-aa4ea0d2997e, U-9fc1995f0d08, U-03e44d179ea4, U-06c7374e1d74, U-244b97010c14, U-f4e1f5bf9361, U-62367bcb5143, U-ac903a9f7909, U-891f15f060e1, U-d2fbca8581d3, U-9b5f26ed3b47, U-5f74d096b26b, U-8e27a982dd52, U-47cbb0c14c2b, U-ee5395b38358, U-e92372e2296b, U-7e9b393ab245, U-b48a2c006bde, U-d19689c10442, U-4a7f5195a026, U-df8d054687bc, U-3b5e1b9b5442, U-83abedac20da, U-ac897a1df683, U-6b9d61010a5c, U-e66aeb0ceedc, U-c470ccd6ebb9, U-1539b47203a7, U-d5a2090778ae, U-6233c7dde969, U-8ab55339305b, U-0613b019de05, U-38edfdd8583d, U-bc493477f647, U-2e406578fff3, U-c2c5b8a01b83, U-7cb6af3f3c81, U-4ad335301ef2, U-a8acad204d18, U-3fb294fa0b42, U-b176820977ab, U-f8e2092f8a61, U-cea8bd210851, U-ba8f920cf992, U-fdc7a2a48d62, U-33d34e6bcb0e, U-25e7062e416e, U-8dbe592e2fd8, U-ff53232978b6, U-8f36b6b03a7c, U-bc48012a10d4, U-ee6e50cb42c5, U-eb7230bab995, U-6f870f3eb8b0, U-6eaf6a17c2a7, U-db878f950b26, U-97244b0df423, U-96adca8a4d0b, U-e76b846a9c3a, U-f6d2779b5ba1, U-41aa72c61809, U-f03e1251fbb7, U-fed4a4b7d9e6, U-ab1c9ce1f7ba, U-b48bf62e891f, U-2bcd7dc3d481, U-48709b7fd557, U-a344de3226e9, U-d68a0c6d2840, U-38bda8ca9b4c, U-c8f74a3e4bf4, U-26bf8c621d56, U-0b55ec3d69be, U-c2e2d7600bcd, U-47191ddaeff6, U-db35699131ac, U-fe622dc65c96, U-adfe56a06ac1, U-e55118766a43, U-c37cda8c0664, U-eb7d1145802d, U-f0f33f9d627e, U-6b7e12f1fd2a, U-2e6d3df2e7c2, U-67b23860af66, U-7eb5a9bc004a, U-2d9002b8be4e, U-b6779d9bb467, U-ac5e31f7ddc8, U-58224b45c0d7, U-a08dce98ec5f, U-22a0a3c492e3, U-0becc185696a, U-b9486da6414a, U-21e98f0c95d7, U-3346742c6d37, U-01952083a034, U-5eb52991b2b7, U-6fffe9de98e2, U-d23d22551fe9, U-46a50dac9b0f, U-eacec96dd738, U-b4dafcc8c811, U-1785e187de11, U-57406a101e94, U-3fa1ca803b3f, U-6b2909c8bcca, U-5ecaada06433, U-a6e9b6e7fdce, U-fd728288cb02, U-fda538d81912, U-434b9ded4c42, U-28f56e306ee0, U-b28fb62a957f, U-542f4e9b9901, U-f19dd39fa79f, U-7db01e5e915e, U-df8737553740, U-dc9c3c089bfb | not_obligation: export metadata, markup or unrelated custom-field text of the done story, not a requirement |
| U-10ad6346f8c8, U-d9623e56e63b, U-a6ed51704d3b, U-cc9d4021bbcb, U-3b23178a70ce | R-1 |
| U-5ecbf6bf6379, U-5400c2ccfa9a, U-0d61bc2d670b | R-2 |
| U-e760a3b991b2, U-23b104e5d6a2, U-87faffd3cb03, U-8d2c4c27d676 | R-3 |
| U-ce821d74bc0b | R-5 |

## Contradiction matrix

| R | parent story/feature | comments & notes (ticket + parent) | area cases | area open bugs |
|---|---|---|---|---|
| R-1 | ok:XPANBFLFA-44 S3 | silent | n/a:no cart case in the area | n/a:none recorded |
| R-2 | contradicts:"Then I should see an "Out of stock" message and no item is added" (task/XPANBFLFA-44.xml); code says '"<title>" is out of stock' and the card button is disabled | silent | n/a:no cart case in the area | n/a:none recorded |
| R-3 | ok:XPANBFLFA-44 S3 | silent | n/a:no cart case in the area | n/a:none recorded |
| R-4 | ok:XPANBFLFA-44 S1 | silent | n/a:no cart case in the area | n/a:none recorded |
| R-5 | contradicts:"Ensure guest carts persist using cookies/local storage." (task/XPANBFLFA-44.xml); code: cookie only, no local storage | silent | n/a:no cart case in the area | n/a:none recorded |
| R-6 | silent | silent | n/a:no cart case in the area | n/a:none recorded |
| R-7 | silent | silent | ok:MB-cartRules-fits | n/a:none recorded |
| R-8 | silent | silent | n/a:no cart case in the area | n/a:none recorded |
| R-9 | silent | silent | ok:MB-cartRules-merge | n/a:none recorded |
| R-10 | silent | silent | n/a:no cart case in the area | n/a:none recorded |
| R-11 | silent | silent | n/a:no cart case in the area | n/a:none recorded |
| R-12 | silent | silent | n/a:no cart case in the area | n/a:none recorded |
| R-13 | silent | silent | n/a:no cart case in the area | n/a:none recorded |

## Behaviour claims

| R | before | before_ref | now | now_ref | differs | question | origin |
|---|---|---|---|---|---|---|---|
| R-8 | unknown | absent | integer 1..999 accepted, else refused | current-code:../MyBooks/src/lib/validation/schemas.ts:41 | unknown | Q5 | |
| R-10 | unknown | absent | repeat add sums into one line | current-code:../MyBooks/src/lib/services/cartService.ts:53 | unknown | Q5 | |
| R-11 | unknown | absent | failed add: stable error code, cart unchanged | current-code:../MyBooks/src/lib/services/cartService.ts:33 | unknown | Q5 | |
| R-12 | unknown | absent | cart rows selected by owner (user id or session id) | current-code:../MyBooks/src/lib/cartOwner.ts:7 | unknown | Q5 | |

## Reading forks

| R | Reading A | Reading B | Behavior difference | Decision |
|---|---|---|---|---|
| R-2 | the message text must be "Out of stock" | any out-of-stock message is fine | wording only; the card button is disabled so the click path never fires | Q1 a adopted until answered |
| R-5 | persistence by cookie is enough | local storage is also required | a cart survives only in the cookie jar | Q2 a adopted until answered |
| R-9 | merge keeps the higher quantity | merge adds the two quantities | guest 2 + user 3 gives 3 or 5 | Q3 a adopted until answered |

## Source completeness

| source | relation | relevance | assessment receipt | full-read receipt | revision/hash | status | gap or exclusion reason |
|---|---|---|---|---|---|---|---|
| SRC-5b289e26d85e2794df0a | task | relevant | work/sources/SRC-5b289e26d85e2794df0a | work/sources/SRC-5b289e26d85e2794df0a/c7faf8982724/ticket.json | sha256:c7faf8982724 | read | |
| SRC-eb279bc2d4fd95ef873b | normative | relevant | work/sources/SRC-eb279bc2d4fd95ef873b | work/sources/SRC-eb279bc2d4fd95ef873b/bfbae64801e7/ticket.json | sha256:bfbae64801e7 | read | |
| SRC-980ad6bf70a5c85f7c93 | normative | relevant | work/sources/SRC-980ad6bf70a5c85f7c93 | work/sources/SRC-980ad6bf70a5c85f7c93/618ad7ac3b24/ticket.json | sha256:618ad7ac3b24 | read | |
| XPANBFLFA-141..167 | referenced | unknown | none | none | none | unavailable | linked test tickets, tracker not reachable |

manifest_gap: ../MyBooks/src/components/Navigation.tsx:58 - looked for where the cart is shown after an add (header count badge, cart page); context-manifest.json records only the add paths, not the display components, so R-13 cites Navigation.tsx read in this repair.
