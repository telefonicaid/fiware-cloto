Feature: Update Elasticity Rule
  As a user
  I want to update elasticity rules
  In order to manage automatically the servers

  @basic
  Scenario Outline: Update a scale rule with all parameters

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the scalability rule with "<new_name>" and "<new_action>" in "<server_id>"
    Then the rule is updated in Policy Manager

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_action  |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 1             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 0             | less equal      | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 0             | less            | 1             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 0             | less            | 0             | less equal      | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | qaforever   | scaleUp     |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleDown   |
    | qatestserver| 1             | less equal      | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 1             | less            | 1             | less equal      | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| 1             | less equal      | 1             | less equal      | 0             | less            | 0             | less            | !@#$%^&*()_ | scaleDown   |


  @basic
  Scenario Outline: Update a notify rule with all parameters

    Given the created notify rule in the server with id "<server_id>" with the following parameters
      | body    | email       | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | hello!  | aaa@aaa.es  | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the notify rule with "<new_name>", "<new_body>" and "<new_email>" in "<server_id>"
    Then the rule is updated in Policy Manager

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_body    | new_email   |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | Bye!        | aaa@aaa.es  |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | qa@test.es  |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | !@#$%^&*()_ | qa@test.es  |


  @basic
  Scenario Outline: Update a scale rule with some parameters with empty strings

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the scalability rule with "<new_name>" and "<new_action>" in "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_action  | Error_code  | FaultElement  |
    | qatestserver|               | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 1             |                 | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less equal      |               | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 1             |                 | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less equal      | 0             | less            | 0             | less            |             | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | qaforever   |             | 400         | badRequest    |
    | qatestserver|               |                 | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver|               |                 |               |                 | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver|               |                 |               |                 | 0             | less            | 0             | less            |             |             | 400         | badRequest    |


  Scenario Outline: Update a notify rule with some parameters with empty strings

    Given the created notify rule in the server with id "<server_id>" with the following parameters
      | body    | email       | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | hello!  | aaa@aaa.es  | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the notify rule with "<new_name>", "<new_body>" and "<new_email>" in "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_body    | new_email   | Error_code  | FaultElement  |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        |             | aaa@aaa.es  | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      |             | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        |             |             | 400         | badRequest    |


  @basic
  Scenario Outline: Update a scale rule with incorrect parameters

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the scalability rule with "<new_name>" and "<new_action>" in "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_action  | Error_code  | FaultElement  |
    | qatestserver| -1            | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 101           | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 100.1         | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 5'5           | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 5,5           | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| testing       | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 1 0           | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 1F            | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | -1            | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 101           | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 100.1         | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 5,5           | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 5'5           | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | qa            | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 1 0           | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 1F            | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | qa          | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | les s           | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | testing         | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less less       | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | lessequals      | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | equals less     | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | Less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | LESS            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | _less           | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less_           | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less?           | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | les s           | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | testing         | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less less       | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | lessequals      | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | equals less     | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | Less            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | LESS            | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | _less           | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less_           | 0             | less            | 0             | less            | test        | scaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scale       | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleup     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scale Up    | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scale_Up    | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp_    | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp?    | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | testing     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | ScaleUp     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | SCALEUP     | 400         | badRequest    |

  Scenario Outline: Update a notify rule with incorrect parameters

    Given the created notify rule in the server with id "<server_id>" with the following parameters
      | body    | email       | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | hello!  | aaa@aaa.es  | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the notify rule with "<new_name>", "<new_body>" and "<new_email>" in "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_body    | new_email     | Error_code  | FaultElement  |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | aaaaaa.es     | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | aaaa@aaa      | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | aaaa@aaa@a.es | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | aaaa@         | 400         | badRequest    |
    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | hello!      | @             | 400         | badRequest    |



  Scenario Outline: Update a non existent rule

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    When I update "<another_rule_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | another_rule_id | Error_code  | FaultElement  |
    | qatestserver| testing         | 404         | itemNotFound  |
    | qatestserver| qa              | 404         | itemNotFound  |

  Scenario Outline: Update a existent rule in other server

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the scalability rule with "<new_name>" and "<new_action>" in "<another_server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | another_server_id | Error_code  | FaultElement  | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_action  |
    | qatestserver| testingserver     | 404         | itemNotFound  | 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | qatestserver| qaserver          | 404         | itemNotFound  | 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |


  @security
  Scenario Outline: Update a rule with incorrect token

    Given the created scale rule in the server with id "<server_id>" with the following parameters
      | operation | name    | cpu_value | cpu_operand | mem_value | mem_operand | hdd_value | hdd_operand | net_value | net_operand |
      | scaleUp   | test    | 0         | less        | 0         | less        | 0         | less        | 0         | less        |
    And an incorrect token with value "<token>"
    And parameter "cpu" with value "<new_cpu_value>" and operand "<new_cpu_operand>"
    And parameter "mem" with value "<new_mem_value>" and operand "<new_mem_operand>"
    And parameter "hdd" with value "<new_hdd_value>" and operand "<new_hdd_operand>"
    And parameter "net" with value "<new_net_value>" and operand "<new_net_operand>"
    When I update the scalability rule with "<new_name>" and "<new_action>" in "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | Error_code  | FaultElement  | token     | server_id   | new_cpu_value | new_cpu_operand | new_mem_value | new_mem_operand | new_hdd_value | new_hdd_operand | new_net_value | new_net_operand | new_name    | new_action  |
    | 401         | unauthorized  | 1a2b3c    | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | 401         | unauthorized  | old_token | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | 401         | unauthorized  |           | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
    | 401         | unauthorized  | null      | qatestserver| 0             | less            | 0             | less            | 0             | less            | 0             | less            | test        | scaleUp     |
