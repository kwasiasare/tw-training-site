---
course: cloud-security-engineer
title: Data Classification and Sensitivity Labels
month: 3
monthTitle: Data Security & AI Governance with Microsoft Purview
lesson: 1
summary: 'You cannot protect data you have not identified, so every Microsoft Purview data security control
  begins with classification. This lesson walks the full classification story: Sensitive Information Types
  (SITs) that pattern-match content such as credit card and national ID numbers, trainable classifiers
  that recognize categories like contracts by example, and sensitivity labels that carry protection such
  as encryption and content marking. You will build a custom employee-ID SIT from a regex with confidence
  and supporting evidence, then publish labels through label policies and auto-labeling policies that
  scan SharePoint, OneDrive, and Exchange. By the end you can design a classification taxonomy and decide
  where manual, recommended, and automatic labeling each belong.'
objectives:
- Explain how Purview classification underpins DLP, Insider Risk, and Copilot data protection
- Differentiate built-in versus custom Sensitive Information Types and the role of confidence and proximity
- Author a custom SIT from a regex with primary and supporting evidence and a confidence level
- Describe when to use trainable classifiers instead of pattern-based SITs
- Configure sensitivity labels with encryption, content marking, and label scope, then publish them via
  a label policy
- Compare manual, recommended, and automatic labeling and build an auto-labeling policy across M365 workloads
video: cse-m3-l01-data-classification-and-sensitivity-labels.mp4
quiz:
- q: Why is data classification the prerequisite for almost every other Purview data security control?
  options:
  - Because classification automatically encrypts every file in the tenant
  - Because controls like DLP, auto-labeling, and Copilot protection act on data that has first been identified
    and categorized
  - Because classification is required to license Microsoft 365
  - Because it replaces the need for Conditional Access
  answer: 1
  why: DLP rules, auto-labeling, Insider Risk indicators, and Copilot exclusions all key off classified
    content. If the platform cannot tell that a document holds a credit card number or carries a Confidential
    label, no downstream policy can act on it. Classification is the foundation the rest of the stack
    stands on.
- q: A custom Sensitive Information Type matches a 9-digit pattern but produces too many false positives
    on random invoice numbers. Which adjustment most directly raises precision?
  options:
  - Lower the confidence level so more matches are returned
  - Add supporting (corroborative) evidence such as keywords like 'Employee ID' within a proximity window
    and require it for a high-confidence match
  - Remove the regex and rely only on a trainable classifier
  - Publish the SIT to more locations
  answer: 1
  why: Precision improves when the primary pattern must be corroborated by supporting evidence (keywords)
    found within a defined character proximity. Requiring that keyword evidence for the high-confidence
    match suppresses bare 9-digit numbers that lack the surrounding context of a real employee ID.
- q: When is a trainable classifier a better choice than a Sensitive Information Type?
  options:
  - When the data is a fixed, well-structured pattern like a 16-digit card number
  - When you need to recognize a category of content by its language and style, such as contracts or harassment,
    that has no reliable regex
  - When you only want to match exact dictionary terms
  - When you need the result instantly with no training data
  answer: 1
  why: SITs excel at structured patterns (card numbers, NHS or SSN formats). Trainable classifiers learn
    from sample documents to recognize fuzzy categories such as source code, contracts, or resumes that
    have no dependable regex. The trade-off is that a classifier must be trained and tested on examples
    before publishing.
- q: Two sensitivity labels could both apply to a document via different auto-labeling policies. How does
    Purview decide which one wins?
  options:
  - The label created most recently always wins
  - Both labels are applied at once
  - Label priority (order in the list) determines precedence; the higher-priority label is applied and
    only one label applies at a time
  - The label with encryption is always skipped
  answer: 2
  why: A file carries at most one sensitivity label at a time. Labels have a priority order, and the higher-priority
    (typically more restrictive) label takes precedence when more than one could apply. Understanding
    ordering is essential when designing overlapping auto-labeling policies.
- q: What is the practical effect of a sensitivity label that applies encryption with a 'Co-Author' permission
    set scoped to your finance team?
  options:
  - Anyone with the file link can open and edit it
  - The protection travels with the file, and only the assigned finance users get the granted rights even
    if the file leaves the tenant
  - The file is deleted after 30 days
  - Only content marking (a footer) is added with no access control
  answer: 1
  why: Label-applied encryption uses Azure Rights Management, so the usage rights are bound to the content
    itself. Wherever the file travels, only the assigned identities receive the granted rights (such as
    co-author), which is why labels protect data even outside the tenant boundary.
- q: Your organization wants users to label most documents themselves but wants Purview to suggest a label
    when a file clearly contains regulated data, without forcing it. In two to four sentences, explain
    how manual, recommended, and automatic labeling differ and which combination fits this requirement.
  answer: Manual labeling lets users pick a label from the bar themselves, recommended labeling shows
    a policy tip suggesting a specific label when matching content is detected but leaves the final choice
    to the user, and automatic labeling applies a label with no user interaction based on conditions.
    The requirement is best met by enabling manual labeling as the default and adding a recommended-labeling
    condition (for example, when a financial or PII SIT is detected) so users are prompted but retain
    control. You can later add service-side auto-labeling policies for high-confidence cases where user
    discretion is not needed.
  why: The scenario explicitly wants user discretion preserved while nudging correct behavior, which is
    exactly the recommended-labeling pattern layered on top of manual labeling, with automatic labeling
    reserved for cases that should not depend on a user's choice.
resources:
- label: Learn about sensitivity labels
  url: https://learn.microsoft.com/en-us/purview/sensitivity-labels
