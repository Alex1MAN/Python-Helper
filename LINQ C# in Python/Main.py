
print("=================================== LINQ C# in Python")

class Sklad:
	def __init__(self, code, name, dates_of_changes=None):
		self.code = code
		self.name = name
		# Initialize with unique sorted dates
		self.dates_of_changes = sorted(list(set(dates_of_changes or [])))
	
	def __eq__(self, other):
		if not isinstance(other, Sklad):
			return False
		# All fields
		return self.code == other.code and \
				self.name == other.name and \
				self.dates_of_changes == other.dates_of_changes
	
	def __hash__(self):
		# Hash of all fields
		return hash((self.code, 
			   self.name, 
			   tuple(self.dates_of_changes)))
	
	def remove_duplicates_from_dates(self):
		# Remove duplicate dates from dates_of_changes list and sort them
		self.dates_of_changes = sorted(list(set(self.dates_of_changes)))
		return self.dates_of_changes
	
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
	dates = [f"{j:02d}.12.2025" for j in range(1, 4)]  # Add some sample dates with duplicates
	if i % 3 == 0:  # Add duplicate date for some items
		dates.append("01.12.2025")
		dates.append("01.12.2025")  # Duplicate
	listOfSklads.append(Sklad(code, name, dates))
# Second cycle for creating duplicates
for i in range(list_size):
	code = f"A{i + 1:0{width}d}"
	name = f"New name {i + 1}"
	dates = [f"{j:02d}.12.2025" for j in range(1, 4)]
	if i % 3 == 0:
		dates.append("01.12.2025")
		dates.append("01.12.2025")
	listOfSklads.append(Sklad(code, name, dates))


print(f"\nlen(listOfSklads) - {len(listOfSklads)}:")
for curSklad in listOfSklads:
	print(f"code: {curSklad.code}, name: {curSklad.name}, dates: {curSklad.dates_of_changes}")


print("\nCleaning duplicates from dates in first item:")
listOfSklads[0].dates_of_changes = ["01.12.2025", "02.12.2025", "01.12.2025", "03.12.2025", "01.12.2025"]
print(f"Before: {listOfSklads[0].dates_of_changes}")
listOfSklads[0].remove_duplicates_from_dates()
print(f"After: {listOfSklads[0].dates_of_changes}")


print("\nAfter removing full duplicates:")
unique_sklads = Sklad.remove_full_duplicates(listOfSklads)
for curSklad in unique_sklads:
	print(f"code: {curSklad.code}, name: {curSklad.name}, dates: {curSklad.dates_of_changes}")


print("\nLINQ descending sort by field 'code'")
sorted_sklads = Sklad.sort_by_code_desc(listOfSklads)
for sklad in sorted_sklads:
	print(f"code: {sklad.code}, name: {sklad.name}, dates: {sklad.dates_of_changes}")


print("\nLINQ found all sklads, which field 'code' contains '1'")
filtered_sklads = Sklad.filter_by_code_contains(listOfSklads, "1")
for sklad in filtered_sklads:
	print(f"code: {sklad.code}, name: {sklad.name}, dates: {sklad.dates_of_changes}")
