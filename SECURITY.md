# Security policy

## Reporting a vulnerability

Please report suspected StudyCanvas vulnerabilities privately by emailing [studycanvas.app@gmail.com](mailto:studycanvas.app@gmail.com) with the subject `StudyCanvas security report`.

Include:

- the affected page or feature
- the steps needed to reproduce the issue
- the impact you believe is possible
- screenshots or a minimal proof of concept, if safe to share
- whether you have already disclosed the issue anywhere else

Please do not include real student material, active session tokens, credentials or destructive proof in the report.

I will acknowledge the report, investigate it and keep you updated where contact details are available. Please allow time for a fix before public disclosure.

## In scope

- `https://studycanvas.app`
- authentication and access control
- StudyCanvas API routes
- document upload and conversion
- generated rich text, links and embedded content
- local workspace handling where application behaviour creates the risk
- paid-model endpoint abuse
- live voice token handling

## Out of scope

- social engineering
- denial-of-service testing that creates material load or cost
- automated scanning that ignores rate limits
- attacks against third-party services without a StudyCanvas-specific weakness
- issues requiring a compromised device, browser or external account
- model answers that are merely incorrect rather than security-relevant

## Safe harbour

Good-faith research that respects this policy, avoids privacy harm and does not disrupt the service is welcome. I ask that researchers stop once the issue is demonstrated, report it privately and avoid retaining data they do not own.
