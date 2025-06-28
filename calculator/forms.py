from django import forms

class TransportationForm(forms.Form):
    TRANSPORT_CHOICES = [
        ('Car', 'Car'),
        ('Bus', 'Bus'),
        ('Train', 'Train'),
        ('Bicycle', 'Bicycle'),
        ('Walking', 'Walking'),
        ('Motorcycle', 'Motorcycle'),
        ('Airplane', 'Airplane'),
        ('Other', 'Other'),
    ]
    
    FUEL_CHOICES = [
        ('Petrol/Gasoline', 'Petrol/Gasoline'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('CNG/LPG', 'CNG/LPG'),
    ]
    
    primary_mode = forms.ChoiceField(choices=TRANSPORT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    distance_km = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5'}))
    
    # Conditional fields
    fuel_type = forms.ChoiceField(choices=FUEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    passengers = forms.IntegerField(min_value=1, required=False, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    duration_minutes = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-input'}))

class FoodDietForm(forms.Form):
    DIET_CHOICES = [
        ('Omnivore (regular meat consumption)', 'Omnivore (regular meat consumption)'),
        ('Flexitarian (occasional meat)', 'Flexitarian (occasional meat)'),
        ('Pescatarian (fish but no meat)', 'Pescatarian (fish but no meat)'),
        ('Vegetarian (no meat or fish)', 'Vegetarian (no meat or fish)'),
        ('Vegan (no animal products)', 'Vegan (no animal products)'),
    ]
    
    FOOD_SOURCE_CHOICES = [
        ('Home-cooked', 'Home-cooked'),
        ('Restaurant', 'Restaurant'),
        ('Office/School Cafeteria', 'Office/School Cafeteria'),
        ('Delivery/Takeout', 'Delivery/Takeout'),
        ('Other', 'Other'),
    ]
    
    diet_type = forms.ChoiceField(choices=DIET_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    # Breakfast
    had_breakfast = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    breakfast_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}))
    breakfast_dairy_level = forms.IntegerField(min_value=0, max_value=5, required=False, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    breakfast_meat_level = forms.IntegerField(min_value=0, max_value=5, required=False, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    
    # Lunch
    had_lunch = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    lunch_source = forms.ChoiceField(choices=FOOD_SOURCE_CHOICES, required=False, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    lunch_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}))
    lunch_meat_level = forms.IntegerField(min_value=0, max_value=5, required=False, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    has_lunch_invoice = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    
    # Dinner
    had_dinner = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    dinner_source = forms.ChoiceField(choices=FOOD_SOURCE_CHOICES, required=False, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    dinner_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}))
    dinner_meat_level = forms.IntegerField(min_value=0, max_value=5, required=False, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    has_dinner_invoice = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    
    # Other
    snacks_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}))
    food_waste_level = forms.IntegerField(min_value=0, max_value=5, required=False, widget=forms.NumberInput(attrs={'class': 'form-range'}))

class HomeEnergyForm(forms.Form):
    HOME_TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('Small house', 'Small house'),
        ('Medium house', 'Medium house'),
        ('Large house', 'Large house'),
        ('Other', 'Other'),
    ]
    
    ELECTRICITY_CHOICES = [
        ('Grid electricity', 'Grid electricity'),
        ('Solar panels', 'Solar panels'),
        ('Wind power', 'Wind power'),
        ('Other renewable', 'Other renewable'),
        ('Don\'t know', 'Don\'t know'),
    ]
    
    home_type = forms.ChoiceField(choices=HOME_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    household_size = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    electricity_sources = forms.MultipleChoiceField(choices=ELECTRICITY_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}))
    electricity_provider = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    
    ac_hours = forms.IntegerField(min_value=0, max_value=24, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    heating_hours = forms.IntegerField(min_value=0, max_value=24, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    
    shower_minutes = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    did_laundry = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    laundry_loads = forms.IntegerField(min_value=1, required=False, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    
    LAUNDRY_TEMP_CHOICES = [
        ('Cold', 'Cold'),
        ('Warm', 'Warm'),
        ('Hot', 'Hot'),
    ]
    laundry_temperature = forms.ChoiceField(choices=LAUNDRY_TEMP_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    used_dishwasher = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))

class ConsumerGoodsForm(forms.Form):
    PURCHASED_CHOICES = [
        ('Clothing', 'Clothing'),
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Books/Media', 'Books/Media'),
        ('Toys', 'Toys'),
        ('Household items', 'Household items'),
        ('None', 'None'),
    ]
    
    ITEMS_NEW_CHOICES = [
        ('All new', 'All new'),
        ('Mixture of new and second-hand', 'Mixture of new and second-hand'),
        ('All second-hand', 'All second-hand'),
    ]
    
    PACKAGING_CHOICES = [
        ('Minimal/eco-friendly packaging', 'Minimal/eco-friendly packaging'),
        ('Standard packaging', 'Standard packaging'),
        ('Excessive packaging', 'Excessive packaging'),
    ]
    
    DELIVERY_CHOICES = [
        ('Standard', 'Standard'),
        ('Express/Next day', 'Express/Next day'),
        ('Same day', 'Same day'),
    ]
    
    purchased_items = forms.MultipleChoiceField(choices=PURCHASED_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}))
    items_new_or_used = forms.ChoiceField(choices=ITEMS_NEW_CHOICES, required=False, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    item_packaging = forms.ChoiceField(choices=PACKAGING_CHOICES, required=False, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    
    ordered_online = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    delivery_option = forms.ChoiceField(choices=DELIVERY_CHOICES, required=False, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    
    recycling_percentage = forms.IntegerField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={'class': 'form-range'}))
    does_compost = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    single_use_plastic_count = forms.IntegerField(min_value=0, max_value=20, widget=forms.NumberInput(attrs={'class': 'form-range'}))

class FoodInvoiceForm(forms.Form):
    invoice_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}))