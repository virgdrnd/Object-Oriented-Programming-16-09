class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def get_discount(self):
        return 0.0


class RegularMember(Member):
    pass


class RoyalMember(Member):
    def get_discount(self):
        return 0.15


class Item:
    def __init__(self, title, price, stock):
        self.title = title
        self.price = price
        self.stock = stock


class CD(Item):
    pass


class Tape(Item):
    pass


class Order:
    def __init__(self, member):
        self.member = member
        self.items = []
        self.status = "PROCESSING"

    def add_item(self, item):
        if item.stock == 0 and not isinstance(self.member, RoyalMember):
            print(f"{item.title} unavailable for regular members.")
            return
        if item.stock == 0:
            self.status = "AWAITING_STOCK"
        self.items.append(item)

    def total(self):
        subtotal = sum(i.price for i in self.items)
        return subtotal * (1 - self.member.get_discount())


if __name__ == "__main__":
    royal = RoyalMember("M1", "Lucas")
    cd1 = CD("Album 1", 20.0, 5)
    cd2 = CD("Album 2", 18.0, 0)

    order = Order(royal)
    order.add_item(cd1)
    order.add_item(cd2)
    print(order.status, order.total())
