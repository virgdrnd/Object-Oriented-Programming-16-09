from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET


# --- 1. ADAPTER PATTERN ---

class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy_generator: LegacyReportGenerator):
        self.legacy = legacy_generator

    def generate(self, data: dict) -> str:
        xml_str = self.legacy.generate_report(data)
        root = ET.fromstring(xml_str)
        parsed = {child.tag: child.text for child in root}
        return json.dumps(parsed)


# --- 2. DECORATOR PATTERN ---

class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base order ({self.base_price}€)"


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()


class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 15.0

    def get_description(self) -> str:
        return self._order.get_description() + " + Express Shipping"


class InsuranceDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return round(self._order.get_cost() * 1.05, 2)

    def get_description(self) -> str:
        return self._order.get_description() + " + Insurance (5%)"


class GiftWrapDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 5.0

    def get_description(self) -> str:
        return self._order.get_description() + " + Gift Wrap"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float = 15):
        super().__init__(order)
        self.percent = percent

    def get_cost(self) -> float:
        return round(self._order.get_cost() * (1 - self.percent / 100), 2)

    def get_description(self) -> str:
        return self._order.get_description() + f" - Discount ({self.percent}%)"


class PremiumMemberDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return round(self._order.get_cost() * 0.90, 2)

    def get_description(self) -> str:
        return self._order.get_description() + " - Premium (10%)"


if __name__ == "__main__":
    # Adapter test
    dashboard = AnalyticsDashboard()
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    json_report = report_generator.generate({"total_sales": 150000, "orders": 1234})
    dashboard.display(json_report)

    print("\n---\n")

    # Decorator test
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost()}€")
