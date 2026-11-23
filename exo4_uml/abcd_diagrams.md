# Exo 2 - ABCD Records

## Use Case Diagram (Level 1 & 2)

```mermaid
flowchart LR
    Member[Member]
    NonMember[Non-Member]
    OrderClerk[Order Processing Clerk]
    CollectionClerk[Collection Dept Clerk]

    subgraph ABCD_Records_System[ABCD Records System]
        PO([Place Order])
        VM([Verify Membership])
        SMA([Send Membership Application])
        PRO([Process Order])
        AD([Apply Discount])
        OUI([Order Unavailable Items])
        MP([Make Payment])

        PO -.->|<<include>>| VM
        SMA -.->|<<extend>>| VM
        PRO -.->|<<include>>| MP
        AD -.->|<<extend>>| PRO
        OUI -.->|<<extend>>| PRO
    end

    Member --- PO
    Member --- MP
    NonMember --- PO
    OrderClerk --- PRO
    CollectionClerk --- MP
```

## Complete Class Diagram (Level 2)

```mermaid
classDiagram
    class Person {
        <<abstract>>
        #id: str
        #name: str
        #address: str
        #phone: str
    }
    class Member {
        -memberId: str
        -joinDate: Date
        +placeOrder()
        +getDiscount() float
    }
    class RegularMember
    class RoyalMember {
        -discountRate: float
        -priorityLevel: int
        +canOrderUnavailable() bool
    }
    class OrderProcessingClerk {
        -employeeId: str
        +verifyMembership()
        +processOrder()
        +printInvoice()
        +printShippingList()
    }
    class CollectionDeptClerk {
        -employeeId: str
        +processPayment()
    }
    class Order {
        -orderId: str
        -orderDate: Date
        -totalAmount: float
        -status: str
        +calculateTotal()
    }
    class OrderLine {
        -quantity: int
        -unitPrice: float
        +calculateLineTotal()
    }
    class Item {
        <<abstract>>
        #itemId: str
        #title: str
        #price: float
        #stockQuantity: int
        +checkAvailability() bool
    }
    class CD
    class Tape
    class DailyRecord {
        -recordDate: Date
        +addOrder()
    }
    class Invoice {
        -invoiceId: str
        -totalAmount: float
    }
    class ShippingList {
        -shippingId: str
    }
    class Payment {
        <<abstract>>
        #paymentId: str
        #amount: float
        +process()*
    }
    class CashPayment
    class CheckPayment
    class BankDraft

    Person <|-- Member
    Person <|-- OrderProcessingClerk
    Person <|-- CollectionDeptClerk
    Member <|-- RegularMember
    Member <|-- RoyalMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- CashPayment
    Payment <|-- CheckPayment
    Payment <|-- BankDraft

    Member "1" -- "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" -- "1" Item : references
    DailyRecord "1" o-- "0..*" Order : records
    Order "1" -- "1" Invoice : generates
    Order "1" -- "1" ShippingList : generates
    Order "1" -- "1" Payment : paid by
```

## Sequence Diagrams (Level 2 & 3)

### Scenario: Royal Member Orders 2 CDs (1 Unavailable) & Pays by Check
```mermaid
sequenceDiagram
    actor RoyalMember
    participant OrderProcessingClerk
    participant ItemFile
    participant Order
    participant CollectionDeptClerk

    RoyalMember->>OrderProcessingClerk: placeOrder(2 CDs)
    OrderProcessingClerk->>ItemFile: checkAvailability()
    ItemFile-->>OrderProcessingClerk: 1 available, 1 out of stock
    OrderProcessingClerk->>Order: createOrder(AWAITING_STOCK)
    OrderProcessingClerk->>Order: applyRoyalDiscount()
    OrderProcessingClerk-->>RoyalMember: invoice & shippingList
    RoyalMember->>CollectionDeptClerk: payByCheck()
    CollectionDeptClerk-->>RoyalMember: receipt
```

### Membership Verification (Success & Failure)
```mermaid
sequenceDiagram
    actor Sender
    participant OrderProcessingClerk
    participant MemberFile

    Sender->>OrderProcessingClerk: submitOrderForm()
    OrderProcessingClerk->>MemberFile: checkMember(id)
    alt Is Member
        MemberFile-->>OrderProcessingClerk: found (Royal or Regular)
        OrderProcessingClerk-->>Sender: proceedWithOrder()
    else Not a Member
        MemberFile-->>OrderProcessingClerk: notFound
        OrderProcessingClerk-->>Sender: sendMembershipApplication()
    end
```
