Feature: Get the list of all servers
  As a user
  I want to obtain a server list
  In order to manage all the servers

  @basic
  Scenario Outline: retrieve a server list with several servers in tenant with rules

    Given a number of servers equat to "<server_number>" in a tenant with rules created
    When I retrieve the server list
    Then I obtain the server list

    Examples:

    | server_number |
    | 1             |
    | 2             |
    | 5             |
    | 10            |

  Scenario Outline: retrieve a server list with one server without rules

    Given a created server with server id "<server_id>" without rules
    When I retrieve the server list
    Then I obtain the server list without rules

    Examples:

    | server_id       |
    | qatestserver    |

  @security
  Scenario Outline: Retrieve a server list with incorrect credentials

    Given a number of servers equat to "<server_number>" in a tenant with rules created
    And an incorrect token with value "<token>"
    When I retrieve the server list
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_number |
      | 401         | unauthorized  | 1a2b3c    | 1             |
      | 401         | unauthorized  | old_token | 1             |
      | 401         | unauthorized  |           | 1             |
      | 401         | unauthorized  | null      | 1             |
