from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os


# --- 1. FACTORY PATTERN ---

class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        pass


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card = details.get("card_number", "")
        cvv = details.get("cvv", "")
        return len(card) == 16 and len(cvv) == 3

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid card details"}
        fee = round(amount * 0.029, 2)
        return {"success": True, "method": "credit_card", "amount": amount + fee, "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        return len(details.get("iban", "")) >= 15

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        fee = 1.50
        return {"success": True, "method": "bank_transfer", "amount": amount + fee, "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        return "@" in details.get("email", "")

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        fee = round(amount * 0.034 + 0.30, 2)
        return {"success": True, "method": "paypal", "amount": amount + fee, "fee": fee}


class PaymentFactory:
    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor,
        }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_cls = self._processors.get(payment_type)
        if not processor_cls:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_cls()


# --- 2. BUILDER PATTERN ---

@dataclass
class Employee:
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    department: str = ""
    position: str = ""
    salary: float = 0.0
    has_laptop: bool = False
    has_parking: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False


class EmployeeBuilder:
    def __init__(self):
        self._employee = Employee()

    def with_name(self, first_name: str, last_name: str):
        self._employee.first_name = first_name
        self._employee.last_name = last_name
        return self

    def with_email(self, email: str):
        self._employee.email = email
        return self

    def with_job(self, department: str, position: str, salary: float):
        self._employee.department = department
        self._employee.position = position
        self._employee.salary = salary
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False):
        self._employee.has_laptop = laptop
        self._employee.has_parking = parking
        return self

    def with_access(self, vpn: bool = False, admin: bool = False):
        self._employee.has_vpn_access = vpn
        self._employee.has_admin_rights = admin
        return self

    def build(self) -> Employee:
        if not self._employee.first_name or not self._employee.last_name:
            raise ValueError("Name is required")
        if "@" not in self._employee.email:
            raise ValueError("Valid email is required")
        if self._employee.salary < 0:
            raise ValueError("Salary cannot be negative")
        return self._employee


class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        self.with_name(first_name, last_name)
        self.with_email(email)
        self.with_job("Engineering", "Developer", 60000)
        self.with_equipment(laptop=True)
        self.with_access(vpn=True)


# --- 3. SINGLETON PATTERN ---

class ConfigManager:
    _instance = None

    def __init__(self):
        self._config = self._load_config()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_config(self) -> dict:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return {
            "app": {"name": "PaymentPlatform", "debug": True},
            "database": {"host": "localhost", "port": 5432},
            "email": {"smtp_host": "smtp.company.com", "sender": "no-reply@company.com"},
            "payment": {"api_key": "sk_test_123456", "environment": "sandbox"},
        }

    def get(self, key: str):
        value = self._config
        for part in key.split("."):
            value = value[part]
        return value


if __name__ == "__main__":
    # Factory test
    factory = PaymentFactory()
    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    # Builder test
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    dev = DeveloperBuilder("Jane", "Smith", "jane@company.com").build()
    print(employee)
    print(dev)

    # Singleton test
    c1 = ConfigManager.get_instance()
    c2 = ConfigManager.get_instance()
    print("Same instance:", c1 is c2)
    print("DB host:", c1.get("database.host"))
