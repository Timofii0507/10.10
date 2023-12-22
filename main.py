class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - {self.price} грн. - {self.quantity} шт."


class Cart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

    def remove_item(self, item):
        self.items.remove(item)
        self.total -= item.price

    def show_items(self):
        print("Товари у вашому кошику:")
        for item in self.items:
            print(item)

    def clear_items(self):
        self.items = []
        self.total = 0


class User:
    def __init__(self, name, username, password, role="user"):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def is_admin(self):
        return self.role == "admin"


class CashRegister:
    def __init__(self):
        self.products = []
        self.cart = Cart()
        self.user = None
        self.users = []
        self.load_users()
        self.load_products()

    def load_users(self):
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    name, username, password, role = line.strip().split(",")
                    user = User(name, username, password, role)
                    self.users.append(user)
        except FileNotFoundError:
            print("Файл users.txt не знайдено. Створюю новий файл.")
            self.save_users()

    def save_users(self):
        with open("users.txt", "w") as file:
            for user in self.users:
                file.write(f"{user.name},{user.username},{user.password},{user.role}\n")

    def load_products(self):
        try:
            with open("products.txt", "r") as file:
                for line in file:
                    name, price, quantity = line.strip().split(",")
                    product = Product(name, float(price), int(quantity))
                    self.products.append(product)
        except FileNotFoundError:
            print("Файл products.txt не знайдено. Створюю новий файл.")
            self.save_products()
    def save_products(self):
        with open("products.txt", "w") as file:
            for product in self.products:
                file.write(f"{product.name},{product.price},{product.quantity}\n")
    def login(self):
        username = input("Введіть логін: ")
        password = input("Введіть пароль: ")
        for user in self.users:
            if user.username == username and user.password == password:
                self.user = user
                print(f"Ви увійшли в систему, {user.name} ({user.role})!")
                return
        print("Неправильний логін або пароль. Спробуйте ще раз.")
    def run(self):
        print("Вітаємо вас у додатку \"Касовий апарат\"")
        while True:
            print("Меню:")
            print("1. Зареєструватись в системі")
            print("2. Увійти в систему")
            print("3. Переглянути доступні товари")
            print("4. Купити товар")
            print("5. Оплатити товари з кошика")
            print("6. Додати товар (тільки для адміністратора)")
            print("7. Змінити інформацію про товар (тільки для адміністратора)")
            print("8. Вийти з системи")
            choice = input("Введіть ваш вибір: ")
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.show_products()
            elif choice == "4":
                self.buy_product()
            elif choice == "5":
                self.pay()
            elif choice == "6":
                if self.user and self.user.is_admin():
                    self.add_product()
                else:
                    print("Тільки адміністратор може додавати товар.")
            elif choice == "7":
                if self.user and self.user.is_admin():
                    self.edit_product()
                else:
                    print("Тільки адміністратор може змінювати інформацію про товар.")
            elif choice == "8":
                self.save_users()
                self.save_products()
                print("До побачення!")
                break
            else:
                print("Неправильний вибір, спробуйте ще раз")
    def register_user(self):
        name = input("Введіть ваше ім'я: ")
        username = input("Введіть логін: ")
        password = input("Введіть пароль: ")
        role = input("Виберіть роль (user або admin): ").lower()
        if role not in ["user", "admin"]:
            print("Невірна роль. Обрано роль користувача.")
            role = "user"
        user = User(name, username, password, role)
        self.users.append(user)
        print(f"Ви успішно зареєструвалися в системі, {name} ({role})!")
        with open("users.txt", "a") as file:
            file.write(f"{user.name},{user.username},{user.password},{user.role}\n")
    def add_product(self):
        try:
            name = input("Введіть назву товару: ")
            price = float(input("Введіть ціну товару: "))
            quantity = int(input("Введіть кількість товару: "))
        except ValueError:
            print("Некоректне введення. Будь ласка, введіть числові значення.")
            return
        product = Product(name, price, quantity)
        self.products.append(product)
        print(f"Ви додали новий товар: {product}")
        with open("products.txt", "a") as file:
            file.write(f"{product.name},{product.price},{product.quantity}\n")
    def edit_product(self):
        if not self.user or not self.user.is_admin():
            print("Доступ заборонений. Тільки адміністратор може змінювати товари.")
            return
        self.show_products()
        try:
            index = int(input("Введіть номер товару, який хочете змінити: "))
            product = self.products[index - 1]
        except (ValueError, IndexError):
            print("Некоректний номер товару. Будь ласка, введіть дійсне число.")
            return
        print(f"Ви обрали товар: {product}")
        new_name = input("Введіть нову назву товару або натисніть Enter, щоб залишити стару: ")
        if self.user.is_admin():
            new_price = input("Введіть нову ціну товару або натисніть Enter, щоб залишити стару: ")
            new_quantity = input("Введіть нову кількість товару або натисніть Enter, щоб залишити стару: ")
            if new_name:
                product.name = new_name
            if new_price:
                try:
                    product.price = float(new_price)
                except ValueError:
                    print("Некоректне введення. Будь ласка, введіть числове значення.")
            if new_quantity:
                try:
                    product.quantity = int(new_quantity)
                except ValueError:
                    print("Некоректне введення. Будь ласка, введіть ціле число.")
        else:
            if new_name:
                print("Недостатньо прав для зміни інших параметрів товару.")
                return
        print(f"Ви змінили товар: {product}")
        self.save_products()
    def show_products(self):
        print("Доступні товари:")
        for i, product in enumerate(self.products):
            print(f"{i + 1}. {product}")
    def buy_product(self):
        if not self.user:
            print("Будь ласка, увійдіть в систему.")
            return
        self.show_products()
        try:
            index = int(input("Введіть номер товару, який хочете купити: "))
            product = self.products[index - 1]
        except (ValueError, IndexError):
            print("Некоректний номер товару. Будь ласка, введіть дійсне число.")
            return
        if product.quantity <= 0:
            print(f"На жаль, товар {product.name} закінчився")
            return
        self.cart.add_item(product)
        product.quantity -= 1
        print(f"Ви додали товар {product.name} у ваш кошик")
    def pay(self):
        if not self.user:
            print("Будь ласка, увійдіть в систему.")
            return
        self.cart.show_items()
        print(f"Загальна сума до оплати: {self.cart.total} грн.")
        try:
            cash = float(input("Введіть суму готівкою: "))
        except ValueError:
            print("Некоректне введення. Будь ласка, введіть числове значення.")
            return
        if cash >= self.cart.total:
            change = cash - self.cart.total
            print(f"Ваша решта: {change} грн.")
            self.cart.clear_items()
            print("Дякуємо за покупку!")
        else:
            print("Ви ввели недостатню суму")
if __name__ == "__main__":
    cash_register = CashRegister()
    cash_register.run()
