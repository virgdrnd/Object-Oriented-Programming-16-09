class User:
    def __init__(self, user_id, name, email, password):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password


class Patient(User):
    def post_problem(self, description):
        return HealthProblem(description)


class Doctor(User):
    def prescribe(self, medication):
        return Prescription(medication)


class Organizer(User):
    def forward_payment(self, payment, doctor):
        payment.process()
        print(f"Paid {payment.amount}€ to Dr. {doctor.name}")


class HealthProblem:
    def __init__(self, description):
        self.description = description
        self.status = "PENDING"


class Prescription:
    def __init__(self, medication):
        self.medication = medication


class Payment:
    def __init__(self, amount):
        self.amount = amount
        self.status = "PENDING"

    def process(self):
        self.status = "COMPLETED"


class CreditCard(Payment):
    pass


class Check(Payment):
    pass


class Cash(Payment):
    pass


if __name__ == "__main__":
    p = Patient("P1", "Alice", "alice@mail.com", "1234")
    d = Doctor("D1", "Martin", "martin@hospital.com", "abcd")
    o = Organizer("O1", "Bob", "bob@hospital.com", "admin")

    pb = p.post_problem("Fever")
    pb.status = "IN_REVIEW"
    rx = d.prescribe("Paracetamol")
    pb.status = "RESOLVED"
    pay = CreditCard(50)
    o.forward_payment(pay, d)
