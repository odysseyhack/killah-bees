addressFields(AddressBaseFields) :- subset(AddressBaseFields, [addressFullAddress, addressPOBox, addressThoroughfare, addressLocatorDesignator, addressLocatorName, addressAddressArea, addressPostName, addressAdminUnitL1, addressAdminUnitL2, addressPostCode, addressAddressID]).
locationFields(LocationBaseFields) :- subset(LocationBaseFields, [locationGeographicName, locationGeographicIdentifier, locationAddress, locationGeometry]).
jurisdictionFields(JurisdictionBaseFields) :- subset(JurisdictionBaseFields, [jurisdictionName, jurisdictionIdentifier]).
personFields(PersonBaseFields) :- subset(PersonBaseFields, [personIdentifier, personFullName, personGivenName, personFamilyName, personPatronymicName, personAlternativeName, personGender, personBirthName, personDateOfBirth, personDateOfDeath]).

addressIdentified(AddressInputFields) :- subset([addressFullName], AddressInputFields).
addressIdentified(AddressInputFields) :- subset([addressPOBox,addressPostCode], AddressInputFields).
addressIdentified(AddressInputFields) :- subset([addressPOBox, addressThoroughfare, addressAddressArea], AddressInputFields).

jurisdictionIdentified(JurisdictionInputFields) :- subset([jurisdictionName], JurisdictionInputFields).

locationIdentified(LocationInputFields) :- subset([locationGeographicName], LocationInputFields).
locationIdentified(LocationInputFields) :- subset([locationGeometry], LocationInputFields).
locationIdentified(LocationInputFields) :- subset([locationAddress], LocationInputFields).

breach(PersonBaseFields, PersonCountryOfBirth, PersonCountryOfDeath, PersonPlaceOfBirth, PersonPlaceOfDeath, PersonCitizenship, PersonResidency, PersonAddress) :-
       subset([personFullName], PersonBaseFields), locationIdentified(PersonCountryOfBirth) ;
       subset([personFullName], PersonBaseFields), addressIdentified(PersonAddress) ;
       subset([personFullName, personDateOfBirth], PersonBaseFields), locationIdentified(PersonCountryOfBirth).