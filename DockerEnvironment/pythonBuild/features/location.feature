Feature: location
    Scenario: Update location
        Given that the user is registered to the service
        When the user sends My current location is xxxx
        Then data is updated in the backend
    Scenario: Confirm location change
        Given that the user is registered to the service
        When the user has send a proper location update string
        Then the user gets a confirmation about the location change
    Scenario: Handle wrong location
        Given that the user is registered to the service
        When the user has send a bad location update string
        Then the user gets a error message