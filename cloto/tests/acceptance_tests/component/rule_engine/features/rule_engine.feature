Feature: As Scalability Manager
  I want fire some rules depending the facts arrived
  In order to offer scalability options

  @basic
  Scenario Outline: Action fired when fact arrives and rule is satisfied
    Given the following rule subscribed in "<server_id>"
    | name  | condition                                              | action       |
    | rule1 | ?serv <- (server (server-id ?x) (cpu ?y&:(> ?y 0.10))' | <action_type>|
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then The rule is fired

    Examples:
    | action_type                                     | server_id | cpu   | memory  | disk  | network |
    | assert (alertCPU ?x))(python-call scale_up)     | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | assert (alertCPU ?x))(python-call scale_up)     | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | assert (alertCPU ?x))(python-call notify_user)  | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  @basic
  Scenario Outline: Action not fired when fact arrives and rule is not satisfied
    Given the following rule subscribed in "<server_id>"
    | name  | condition                                              | action       |
    | rule1 | ?serv <- (server (server-id ?x) (cpu ?y&:(> ?y 0.90))' | <action_type>|
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then The rule is not fired

    Examples:
    | action_type                                     | server_id | cpu   | memory  | disk  | network |
    | assert (alertCPU ?x))(python-call scale_up)     | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | assert (alertCPU ?x))(python-call scale_up)     | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | assert (alertCPU ?x))(python-call notify_user)  | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  Scenario Outline: Actions behaviour with only one attribute in conditions
    Given the following rule subscribed in "<server_id>"
    | name  | condition                                                    | action                                     |
    | rule1 | ?serv <- (server (server-id ?x) (<attribute> ?y&:(> ?y 0.90))| assert (alertCPU ?x))(python-call scale_up)|
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then The rule is fired

    Examples:
    | attribute | server_id | cpu   | memory  | disk  | network |
    | cpu       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | memory    | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | hdd       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | network   | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  Scenario Outline: Actions behaviour with several attributes in conditions including operants
    Given the following rule subscribed in "<server_id>"
    | name  | condition                                       | action                                     |
    | rule1 | u'?serv <- (server (server-id ?x) <attributes>) | assert (alertCPU ?x))(python-call notify)  |
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then The rule is fired
    Examples:

    | attributes                                                                                                | server_id | cpu   | memory  | disk  | network |
    | (cpu ?y&:(< ?y 0.01))&(mem ?y&:(< ?z 0.01)                                                                | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (cpu ?y&:(< ?y 0.01))&(mem ?z&:(< ?z 0.01)&(hd ?s&:(< ?s 0.01)                                            | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (cpu ?y&:(< ?y 0.01))&(mem ?z&:(< ?z 0.01)&(hd ?s&:(< ?s 0.01)&(network ?t&:(< ?t 0.01)                   | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (cpu ?y&:(< ?y 0.01))or(mem ?y&:(< ?z 0.01)                                                               | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (cpu ?y&:(< ?y 0.01))or(mem ?z&:(< ?z 0.01)or(hd ?s&:(< ?s 0.01)                                          | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | ((cpu ?y&:(< ?y 0.01))or(mem ?z&:(< ?z 0.01)or(hd ?s&:(< ?s 0.01)or(network ?t&:(< ?t 0.01)               | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (((cpu ?y&:(< ?y 0.01))or((network ?t&:(< ?t 0.01))) & (((hd ?s&:(< ?s 0.01))or((network ?t&:(< ?t 0.01)))| qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | (((cpu ?y&:(< ?y 0.01))&((network ?t&:(< ?t 0.01))) or (((hd ?s&:(< ?s 0.01))&((network ?t&:(< ?t 0.01))) | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  Scenario: Several actions fired
  Scenario: Timeout configured between rule fired