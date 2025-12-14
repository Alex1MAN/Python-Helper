
print("=================================== LINQ C# in Python")

class Sklad:
    def __init__(self, code, name):
        self.code = code
        self.name = name
    
    def __eq__(self, other):
        if not isinstance(other, Sklad):
            return False
        return self.code == other.code and self.name == other.name  # All fields
    
    def __hash__(self):
        return hash((self.code, self.name))  # Hash of all fields
    
    @staticmethod
    def remove_full_duplicates(sklad_list):
        # Remove full duplicates saving order in list
        return list(dict.fromkeys(sklad_list))
    
    @staticmethod
    def remove_duplicates_by_code(sklad_list):
        # Remove duplicates ONLY BY field 'code'
        seen_codes = set()
        unique = []
        for sklad in reversed(sklad_list):
            if sklad.code not in seen_codes:
                seen_codes.add(sklad.code)
                unique.append(sklad)
        return unique[::-1]
    
    @staticmethod
    def sort_by_code_asc(sklad_list):
        # Sort by 'code' by ascending
        return sorted(sklad_list, key=lambda x: x.code)
    
    @staticmethod
    def sort_by_code_desc(sklad_list):
        # Sort by 'code' by descending
        return sorted(sklad_list, key=lambda x: x.code, reverse=True)
    
    @staticmethod
    def sort_by_name_asc(sklad_list):
        # Sort by 'name' by ascending
        return sorted(sklad_list, key=lambda x: x.name)
    
    @staticmethod
    def sort_by_name_desc(sklad_list):
        # Sort by 'name' by descending
        return sorted(sklad_list, key=lambda x: x.name, reverse=True)
    
    @staticmethod
    def filter_by_code_contains(sklad_list, text):
        # Return list of classes, in which field 'code' contains 'text' (string)
        return list(filter(lambda x: text in x.code, sklad_list))


listOfSklads = []

list_size = 10;
width = len(str(list_size + 1))
for i in range(list_size):
    code = f"A{i + 1:0{width}d}"  # Dynamic stadart length of field
    name = f"New name {i + 1}"
    listOfSklads.append(Sklad(code, name))
# Second cycle for creating duplicates
for i in range(list_size):
    code = f"A{i + 1:0{width}d}"
    name = f"New name {i + 1}"
    listOfSklads.append(Sklad(code, name))


print(f"\nlen(listOfSklads) - {len(listOfSklads)}, list itself:")
for curSklad in listOfSklads:
    print(f"code: {curSklad.code}, name: {curSklad.name}")


print("\nAfter removing full duplicates:")
unique_sklads = Sklad.remove_full_duplicates(listOfSklads)
for curSklad in unique_sklads:
    print(f"code: {curSklad.code}, name: {curSklad.name}")


print("\nLINQ sort descending by code field")
sorted_sklads = Sklad.sort_by_code_desc(listOfSklads)
for sklad in sorted_sklads:
    print(f"code: {sklad.code}, name: {sklad.name}")


print("\nLINQ found all sklads, which code contains '1'")
filtered_sklads = Sklad.filter_by_code_contains(listOfSklads, "1")
for sklad in filtered_sklads:
    print(sklad.code, sklad.name)
