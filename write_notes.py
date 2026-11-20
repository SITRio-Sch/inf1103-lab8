"""Generate Lab 9.docx: Predict-first notes, results, and reflection."""

from docx import Document

doc = Document()

doc.add_heading("INF1103 Lab 9 - Design Patterns and Error Handling", level=0)
doc.add_paragraph("RIO IZFIL BIN RENNIE - SIT-2610-INF1103")

doc.add_heading("1. Reviewed design patterns and error handling", level=1)
doc.add_paragraph(
    "Strategy moves one decision (which discount to apply) into a family of interchangeable "
    "classes behind an abstract DiscountStrategy. Order depends only on the abstract class, so a "
    "new discount is a new class, not an edit to Order - this keeps the Open/Closed Principle."
)
doc.add_paragraph(
    "Factory centralises object creation. ProductFactory.create() is the only place that knows "
    "the concrete product classes; everywhere else receives a Product, so adding a new product "
    "type changes one module instead of every creation site."
)
doc.add_paragraph(
    "Validation checks data before a rule is applied (if statements raising ValueError with a "
    "clear message, e.g. price must be greater than zero). Exception handling responds to an "
    "exception that already happened (try / except, e.g. catching FileNotFoundError). They "
    "complement each other: validation protects the invariants of a class; exception handling "
    "keeps the program alive around failures like bad input or a missing file."
)
doc.add_paragraph(
    "Automated tests (test_lab9.py, 17 tests) check the strategy and factory behaviour so the "
    "CI pipeline can confirm every push."
)

doc.add_heading("1.5 Diagnose the Lab 8 code before changing anything", level=2)
doc.add_paragraph(
    "(1) ifelif blocks: Lab 8 had no discount code, so the lecture's example (if discount_type "
    "== 'none' / elif 'percentage' / elif 'bulk' inside calculate_total()) is exactly what must "
    "not be written - it puts every discount decision inside Order. Section 2 instead moves the "
    "behaviour into DiscountStrategy classes, so Order's calculate_total only calls "
    "strategy.apply(total)."
)
doc.add_paragraph(
    "(2) Places creating PhysicalProduct or DigitalProduct directly: the create_oop_inventory() "
    "loop and the add_product() menu function in inventory_manager.py each built concrete "
    "classes with an if on the type string. Section 3 replaced both with ProductFactory.create(), "
    "so both loops now only see the base Product type."
)
doc.add_paragraph(
    "(3) Crash spot: add_product() used price = float(input('Price: ')) with no try, so typing "
    "'abc' crashed the program with ValueError. Section 5 replaced it with get_positive_float(), "
    "which catches the error and asks again; load_products() wraps file reading in try / except "
    "so a missing file or bad row no longer crashes."
)

doc.add_heading("2. Strategy pattern - Predict first answers", level=1)
doc.add_paragraph(
    "2.1 The simple if/elif version lives inside Order.calculate_total(). A 5% student discount "
    "would need a new elif branch and an extra discount_type value, so the class and method that "
    "must change are Order.calculate_total itself - editing existing code, which breaks OCP. "
    "With the Strategy version: the only thing that changes is a new DiscountStrategy subclass. "
    "StudentDiscount was added that way (Section 2.4) and Order was not edited; verified by "
    "test_student_discount_five_percent and test_new_strategy_needs_no_order_change, which uses "
    "a LoyaltyDiscount class defined only inside the test file."
)
doc.add_paragraph(
    "2.2 NoDiscount returns the total unchanged. PercentageDiscount(10) returns total * 0.90. "
    "BulkDiscount(200, 20) returns total - 20 only when total >= 200."
)
doc.add_paragraph(
    "2.3 Predicted: an order totalling 250 with BulkDiscount(200, 20) gives 230; with "
    "PercentageDiscount(10) it gives 225. Actual run (demo_lab9.py): 230.0 and 225.0 - matched."
)
doc.add_paragraph(
    "2.4 Extension: StudentDiscount (5% off) was added as a fifth subclass of DiscountStrategy in "
    "discount_strategy.py; Order needed no change - demo_lab9.py shows the same 250 order now "
    "returning 237.5. Prediction about the relationship: I first guessed composition. Looking at "
    "the code, strategies are created outside Order and passed in (or set later with "
    "set_discount), and two orders can share the same PercentageDiscount(20) object - the client "
    "owns the strategy's lifecycle, so the relationship is aggregation, not composition. Order "
    "uses exactly one DiscountStrategy (multiplicity 1). The only composed piece stays "
    "Order -> OrderLine, which Order creates itself. Prediction was wrong; I changed the answer "
    "to aggregation and drew it with an open diamond in uml_lab9."
)

