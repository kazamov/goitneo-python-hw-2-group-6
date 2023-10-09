from collections import UserDict


class InvalidFieldType(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidPhoneLengthError(Exception):
    pass


class InvalidPhoneFormatError(Exception):
    pass


class Field:
    _value = None

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, __obj: object) -> bool:
        return self._value == __obj._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value


class Name(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if not isinstance(value, str):
            raise InvalidFieldType("name")
        elif len(value) == 0:
            raise InvalidNameError
        self._value = value


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if not isinstance(value, str):
            raise InvalidFieldType("phone")
        elif len(value) < 0:
            raise InvalidPhoneLengthError
        elif not value.isdigit():
            raise InvalidPhoneFormatError

        self._value = value


class Record:
    def __init__(self, name: str, phone: str = None):
        self.name = Name(name)
        self.phones: list[Phone] = []
        if phone:
            self.add_phone(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        if new_phone not in self.phones:
            self.phones.append(new_phone)
        return f"{new_phone} add to {self.name}"

    def delete_phone(self, phone_str: str):
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, prev_phone: str, next_phone: str):
        # phone = self.find_phone(prev_phone)
        new_phone = Phone(next_phone)
        idx = self.phones.index(Phone(prev_phone))
        if idx >= 0 and new_phone not in self.phones:
            # phone.value = next_phone
            self.phones[idx] = new_phone
            return f"Change {prev_phone} to {new_phone}"
        return f"No phone {prev_phone} or {new_phone} present in contact book"

    def find_phone(self, phone_str: str) -> Phone:
        phone = None
        for p in self.phones:
            if p.value == phone_str:
                phone = p
                break
        return phone


class AddressBook(UserDict):
    def add_record(self, record: Record) -> str:
        self.data[record.name.value] = record
        return f"{record} add successful"

    def find(self, name: str) -> Record:
        return self.data[name] if name in self.data else None

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)


def main():
    try:
        # Створення нової адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)

        # Виведення всіх записів у книзі
        for record in book.data.values():
            print(record)

        # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

        # Видалення запису Jane
        book.delete("Jane")

    except InvalidFieldType as e:
        print(f"The {e.args[0]} field should be a string")
    except InvalidNameError:
        print("The username is required.")
    except InvalidPhoneLengthError:
        print("The phone number length should be 10 digits.")
    except InvalidPhoneFormatError:
        print("The phone number should contain only digits.")
    except Exception:
        print("System error")


if __name__ == "__main__":
    main()
