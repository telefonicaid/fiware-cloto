Feature: Get the list of all servers
  As a user
  I want to obtain a server list
  In order to manage all the servers

  Scenario: Retrieve a servers list from one tenant without servers
    Given a tenant without servers
    When I retrieve the server list
    Then I obtain zero results

  Scenario Outline: retrieve a server list with several servers in tenant with rules

    Given a "<server_number>" of servers in a tenant with rules created
    When I retrieve the server list
    Then I obtain the server list

    Examples:

    | server_number |
    | 1             |
    | 2             |
    | 5             |
    | 20            |
