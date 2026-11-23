from abc import ABC, abstractmethod
import json


# --- 1. STRATEGY PATTERN ---

class FormatStrategy(ABC):
    extension = ".txt"

    @abstractmethod
    def format(self, data: list[dict]) -> str:
        pass


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def format(self, data: list[dict]) -> str:
        lines = ["PDF REPORT", "=" * 40]
        for item in data:
            lines.append(f"{item['name']:20} | {item['value']:10} |")
        lines.append("=" * 40)
        return "\n".join(lines)


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def format(self, data: list[dict]) -> str:
        lines = ["EXCEL REPORT", "Name\tValue"]
        for item in data:
            lines.append(f"{item['name']}\t{item['value']}")
        return "\n".join(lines)


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def format(self, data: list[dict]) -> str:
        lines = ["name,value"]
        for item in data:
            lines.append(f"{item['name']},{item['value']}")
        return "\n".join(lines)


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def format(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    extension = ".html"

    def format(self, data: list[dict]) -> str:
        rows = "".join(f"<tr><td>{i['name']}</td><td>{i['value']}</td></tr>" for i in data)
        return f"<table>{rows}</table>"


class ReportGenerator:
    def __init__(self, data: list[dict]):
        self.data = data
        self._strategy: FormatStrategy | None = None

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if not self._strategy:
            raise ValueError("No strategy set")
        return self._strategy.format(self.data)

    def save_report(self, filename: str) -> None:
        content = self.generate_report()
        with open(filename + self._strategy.extension, "w") as f:
            f.write(content)


# --- 2. TEMPLATE METHOD PATTERN ---

class DataPipeline(ABC):
    def __init__(self, source: str):
        self.source = source
        self.data: list[dict] = []

    def run(self) -> str:
        self.connect()
        self.extract()
        self.transform()
        self.validate()
        self.load()
        self.cleanup()
        return f"{self.__class__.__name__} finished"

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def extract(self) -> None:
        pass

    @abstractmethod
    def transform(self) -> None:
        pass

    def validate(self) -> None:
        if not self.data:
            raise ValueError("No data extracted")
        print(f"Validated {len(self.data)} records")

    def load(self) -> None:
        print(f"Loaded {len(self.data)} records to destination")

    def cleanup(self) -> None:
        self.data = []
        print("Cleanup complete")


class CSVPipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to CSV: {self.source}")

    def extract(self) -> None:
        self.data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def transform(self) -> None:
        for row in self.data:
            row["name"] = row["name"].upper()


class APIPipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to API: {self.source}")

    def extract(self) -> None:
        self.data = [{"user_id": 101, "score": 92}]

    def transform(self) -> None:
        for row in self.data:
            row["grade"] = "A" if row["score"] >= 90 else "B"


class DatabasePipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to DB: {self.source}")

    def extract(self) -> None:
        self.data = [{"product_id": 501, "price": 1200}]

    def transform(self) -> None:
        for row in self.data:
            row["tax"] = row["price"] * 0.2


class XMLPipeline(DataPipeline):
    def connect(self) -> None:
        print(f"Connecting to XML: {self.source}")

    def extract(self) -> None:
        self.data = [{"order_id": 1, "status": "paid"}]

    def transform(self) -> None:
        for row in self.data:
            row["status"] = row["status"].upper()


if __name__ == "__main__":
    # Strategy test
    data = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000}]
    gen = ReportGenerator(data)
    gen.set_strategy(PDFFormatStrategy())
    print(gen.generate_report())
    gen.set_strategy(HTMLFormatStrategy())
    print(gen.generate_report())

    print("\n---\n")

    # Template Method test
    for pipeline in [
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ]:
        print(pipeline.run())