doc.add_heading("3. Factory pattern - Predict first answers", level=1)
doc.add_paragraph(
    "3.2 Predicted: ProductFactory.create('service', ...) raises ValueError('Unknown product "
    "type: service'); the caller catches it, nothing changes, and the run continues instead of "
    "crashing. Actual run confirmed exactly that."
)
doc.add_paragraph(
    "3.3 Without the factory, adding BundleProduct would need edits in: the import list, the "
    "type branch in create_oop_inventory(), the type branch in add_product(), load_products(), "
    "and any isinstance checks - 5 places, every one breaking OCP. With the factory added, the "
    "change is one new class plus one branch inside ProductFactory.create() - a single place. "
    "This is acceptable because each change is explained by one new product type, and callers "
    "still only see Product (LSP holds)."
)

doc.add_heading("4. Validation vs exception handling", level=1)
doc.add_paragraph(
    "Validation is proactive: OrderLine raises ValueError('Quantity must be greater than zero.') "
    "before any state is stored; Product raises when price <= 0 or stock < 0. Exception handling "
    "is reactive: load_products catches ValueError from the factory and FileNotFoundError from "
    "open(). Rejection decision: a missing file kills the whole load (there is nothing to load), "
    "but a bad row only skips that row - valid products do not depend on invalid ones, so partial "
    "loading keeps the system usable. On the Lab 8 discussion: DigitalProduct should not allow "
    "negative stock because callers rely on the base Product guarantee; a subclass that loosens "
    "that rule breaks LSP."
)

doc.add_heading("5. Exception handling - Predict first answers", level=1)
doc.add_paragraph(
    "5.1 Predicted: entering abc prints 'Please enter a valid number, e.g. 12.50'; entering -5 "
    "prints 'Please enter a number greater than zero.'; 12.50 returns 12.5. Actual run matched "
    "exactly, including the repeated prompt."
)
doc.add_paragraph(
    "5.2 Predicted: 3 products load (P001, D001, P003); the service row is skipped with a "
    "message (unknown product type) and Office Chair is skipped (price 'abc' cannot become a "
    "number); else runs for an existing file, except runs for a missing file, and finally prints "
    "'Load attempt finished.' in both cases. Actual run confirmed all of it."
)

doc.add_heading("6. UML class diagram", level=1)
doc.add_paragraph(
    "uml_lab9.drawio / uml_lab9.png add DiscountStrategy (abstract, +apply(total)) with "
    "NoDiscount, PercentageDiscount, BulkDiscount and StudentDiscount inheriting from it. Order "
    "holds exactly one DiscountStrategy: an open diamond (aggregation, multiplicity 1) because "
    "the client creates the strategy and orders can share it. ProductFactory has a dashed "
    "dependency arrow labelled creates() to Product. The Section 1.5 diagnose notes informed "
    "these changes: the creation sites became a factory dependency instead of direct subclass "
    "coupling."
)

doc.add_heading("7. Testing and review", level=1)
doc.add_paragraph(
    "python -m pytest test_lab9.py: 17 passed, also inside the Docker container. Coverage: totals "
    "through strategies with no if/elif in Order, new strategies without changing Order "
    "(StudentDiscount and LoyaltyDiscount), set_discount swapping, factory creating both types and "
    "raising on unknown type and bad price, quantity / price / stock validation, "
    "get_positive_float looping, load_products skipping bad rows and handling a missing file."
)

doc.add_heading("8. Reflection", level=1)
doc.add_paragraph(
    "Where a pattern over-complicates: if the team project had only one discount behaviour, "
    "Strategy would be over-engineering - one if statement would be simpler and clearer. The "
    "Factory is genuinely worth it in my group project because physical and digital products "
    "already exist and new types are likely; the Strategy fits our project only once discounts "
    "or fulfilment behaviours actually vary."
)
doc.add_paragraph(
    "Validation failure vs exception example: price <= 0 is a validation failure (the object "
    "refuses to exist), while float('abc') raising inside get_positive_float is handled as an "
    "exception and turned into a retry prompt."
)
doc.add_paragraph(
    "Prediction that was wrong: Section 2.4 (composition vs aggregation). The assumption was that "
    "Order owns its discount; running the code showed strategies are supplied by the client and "
    "shared between orders, so I rewrote it as aggregation and updated the diagram."
)

doc.add_heading("9. Git and Docker workflow", level=1)
doc.add_paragraph(
    "git status -> git add . -> git commit -> git push origin: the Lab 9 code commit plus a "
    "submission-artifacts commit (notes, screenshots, UML) pushed to "
    "https://github.com/SITRio-Sch/inf1103-lab8.git. docker build -t inf1103-lab9 ., then "
    "docker run for the program, the demo, and pytest (17 passed). Screenshots of both "
    "workflows: git_workflow.png and docker_workflow.png."
)

doc.save("Lab 9.docx")
print("Lab 9.docx written")
