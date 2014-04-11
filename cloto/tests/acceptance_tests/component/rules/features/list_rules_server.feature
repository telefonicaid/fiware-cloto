Feature: As a user
  I want list all the rules of specific server
  In order to manage the rules of a server

  @basic
  Scenario Outline: List server with only one rule

    Given "<number>" of rules created in "<server_id>"
    When I get the rules list from "<server_id>"
    Then I obtain all the rules of the server

    Examples:

    | number  | server_id     |
    | 1       | qatestserver  |


  Scenario Outline: List server with several rules
    Given "<number>" of rules created in "<server_id>"
    When I get the rules list from "<server_id>"
    Then I obtain all the rules of the server

    Examples:

    | number  | server_id     |
    | 2       | qatestserver  |
    | 5       | qatestserver  |
    | 100     | qatestserver  |

  Scenario Outline: List server without rules created

    Given a created "<server_id>" without rules
    When I get the rules list from "<server_id>"
    Then I obtain zero rules

    Examples:

    | server_id       |
    | qatestserver    |

  Scenario Outline: List rules from non existent server

    Given a created "<server_id>" inside tenant
    When I get the rules list from "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id | Error_code  | FaultElement  |
    | random    | 404         | itemNotFound  |

  @security
  Scenario Outline: List rules with incorrect token

    Given a created rule in the in the "<server_id>"
    And incorrect "<token>"
    When I get the rules list from "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_id   | name    | condition | action  |
      | 401         | unauthorized  | 1a2b3c    | qatestserver| random  | default   | default |
      | 401         | unauthorized  | old_token | qatestserver| random  | default   | default |
      | 401         | unauthorized  |           | qatestserver| random  | default   | default |
      | 401         | unauthorized  | null      | qatestserver| random  | default   | default |

