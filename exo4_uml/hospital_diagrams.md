# Exo 1 - Hospital Management System

## Task 1 - Basic Class Diagram
Patient submits health problems, Organizer acts as intermediary and consults Doctor.

```mermaid
classDiagram
    class Patient {
        -idPatient: int
        -name: str
        -password: str
        -age: int
        +pay()
        +sendHealthProblem()
    }
    class Doctor {
        -idDoctor: int
        -name: str
        -specialization: str
        +providePrescription()
        +analyzeHealthProblem()
    }
    class Organizer {
        -idOrganizer: int
        -name: str
        -passwordSystem: str
        +readHealthProblem()
        +consultDoctor()
        +sendPrescription()
        +forwardPayment()
    }

    Patient "0..*" -- "1..*" Organizer : contacts
    Patient "0..*" -- "0..*" Doctor : consults
    Doctor "1..*" -- "0..*" Organizer : advises
```

## Task 2 - Complete Class Diagram & Sequence Diagram

```mermaid
classDiagram
    class Patient {
        -id: str
        -name: str
        -email: str
        -password: str
        +login()
        +postProblem()
        +viewPrescription()
        +makePayment()
    }
    class Doctor {
        -id: str
        -name: str
        -specialization: str
        -password: str
        +login()
        +viewProblem()
        +prescribeSolution()
    }
    class Organizer {
        -id: str
        -name: str
        -password: str
        +login()
        +readProblem()
        +sendPrescription()
        +collectFee()
        +payDoctor()
        +createMember()
        +updateSystem()
    }
    class HealthProblem {
        -idHealthProblem: str
        -type: str
        -date: Date
        -symptoms: str
    }
    class Prescription {
        -idPrescription: str
        -amount: float
        -date: Date
        -medication: str
    }
    class Payment {
        <<abstract>>
        #idPayment: str
        #date: Date
        #location: str
        +pay()*
    }
    class CreditCard
    class Check
    class Cash

    Payment <|-- CreditCard
    Payment <|-- Check
    Payment <|-- Cash

    Patient "1" -- "0..*" HealthProblem : submits
    Organizer "1" -- "0..*" HealthProblem : manages
    Doctor "1" -- "0..*" HealthProblem : analyzes
    Doctor "1" -- "0..*" Prescription : writes
    HealthProblem "1" -- "0..*" Prescription : receives
    Patient "1" -- "0..*" Payment : makes
    Organizer "1" -- "0..*" Payment : processes
    Payment "0..*" -- "1" Doctor : forwarded to
```

```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor

    Patient->>Organizer: submitProblem()
    Organizer->>Doctor: consult()
    Doctor-->>Organizer: providePrescription()
    Organizer-->>Patient: sendPrescription()
    Patient->>Organizer: makePayment()
    Organizer-->>Patient: validated
    Organizer->>Doctor: forwardPayment()
    Doctor-->>Organizer: wellReceived
```

## Task 3 - Advanced Class Diagram & System Sequence Diagrams

```mermaid
classDiagram
    class User {
        <<abstract>>
        #id: str
        #name: str
        #email: str
        #password: str
        +login()
        +logout()
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class PaymentStatus {
        <<enumeration>>
        PENDING
        COMPLETED
        FAILED
    }
    class Patient {
        -address: str
        -phone: str
        +postProblem()
        +viewPrescription()
        +makePayment()
    }
    class Doctor {
        -specialization: str
        -licenseNumber: str
        +viewProblem()
        +prescribeSolution()
    }
    class Organizer {
        -role: str
        +readProblem()
        +forwardToDoctor()
        +sendPrescription()
        +payDoctor()
        +createMember()
    }
    class HealthProblem {
        -id: str
        -description: str
        -datePosted: Date
        -status: ProblemStatus
    }
    class Prescription {
        -id: str
        -medication: str
        -dateIssued: Date
        -previousPrescriptions: List
    }
    class Payment {
        <<abstract>>
        #id: str
        #amount: float
        #date: Date
        #status: PaymentStatus
        +process()*
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Payment <|-- CreditCard
    Payment <|-- Check
    Payment <|-- Cash

    Patient "1" -- "0..*" HealthProblem : submits
    Organizer "1" -- "0..*" HealthProblem : manages
    Doctor "1" -- "0..*" Prescription : creates
    HealthProblem "1" -- "0..*" Prescription : receives
    Patient "1" -- "0..*" Payment : makes
    Payment "0..*" -- "1" Doctor : paid to
```

### 1. Patient Registration
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Database

    Patient->>Organizer: requestRegistration()
    Organizer->>Database: checkEmail()
    Database-->>Organizer: available
    Organizer->>Database: createPatientRecord()
    Database-->>Organizer: created
    Organizer-->>Patient: sendCredentials(id, password)
```

### 2. Consultation Flow
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    participant Database

    Patient->>Organizer: postProblem()
    Organizer->>Database: saveProblem(PENDING)
    Organizer->>Organizer: updateStatus(IN_REVIEW)
    Organizer->>Doctor: forwardProblem()
    Doctor->>Doctor: createPrescription()
    Doctor-->>Organizer: prescriptionReady
    Organizer->>Database: updateStatus(RESOLVED)
    Organizer-->>Patient: sendPrescription()
```

### 3. Payment Processing
```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Payment
    participant Doctor

    Patient->>Organizer: requestPayment()
    alt Cash
        Patient->>Organizer: payCash()
    else Check
        Patient->>Organizer: submitCheck()
    else Credit Card
        Patient->>Organizer: submitCard()
        Organizer->>Payment: processCard()
        Payment-->>Organizer: success
    end
    Organizer-->>Patient: paymentReceipt
    Organizer->>Doctor: transferPayment()
    Doctor-->>Organizer: paymentReceived
```
