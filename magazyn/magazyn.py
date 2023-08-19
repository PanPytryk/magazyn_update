import json
from typing import Any


program_status = True


template: dict[str, int | float] = {
    "price": 0,
    "amount": 0
}


def get_json_file_data(file_name: str):
    with open(f"{file_name}.json", "r") as read_file:
        return json.load(read_file)


def update_json_file_data(file_name: str, data: Any):
    with open(f"{file_name}.json", "w") as write_file:
        json.dump(data, write_file, indent=4, sort_keys=True)

company: dict[str, Any] = get_json_file_data("company")


history: list[dict[str, str | float | int]] = company["history"]
warehouse: dict[str, dict[str, int | float]] = company["warehouse"]
account: dict[str, float] = company["account"]


def update_balance(value: float):
    record: dict[str, str | float | int] = {
            "type": "account",
            "balance": account["balance"]
        }

    if account["balance"] + value >= 0:
        account["balance"] += value

        record["new_balance"] = account["balance"]
        history.append(record)
        return True

    
    else:
        print("Brak wystarczających środków na koncie")
        return False


def purchase(product_name: str, price: float, amount: int):
    if update_balance((-1)*amount*price):
        product: dict[str, int | float] = warehouse.get(product_name, template.copy())

        product["amount"] += amount
        product["price"] = price
        warehouse[product_name] = product

        history.append(
            {
                "type": "purchase",
                "product_name": product_name,
                "price": product["price"],
                "balance": account["balance"]
            }
        )

def disposal(product_name: str, amount: int, product: dict[str, int | float]):
    if amount <= product["amount"]:
        product["amount"] -= amount
        warehouse[product_name] = product
        update_balance(amount*product["price"])

        history.append(
            {
                "type": "disposal",
                "product_name": product_name,
                "price": product["price"],
                "balance": account["balance"]
            }
        )
    else:
        print("Brak wystarczającej liczby sztuk produktu na stanie")
        

def get_product(product_name: str):
    return warehouse.get(product_name)


def get_account():
    history.append(
        {
            "type": "account",
            "balance": account["balance"]
        }
    )
    print("Stan konta: ", account.get("balance"))


def get_history(range_l: int, range_r: int) -> list[dict[str, str | float]]:
    return history[range_l:range_r]


def get_overview(start_idx: int, end_idx: int) -> list[dict[str, str | float]]:
    if (start_idx, end_idx) == (0, -1):
        return get_history(start_idx, end_idx)

    history_range = range(len(history))
    if start_idx in history_range and end_idx in history_range:
        if start_idx > end_idx:
            return get_history(end_idx, start_idx)
        else:
            return get_history(start_idx, end_idx)
        
    else:
        return []


def overview(start_idx: int = 0, end_idx: int = -1):
    for record in get_overview(start_idx, end_idx):
        for atr_name, value in record.items():
            print(f"{atr_name}: {value:<10}")
        print()


def warehouse_eq():
    for product_name, value in warehouse.items():
        print(f"{product_name:<20}", end=" ")
        for atr_name, v in value.items():
            print(f"{atr_name}: {v:<10}", end=" ")
        print()


def overview_range(start_idx: int, end_idx: int) -> tuple[int, int]:
    if start_idx == end_idx:
        print("Błędnie podane parametry, zastosowano domyślne")
        return (0, -1)

    elif start_idx < len(history) and end_idx < len(history):
        return (start_idx, end_idx)

    else:
        print("Błędnie podane parametry, zastosowano domyślne")
        return (0, -1)



while program_status is True:
    command = input("Podaj opcję: ").lower()

    if command in ["saldo"]:
        value = int(input("value: "))
        update_balance(value)


    elif command in ["sale", "sprzedaż"]:
        product_name = input("Product name: ").lower()
        product = get_product(product_name)
        if product is not None:
            if product["amount"] > 0:
              
                amount = int(input("amount: "))
                disposal(product_name, amount, product)
            else:
                print("Brak produktu na stanie")
        else:
            print("Brak produktu na stanie")



    elif command in ["purchase", "zakup"]:
        product_name = input("product_name: ").lower()
        price = float(input("price: "))
        amount = int(input("amount: "))

        purchase(product_name, price, amount)
    
    elif command in ["magazyn", "eq"]:
        product_name = input("product name: ").lower()
        on_warehouse = warehouse.get(product_name)
        if on_warehouse is not None:
            print(f"{product_name:<10}", end=" ")
            for atr_name, v in on_warehouse.items():
                print(f"{atr_name}: {v:<10}", end=" ")
            print()
        else:
            print("Brak produktu na stanie")


    elif command in ["lista", "list"]:
        warehouse_eq()

    elif command in ["overview", "przegląd"]:
        start_idx = int(input("start_idx: "))
        end_idx = int(input("end_idx: "))
        overview(*overview_range(start_idx, end_idx)) 



    elif command in ["konto", "balance"]:
        get_account()

    elif command == "koniec":
        update_json_file_data("company", company)
        program_status = False

    else:
        print("Podana komenda nie istnieje")

    update_json_file_data("company", company)
