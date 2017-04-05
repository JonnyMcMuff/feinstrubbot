Feature: SetLocation
  Scenario: BackendUpdate
    Given that the user is registered to the service
    When the user sends "My current location is xxxx"
    Then the data is updated in the backend
  Scenario: GetConfirmation
     Given  that the user is registered to the service
     When the user has send a proper location update string
     Then the user gets a confirmation about the location change
  Scenario: Fail
    Given that the user is registered to the service
    When the user has send a bad location update string
    Then the user gets a error message