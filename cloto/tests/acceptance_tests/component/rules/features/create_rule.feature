Feature: Create Elasticity Rule
  As a user
  I want to create elasticity rules
  In order to manage automatically the servers


Scenario Outline: Create a new specific rule for scale_up or scale_down

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a scale rule with "<name>" and "<action>"
  Then the rule is saved in Policy Manager

  Examples:
  | server_id | name        | cpu_value | cpu_operand | mem_value | mem_operand   | action    |
  | qatest    | random      | 90        | greater     | 98        | greater equal | scaleUp   |
  | qatest    | random      | 10        | less        | 5         | less equal    | scaleDown |
  | qatest    | !@#$%^&*()_ | 10        | less        | 5         | less equal    | scaleDown |


Scenario Outline: Create a new specific rule for notify mail

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a notify rule with "<name>", "<body>" and "<email>"
  Then the rule is saved in Policy Manager

  Examples:
  | server_id | name    | cpu_value | cpu_operand | mem_value | mem_operand   | body  | email         |
  | qatest    | random  | 90        | greater     | 98        | greater equal | hello!| aaaa@aaaa.es  |
  | qatest    | random  | 10        | less        | 5         | less equal    | hello!| aaaa@aaaa.es  |


Scenario Outline: Create a new specific rule for scale without some value

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a scale rule with "<name>" and "<action>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | name    | cpu_value | cpu_operand | mem_value | mem_operand   | action    | Error_code  | FaultElement  |
  | qatest    |         | 90        | greater     | 98        | greater equal | scaleUp   | 400         | badRequest    |
  | qatest    | random  |           | greater     | 98        | greater equal | scaleUp   | 400         | badRequest    |
  | qatest    | random  | 90        |             | 98        | greater equal | scaleUp   | 400         | badRequest    |
  | qatest    | random  | 90        | greater     |           | greater equal | scaleUp   | 400         | badRequest    |
  | qatest    | random  | 90        | greater     | 98        |               | scaleUp   | 400         | badRequest    |
  | qatest    | random  | 90        | greater     | 98        | greater equal |           | 400         | badRequest    |


Scenario Outline: Create a new specific rule for notify without some value

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a notify rule with "<name>", "<body>" and "<email>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | name    | cpu_value | cpu_operand | mem_value | mem_operand   | body  | email         | Error_code  | FaultElement  |
  | qatest    | random  | 90        | greater     | 98        | greater equal |       | aaaa@aaaa.es  | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | hello!|               | 400         | badRequest    |


Scenario Outline: Create a new specific rule for scale without some parameter

  Given a created "<server_id>" inside tenant
  And some rule prepared with all data
  And the "<parameter>" deleted
  When I create an incorrect rule
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | parameter   | Error_code  | FaultElement  |
  | qatest    | action      | 400         | badRequest    |
  | qatest    | actionName  | 400         | badRequest    |
  | qatest    | operation   | 400         | badRequest    |
  | qatest    | name        | 400         | badRequest    |
  | qatest    | cpu         | 400         | badRequest    |
  | qatest    | value       | 400         | badRequest    |
  | qatest    | operand     | 400         | badRequest    |
  | qatest    | mem         | 400         | badRequest    |



Scenario Outline: Create a new specific rule for scale without None as value

  Given a created "<server_id>" inside tenant
  And some rule prepared with all data
  And the "<parameter>" replaced to "None"
  When I create an incorrect rule
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | parameter   | Error_code  | FaultElement  |
  | qatest    | action      | 400         | badRequest    |
  | qatest    | actionName  | 400         | badRequest    |
  | qatest    | operation   | 400         | badRequest    |
  | qatest    | name        | 400         | badRequest    |
  | qatest    | cpu         | 400         | badRequest    |
  | qatest    | value       | 400         | badRequest    |
  | qatest    | operand     | 400         | badRequest    |
  | qatest    | mem         | 400         | badRequest    |


