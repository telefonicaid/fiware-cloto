Feature: Create Elasticity Rule
  As a user
  I want to update elasticity rules
  In order to manage automatically the servers

  Scenario Outline: Update a rule with all parameters

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I update the rule with "<another_name>", "<another_condition>" and "<another_action>" in "<server_id>"
    Then the rule is updated in Policy Manager

    Examples:

    | server_id   | name    | condition | action  | another_name  | another_condition | another_action  |
    | qatestserver| name1   | condition1| action1 | another_name1 | another_condition1| another_action1 |
    | qatestserver| name2   | condition2| action2 | another_name2 | condition2        | action2         |
    | qatestserver| name3   | condition3| action3 | name3         | another_condition3| action3         |
    | qatestserver| name4   | condition4| action4 | name4         | condition4        | another_action4 |
    | qatestserver| name5   | condition5| action5 | name5         | condition5        | action5         |

  Scenario Outline: Update a rule with some parameters

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I update the rule with "<another_name>", "<another_condition>" and "<another_action>" in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name    | condition | action  | another_name  | another_condition | another_action  | Error_code  | FaultElement  |
    | qatestserver| name1   | condition1| action1 | another_name1 | None              | None            | 400         | badRequest    |
    | qatestserver| name2   | condition2| action2 | None          | another_condition2| None            | 400         | badRequest    |
    | qatestserver| name3   | condition3| action3 | None          | None              | another_action3 | 400         | badRequest    |
    | qatestserver| name4   | condition4| action4 | None          | None              | None            | 400         | badRequest    |
    | qatestserver| name5   | condition5| action5 | name5         | None              | None            | 400         | badRequest    |
    | qatestserver| name6   | condition6| action6 | None          | condition6        | None            | 400         | badRequest    |
    | qatestserver| name7   | condition7| action7 | None          | None              | action7         | 400         | badRequest    |



  Scenario Outline: Update a rule with invalid parameters

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I update the rule with "<another_name>", "<another_condition>" and "<another_action>" in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name  | condition | action  | Error_code  | FaultElement  | another_name  | another_condition | another_action  |
    | qatestserver| name1 | default   | default | 400         | badRequest    |               | condition1        | action1         |
    | qatestserver| name2 | default   | default | 400         | badRequest    | another_name2 |                   | action2         |
    | qatestserver| name3 | default   | default | 400         | badRequest    | another_name3 | condition3        |                 |
    | qatestserver| name4 | default   | default | 400         | badRequest    | long_name     | condition4        | action4         |
    | qatestserver| name5 | default   | default | 400         | badRequest    | qa            | condition5        | action5         |


  Scenario Outline: Update a rule with incorrect token

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    And incorrect "<token>"
    When I update the rule with "<another_name>", "<another_condition>" and "<another_action>" in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | Error_code  | FaultElement  | token     | server_id   | name    | condition | action  | another_name  | another_condition | another_action  |
    | 401         | unauthorized  | 1a2b3c    | qatestserver| random  | default   | default | another_name1 | another_condition1| another_action1 |
    | 401         | unauthorized  | old_token | qatestserver| random  | default   | default | another_name2 | another_condition2| another_action2 |
    | 401         | unauthorized  |           | qatestserver| random  | default   | default | another_name3 | another_condition3| another_action3 |
    | 401         | unauthorized  | null      | qatestserver| random  | default   | default | another_name4 | another_condition4| another_action4 |


  Scenario Outline: Update a non existent rule

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I update "<another_rule_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | another_rule_id | Error_code  | FaultElement  |
    | qatestserver| random    | default   | default | testing         | 404         | itemNotFound  |
    | qatestserver| alertCPU  | default   | default | qa              | 404         | itemNotFound  |

  Scenario Outline: Update a existent rule in other server

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I update the rule with "<name>", "<condition>" and "<action>" in "<another_server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | another_server_id | Error_code  | FaultElement  |
    | qatestserver| random    | default   | default | testingserver     | 404         | itemNotFound  |
    | qatestserver| alertCPU  | default   | default | qaserver          | 404         | itemNotFound  |