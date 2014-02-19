Feature: Create Elasticity Rule
  As a user
  I want to create elasticity rules
  In order to manage automatically the servers

  Scenario Outline: Create a rule

    Given a created "<server_id>" inside tenant
    When I create a rule with "<name>", "<condition>" and "<action>"
    Then the rule is saved in Policy Manager

    Examples:

    | server_id   | name    | condition | action  |
    | qatestserver| random  | default   | default |


  Scenario Outline: Create a rule with missing parameters

    Given a created "<server_id>" inside tenant
    When I create a rule with "<name>", "<condition>" and "<action>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | Error_code  | FaultElement  |
    #| qatestserver| None      | default   | default | 400         | badRequest    |
    #| qatestserver| random    | None      | default | 400         | badRequest    |
    #| qatestserver| random    | default   | None    | 400         | badRequest    |
    #| qatestserver| random    |           | default | 400         | badRequest    |
    #| qatestserver|           | default   | default | 400         | badRequest    |
    #| qatestserver| random    | default   |         | 400         | badRequest    |
    #| qatestserver| random    | default   | default | 400         | badRequest    |
    | qatestserver| long_name | default   | default | 400         | badRequest    |