Scenario Outline: Create a new specific rule with incorrect actionName

  Given a created "<server_id>" inside tenant
  And some rule prepared with all data
  And the "<parameter>" replaced to "<new_value>"
  When I create an incorrect rule
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | parameter   | Error_code  | FaultElement  | new_value   |
  | qatest    | actionName  | 400         | badRequest    | ActionName  |
  | qatest    | actionName  | 400         | badRequest    | actionname  |
  | qatest    | actionName  | 400         | badRequest    | ACTIONNAME  |
  | qatest    | actionName  | 400         | badRequest    | Actionname  |
  | qatest    | actionName  | 400         | badRequest    | actionName_ |
  | qatest    | actionName  | 400         | badRequest    | actionName? |
  | qatest    | actionName  | 400         | badRequest    | action Name |


Scenario Outline: Create a new specific rule for scale with incorrect parameters

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a scale rule with "<name>" and "<action>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | name    | cpu_value | cpu_operand | mem_value | mem_operand   | action    | Error_code  | FaultElement  |
  | qatest    | random  | -1        | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 101       | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 100.1     | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 5'5       | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 5,5       | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | testing   | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 1 0       | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 1F        | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | -1        | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 101       | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 100.1     | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5'5       | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5,5       | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5 0       | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5F        | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | testing   | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | les s       | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | testing     | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less less   | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | equal less  | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scaleDown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scale     | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | testing   | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scale Down| 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scaledown | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scale Up  | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scaleup   | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | ScaleUp   | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | SCALEUP   | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | scaleUp_  | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | SCALEUP?  | 400         | badRequest    |
  | qatest    | qa      | 10        | less        | 5         | less equal    | scaleDown | 400         | badRequest    |

Scenario Outline: Create a new specific rule for notify with incorrect parameters

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a notify rule with "<name>", "<body>" and "<email>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:
  | server_id | name    | cpu_value | cpu_operand | mem_value | mem_operand   | body  | email         | Error_code  | FaultElement  |
  | qatest    | random  | 90        | greater     | 98        | greater equal | hello!| aaaa@aaaa     | 400         | badRequest    |
  | qatest    | random  | 10        | less        | 5         | less equal    | hello!| aaaaaaaa.es   | 400         | badRequest    |


Scenario Outline: Create a rule in not existent tenant_id and / or server_id

  Given a non created "<tenant_id>" and "<server_id>"
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  When I create a scale rule with "<name>" and "<action>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:

  | Error_code  | FaultElement  | server_id   | name    | cpu_value | cpu_operand | mem_value | mem_operand   | action    | tenant_id |
  | 401         | unauthorized  | qatestserver| random  | 90        | greater     | 98        | greater equal | scaleUp   | qatest    |
  | 401         | unauthorized  | qatest      | random  | 90        | greater     | 98        | greater equal | scaleUp   | qatest    |


@security
Scenario Outline: Create a rule with incorrect token

  Given a created "<server_id>" inside tenant
  And parameter "cpu" with "<cpu_value>" and "<cpu_operand>"
  And parameter "mem" with "<mem_value>" and "<mem_operand>"
  And incorrect "<token>"
  When I create a scale rule with "<name>" and "<action>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:

  | Error_code  | FaultElement  | token     | server_id   | name    | cpu_value | cpu_operand | mem_value | mem_operand   | action    |
  | 401         | unauthorized  | 1a2b3c    | qatestserver| random  | 90        | greater     | 98        | greater equal | scaleUp   |
  | 401         | unauthorized  | old_token | qatestserver| random  | 90        | greater     | 98        | greater equal | scaleUp   |
  | 401         | unauthorized  |           | qatestserver| random  | 90        | greater     | 98        | greater equal | scaleUp   |
  | 401         | unauthorized  | null      | qatestserver| random  | 90        | greater     | 98        | greater equal | scaleUp   |