- label: Learn about sensitive information types
  url: https://learn.microsoft.com/en-us/purview/sit-sensitive-information-type-learn-about
- label: Create a custom sensitive information type
  url: https://learn.microsoft.com/en-us/purview/create-a-custom-sensitive-information-type
- label: Apply a sensitivity label automatically
  url: https://learn.microsoft.com/en-us/purview/apply-sensitivity-label-automatically
---

## Classification Is the Foundation

Every data protection control you will build in this module, DLP rules, Insider Risk indicators, and Copilot guardrails, depends on one thing: the platform knowing **what** a piece of content is. Microsoft Purview answers that question through **data classification**. If Purview can recognize that a spreadsheet holds credit card numbers, or that a document carries a `Confidential` label, then downstream policies can encrypt it, block its sharing, or hide it from Copilot. If it cannot, nothing else can act. So we start here.

Classification in Purview has three engines that work together:

- **Sensitive Information Types (SITs)** - pattern matchers for structured data.
- **Trainable classifiers** - machine-learned recognizers for fuzzy categories.
- **Sensitivity labels** - the durable tags that carry protection and travel with the data.

## Sensitive Information Types: Built-in and Custom

A **SIT** detects a specific kind of content, usually by a regular expression plus corroborating evidence. Microsoft ships hundreds of **built-in SITs**: U.S. Social Security Number, credit card number (validated with the Luhn checksum), IBAN, passport and national ID numbers for dozens of countries, and more. You can use these immediately in DLP and auto-labeling.

When your data is organization-specific, you build a **custom SIT**. A SIT match is more than a regex; it is tuned with:

- **Primary element** - the core pattern (the regex or a keyword list).
- **Supporting / corroborative evidence** - additional keywords or patterns that must appear nearby.
- **Proximity** - how many characters apart the primary and supporting evidence may be (default 300).
- **Confidence level** - low, medium, or high, reflecting how much corroboration was required.

More corroboration means higher precision (fewer false positives) at the cost of recall. You typically reference the **high confidence** match in production policies.

## Worked Example: A Custom Employee-ID SIT

Suppose every employee ID at Contoso looks like `EMP-` followed by 6 digits, e.g. `EMP-004217`. A bare regex would also fire on unrelated strings, so we add supporting keywords.

```text
Primary pattern (regex):   EMP-\d{6}
Supporting keywords:       "employee id", "emp id", "staff number", "personnel"
Proximity:                 300 characters
Confidence:                High = regex match AND a supporting keyword within proximity
                           Medium = regex match alone
```

In the Purview portal you go to **Data classification > Classifiers > Sensitive info types > Create**, define the **primary element** with the regex, add a **supporting elements** group containing the keyword list, set the **character proximity**, and assign the **confidence level** for each combination. Always use **Test** with sample text before publishing: paste a few real-looking and decoy strings and confirm the high-confidence rule only fires when a keyword is present.

## Trainable Classifiers

Some content has no reliable pattern. There is no regex for "this is a legal contract" or "this is source code" or "this looks like harassment." For these, Purview offers **trainable classifiers**. Microsoft provides many **pre-trained** classifiers (Resumes, Source Code, Contracts, Threat, Profanity, and more) that are ready to use. For organization-specific categories you create a **custom trainable classifier**: you feed it 50+ positive sample documents, let it learn, then **test** it against a separate set and review its accuracy before publishing. Use a classifier when you are categorizing by meaning and style rather than by a fixed format; use a SIT when the data is structured.

## Sensitivity Labels and Label Policies

A **sensitivity label** is a persistent, human-readable tag, for example `Public`, `General`, `Confidential`, `Highly Confidential`, that can also enforce protection. A label can:

- **Encrypt** content (via Azure Rights Management), binding usage rights such as view or co-author to specific users or groups, so protection travels with the file even outside the tenant.
- **Apply content marking** - headers, footers, and watermarks (e.g. a `CONFIDENTIAL` footer).
- **Control container, meeting, and site settings**, and govern access for groups and SharePoint sites.

Labels are organized in a priority-ordered list and may have **sublabels**. A file carries **one label at a time**; when more than one could apply, the **higher-priority** label wins. Labels also have a **scope** (items, groups and sites, schematized data assets), which decides where they can be used.

Labels do nothing until **published**. A **label policy** publishes a chosen set of labels to specific users and groups and configures behavior such as a **default label**, whether a **justification** is required to lower a label, and whether labeling is **mandatory**.

## Manual, Recommended, and Automatic Labeling

There are three ways a label gets applied:

- **Manual** - the user selects a label from the Sensitivity bar in Office apps. Maximum user control, depends on user diligence.
- **Recommended** - when a label policy detects matching content (e.g. a financial SIT), the app shows a **policy tip** suggesting a label, but the user decides. A good balance of guidance and control.
- **Automatic** - the label is applied with no user interaction. This happens **client-side** (in Office apps as the user works) or **service-side** via an **auto-labeling policy**.

## Auto-Labeling Policies Across M365

**Auto-labeling policies** run in the service and scan content at rest and in transit across **SharePoint, OneDrive, and Exchange**. You define **conditions** (which SITs or trainable classifiers, at what confidence, and a minimum instance count) and the **label** to apply. Best practice is to run the policy in **simulation mode** first: Purview reports which items *would* be labeled so you can validate accuracy and tune conditions before turning enforcement on. Once confident, you enable the policy and it labels existing and new matching content. Combined with client-side automatic labeling, this gives you coverage for both data being created and the large back catalog of data already sitting in your tenant, which is exactly the readiness work that later makes DLP and Copilot protection effective.
