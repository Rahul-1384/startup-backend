from django.db import models
from account.models import User  

class Address(models.Model):
    class CountryRegionChoices(models.TextChoices):
        AFGHANISTAN = 'Afghanistan', 'Afghanistan'
        ALBANIA = 'Albania', 'Albania'
        ALGERIA = 'Algeria', 'Algeria'
        ANDORRA = 'Andorra', 'Andorra'
        ANGOLA = 'Angola', 'Angola'
        ARGENTINA = 'Argentina', 'Argentina'
        AUSTRALIA = 'Australia', 'Australia'
        AUSTRIA = 'Austria', 'Austria'
        BANGLADESH = 'Bangladesh', 'Bangladesh'
        BELGIUM = 'Belgium', 'Belgium'
        BRAZIL = 'Brazil', 'Brazil'
        CANADA = 'Canada', 'Canada'
        CHINA = 'China', 'China'
        DENMARK = 'Denmark', 'Denmark'
        EGYPT = 'Egypt', 'Egypt'
        FRANCE = 'France', 'France'
        GERMANY = 'Germany', 'Germany'
        INDIA = 'India', 'India'
        INDONESIA = 'Indonesia', 'Indonesia'
        ITALY = 'Italy', 'Italy'
        JAPAN = 'Japan', 'Japan'
        MEXICO = 'Mexico', 'Mexico'
        NETHERLANDS = 'Netherlands', 'Netherlands'
        PAKISTAN = 'Pakistan', 'Pakistan'
        RUSSIA = 'Russia', 'Russia'
        SAUDI_ARABIA = 'Saudi Arabia', 'Saudi Arabia'
        SINGAPORE = 'Singapore', 'Singapore'
        SOUTH_AFRICA = 'South Africa', 'South Africa'
        SOUTH_KOREA = 'South Korea', 'South Korea'
        SPAIN = 'Spain', 'Spain'
        SWEDEN = 'Sweden', 'Sweden'
        SWITZERLAND = 'Switzerland', 'Switzerland'
        TURKEY = 'Turkey', 'Turkey'
        UK = 'United Kingdom', 'United Kingdom'
        USA = 'United States', 'United States'
        OTHER = 'Other', 'Other'
    
    class StateChoices(models.TextChoices):
        ANDHRA_PRADESH = 'Andhra Pradesh', 'Andhra Pradesh'
        ARUNACHAL_PRADESH = 'Arunachal Pradesh', 'Arunachal Pradesh'
        ASSAM = 'Assam', 'Assam'
        BIHAR = 'Bihar', 'Bihar'
        CHHATTISGARH = 'Chhattisgarh', 'Chhattisgarh'
        GOA = 'Goa', 'Goa'
        GUJARAT = 'Gujarat', 'Gujarat'
        HARYANA = 'Haryana', 'Haryana'
        HIMACHAL_PRADESH = 'Himachal Pradesh', 'Himachal Pradesh'
        JAMMU_AND_KASHMIR = 'Jammu and Kashmir', 'Jammu and Kashmir'
        JHARKHAND = 'Jharkhand', 'Jharkhand'
        KARNATAKA = 'Karnataka', 'Karnataka'
        KERALA = 'Kerala', 'Kerala'
        MADHYA_PRADESH = 'Madhya Pradesh', 'Madhya Pradesh'
        MAHARASHTRA = 'Maharashtra', 'Maharashtra'
        MANIPUR = 'Manipur', 'Manipur'
        MEGHALAYA = 'Meghalaya', 'Meghalaya'
        MIZORAM = 'Mizoram', 'Mizoram'
        NAGALAND = 'Nagaland', 'Nagaland'
        ORISSA = 'Odisha', 'Odisha'
        PUNJAB = 'Punjab', 'Punjab'
        RAJASTHAN = 'Rajasthan', 'Rajasthan'
        SIKKIM = 'Sikkim', 'Sikkim'
        TAMIL_NADU = 'Tamil Nadu', 'Tamil Nadu' 
        TRIPURA = 'Tripura', 'Tripura'
        UTTAR_PRADESH = 'Uttar Pradesh', 'Uttar Pradesh'
        UTTARAKHAND = 'Uttarakhand', 'Uttarakhand'
        WEST_BENGAL = 'West Bengal', 'West Bengal'
        OTHER = 'Other', 'Other'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    country_region = models.CharField(
        max_length=150,
        choices=CountryRegionChoices.choices,
        default=CountryRegionChoices.INDIA
    )
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    flat_building_apartment = models.CharField(max_length=255)
    area_street_village = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=150,
        choices=StateChoices.choices,
        default=StateChoices.UTTAR_PRADESH)
    default_address = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.default_address:
            Address.objects.filter(user=self.user, default_address=True).update(default_address=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.flat_building_apartment}, {self.city}"