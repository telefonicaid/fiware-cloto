Feature: Get the list of all servers
  As a user
  I want to obtain a server list
  In order to manage all the servers


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

  Scenario Outline: retrieve a server list with one server without rules

    Given a created "<server_id>" without rules
    When I retrieve the server list
    Then I obtain the server list without rules

    Examples:

    | server_id       |
    | qatestserver    |

  Scenario Outline: Retrieve a server list with incorrect credentials

    Given a "<server_number>" of servers in a tenant with rules created
    And incorrect "<token>"
    When I retrieve the server list
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_number |
      | 401         | unauthorized  | 1a2b3c    | 1             |
      | 401         | unauthorized  | old_token | 1             |
      | 401         | unauthorized  |           | 1             |
      | 401         | unauthorized  | null      | 1             |