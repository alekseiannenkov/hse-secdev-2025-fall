# BDD приемочные сценарии (Gherkin)

## Feature: JWT expiration (NFR-02)
Scenario: Token expires after TTL
  Given user obtains an access token now with exp = now + 24h
  When 24 hours pass
  Then any request with this token returns 401 unauthorized

Scenario: Expired token is rejected (negative)
  Given a token with exp in the past
  When I call GET /wishes
  Then response status is 401
  And body.error.code = "unauthorized"

## Feature: Owner-only access (NFR-03)
Scenario: Foreign wish access forbidden
  Given user A owns wish X
  And user B is authenticated
  When user B GETs /wishes/X
  Then response status is 403
  And body.error.code = "forbidden"

Scenario: Owner can read own wish
  Given user A owns wish X
  When user A GETs /wishes/X
  Then response status is 200

## Feature: Price validation (NFR-04)
Scenario: Negative price is rejected
  When user creates a wish with price_estimate = -1
  Then response status is 422
  And body.error.code = "validation_error"

Scenario: Empty price is allowed
  When user creates a wish without price_estimate
  Then response status is 201

## Feature: Error contract (NFR-05)
Scenario: Not found item
  When I GET /items/999
  Then response status is 404
  And response body contains "error.code = not_found"

Scenario: Validation error
  When I POST /items with name=""
  Then response status is 422
  And response body contains "error.code = validation_error"

## Feature: Rate limiting on auth (NFR-09)
Scenario: Too many login attempts (negative)
  Given 61 requests/min from one IP to POST /auth/login with wrong password
  When the 61st request is processed
  Then response status is 429
