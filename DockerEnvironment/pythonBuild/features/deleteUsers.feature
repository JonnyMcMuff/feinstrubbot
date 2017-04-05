Feature: Delete Users
  Scenario: administrative delete
    Given that there is a valid administrator
    When the administrator has access to the database
    Then s/he can query the registered users and delete all that have not been active over a defined period (e.g. 2 years) of time. When the user is deleted the user will be notified.