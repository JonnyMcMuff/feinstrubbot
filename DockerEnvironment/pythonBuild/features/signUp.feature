Feature: SignUp
  Scenario: Working SignUp
    Given a working telegram account
    When the user sends the registration string to the bot
    Then the user is notified about the registration result
  Scenario: Failing SignUp
    Given a registration fails
    When the user name is already in use
    Then the system should report that to the user
